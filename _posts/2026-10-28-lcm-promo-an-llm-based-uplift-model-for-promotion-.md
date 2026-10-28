---
title: "LCM-Promo: An LLM-Based Uplift Model for Promotion Allocation"
description: "트랜잭션 커머스 데이터로 파인튜닝된 Large Commerce Model을 활용하여 단일 토큰 출력 기반의 단조 프로모션 반응 곡선을 학습하고 프로모션 비용 대비 전환율을 최적화한 업리프트 모델링 연구"
date: 2026-03-30 09:00:00 +0900
categories:
  - papers
  - causal-ml
paper_authors:
  - Nesta Midavaine
  - Floris Fok
  - Paulo Mendes
  - Joao Silva
  - Önder Akaçık
  - Dimas Lima
  - Zülküf Genç
paper_url: "https://arxiv.org/abs/2610.37570v1"
tags:
  - Uplift Modeling
  - LLM
  - E-Commerce
  - Promotion Optimization
toc: true
mermaid: false
---

## 3줄 요약
- 이커머스 트랜잭션 로그를 사전 학습 및 파인튜닝한 Large Commerce Model(LCM)을 기반으로 고객별 인과적 프로모션 반응 곡선을 추정하는 LCM-Promo를 제안함.
- 세션 문맥(요일, 배송 슬롯 등)을 컨디셔닝하고 단일 토큰(Single-token) 출력을 전환 임계 확률로 해석하여 할인 깊이에 따른 반응 곡선의 단조성(Monotonicity)을 보장함.
- Churn 유저 재활성화 실서비스 A/B 테스트에서 기존 Segment-EMA 베이스라인 대비 프로모션 비용을 6% 절감하면서도 전환율을 1% 향상시킴.

---

## 논문이 해결하는 문제
이커머스 환경에서 할인 및 프로모션 예산 할당(Promotion Allocation)은 전체 손익(P&L)에 직결되는 핵심 의사결정 과제입니다. 프로모션 없이도 구매할 고객(Sure Things)에게 과도한 인센티브를 지급하는 것은 마진 손실을 유발하고, 할인에 반응하지 않는 이탈 고객(Lost Causes)에게 예산을 낭비하는 것은 ROI를 급격히 저하시킵니다. 

따라서 처치(Treatment, 프로모션)로 인해 발생하는 순증 효과(Incremental Effect)를 추정하는 **업리프트 모델링(Uplift Modeling)**이 필수적입니다. 그러나 기존 모델들은 다음과 같은 현실적인 제약을 겪습니다:
1. 유저의 복잡한 시계열적 구매 이력 및 세션 수준의 문맥 정보(요일, 배송 마감 시각 등)를 유기적으로 반영하지 못함.
2. 할인율이 증가함에 따라 전환 확률이 감소하지 않아야 한다는 **단조 반응성(Monotonic Promotion-Response)** 제약을 위반하여 비논리적인 최적화 결과를 도출함.

---

## 기존 방법의 한계
- **세그먼트 기반 휴리스틱 및 지수이동평균(Segment-EMA)**: 실무에서 널리 쓰이는 Segment-EMA 방식은 유저를 RFM(Recency, Frequency, Monetary) 등으로 거칠게 군집화한 뒤 과거 반응률의 이동평균을 적용합니다. 이는 개별 세션의 실시간 문맥(요일, 시간대, 배송 가용 슬롯)을 반영하지 못하며 개인화 수준이 매우 낮습니다.
- **전통적 C-Learner / T-Learner (GBDT 기반)**: LightGBM, XGBoost 등을 기반으로 개별 할인율별 모델을 구축하거나 통합 다중 처치 모델을 학습할 경우, 복잡한 텍스트/시퀀스형 커머스 메타데이터(카테고리 탐색 패턴, 쿠폰 소진 이력)를 임베딩하기 어렵습니다. 또한 예측된 반응 곡선이 비단조(Non-monotonic) 성질을 띠어 사후 보정(Post-hoc calibration/isotonic regression)이 별도로 요구됩니다.

---

## 핵심 기여
1. **Large Commerce Model (LCM)의 업리프트 적용**: 대규모 상거래 트랜잭션 데이터로 사전 학습된 언어 모델을 업리프트 및 프로모션 할당 태스크에 맞춰 파인튜닝한 태스크 특화 프레임워크 제시.
2. **단일 토큰 출력 기반 단조 반응 곡선(Monotonic Response Curve)**: 할인 깊이(Discount Depth)에 따른 전환 임계치를 이산화하고, 이를 LLM의 단일 토큰 로짓(Logit)과 누적 확률 관계로 매핑하여 모델 자체에서 구조적으로 단조성을 보장.
3. **대규모 프로덕션 A/B 테스트 검증**: 실제 Churn 재활성화 캠페인 배포 환경에서 베이스라인 대비 **전환율 1% 상승 및 프로모션 비용 6% 절감**을 동시에 달성하며 실무적 유효성을 입증.

---

## 제안 방법과 주요 수식

### 1. 문제 정의 및 조건부 인과 반응
고객 $i$의 이전 거래 시퀀스와 현재 세션 문맥을 $X_i \in \mathcal{X}$라 하고, 할당 가능한 프로모션 처치를 $T_i \in \{0, d_1, d_2, \dots, d_K\}$ ($0$은 무할인, $d_k$는 증가하는 할인 깊이)라 정의합니다. 목적은 각 처치에 따른 잠재적 전환 결과 $Y_i(T) \in \{0, 1\}$에 대한 조건부 기대 전환율을 추정하는 것입니다:

$$\mu_k(X_i) = \mathbb{E}[Y_i(d_k) \mid X_i] = P(Y_i = 1 \mid X_i, T = d_k)$$

개별 처치 효과(Individual Treatment Effect, Uplift)는 다음과 같습니다:

$$\tau_k(X_i) = \mu_k(X_i) - \mu_0(X_i)$$

### 2. 단일 토큰을 활용한 임계치 기반 단조성 보장
할인 깊이 $d_k$가 커질수록 구매 전환 확률은 비감소(Non-decreasing)해야 합니다:

$$\mu_0(X_i) \le \mu_1(X_i) \le \dots \le \mu_K(X_i)$$

LCM-Promo는 이를 위해 고객 $i$가 구매를 결정하는 **최소 할인 임계치(Reservation Discount Threshold)** $D_i^* \in \{0, d_1, \dots, d_K, \infty\}$ 개념을 도입합니다. 즉, 제공된 할인 $d$가 유저의 내부 임계치 $D_i^*$ 이상일 때만 전환이 일어납니다:

$$Y_i(d_k) = \mathbf{1}(D_i^* \le d_k)$$

따라서 전환 확률은 누적 분포 함수(CDF)로 표현됩니다:

$$P(Y_i = 1 \mid X_i, T = d_k) = P(D_i^* \le d_k \mid X_i) = \sum_{j=0}^{k} P(D_i^* = d_j \mid X_i)$$

LCM-Promo는 LLM의 생성 헤드에서 다음 토큰으로 임계 클래스 토큰 $v \in \{v_0, v_1, \dots, v_K, v_\infty\}$를 예측하도록 설계됩니다. 모델의 로짓 벡터 $z(X_i)$에 소프트맥스를 적용하여 각 임계치 토큰의 확률을 계산합니다:

$$p_j(X_i) = P(D_i^* = d_j \mid X_i) = \frac{\exp(z_j(X_i))}{\sum_{m=0}^{K+1} \exp(z_m(X_i))}$$

이때 각 할인 깊이 $d_k$에서의 예측 전환 확률 $\hat{\mu}_k(X_i)$는 다음과 같이 닫힌 형태로 계산되며, $p_j(X_i) \ge 0$이므로 수학적으로 엄격한 단조성이 자연스럽게 만족됩니다:

$$\hat{\mu}_k(X_i) = \sum_{j=0}^{k} p_j(X_i)$$

### 3. 학습 손실 함수
프로덕션 로그에서 실제 관측된 로그는 특정 처치 $T_i = d_{k_i}$와 그에 따른 관측 전환 결과 $y_i \in \{0, 1\}$ 쌍입니다. Censored Data 형태를 띠므로, 로그 우도 함수는 관측된 구간에 대한 Marginal Likelihood로 정의됩니다:

$$\mathcal{L}(\theta) = -\sum_{i=1}^{N} \left[ y_i \log \left(\sum_{j=0}^{k_i} p_j(X_i; \theta)\right) + (1 - y_i) \log \left(\sum_{j=k_i+1}^{K+1} p_j(X_i; \theta)\right) \right]$$

단일 포워드 패스로 모든 토큰 로짓 $z(X_i)$가 계산되므로 추론 지연 시간(Inference Latency)이 $O(1)$ 토큰 생성 비용으로 제한됩니다.

---

## 핵심 구조

```
[User History & Context]
 (RFM, Order History, Day of Week, Delivery Slot)
             │
             ▼
    ┌─────────────────┐
    │  Prompt Builder │
    └────────┬────────┘
             │ Context String
             ▼
    ┌─────────────────┐
    │  LCM Backbone   │  (Fine-tuned Commerce LLM)
    └────────┬────────┘
             │ Hidden State
             ▼
    ┌─────────────────┐
    │ Single-Token    │  Logits for thresholds:
    │ Output Head     │  [v_0, v_1, ..., v_K, v_inf]
    └────────┬────────┘
             │ Softmax & Cumulative Sum
             ▼
    ┌─────────────────────────┐
    │ Monotonic Response Curve│  P(Y=1 | X, T=d_k)
    └────────┬────────────────┘
             │
             ▼
    ┌─────────────────────────┐
    │ Budget-Constrained      │  Optimal Promotion Allocation
    │ Knapsack Optimizer      │  argmax Uplift s.t. Budget
    └─────────────────────────┘
```

![LCM-Promo Conceptual Architecture](https://static.arxiv.org/static/design-system/latest/logos/arxiv-logo.svg)
*Figure: LCM-Promo 개념 아키텍처 다이어그램 (대체 참조)*

### 파이프라인 데이터 흐름
1. **Context Encoding**: 유저의 과거 결제 간격, 구매 카테고리 시퀀스, 현재 장바구니/세션 문맥(요일, 배송 슬롯 마감 여부)이 텍스트 프롬프트 형태로 인코딩됩니다.
2. **LCM Backbone 추론**: 도메인 사전 학습된 LLM 트랜스포머 블록을 통과하여 문맥 임베딩을 생성합니다.
3. **Threshold Logits 헤드**: 별도의 자기회귀 디코딩 루프 없이, 단일 위치(Single Next-Token)에서 사전 정의된 임계치 토큰 집합 $\{v_0, \dots, v_K, v_\infty\}$에 대한 로짓을 직접 추출합니다.
4. **Cumulative Response & Allocation**: 소프트맥스 후 누적합 연산을 통해 할인율별 단조 전환 확률 벡터 $\vec{\mu}(X_i)$를 획득하고, Knapsack 스타일의 최적화 알고리즘에 전달하여 전체 예산 제약 하에서 증분 ROI를 극대화하는 프로모션을 할당합니다.

---

## 실험 설정과 결과

### 1. 실험 설정
- **태스크**: Churn 유저 재활성화(Churn Reactivation) 프로모션 할당.
- **비교군(Baseline)**: 이커머스 프로덕션에서 동작 중이던 Segment-EMA (RFM 기반 세그먼트별 과거 반응 지수이동평균 모델).
- **평가 환경**: 실제 대규모 온라인 트래픽 대상 Production A/B Testing.

### 2. 실험 결과

| 모델 | 전환율 변화 (Conversion Rate) | 프로모션 비용 변화 (Cost) | 증분 ROI 평가 |
| :--- | :---: | :---: | :---: |
| **Segment-EMA (Baseline)** | 0.0% (기준) | 0.0% (기준) | - |
| **LCM-Promo (제안 모델)** | **+1.0%** | **-6.0%** | 유의미한 순수익 증가 |

- **효율적 예산 재배치**: 불필요한 할인 없이도 복귀할 유저에게는 낮은 할인을 부여하고, 높은 할인에만 반응하는 탄력적 유저에게 선별적으로 쿠폰을 배정함으로써 6%의 직접 비용 절감을 달성함.
- **전환율 증대**: 세션 문맥(특정 요일 및 배송 슬롯 선호도)을 파악하여 적절한 타이밍에 개입함으로써 전체 전환율이 1.0% 개선됨.

---

## 잘한 점
- **단일 토큰 디코딩을 통한 Latency 최적화**: LLM을 실시간 랭킹/할당 파이프라인에 적용할 때 가장 큰 병목인 Autoregressive Decoding을 제거하고, Single-token Logits 헤드 기반 Cumulative Softmax를 도입하여 추론 지연 시간을 프로덕션 서빙 가능한 수준으로 단축함.
- **도메인 제약 조건(단조성)의 구조적 해결**: Causal ML에서 할인-반응 곡선이 꼬이는(Negative Elasticity) 문제를 사후 Isotonic 보정에 의존하지 않고 모델 아키텍처 내부에서 수학적으로 보장함.
- **오프라인 벤치마크를 넘어선 실서비스 A/B 검증**: 실제 비즈니스 지표(비용 절감 및 전환율)를 통해 인과적 추정의 실효성을 직접 입증함.

---

## 한계와 의문점
- **서빙 비용 vs GBDT 간 트레이드오프**: 아무리 단일 토큰 추론이라 할지라도 수십억 파라미터 수준의 LLM은 경량 GBDT(LightGBM 등) 대비 수십 배의 GPU 연산 비용(FLOPs)을 소모합니다. 6%의 프로모션 비용 절감이 추가 인프라 서빙 비용을 초과하는지 여부에 대한 상세 TCO(Total Cost of Ownership) 분석이 부족합니다.
- **Confounder 통제 검증 부족**: 무작위 대조군(Randomized Controlled Trial, RCT) 데이터가 아닌 관측 트랜잭션 로그로부터 학습할 때 발생하는 강한 선택 편향(Selection Bias/Confounding)을 LLM 표현 학습만으로 완벽히 제거할 수 있는지에 대한 인과적 식별성(Identifiability) 논증이 다소 제한적입니다.

---

## 실무 적용 가능성
- **Churn 방지 및 장바구니 리타겟팅**: 유저의 세션 시퀀스와 이탈 주기가 불규칙한 환경에서 텍스트 기반 시퀀스 인코더로서의 강점을 즉시 활용 가능합니다.
- **하이브리드 캐싱 아키텍처 필요**: 실시간 API 호출 대신, 배치(Batch)로 오프라인에서 유저의 기저 임계치 분포를 예측해 두고, 실시간 서빙 시에는 세션 피처와 결합하는 투스텝(Two-step) 서빙 전략을 병행해야 실무 비용을 통제할 수 있습니다.

---

## 관련 연구와 연결점
- **Uplift Modeling**: Radford et al.의 인과 포레스트 및 Gutman et al.의 다중 처치 업리프트 프레임워크와 연결되며, 이를 딥러닝/LLM 백본으로 확장한 맥락입니다.
- **Foundation Models for Recommendation**: 최근 P5, M6 등 트랜잭션 및 추천 도메인에 LLM을 접목하려는 흐름의 연장선상에 있으며, 순수 추천(Recommendation)을 넘어 인과적 개입(Intervention/Uplift)으로 연구 지평을 넓혔습니다.

---

## 원문 정보
- **Title**: LCM-Promo: An LLM-Based Uplift Model for Promotion Allocation
- **Authors**: Nesta Midavaine, Floris Fok, Paulo Mendes, Joao Silva, Önder Akaçık, Dimas Lima, Zülküf Genç
- **Venue/Repository**: ECML PKDD 2026 (Industrial Track), arXiv:2610.37570v1
- **Published**: 2026-10 (아카이브 프리프린트 메타데이터 기준)
- **URL**: [https://arxiv.org/abs/2610.37570v1](https://arxiv.org/abs/2610.37570v1)

> 이 글은 자동 생성된 초안을 바탕으로 작성되며, 공개 전에 저자·수식·수치·출처를 직접 검수합니다. (arXiv 식별자 및 학회 연도 메타데이터는 공식 확정 여부에 따라 업데이트될 수 있습니다.)
---
title: "New LoRA Skills Should Read but Never Write"
description: "독립적으로 학습된 LoRA 어댑터 결합 시 발생하는 간섭을 해결하기 위해 어댑터 분해의 게이지 대칭성을 정규화하고 단방향 읽기 결합(Read-only)을 적용하는 READ 프레임워크"
date: 2026-09-30 09:00:00 +0900
categories:
  - Paper Reviews
  - peft
paper_authors:
  - Zeyan Li
  - Panqi Yang
  - Qirong Guo
  - Shengda Zhuo
  - SIyuan Qiu
  - Hu Xu
  - Chun Li
  - Jianfeng Xu
paper_url: "https://arxiv.org/abs/2609.31600v1"
tags:
  - LoRA
  - Model Merging
  - PEFT
  - Continual Learning
toc: true
mermaid: false
---

## 3줄 요약

1. 여러 개의 독립된 LoRA 어댑터를 단일 모델로 병합할 때 발생하는 성능 저하(간섭)의 근본 원인이 **어댑터 행렬 분해의 게이지 자유도(Gauge Freedom)**와 **결합 방향성(Coupling Direction)**에 있음을 규명했습니다.
2. 각 어댑터를 불변 표준형(Balanced Canonical Form)으로 정규화하고, 신규 스킬이 이전 스킬의 입력 부분공간만 읽을 수 있고 출력 부분공간에는 쓸 수 없도록 제한하는 **READ (Read-only Expansion of Adapter Deltas)** 기법을 제안합니다.
3. 추가적인 추론 연산 비용, 동적 라우팅, 전체 재학습 없이 신규 스킬의 결합 가중치 행(row)만 점진적으로 학습하여 베이스 모델 가중치로 완전히 흡수(Folding)시킬 수 있음을 입증했습니다.

---

## 논문이 해결하는 문제

LoRA(Low-Rank Adaptation)는 대규모 언어 모델(LLM)을 작업별로 효율적으로 미세조정하는 표준 기법으로 자리 잡았습니다. 그러나 서로 다른 작업에 대해 독립적으로 학습된 여러 개의 LoRA 어댑터를 단일 파라미터 체크포인트로 통합하는 문제에는 근본적인 트레이드오프가 존재합니다.

- **가중치 공간 병합(Weight Merging):** 여러 $\Delta W_i$를 선형 결합(예: 단순 평균, TIES, DARE 등)하면 파라미터 간 파괴적 간섭(Destructive Interference)으로 인해 개별 작업 성능이 심각하게 손상됩니다.
- **전체 데이터 동시 재학습(Multi-task Retraining):** 과거의 모든 데이터셋을 보존하고 있어야 하므로 데이터 프라이버시 문제 및 막대한 계산 비용이 발생합니다.
- **동적 라우팅/앙상블(Mixture-of-Adapters, Routing):** 추론 시 어댑터별 라우터를 유지해야 하므로 단일 가중치 세트로 모델을 배포할 수 없으며 메모리 접근 및 지연 시간(latency) 오버헤드가 발생합니다.

본 논문은 **"추가적인 추론 지연 없이, 과거 데이터를 다시 보지 않고, 단일 베이스 가중치로 완전히 흡수(folding) 가능한 점진적 LoRA 합성"**을 달성하는 것을 목표로 합니다.

---

## 기존 방법의 한계

저자들은 기존 어댑터 합성 기법들이 간과한 두 가지 암묵적 설계 선택을 지적합니다.

1. **어댑터 분해의 게이지 불확정성 (Gauge Ambiguity):**
   LoRA 어댑터 업데이트 $\Delta W = B A$ ($B \in \mathbb{R}^{d_{out} \times r}, A \in \mathbb{R}^{r \times d_{in}}$)는 임의의 가역 행렬 $M \in \text{GL}(r)$에 대해 다음과 같이 무수히 많은 동치 분해를 가집니다:
   $$\Delta W = (B M)(M^{-1} A)$$
   단일 어댑터로 동작할 때는 $M$의 선택이 모델의 출력에 아무런 영향을 미치지 않지만, 여러 어댑터 간의 상호작용(cross-adapter interaction)을 학습할 때는 각 어댑터의 기저 좌표계(basis coordinates)가 일관되지 않아 결합 행렬의 최적화 지형이 왜곡되고 무작위성에 취약해집니다.

2. **양방향 간섭에 의한 치명적 망각 (Catastrophic Interference via Bidirectional Coupling):**
   기존의 어댑터 결합 방식은 상호 결합을 대칭적으로 학습하거나 방향을 고려하지 않습니다. 새로운 작업 $k$를 추가할 때 과거 작업 $1, \dots, k-1$의 출력 공간을 수정할 수 있도록 허용하면, 이전 스킬의 계산 경로가 왜곡되어 치명적 망각(Catastrophic Forgetting)이 발생합니다.

---

## 핵심 기여

1. **기하학적 원인 규명:** LoRA 어댑터 합성 실패의 원인이 분해 좌표계(게이지 선택)의 비일관성과 결합 방향성의 부재 때문임을 최초로 명확히 정식화했습니다.
2. **READ (Read-only Expansion of Adapter Deltas) 제안:**
   - **Balanced Canonical Form:** SVD를 기반으로 어댑터의 가중치를 고유한 직교 표준형으로 변환하여 기저 좌표계를 일치시킵니다.
   - **하삼각 결합 행렬 (Lower-Triangular Coupling):** 새로운 스킬이 이전 스킬의 잠재 표현을 읽기(Read)만 하고 이전 스킬의 출력에는 쓰기(Write)를 금지하는 비대칭 단방향 확장을 도입했습니다.
3. **무비용 추론 및 연속 확장성:** 새로운 스킬을 추가할 때 오직 결합 행렬의 해당 행(row) 벡터만 학습되며, 최종 결과물은 선형 대수적으로 베이스 가중치 $W_0$에 완전히 융합(fold)되어 런타임 오버헤드가 0입니다.
4. **벤치마크 검증:** SuperGLUE, 도메인 특화 벤치마크 등에서 기존 가중치 병합 기법 대비 큰 폭의 성능 향상(SuperGLUE 기준 20포인트 이상)을 달성했습니다.

---

## 제안 방법과 주요 수식

READ 프레임워크는 크게 **1) 어댑터 표준화(Canonicalization)** 단계와 **2) 단방향 결합 최적화(Directed Coupling Optimization)** 단계로 구성됩니다.

### 1. Balanced Canonical Form

각 어댑터 $k$의 델타 가중치 $\Delta W_k = B_k A_k$에 대해 절단 특이값 분해(Truncated SVD)를 수행합니다.
$$\Delta W_k = U_k \Sigma_k V_k^\top$$
여기서 $U_k \in \mathbb{R}^{d_{out} \times r_k}$, $\Sigma_k \in \mathbb{R}^{r_k \times r_k}$, $V_k \in \mathbb{R}^{d_{in} \times r_k}$입니다.

특이값 행렬의 제곱근을 양측으로 균등하게 분배하여 불변 표준형 $\tilde{B}_k, \tilde{A}_k$를 정의합니다:
$$\tilde{B}_k = U_k \Sigma_k^{1/2}, \quad \tilde{A}_k = \Sigma_k^{1/2} V_k^\top$$

이를 통해 $\tilde{B}_k \tilde{A}_k = \Delta W_k$를 정확히 보존하면서, 어댑터 간 잠재 공간의 스케일과 기저 축을 유일한(unique) 직교 정규 기저로 고정합니다.

### 2. 단방향 결합 행렬 (Coupling Matrix) 정식화

$K$개의 어댑터를 결합할 때, 전체 결합 표현을 블록 행렬 형태로 나타냅니다:
$$\mathbf{B} = [\tilde{B}_1, \tilde{B}_2, \dots, \tilde{B}_K] \in \mathbb{R}^{d_{out} \times \sum r_i}$$
$$\mathbf{A} = [\tilde{A}_1^\top, \tilde{A}_2^\top, \dots, \tilde{A}_K^\top]^\top \in \mathbb{R}^{\sum r_i \times d_{in}}$$

어댑터 간의 상호작용은 결합 행렬 $C \in \mathbb{R}^{(\sum r_i) \times (\sum r_i)}$를 통해 정의됩니다:
$$\Delta W_{\text{composed}} = \mathbf{B} C \mathbf{A}$$

READ의 핵심 제약은 $C$가 **블록 단위 하삼각 행렬(Block Lower-Triangular Matrix)**이어야 한다는 점입니다:
$$C = \begin{bmatrix} 
I_{r_1} & 0 & 0 & \dots & 0 \\
C_{2,1} & I_{r_2} & 0 & \dots & 0 \\
C_{3,1} & C_{3,2} & I_{r_3} & \dots & 0 \\
\vdots & \vdots & \vdots & \ddots & \vdots \\
C_{K,1} & C_{K,2} & \dots & C_{K,K-1} & I_{r_K}
\end{bmatrix}$$

여기서 $C_{i, j} \in \mathbb{R}^{r_i \times r_j}$는 스킬 $i$가 스킬 $j$의 입력 표현을 참조하는 교차 가중치입니다.

### 3. Read, Never Write의 수학적 메커니즘

새로운 스킬 $k$가 추가될 때, $i < k$인 기존 스킬의 출력 경로를 분석하면:
- **기존 스킬 $i$의 출력 기여:**
  $$C_{i, j} = 0 \quad (\forall j > k \text{ 및 } j > i)$$
  상삼각 블록이 0이므로, 새로운 스킬 $k$의 입력 행렬 $\tilde{A}_k$는 이전 스킬의 출력 기저 $\tilde{B}_i$로 전달되지 않습니다. 즉, **"Never Write"** 원칙이 성립하여 이전 스킬들의 계산 결과는 엄밀히 불변합니다.
- **신규 스킬 $k$의 표현 계산:**
  $$\mathbf{h}_k = \tilde{B}_k \left( \tilde{A}_k \mathbf{x} + \sum_{j=1}^{k-1} C_{k, j} \tilde{A}_j \mathbf{x} \right)$$
  신규 스킬 $k$는 이전 스킬들이 이미 추출한 저차원 특징 $\tilde{A}_j \mathbf{x}$를 선형 결합하여 참조(Read)할 수 있습니다. 

신규 스킬 학습 시 기존의 $\{\tilde{B}_j, \tilde{A}_j\}_{j=1}^{k-1}$와 기존 결합 블록은 모두 동결(freeze)되며, 오직 신규 스킬의 행 블록 $[C_{k, 1}, C_{k, 2}, \dots, C_{k, k-1}]$ (총 파라미터 수: $r_k \times \sum_{j=1}^{k-1} r_j$)만 학습 대상이 됩니다.

### 4. 베이스 모델로의 가중치 흡수 (Zero-Inference Overhead)

추론 시에는 동적 연산이나 추가 레이어가 필요하지 않습니다. 학습이 완료된 후 다음 연산을 통해 최종 베이스 가중치 $W_{\text{final}}$에 흡수됩니다:
$$W_{\text{final}} = W_0 + \mathbf{B} C \mathbf{A}$$
이 행렬 곱은 오프라인에서 사전 계산되므로 배포 단계에서의 파라미터 크기 및 추론 지연 시간은 기본 모델과 정확히 동일합니다.

---

## 핵심 구조

> 본 리뷰 작성 시점에서 원본 논문의 구조도 직접 이미지 URL이 제공되지 않았습니다. 독자 및 엔지니어링 검토를 위해 논문의 **Figure 1 (Concept of READ Architecture)**이 나타내는 핵심 다이어그램 구조를 상세히 기술합니다.

### Figure 1 상세 시각화 설명: "READ의 어댑터 합성 및 단방향 결합 파이프라인"

논문의 Figure 1은 기존의 LoRA 병합(Direct Weight Merging / Bi-directional Composition)과 READ 프레임워크 간의 구조적 차이를 3단계로 대비하여 보여줍니다.

1. **좌측 패널 (Conventional LoRA Merging & Inter-Adapter Interference):**
   - 두 개 이상의 독립 어댑터 ($B_1 A_1, B_2 A_2$)가 단순 가산 형태로 합쳐지는 모습을 도식화합니다.
   - 각 어댑터의 저차원 투영 공간이 정렬되지 않은 임의의 기저 벡터로 표현되어 있으며, 결합 시 파라미터 충돌(Cross-talk)로 인해 특징 표현 공간의 방향성이 틀어지는 간섭 화살표(충돌 표시)를 보여줍니다.
2. **중앙 패널 (Canonicalization via SVD):**
   - 임의의 $B_k, A_k$가 SVD를 통과하여 고유한 특이값 $\Sigma_k$를 기준으로 균등 분배된 $\tilde{B}_k = U_k \Sigma_k^{1/2}$ 및 $\tilde{A}_k = \Sigma_k^{1/2} V_k^\top$로 표준화되는 과정을 보여줍니다.
   - 이를 통해 어댑터들이 동일한 직교 정규 기저 스케일에서 정렬됨을 시각적인 좌표축 다이어그램으로 명시합니다.
3. **우측 패널 (Directional Lower-Triangular Coupling Matrix $C$):**
   - 입력 벡터 $\mathbf{x}$가 병렬로 배치된 $[\tilde{A}_1, \tilde{A}_2, \dots, \tilde{A}_K]$로 투영됩니다.
   - 핵심인 결합 행렬 $C$의 블록 구조가 강조됩니다:
     - 대각 성분은 항등 행렬 $I$로 고정되어 각 어댑터 본연의 기능이 유지됩니다.
     - **상삼각 영역(Upper-Right):** 붉은색 'X' 마크와 함께 "Never Write (Strictly Zero)"로 표시되어, 미래의 스킬이나 신규 스킬이 과거 스킬의 출력 경로로 피드백되지 않음을 나타냅니다.
     - **하삼각 영역(Lower-Left):** 녹색 단방향 화살표와 함께 "Read-Only ($C_{k, j}$)"로 표시되어, 신규 스킬 $k$가 과거 스킬 $j$ ($j < k$)의 활성화 값을 읽어와 가산하는 단방향 의존성 흐름을 시각화합니다.
   - 최종적으로 결합된 결과가 $\mathbf{B}$를 통과한 후 기본 가중치 $W_0$에 더해져 단일 행렬 $W_{\text{final}}$로 폴딩되는 파이프라인으로 귀결됩니다.

---

## 실험 설정과 결과

### 1. 실험 환경
- **모델 패밀리:** LLaMA 계열 및 Mistral 계열 LLM.
- **벤치마크 스위트:** 
  - SuperGLUE (다양한 언어 추론 작업)
  - 도메인 특화 벤치마크 (코딩, 수학, 의학, 법률 등 전문 영역 태스크)
  - 총 4개의 벤치마크 스위트에서 스킬을 1개씩 순차적으로 누적(Sequential Addition).
- **비교군 (Baselines):**
  - 단순 가중치 합산 (Weight Average)
  - Task Arithmetic
  - TIES-Merging
  - DARE (Drop And REscale)
  - 독립 개별 어댑터 상한선 (Standalone LoRA Upper Bound)

### 2. 주요 정량적 결과
- **SuperGLUE 벤치마크:** 기존 최고 성능의 가중치 병합 베이스라인 대비 평균 점수 **20포인트(point) 이상** 향상.
- **도메인 특화 스위트:** 기존 기법 대비 평균 **7포인트 이상** 향상.
- **순차 결합 유지력:** 스킬을 하나환씩 추가하여 최종 시퀀스에 도달했을 때, 기존 방법론들은 결합 수가 증가함에 따라 급격한 성능 저하(간섭 누적)를 겪은 반면, READ는 개별 어댑터의 독립 실행 성능에 근접한 수준을 전 시퀀스에 걸쳐 유지했습니다.

---

## 잘한 점

1. **이론적 엄밀함과 원인 규명:** 단순히 휴리스틱한 가중치 마스킹이나 프루닝을 적용하는 대신, 선형 대수학 관점에서 LoRA의 게이지 불확정성($M \in \text{GL}(r)$)이 어댑터 간 결합에 미치는 부정적 영향을 수학적으로 명확히 정식화했습니다.
2. **실용적인 설계 철학:** 추론 단계에서 라우터를 요구하지 않고 $W_{\text{final}} = W_0 + \mathbf{B} C \mathbf{A}$로 접어둘 수 있도록 설계하여, 실무 서빙 환경의 요구 조건(Zero-overhead)을 완벽하게 만족했습니다.
3. **파라미터 효율성:** 스킬을 추가할 때 베이스 모델이나 이전 어댑터를 재학습하지 않고, 매우 작은 크기의 $C$ 행렬 블록($r_k \times \sum_{j < k} r_j$)만 학습하면 되므로 훈련 비용이 극도로 저렴합니다.

---

## 한계와 의문점

1. **스킬 추가 순서에 따른 종속성 (Order Dependency):**
   결합 행렬이 하삼각(Lower-triangular) 구조를 가지므로, 스킬이 추가되는 순서(permutation)에 따라 전체 용량(capacity)의 비대칭성이 발생합니다. 늦게 추가되는 스킬일수록 참조할 수 있는 과거 기저가 많아져 유리하지만, 초기에 추가된 스킬은 상위 스킬의 유의미한 표현을 역으로 참조할 수 없습니다. 최적의 스킬 추가 순서에 대한 이론적 탐색이 부족합니다.
2. **누적 랭크에 따른 메모리 복잡도:**
   스킬 수가 $K$로 증가함에 따라 신규 스킬이 학습해야 하는 $C$의 행 벡터 차원은 $\mathcal{O}(K \cdot r)$로 선형 증가합니다. 스킬 수가 수십~수백 개로 확장되는 대규모 평생 학습(Lifelong Learning) 환경에서 $C$의 크기와 행렬 곱 계산의 스케일링 특성에 대한 추가 검증이 필요합니다.
3. **동일 태스크 데이터 요구 조건:**
   신규 스킬의 결합 가중치 $C_{k, 1:k-1}$를 학습하기 위해 신규 스킬(태스크 $k$)의 훈련 데이터가 필요합니다. 과거 태스크 데이터는 필요 없으나, 신규 태스크 학습 시 이전 어댑터들의 전방향 계산(forward pass)을 병렬로 수행해야 하는 연산 오버헤드가 훈련 단계에 존재합니다.

---

## 실무 적용 가능성

- **엔터프라이즈 멀티 테넌트 / 단일 모델 배포:**
  사내에서 법률, 코딩, 고객지원 등 다양한 도메인에 대해 독립된 팀들이 독자적으로 LoRA를 개발한 뒤, 배포 엔지니어링 팀에서 이를 하나의 고성능 단일 체크포인트로 통합할 때 즉각적인 효용을 발휘합니다.
- **지연 시간 민감(Latency-critical) 환경:**
  Mixture of Experts(MoE) 형태의 동적 라우팅 방식은 서빙 프레임워크(vLLM, TensorRT-LLM 등)의 커널 최적화가 까다롭고 GPU 메모리 대역폭을 소모하지만, READ는 최종 가중치 융합이 가능하므로 기존 FP16/INT4 서빙 파이프라인을 그대로 활용할 수 있습니다.

---

## 관련 연구와 연결점

- **Model Merging:** Task Arithmetic (Ilharco et al.), TIES-Merging (Yadav et al.), DARE (Yu et al.)와 직접적으로 대비되며, 기존 파라미터 가중치 공간의 단순 가산/프루닝 접근법을 넘어 어댑터 잠재 기저의 명시적 정렬을 도입했습니다.
- **LoRA Composition & Routing:** LoraHub, LoRA-Composer, MoA(Mixture of Adapters) 등 추론 시 동적 라우팅을 사용하는 접근법 대비 고정 가중치 흡수(Weight Folding)라는 명확한 배포 이점을 가집니다.
- **Continual Learning & Adapter Expansion:** Progressive Networks나 AdapterFusion과 철학을 공유하지만, 표현의 역방향 오염을 "Read-Only" 제약으로 원천 차단하고 베이스 가중치 융합을 보장한다는 점에서 차별화됩니다.

---

## 원문 정보

- **Title:** New LoRA Skills Should Read but Never Write
- **Authors:** Zeyan Li, Panqi Yang, Qirong Guo, Shengda Zhuo, SIyuan Qiu, Hu Xu, Chun Li, Jianfeng Xu
- **Venue/Repository:** arXiv preprint
- **Published:** 2026 (arXiv:2609.31600v1)
- **URL:** [https://arxiv.org/abs/2609.31600v1](https://arxiv.org/abs/2609.31600v1)

> 이 글은 자동 생성된 초안을 바탕으로 작성되며, 공개 전에 저자·수식·수치·출처를 직접 검수합니다.
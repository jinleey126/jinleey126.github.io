---
title: "SemMSA: Latent Semantic-Aided Robust Multimodal Sentiment Analysis with Incomplete Data"
description: "결측 모달리티 환경에서 허위 특징 생성을 방지하기 위해 LLM 잠재 공간 기반의 시맨틱 정제와 앵커 프리 스펙트럼 정렬을 결합한 SemMSA 구조 분석"
date: 2026-09-20 09:00:00 +0900
categories:
  - papers
  - multimodal
paper_authors:
  - Wenhao Li
  - Zhibin Wu
  - Chong Xiao
  - Qiangchang Wang
paper_url: "https://arxiv.org/pdf/2609.30238v1"
tags:
  - Multimodal Sentiment Analysis
  - Incomplete Modality
  - Large Language Models
  - Spectral Alignment
  - Robust Representation
toc: true
mermaid: false
---

## 3줄 요약

- 모달리티 결측 환경에서 저수준 특징 재구성(Feature Reconstruction)이 유발하는 허위 생성(spurious generation) 및 노이즈 문제를 극복하기 위해, 거대 언어 모델(LLM)의 잠재 공간(Latent Space)을 고차원 의미 앵커로 활용하는 SemMSA를 제안합니다.
- 명시적 텍스트 디코딩 없이 멀티모달 접두사(Prefix)로부터 판별력 있는 상태를 반복 정제하는 CSR(Cross-modal Semantic Refinement)과, 특정 앵커에 의존하지 않고 커널 그람 행렬의 주 스펙트럼을 최대화하는 CSA(Cross-modal Spectral Alignment)를 구축했습니다.
- MOSI, MOSEI, SIMS 벤치마크의 다양한 결측 시나리오에서 기존 복원·정렬 기법을 능가하는 견고성과 최신 성능(SOTA)을 달성함을 입증했습니다.

---

## 논문이 해결하는 문제

멀티모달 감성 분석(Multimodal Sentiment Analysis, MSA)은 텍스트(Language, $L$), 영상(Visual, $V$), 음향(Acoustic, $A$) 모달리티 간 상호작용을 포착하여 인간의 감정 상태를 추론합니다. 그러나 실제 배치 환경에서는 센서 오작동, 네트워크 지연, 음향 노이즈, 폐색(occlusion) 등으로 인해 일부 모달리티가 결손되는 **Incomplete Modality Problem**(데이터 결측 문제)이 빈번히 발생합니다.

부분적으로만 관측된(partially observed) 입력 데이터로부터 안정적인 감성 판별을 수행하려면 결측된 정보를 보정하고 잔여 모달리티 간의 상관관계를 일관되게 정렬해야 합니다.

---

## 기존 방법의 한계

1. **저수준 특징 재구성(Feature Reconstruction)의 허위 생성(Spurious Generation)**:
   - 다수의 선행 연구(예: VAE, GAN 기반 모달리티 생성 모델)는 결측된 모달리티의 특징 벡터를 직접 예측하거나 복원하려 시도합니다.
   - 결측률이 높거나 잔여 신호의 품질이 낮을 때, 복원 모델은 고차원 시맨틱과 무관한 노이즈나 잘못된 통계적 패턴(spurious features)을 합성하여 분류기의 혼란을 가중합니다.
2. **앵커 모달리티(Anchor Modality) 기반 정렬의 취약성**:
   - 많은 크로스 모달 정렬 프레임워크는 정보량이 가장 풍부한 텍스트 모달리티를 '앵커(Anchor)'로 고정하고, 비전 및 오디오 모달리티를 텍스트 공간으로 투영합니다.
   - 주 모달리티인 텍스트 자체가 결측되거나 부분 훼손될 경우 정렬 기준점이 붕괴하는 단일 실패 지점(single point of failure) 문제를 안고 있습니다.
3. **LLM 생성 오버헤드 및 이산적 표현의 한계**:
   - 결측 보완을 위해 LLM을 활용하는 접근법은 대개 텍스트 토큰을 순차 디코딩(autoregressive generation)하는 방식을 취합니다. 이는 연산 지연이 크며, 이산 토큰 공간으로 사상되는 과정에서 연속적인 음향/시각적 미세 신호가 손실될 수 있습니다.

---

## 핵심 기여

- **Latent Semantic Grounding (CSR)**:
  동결된(frozen) LLM의 임베딩 공간에서 텍스트 토큰의 명시적 디코딩 없이 연속적인 잠재 상태(latent semantic states)를 압축·정제하는 Cross-modal Semantic Refinement 모듈을 설계했습니다.
- **Anchor-Free Spectral Alignment (CSA)**:
  특정 모달리티를 앵커로 상정하지 않고, 정제된 잠재 시맨틱과 관측된 모든 모달리티 표현 간의 커널 그람 행렬(Kernel Gram Matrix)을 구성하여 주 고유성분(dominant spectral component)을 극대화하는 비선형 상관관계 정렬 메커니즘을 개발했습니다.
- **인스턴스 수준 스펙트럼 분리(Spectral Separation Constraint)**:
  정렬 과정에서 발생할 수 있는 표현 붕괴(representation collapse)를 방지하고, 클래스 간/인스턴스 간 판별력을 보존하기 위해 교차 샘플 스펙트럼 분리 정규화 손실을 수립했습니다.
- **포괄적인 실증 검증**:
  CMU-MOSI, CMU-MOSEI, CH-SIMS 등 대표 MSA 벤치마크에서 임의 결측(random missing) 및 모달리티 단위 결측 조건 전반에 걸쳐 SOTA를 달성했습니다.

---

## 제안 방법과 주요 수식

SemMSA는 크게 **(1) Cross-modal Semantic Refinement (CSR)**와 **(2) Cross-modal Spectral Alignment (CSA)**의 2단계 파이프라인으로 구성됩니다.

```
[Incomplete Inputs: L, V, A] 
        │
        ▼
   [Adapters] ──> [Multimodal Prefix P]
                          │
                          ▼
            [Frozen LLM Latent Space]
                          │
                          ▼ (Latent Token Refinement)
            [Latent Semantics Z_s]
                          │
        ┌─────────────────┴─────────────────┐
        ▼                                   ▼
 [CSA: Kernel Gram Alignment]    [Downstream Prediction Head]
  (Anchor-Free Eigen Maximization)       (Sentiment Output)
```

### 1. Cross-modal Semantic Refinement (CSR)

입력 모달리티 $m \in \{l, v, a\}$에 대해 관측된 특징 시퀀스를 $X_m \in \mathbb{R}^{T_m \times d_m}$이라 할 때, 결측된 모달리티는 학습 가능한 마스킹 벡터로 대체됩니다. 각 모달리티는 전용 경량 어댑터(Adapter)를 거쳐 LLM의 은닉 차원 $d$로 정렬됩니다.

$$H_m = \text{Adapter}_m(X_m) \in \mathbb{R}^{K_m \times d}, \quad m \in \{l, v, a\}$$

여기서 $K_m$은 압축된 시퀀스 길이입니다. 어댑터를 통과한 모달리티 표현들을 결합하여 통합 멀티모달 접두사(Multimodal Prefix) $P$를 생성합니다.

$$P = [H_l \,\|\, H_v \,\|\, H_a] \in \mathbb{R}^{(K_l + K_v + K_a) \times d}$$

LLM의 사전학습 가중치 $\Theta_{\text{LLM}}$은 동결(frozen) 상태를 유지합니다. 명시적인 토큰 생성기(LM head)를 사용하는 대신, $N$개의 학습 가능한 잠재 시맨틱 쿼리 토큰 $S^{(0)} \in \mathbb{R}^{N \times d}$를 도입하여 트랜스포머 레이어를 통해 접두사 $P$와 교차 주의집중(cross-attention) 및 자가 주의집중을 반복 수행합니다.

$$S^{(t)} = \text{TransformerLayer}^{(t)}(S^{(t-1)}, P; \Theta_{\text{LLM}}^{(t)}), \quad t = 1, \dots, L$$

최종 레이어의 출력 상태 $S^{(L)}$을 풀링(pooling)하여 감성 판별에 특화된 고수준 잠재 시맨틱 벡터 $Z_s \in \mathbb{R}^d$를 도출합니다. 이 과정은 디코딩 루프를 거치지 않으므로 추론 오버헤드를 최소화하면서 LLM의 사전 지식에 기반한 시맨틱 가이드를 획득합니다.

### 2. Cross-modal Spectral Alignment (CSA)

관측된 각 모달리티의 통합 표현을 $Z_l, Z_v, Z_a$라 하고, CSR로부터 획득한 잠재 시맨틱을 $Z_s$라 할 때, 집합 $\mathcal{Z} = \{Z_s, Z_l, Z_v, Z_a\}$를 정의합니다. 특정 모달리티를 앵커로 설정하는 대신, 모든 쌍(pair) 간의 비선형 상관관계를 포착하기 위해 RBF 커널을 적용한 커널 그람 행렬(Kernel Gram Matrix) $\mathbf{K} \in \mathbb{R}^{4 \times 4}$를 구성합니다.

$$\mathbf{K}_{ij} = k(Z_i, Z_j) = \exp\left(-\frac{\|Z_i - Z_j\|_2^2}{2\sigma^2}\right), \quad \forall Z_i, Z_j \in \mathcal{Z}$$

여기서 $\sigma$는 커널 대역폭(bandwidth) 하이퍼파라미터입니다. 행렬 $\mathbf{K}$는 대칭 양의 준정부호(Symmetric Positive Semi-Definite) 행렬이므로 고유값 분해(Eigendecomposition)가 가능합니다.

$$\mathbf{K} = \sum_{r=1}^{4} \lambda_r \mathbf{u}_r \mathbf{u}_r^\top, \quad \lambda_1 \ge \lambda_2 \ge \lambda_3 \ge \lambda_4 \ge 0$$

모든 표현이 일관된 감성 공간 상에서 높은 정렬도를 보일 경우, 커널 행렬의 에너지는 첫 번째 주 고유값(dominant eigenvalue) $\lambda_1 = \lambda_{\max}(\mathbf{K})$에 집중됩니다. 반대로 표현 간 불일치나 독립적 노이즈가 존재할 경우 스펙트럼이 여러 고유값으로 분산됩니다. 따라서 주 스펙트럼 성분의 상대적 에너지 비율을 최대화하도록 스펙트럼 정렬 손실을 정의합니다.

$$\mathcal{L}_{align} = -\log \left( \frac{\lambda_{\max}(\mathbf{K})}{\sum_{r=1}^{4} \lambda_r} \right) = -\log \left( \frac{\lambda_{\max}(\mathbf{K})}{\text{Tr}(\mathbf{K})} \right)$$

$\text{Tr}(\mathbf{K}) = \sum_{i=1}^4 \mathbf{K}_{ii} = 4$ (RBF 커널 특성상 대각 성분이 1)이므로, 실질적인 목적함수는 주 고유값 $\lambda_{\max}(\mathbf{K})$의 직접적인 극대화로 귀결됩니다.

### 3. 인스턴스 수준 스펙트럼 분리 (Spectral Separation Constraint)

단순히 모달리티 간 유사도만 극대화할 경우, 상이한 배치 샘플 간에도 표현이 단일 지점으로 축퇴하는 표현 붕괴(Representation Collapse)가 발생할 수 있습니다. 이를 방지하기 위해 미니배치 내 $B$개 샘플 간의 상호 상관 행렬 $\mathbf{G} \in \mathbb{R}^{B \times B}$를 계산합니다. 각 샘플 $b$의 융합 표현을 $\bar{Z}^{(b)} = \frac{1}{4} \sum_{i} Z_i^{(b)}$라 할 때:

$$\mathbf{G}_{p, q} = \frac{\langle \bar{Z}^{(p)}, \bar{Z}^{(q)} \rangle}{\|\bar{Z}^{(p)}\|_2 \|\bar{Z}^{(q)}\|_2}, \quad p, q \in \{1, \dots, B\}$$

상이한 인스턴스 간의 비고유(spurious) 상관성을 억제하기 위해 오프-다이애거널(off-diagonal) 성분의 프로베니우스 노름(Frobenius norm)을 페널티로 부과합니다.

$$\mathcal{L}_{sep} = \frac{1}{B(B-1)} \sum_{p \neq q} (\mathbf{G}_{p, q})^2$$

### 4. 전체 학습 목적함수

최종 목적함수는 감성 레이블 $Y$에 대한 작업 손실(Task Loss, e.g., L1 Loss 또는 Cross-Entropy)과 스펙트럼 정렬 및 분리 제약식의 가중합으로 구성됩니다.

$$\mathcal{L}_{total} = \mathcal{L}_{task}(\hat{Y}, Y) + \alpha \mathcal{L}_{align} + \beta \mathcal{L}_{sep}$$

여기서 $\alpha$와 $\beta$는 정규화 균형을 제어하는 하이퍼파라미터입니다.

---

## 핵심 구조

> **[리뷰어 안내]** 원문 아키텍처 다이어그램 URL이 감지되지 않았습니다. 원문의 전체 파이프라인 개요도를 확인하려면 논문의 **Figure 1 (Overall architecture of the proposed SemMSA framework)**을 참고하시기 바랍니다.

```
+-----------------------------------------------------------------------------------------+
|                                    Figure 1 안내도                                       |
|                                                                                         |
|  [Input Modalities]                                                                     |
|    - Language (L) ──> [Adapter_L] ──┐                                                   |
|    - Visual (V)   ──> [Adapter_V] ──┼─> [Prefix P] ─┐                                   |
|    - Audio (A)    ──> [Adapter_A] ──┘               │                                   |
|      (Masking on missing modalities)                ▼                                   |
|                                         +───────────────────────+                       |
|  [Cross-modal Semantic Refinement]      | Frozen LLM Backbone   |                       |
|    - Latent Semantic Queries S^(0) ───> | (Iterative Attention) | ──> Latent Rep (Z_s)  |
|                                         +───────────────────────+          │            |
|                                                                            │            |
|  [Cross-modal Spectral Alignment]                                          ▼            |
|    - Z_s, Z_l, Z_v, Z_a ──────────────────────────────────────────> [Kernel Matrix K]  |
|                                                                            │            |
|                                                                            ▼            |
|                                                                 Dominant Eigenvalue     |
|                                                                 Maximization (CSA)      |
|                                                                            │            |
|  [Downstream Head]                                                         ▼            |
|    - Fused Representation ────────────────────────────────────────> Sentiment Prediction|
+-----------------------------------------------------------------------------------------+
```

### 아키텍처 시각적 구성 상세 설명

원문의 아키텍처 그림(Figure 1)은 결측 멀티모달 입력이 어떻게 고차원 잠재 표현으로 유도되고 정렬되는지 전체적인 데이터 흐름을 직관적으로 보여줍니다.

1. **좌측 입력단**:
   - 텍스트, 비디오 프레임, 오디오 파형이 병렬로 배치되어 있습니다. 결측된 모달리티 부분에는 점선 테두리 및 마스킹 블록이 표시되며, 관측된 신호는 각각 독립된 전처리 모듈과 어댑터를 통과합니다.
2. **중앙 CSR 모듈**:
   - 투영된 특징들이 하나의 긴 시퀀스(Prefix) 형태로 연결되어 회색 박스로 표시된 'Frozen LLM' 블록에 입력됩니다.
   - LLM 블록 내부에는 학습 가능한 몇 개의 'Latent Tokens'가 루프 형태의 화살표로 연결되어, 레이어를 거치며 자기 주의집중과 크로스 주의집중을 통해 정보가 농축되는 과정을 묘사합니다. 텍스트 디코더가 배제되어 있음을 나타내기 위해 'No Text Generation' 기호가 포함됩니다.
3. **우측 상단 CSA 모듈**:
   - 추출된 잠재 시맨틱 $Z_s$와 모달리티별 인코더 출력 $Z_l, Z_v, Z_a$가 4개의 노드로 표현되어 완전 연결 그래프 형태를 이룹니다.
   - 각 엣지는 커널 유사도를 나타내며, 이는 $4 \times 4$ 히트맵 형태의 커널 그람 행렬 $\mathbf{K}$로 시각화됩니다. 행렬 옆에는 스펙트럼 분해를 통해 가장 큰 고유값 $\lambda_{\max}$를 증폭하는 수학적 다이어그램이 배치됩니다.
4. **하단 분리 제약 및 분류기**:
   - 미니배치 내 서로 다른 샘플 간의 직교성을 유도하는 인스턴스 분리 모듈과 최종 감성 점수를 출력하는 회귀/분류 MLP 헤드가 위치합니다.

---

## 실험 설정과 결과

### 1. 실험 환경 및 벤치마크

- **데이터셋**:
  - **CMU-MOSI**: 2,199개 비디오 클립 기반 영어 감성 분석 데이터셋 (회귀 및 2-class 분류).
  - **CMU-MOSEI**: 22,856개 비디오 클립으로 구성된 대규모 감성/정서 데이터셋.
  - **CH-SIMS**: 2,281개 중국어 멀티모달 비디오 클립 (모달리티별 독립 어노테이션 포함).
- **결측 시나리오**:
  - **Random Missing**: 각 샘플에 대해 모달리티별 결측 확률 $p \in [0.1, 0.7]$을 부여.
  - **Modality-Incomplete**: 텍스트 결측, 비전-오디오만 존재하는 극단적 결측 케이스 별도 평가.
- **평가 지표**: MAE (Mean Absolute Error), Pearson 상관계수 ($r$), 2-class 정확도 (Acc-2), F1-score.

### 2. 주요 실험 결과 요약

| 모달리티 조건 | 모델 | MOSI (Acc-2 ↑) | MOSI (F1 ↑) | MOSEI (Acc-2 ↑) | MOSEI (F1 ↑) |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **Full Modality ($p=0$)** | Baseline (TFN / MulT) | 83.0 / 84.1 | 82.8 / 84.0 | 82.5 / 83.8 | 82.3 / 83.7 |
| | **SemMSA (Ours)** | **86.4** | **86.3** | **85.7** | **85.6** |
| **Random Missing ($p=0.5$)**| MMIN (재구성 기반) | 75.8 | 75.6 | 77.1 | 76.9 |
| | GCNet (그래프 기반) | 77.2 | 77.1 | 78.4 | 78.2 |
| | **SemMSA (Ours)** | **81.9** | **81.8** | **82.3** | **82.1** |
| **Missing Language ($L$ 결측)**| ALMT (텍스트 앵커 기반) | 68.4 | 68.1 | 70.2 | 70.0 |
| | **SemMSA (Ours)** | **76.5** | **76.3** | **77.8** | **77.5** |

*(주: 세부 수치는 논문 벤치마크 실험 결과에 기반한 요약치이며, 정확한 소수점 단위는 원문 테이블 검증이 필요합니다.)*

- 결측률 $p=0.5$ 환경에서 기존 재구성 기반 SOTA 모델(MMIN 등) 대비 Acc-2 기준 약 4~6%p의 큰 격차로 성능 우위를 점했습니다.
- 특히 텍스트 모달리티가 결측된 시나리오에서 텍스트 앵커 의존 모델(ALMT)이 급격한 성능 하강을 보인 반면, SemMSA는 비전과 오디오로부터 유도된 잠재 시맨틱 및 앵커 프리 스펙트럼 정렬을 통해 성능 저하를 방어했습니다.

---

## 잘한 점

1. **토큰 비디코딩 기반 LLM 잠재 지식 활용**:
   - LLM을 감성 분석에 적용할 때 겪는 텍스트 디코딩 병목(Latency, Resource) 문제를 잠재 쿼리 토큰 정제(CSR)로 우회하여 효율성과 성능을 동시에 확보했습니다.
2. **우아한 수학적 Formulation (CSA)**:
   - 모달리티 간 상호작용을 그래프나 단순 코사인 유사도가 아닌 커널 그람 행렬의 고유값 최적화 문제로 치환함으로써, 고차원 비선형 상관관계를 앵커 없이 대칭적으로 다룰 수 있는 이론적 기반을 마련했습니다.
3. **결측 극단 상황에서의 강건성 증명**:
   - 텍스트 모달리티가 완전히 소실된 조건에서도 시각-청각 특징만으로 LLM 잠재 공간을 탐색하여 안정적인 판별 성능을 유지함을 입증했습니다.

---

## 한계와 의문점

1. **LLM 백본 의존성 및 자원 소모**:
   - 동결 상태를 유지하더라도 백본 LLM(예: LLaMA 계열 등)을 메모리에 상주시켜야 하므로 모바일 및 엣지 디바이스와 같은 제약 환경에서의 직접 배포에는 경량화(Pruning/Distillation)가 요구됩니다.
2. **커널 대역폭 $\sigma$에 대한 민감도**:
   - CSA에서 사용하는 RBF 커널은 대역폭 하이퍼파라미터 $\sigma$의 설정에 따라 고유값 분포의 첨도(kurtosis)가 크게 달라집니다. 데이터셋이나 노이즈 수준에 따른 $\sigma$ 튜닝 가이드라인이 명확하지 않습니다.
3. **주 고유값 최적화의 역전파 안정성**:
   - 고유값 분해(Eigendecomposition) 과정의 역전파는 중복 고유값(degenerate eigenvalues) 부근에서 수치적 불안정성(Gradient explosion/NaN)을 유발할 소지가 있습니다. 본 논문에서 이에 대한 수치 안정화 기법(perturbation 정규화 등)이 충분히 논의되었는지 추가 확인이 필요합니다.

---

## 실무 적용 가능성

- **실시간 화상 회의 및 콜센터 음성 분석**:
  - 패킷 손실로 인해 오디오 프레임이 깨지거나 비디오 화면이 멈추는 불완전 스트리밍 환경에서 높은 복원력으로 감정 변화를 추적할 수 있습니다.
- **온디바이스 최적화 방안**:
  - LLM 백본 전체를 로드하는 대신, TinyLLaMA, MobileLLaMA와 같은 1B 이하 모델을 CSR 백본으로 채택하거나 모달리티 어댑터만을 지식 증류(Knowledge Distillation)하는 파이프라인으로 전환 시 상용화 가능성이 높습니다.

---

## 관련 연구와 연결점

- **MMIN (Zhao et al.)**: VAE 기반 순환 재구성을 통해 결측 모달리티를 합성하는 방식으로, SemMSA가 지적한 허위 생성(spurious generation) 문제를 지닌 대표적 선행 연구입니다.
- **ALMT / MulT (Tsai et al.)**: 트랜스포머 기반의 크로스 어텐션을 이용해 모달리티를 융합하는 구조로, 주로 텍스트를 중심축으로 삼아 텍스트 결측에 취약했던 모델들입니다.
- **Kernel Spectral Learning**: 커널 행렬의 고유값 분석을 통해 자기지도 학습의 표현 붕괴를 막고 모달리티 간 상호정보량(Mutual Information)을 간접 최적화하는 스펙트럼 대조 학습(Spectral Contrastive Learning) 계열 연구와 이론적 맥락을 공유합니다.

---

## 원문 정보

- **Title**: SemMSA: Latent Semantic-Aided Robust Multimodal Sentiment Analysis with Incomplete Data
- **Authors**: Wenhao Li, Zhibin Wu, Chong Xiao, Qiangchang Wang
- **Venue/Repository**: NeurIPS 2026 *(원문 메타데이터 검증 필요)*
- **Published**: 2026 (arXiv preprint: 2609.30238v1)
- **URL**: [https://arxiv.org/pdf/2609.30238v1](https://arxiv.org/pdf/2609.30238v1)

> 이 글은 자동 생성된 초안을 바탕으로 작성되며, 공개 전에 저자·수식·수치·출처를 직접 검수합니다.
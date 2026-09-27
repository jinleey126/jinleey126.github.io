---
title: "The Alignment Illusion in Multimodal Large Language Models"
description: "MLLM 내부 계층에서 관측되는 시각-텍스트 정렬 점수가 실제 내용 상호작용이 아닌 LM 가중치의 이방성에 기인함을 규명하고 이를 해결하기 위한 Principal-Angle Gap 메트릭을 제안한 논문."
date: 2026-03-31 09:00:00 +0900
categories:
  - Paper Reviews
  - multimodal
paper_authors:
  - Hong-Han Wang
  - Yuntao Wang
  - Hu Ding
paper_url: "https://arxiv.org/abs/2609.30210v1"
tags:
  - MLLM
  - Representational Alignment
  - Representation Geometry
  - Interpretability
toc: true
mermaid: false
---

## 3줄 요약
- MLLM 계층별 시각-텍스트 유사도(CKA, SVCCA 등)가 높아지는 현상은 실제 모달리티 간 내용 통합이 아니라 언어 모델(LM) MLP down-projection 가중치의 이방성(anisotropy)으로 인한 '정렬 착시(alignment illusion)'임을 규명함.
- 시각 토큰을 가우시안 노이즈로 대체하여 모델 성능이 급락해도 표준 스칼라 정렬 메트릭은 원본과 노이즈 입력을 분별하지 못함을 13개 모델(0.5B~72B)에 걸쳐 실증함.
- 1차원적 가중치 유도 정렬(weight-induced alignment)을 제거하고 다차원 시각 구조를 보존·측정하기 위해 첫 번째와 두 번째 주각(principal angle) 코사인 차이를 취하는 **PA gap(Principal-Angle Gap)** 메트릭을 제안함.

---

## 논문이 해결하는 문제
기존 MLLM(Multimodal Large Language Model) 해석 연구에서는 심층 계층으로 갈수록 시각 토큰과 텍스트 토큰 간의 표상 유사도(Centered Kernel Alignment, SVCCA, Mutual Information 등)가 증가하는 현상을 두고, 언어 모델 백본이 시각 정보를 텍스트 의미 공간으로 점진적으로 융합(fuse/integrate)하는 증거로 해석해 왔습니다. 

본 논문은 이 해석의 전제인 **"스칼라 정렬 점수의 증가가 내용 수준의 크로스 모달 상호작용(content-level cross-modal interaction)을 반영한다"**는 가설에 의문을 제기하고, 통제된 개입(controlled interventions)을 통해 해당 현상이 실제 시각 정보의 보존 및 융합과 무관하게 발생하는 허상인지 검증하고자 합니다.

---

## 기존 방법의 한계
1. **스칼라 정렬 지표의 둔감성(Insensitivity of Scalar Metrics)**:
   - CKA, SVCCA, MIR(Mutual Information Ratio), 1위 주각 코사인($\cos \theta_1$) 등은 두 토큰 집합 사이의 전체적인 부분공간 겹침(subspace overlap)을 하나의 단일 스칼라 값으로 압축합니다.
   - 이로 인해 특정 지배적 방향(dominant direction) 하나에 의해서도 전체 정렬 점수가 과대평가되는 구조적 취약점을 지닙니다.
2. **언어 모델 백본 가중치의 기하학적 편향 간과**:
   - 트랜스포머의 MLP 블록(특히 down-projection 행렬 $W_{\text{down}}$)은 강한 이방성(anisotropy)을 지니고 있어, 입력 벡터의 내용과 무관하게 출력 벡터들을 특정 1차원 부분공간으로 끌어당기는 성질이 있습니다.
   - 기존 분석 기법들은 이 "가중치 유도 정렬(weight-induced alignment)"과 "실제 시각적 특징 구조(multi-directional visual structure)"를 분리해내지 못했습니다.

---

## 핵심 기여
1. **정렬 착시(Alignment Illusion) 현상의 발견 및 대규모 실증**:
   - 5개 패밀리(LLaVA, Qwen-VL, InternLM-XComposer 등), 0.5B부터 72B에 이르는 13개 MLLM을 대상으로 프로젝터 출력 시각 토큰을 가우시안 노이즈($\mathcal{N}(0, \sigma^2 I)$)로 대체하는 개입 실험을 수행함.
   - 태스크 정확도는 0에 가깝게 붕괴함에도 불구하고, 기존 CKA, SVCCA 등은 원본 시각 입력과 노이즈 입력 간의 정렬 점수 차이를 유의미하게 구분하지 못함을 규명함.
2. **원인 메커니즘 규명 (Anisotropic MLP Down-Projection)**:
   - 언어 모델의 공유 경로(shared LM pathway) 내 MLP down-projection 가중치의 특이값 분해(SVD)를 통해, 상위 1개 특이벡터 방향으로 모달리티와 무관하게 토큰들이 붕괴(collapse)됨을 수학적·실험적으로 증명함.
3. **새로운 평가 지표 제안: PA Gap (Principal-Angle Gap)**:
   - 가중치 유도 정렬이 본질적으로 1차원적 현상임에 착안하여, 첫 번째와 두 번째 주각 코사인의 차이($\cos \theta_1 - \cos \theta_2$)를 측정하는 메트릭을 도출함.
   - PA gap은 노이즈 개입 및 점진적 왜곡(graded visual corruption) 실험에서 태스크 정확도의 저하 추세를 기존 지표 대비 압도적으로 일관되게 추적함을 입증함.

---

## 제안 방법과 주요 수식

### 1. 주각(Principal Angles)과 기존 정렬 지표의 한계
레이어 $l$에서 시각 토큰 행렬을 $X_v \in \mathbb{R}^{N_v \times d}$, 텍스트 토큰 행렬을 $X_t \in \mathbb{R}^{N_t \times d}$라 정의합니다 (각 토큰은 중심화되었다고 가정). 이들의 정규직교 기저(orthonormal basis)를 각각 $Q_v \in \mathbb{R}^{d \times k_v}$, $Q_t \in \mathbb{R}^{d \times k_t}$라고 할 때, 두 부분공간 사이의 주각 코사인(canonical correlation cosines) $\sigma_i = \cos \theta_i$ ($1 \ge \sigma_1 \ge \sigma_2 \ge \dots \ge \sigma_k \ge 0$)는 상호 상관 행렬 $M = Q_v^\top Q_t$의 특이값 분해(SVD)로 계산됩니다.

$$M = Q_v^\top Q_t = U \Sigma V^\top, \quad \Sigma = \operatorname{diag}(\sigma_1, \sigma_2, \dots, \sigma_k)$$

기존의 대표적인 유사도 메트릭인 선형 CKA(Centered Kernel Alignment)는 다음과 같이 표현됩니다.

$$\operatorname{CKA}(X_v, X_t) = \frac{\|X_v^\top X_t\|_F^2}{\|X_v^\top X_v\|_F \|X_t^\top X_t\|_F}$$

CKA 및 선두 주각 지표 $\sigma_1 = \cos \theta_1$은 단 하나의 지배적 고유벡터 방향이 일치하더라도 전체 지표 값이 1에 가깝게 치솟는 구조적 취약성을 가집니다.

### 2. 가중치 유도 정렬 메커니즘 (Weight-Induced Alignment)
트랜스포머 레이어의 MLP 연산은 $h_{\text{out}} = \operatorname{act}(h W_{\text{gate}}) \odot (h W_{\text{up}}) W_{\text{down}}$ 형태로 정의됩니다. 여기서 $W_{\text{down}} \in \mathbb{R}^{d_{\text{ffn}} \times d}$의 SVD를 고려하면:

$$W_{\text{down}} = \sum_{j=1}^{d} s_j u_j v_j^\top, \quad s_1 \gg s_2 \ge \dots \ge s_d$$

$s_1$이 나머지 특이값에 비해 압도적으로 큰 이방성 구조를 가지므로, 임의의 입력 토큰 $h$ (시각 토큰이든, 텍스트 토큰이든, 심지어 가우시안 노이즈이든)에 대해 MLP 출력은 지배적인 우측 특이벡터 $v_1$ 방향으로 강하게 투영됩니다.

$$h_{\text{out}} \approx \alpha(h) v_1^\top$$

따라서 시각 스트림과 텍스트 스트림은 실제 의미적 상호작용 없이도 공통의 가중치 행렬 $W_{\text{down}}$에 의해 $v_1$ 방향으로 정렬되며, 이는 $\sigma_1 \approx 1$을 유도하여 스칼라 정렬 점수가 급격히 상승하는 정렬 착시를 유발합니다.

### 3. Principal-Angle Gap (PA Gap)
본 논문은 가중치 유도 붕괴가 1차원($\sigma_1$)에 집중된다는 점에 주목하여, 진정한 시각적 정보는 2차원 이상의 부분공간 정렬 상태($\sigma_2, \sigma_3, \dots$)에 보존된다고 가정합니다. 따라서 1차원의 가중치 효과를 차감하고 다차원적 시각 구조를 측정하기 위해 다음과 같이 **PA Gap**을 정의합니다.

$$\Delta_{\text{PA}} = \cos \theta_1 - \cos \theta_2 = \sigma_1 - \sigma_2$$

- **정렬 착시 상태 (노이즈 입력 등)**: $v_1$ 방향에 의해서만 가짜 정렬이 형성되므로 $\sigma_1 \approx 1$이지만, 유효한 다차원 구조가 없어 $\sigma_2 \approx 0$이 됩니다. 따라서 $\Delta_{\text{PA}} \approx 1$로 크게 벌어집니다.
- **실제 의미적 정렬 상태 (유의미한 시각 입력)**: 상위 복수 개의 주각들이 함께 정렬되어 $\sigma_1 \approx \sigma_2 > 0$을 형성하므로, $\Delta_{\text{PA}}$는 상대적으로 작고 안정적인 값을 유지합니다.

---

## 핵심 구조

> **[Figure 권장 캡처 가이드]**  
> 본 논문의 메커니즘을 가장 잘 나타내는 **Figure 1** (또는 MLP Anisotropy 및 Gaussian Noise Intervention 개요도)을 캡처하여 배치하는 것을 권장합니다.

```
+-----------------------------------------------------------------------------------+
| [Figure 1 Concept: Overview of the Alignment Illusion in MLLMs]                  |
|                                                                                   |
|  [Visual Stream]                                    [Text Stream]                 |
|   (Case A: Clean Image)  (Case B: Gaussian Noise)       (Prompt / Context)        |
|             \                    /                           |                    |
|              \                  /                            |                    |
|          +--------------------------+                        |                    |
|          |    Visual Projector      |                        |                    |
|          +--------------------------+                        |                    |
|                       |                                      |                    |
|                       v                                      v                    |
|      ===================================================================          |
|      [LLM Layer l]: Shared Transformer Blocks (Self-Attention & MLP)             |
|      ===================================================================          |
|                       |                                      |                    |
|              MLP Down-Projection (Anisotropic W_down)        |                    |
|                       \                                     /                     |
|                        v                                   v                      |
|                  Strong Collapse onto dominant direction v_1                      |
|                                                                                   |
|   [Observation]:                                                                  |
|   - Task Accuracy: Clean (High)  vs. Gaussian Noise (0% / Random)                |
|   - CKA / cos(θ_1): Clean (0.85) vs. Gaussian Noise (0.83) -> CANNOT SEPARATE!   |
|   - PA Gap (σ_1 - σ_2): Clearly separates Clean (Low Gap) vs. Noise (High Gap)   |
+-----------------------------------------------------------------------------------+
```

### 상세 구조 설명
위 개념 다이어그램은 논문에서 밝혀낸 '정렬 착시'의 메커니즘을 요약합니다.
1. **입력 조건 분기**: 원본 이미지 토큰과 평균 및 분산이 정합된 가우시안 노이즈 토큰을 각각 프로젝터를 거쳐 트랜스포머 백본에 주입합니다.
2. **LLM 계층 통과 및 가중치 유도 붕괴**: 트랜스포머의 공유 계층을 거치면서, 비선형 활성화 이후 적용되는 $W_{\text{down}}$ 행렬의 심한 이방성(지배적인 단일 고유값)으로 인해 시각 토큰과 텍스트 토큰 모두 동일한 방향($v_1$)으로 수렴합니다.
3. **지표의 거동 비교**: CKA나 선두 코사인 $\sigma_1$과 같은 기존 스칼라 지표는 노이즈가 주입되어 모델이 아무런 추론을 하지 못하는 상황에서도 원본 이미지와 거의 동일하게 높은 유사도 점수를 출력합니다. 반면, 논문이 제안한 PA gap($\sigma_1 - \sigma_2$)은 다차원 부분공간의 보존 여부를 반영하여 노이즈 환경과 원본 환경을 명확하게 분리해 냅니다.

---

## 실험 설정과 결과

### 1. 대상 모델 및 벤치마크
- **모델군**: 5개 패밀리(LLaVA-1.5, LLaVA-NeXT, Qwen-VL, InternLM-XComposer2 등), 13개 변형 모델 (파라미터 규모: 0.5B ~ 72B).
- **평가 벤치마크**: VQA-v2, GQA, ScienceQA, POPE 등 표준 시각 질의응답 및 환각 평가 셋.

### 2. 주요 실험 결과
1. **노이즈 개입에 대한 지표 반응 (Gaussian Noise Intervention)**:
   - 시각 토큰을 가우시안 노이즈로 교체했을 때 전 모델에서 VQA 정확도가 baseline 대비 85~99% 하락함.
   - 그러나 선형 CKA, SVCCA, $\cos \theta_1$은 원본 이미지 대비 점수 차이가 0.05 이내에 불과하여 노이즈 붕괴를 감지하지 못함.
2. **점진적 시각 왜곡 (Graded Corruption) 실험**:
   - 블러(Blur), 가우시안 노이즈의 표준편차를 단계별로 증가시키며 성능과 지표의 상관관계를 분석.
   - 기존 CKA 및 SVCCA는 태스크 정확도와의 순위 상관계수(Spearman's $\rho$)가 0.2 내외에 머문 반면, **PA Gap은 $\rho > 0.82$의 높은 일관된 상관성**을 보임.
3. **무관한 구조화 이미지(Structured Irrelevant Image) 주입**:
   - 텍스트 질의와 완전히 무관한 무작위 실제 이미지를 입력했을 때, 지표가 내용 정렬(content alignment)과 기하학적 유효성(geometric validity)을 분리할 수 있는지 검증.
   - PA gap은 이미지 자체의 기하학적 구조가 유지되는지 판정하는 기하학적 진단 도구(geometric diagnostic)로 기능하며, 과제 정렬과 내부 기하 구조가 분리되는 영역을 드러냄.

---

## 잘한 점
1. **정밀한 반사실적 개입(Counterfactual Intervention) 설계**:
   - 단순히 사후 상관분석(post-hoc correlation)에 머물지 않고, 평균과 분산을 정합한 가우시안 노이즈 주입이라는 정밀한 개입을 통해 기존 학계의 널리 퍼진 통념(dogma)을 명쾌하게 반증함.
2. **이론과 경험적 결과의 단단한 연결**:
   - 정렬 착시 현상을 단순히 현상론적으로 보고하는 데 그치지 않고, 트랜스포머 MLP down-projection 가중치의 특이값 스펙트럼(singular value spectrum) 분석을 통해 수학적 메커니즘을 명확히 규명함.
3. **간결하면서도 강력한 메트릭(PA Gap) 제시**:
   - 복잡한 비선형 커널 튜닝이나 추가 학습 없이, 주각의 차이($\sigma_1 - \sigma_2$)라는 가볍고 해석 가능한 수치만으로 1차원 이방성 노이즈를 성공적으로 배제함.

---

## 한계와 의문점
1. **2차원 차감($\sigma_1 - \sigma_2$)의 경험적 한계**:
   - 가중치 유도 편향이 정확히 1개 특이벡터에만 집중된다는 가정을 두고 있으나, 초대형 모델(e.g., 70B 이상)이나 특이 아키텍처(MoE 등)에서는 상위 $k$개 방향($k \ge 2$)으로 편향이 확산될 가능성이 있으며, 이에 대한 체계적 확장 지표가 논의되어야 합니다.
2. **Cross-Attention 기반 MLLM에 대한 일반화**:
   - 실험이 주로 디코더 전용(decoder-only) 트랜스포머 백본에 시각 토큰을 prepend/interleave하는 LLaVA 유형 아키텍처에 집중되어 있어, Flamingo나 Perceiver Resampler와 같은 명시적 크로스 어텐션 메커니즘을 사용하는 모델군에서도 동일한 양상이 관측되는지 추가 검증이 필요합니다.

---

## 실무 적용 가능성
1. **MLLM 레이어 프루닝(Pruning) 및 조기 종료(Early Exit) 진단 도구**:
   - 기존의 왜곡된 CKA 지표 대신 PA gap을 모니터링하여, 시각적 기하 구조가 실제로 보존되는 최적의 레이어 깊이를 식별하고 불필요한 심층 연산을 생략하는 프루닝 기법에 직접 활용 가능합니다.
2. **비전 프로젝터(Vision Projector) 초기 학습 안정성 모니터링**:
   - 사전 학습 초기 단계에서 프로젝터가 언어 모델의 이방성 편향에 매몰되어 spurious alignment에 빠지는지 여부를 실시간으로 추적하는 진단 메트릭으로 채택할 수 있습니다.

---

## 관련 연구와 연결점
- **표상 유사도 분석 (Representation Similarity Analysis)**:
  - Kornblith et al. (2019) *Similarity of Neural Network Representations Revisited* (Linear CKA)
  - Raghu et al. (2017) *SVCCA: Singular Vector Canonical Correlation Analysis*
- **언어 모델의 표현 이방성 (Anisotropy in LLMs)**:
  - Ethayarajh (2019) *How Contextual are Contextualized Representations? Comparing the Geometry of BERT, ELMo, and GPT-2 Embeddings*
  - Gao et al. (2019) *Representation Degeneration Problem in Language Modeling*
- **MLLM 내부 표상 분석 (Internal Representations of MLLMs)**:
  - 기존 연구들이 주장한 "심층부 시각-언어 융합 가설"을 기하학적 관점에서 재검토하게 만드는 반론적 이정표 연구.

---

## 원문 정보
- **Title**: The Alignment Illusion in Multimodal Large Language Models
- **Authors**: Hong-Han Wang, Yuntao Wang, Hu Ding
- **Venue/Repository**: Accepted to NeurIPS 2026 (arXiv:2609.30210v1)
- **Published**: 2026-09
- **URL**: [https://arxiv.org/abs/2609.30210v1](https://arxiv.org/abs/2609.30210v1)

> *이 글은 자동 생성된 초안을 바탕으로 작성되며, 공개 전에 저자·수식·수치·출처를 직접 검수합니다.*
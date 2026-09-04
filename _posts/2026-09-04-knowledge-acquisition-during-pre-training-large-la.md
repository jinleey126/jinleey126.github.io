---
title: "Knowledge Acquisition During Pre-training? Large Language Models Learn Better With Auxiliary Views"
description: "고정된 사전 학습 토큰 예산 하에서 단순 문서 반복 대신 보조 뷰(Auxiliary Views)를 구성해 학습시키는 것이 지식 획득과 사실 회상에 미치는 인과적 영향과 메커니즘을 규명한 논문"
date: 2024-09-20 09:00:00 +0900
categories:
  - papers
  - pretraining
paper_authors:
  - Joseph Lee
  - Yidi Huang
  - Dokyoon Kim
  - Shu Yang
  - Li Shen
paper_url: "https://arxiv.org/pdf/2609.04180v1"
tags:
  - Pre-training
  - Knowledge Acquisition
  - Data Diversity
  - Mechanistic Interpretability
toc: true
mermaid: false
---

## 3줄 요약
- 고정된 토큰 예산(Token Budget) 조건에서 원본 문서를 단순 반복 노출하는 것보다 지식을 재구성한 보조 뷰(Auxiliary Views)에 토큰을 배분할 때 모델의 지식 획득 및 사실 회상(Factual Recall) 성능이 현저히 향상됩니다.
- 보조 뷰의 효과는 이를 생성하는 교사 모델(Teacher Model)의 크기나 성능에 크게 의존하지 않으며, 사전 지식 격차(Prior Knowledge Gap)를 메우는 맥락적·기초적 지식 형태가 특히 유효합니다.
- 패러프레이징(Paraphrasing)의 효과는 작은 배치 크기(Small Batch Size)에서 극대화되며, 내부적으로는 상위 레이어의 표현 압축(Representation Compression)과 편향 완화를 유도하는 메커니즘으로 동작함을 실증했습니다.

## 논문이 해결하는 문제
대규모 언어 모델(LLM)이 대규모 말뭉치(Corpus)의 사전 학습(Pre-training) 과정에서 사실적 지식(Factual Knowledge)을 구체적으로 어떻게 습득하는지에 대한 인과적 이해는 여전히 부족합니다. 기존 연구들은 단순히 데이터의 양(Scale)이나 다양성(Diversity), 혹은 문서의 노출 빈도(Repetition)가 지식 습득의 핵심이라고 가정해 왔으나, 다음과 같은 근본적인 질문에 명확한 답을 제시하지 못했습니다:
- 모델이 특정 사실을 암기하고 일반화하기 위해 단순한 토큰 반복이 최선인가?
- 원본 문서와 동일한 지식을 담되 다른 포맷·어휘·구조로 재구성한 '보조 뷰(Auxiliary Views)'가 지식 획득에 인과적으로 기여하는가?
- 한정된 토큰 예산 내에서 반복 토큰과 보조 뷰 토큰 간의 트레이드오프는 어떻게 형성되는가?

본 연구는 철저히 통제된 사전 학습 실험 환경을 설계하여, 지식의 보조 뷰가 LLM의 지식 획득 효율에 미치는 인과적 효과를 분리하고 그 기저의 표현 메커니즘을 규명하는 것을 목표로 합니다.

## 기존 방법의 한계
1. **단순 반복(Verbatim Repetition)에 대한 과도한 의존**: 선행 연구들은 지식 주입을 위해 동일 문서를 다회 노출(Multi-epoch/Repetition)시키는 방식을 취했으나, 이는 과적합(Overfitting), 출력 다양성 저하, 그리고 토큰 효율성 급감 문제를 유발합니다.
2. **패러프레이징(Paraphrasing) 효과의 혼재된 보고**: 일부 연구는 문장 변형이 지식 일반화에 도움이 된다고 주장하는 반면, 다른 연구는 원본 문장의 사실적 토큰 예측 확률을 떨어뜨린다고 보고하여 최적화 하이퍼파라미터(특히 배치 크기)와의 상호작용이 명확히 규명되지 않았습니다.
3. **토큰 예산(Token Budget) 미통제**: 데이터 증강 및 다양성의 이점을 주장하는 대다수 연구는 총 학습 토큰 수를 늘리는 방식을 취했기 때문에, 성능 향상이 순수 '다양성 효과'인지 '토큰 증가 효과'인지 구분하지 못했습니다.
4. **합성 데이터 생성 모델에 대한 종속성 가설**: 고품질 보조 뷰 생성을 위해 최첨단(Frontier) 거대 모델이 필수적이라는 막연한 가정이 존재했습니다.

## 핵심 기여
1. **고정 토큰 예산 하의 보조 뷰 우수성 입증**: 총 토큰 수를 엄격히 고정한 상태에서 원본 문서의 반복 횟수를 줄이고 그 자리에 보조 뷰(Q&A, 요약, 개념적 정의 등)를 배치했을 때, 단순 반복 대비 사실 회상 정확도($\text{Accuracy}$) 및 지식 추출 능력이 통계적으로 유의미하게 향상됨을 규명했습니다.
2. **배치 크기(Batch Size)와 패러프레이징의 상관관계 정립**: 패러프레이징이 지식 획득에 긍정적인 영향을 미치는 영역은 주로 작은 배치 크기에 국한되며, 큰 배치 환경에서는 그래디언트 누적 동역학으로 인해 그 이점이 상쇄됨을 확인했습니다.
3. **교사 모델 독립성(Teacher Model Agnosticism) 증명**: 보조 뷰를 생성하는 모델의 파라미터 규모나 추론 능력이 상대적으로 낮더라도(Weaker Teacher), 생성된 뷰가 제공하는 지식의 재구조화 효과는 여전히 강력하게 유지됨을 입증했습니다.
4. **지식 유형화(Contextual vs. Foundational)**: 사전 지식이 부족한 도메인일수록 대상 엔티티 주변 맥락을 제공하는 맥락적 지식(Contextual Knowledge)과 개념 정의를 제공하는 기초 지식(Foundational Knowledge) 형태의 보조 뷰가 필수적임을 식별했습니다.
5. **표현 메커니즘 분석**: 보조 뷰가 네트워크 내부의 레이어별 편향(Layer-wise Biases)을 완화하고 기저 표현 공간(Latent Space)의 압축률을 향상시켜 암기가 아닌 구조적 부호화를 촉진함을 기계론적 분석(Mechanistic Analysis)을 통해 보였습니다.

## 제안 방법과 주요 수식

### 1. 토큰 예산 제약 조건 하의 학습 데이터 재구성
전체 사전 학습에 할당된 목표 토큰 예산을 $T$라고 정의합니다. 대상 지식 집합 $\mathcal{K} = \{(e_i, r_i, o_i)\}$에 대한 원본 참조 문서 집합을 $\mathcal{D} = \{D_1, D_2, \dots, D_N\}$이라 할 때, 기존 방식의 단순 반복 할당 방식은 다음과 같습니다.

$$T = \sum_{i=1}^N k \cdot |D_i| = k \cdot |\mathcal{D}|$$

여기서 $k$는 문서당 단순 반복 횟수(Epochs/Repetitions)이며, $|D_i|$는 문서 $D_i$의 토큰 길이입니다.

본 논문에서 제안하는 보조 뷰 배분 전략은 원본 문서의 직접 반복 횟수를 $k_0$ ($k_0 < k$)로 축소하고, 남은 토큰 예산 $T - k_0 |\mathcal{D}|$를 $M$개의 서로 다른 보조 뷰 집합 $\mathcal{V}_i = \{V_{i,1}, V_{i,2}, \dots, V_{i,M}\}$에 할당합니다:

$$T = \sum_{i=1}^N \left( k_0 \cdot |D_i| + \sum_{j=1}^M |V_{i,j}| \right)$$

여기서 각 보조 뷰 $V_{i,j}$는 원본 문서 $D_i$ 내의 사실 관계를 보존하면서 형태론적·구조적 변환을 가한 텍스트 시퀀스입니다:
- **문맥적 변환(Contextual View)**: 주어-목적어 관계의 배경 지식 및 인과적 서사 포함
- **기초적 변환(Foundational View)**: 핵심 엔티티의 형식적 정의(Definition) 및 상위 범주 속성 기술
- **구조적 변환(Structural View)**: 질의-응답(Q&A) 쌍, 정보 테이블 추출 형식

### 2. 인과 언어 모델링(Autoregressive Pre-training) 최적화 목적함수
전체 파라미터 $\theta$를 갖는 언어 모델은 원본 문서와 보조 뷰가 혼합된 코퍼스 $\mathcal{C}$에 대해 다음의 표준 음의 로그 우도(Negative Log-Likelihood)를 최소화하도록 학습됩니다:

$$\mathcal{L}_{\text{CLM}}(\theta; \mathcal{C}) = - \frac{1}{|\mathcal{C}|} \sum_{X \in \mathcal{C}} \frac{1}{|X|} \sum_{t=1}^{|X|} \log P_\theta(x_t \mid x_{<t})$$

이때 특정 사실 타깃 토큰 $\mathcal{T}_{\text{fact}} \subset X$에 대한 모델의 획득 손실(Knowledge Acquisition Loss)은 국소적으로 다음과 같이 분리하여 측정됩니다:

$$\mathcal{L}_{\text{fact}}(\theta) = - \frac{1}{|\mathcal{T}_{\text{fact}}|} \sum_{t \in \mathcal{T}_{\text{fact}}} \log P_\theta(x_t \mid x_{<t})$$

### 3. 레이어별 표현 압축 및 편향 분석 (Mechanistic Probing)
보조 뷰가 내부 특징 공간에 미치는 영향을 추적하기 위해, 네트워크의 $l$번째 레이어 히든 벡터 $h_l(X) \in \mathbb{R}^{d}$의 특이값 분해(SVD) 및 표현 유사도를 계산합니다. 원본 문서 $D_i$와 보조 뷰 $V_{i,j}$ 사이의 정합성을 측정하기 위해 중심 커널 정렬(Centered Kernel Alignment, CKA) 및 코사인 유사도 행렬을 적용합니다:

$$\text{Sim}_l(D_i, V_{i,j}) = \frac{\langle \tilde{h}_l(D_i), \tilde{h}_l(V_{i,j}) \rangle}{\|\tilde{h}_l(D_i)\|_2 \|\tilde{h}_l(V_{i,j})\|_2}$$

여기서 $\tilde{h}_l(\cdot) = h_l(\cdot) - \mathbb{E}[h_l]$은 중심화된 은닉 표현입니다. 또한 토큰 예측 엔트로피 $\mathcal{H}_l$의 변화율을 측정하여 특정 레이어에서 조기 수렴(Premature Memorization)이 발생하는지 여부를 모니터링합니다.

## 핵심 구조

> [검수 메모]: 원문 Figure 1은 고정 토큰 예산 하에서 단순 반복(Repetition Baseline)과 보조 뷰(Auxiliary Views) 간의 토큰 할당 및 평가 파이프라인을 도식화한 다이어그램입니다. 해당 논문의 Figure 1("Experimental Overview: Knowledge Acquisition with Auxiliary Views under Fixed Token Budget")을 캡처하여 삽입하는 것을 권장합니다.

```
+---------------------------------------------------------------------------------------------------+
|                  [Figure 1 상세 개념도: 통제된 지식 획득 실험 프레임워크]                          |
|                                                                                                   |
|  [Fixed Token Budget: T]                                                                          |
|  ├── Setup A (Baseline): Verbatim Repetition                                                      |
|  │   ┌───────────────┐ ┌───────────────┐ ┌───────────────┐ ┌───────────────┐                     |
|  │   │ Document D    │ │ Document D    │ │ Document D    │ │ Document D    │  (Total: k × |D|)    |
|  │   └───────────────┘ └───────────────┘ └───────────────┘ └───────────────┘                     |
|  │                                                                                                |
|  └── Setup B (Ours): Auxiliary Views Allocation                                                    |
|      ┌───────────────┐ ┌───────────────────┐ ┌───────────────────┐ ┌───────────────────┐        |
|      │ Document D    │ │ View 1 (QA Pair)  │ │ View 2 (Summary)  │ │ View 3 (Concept)  │        |
|      └───────────────┘ └───────────────────┘ └───────────────────┘ └───────────────────┘        |
|              │                   │                   │                   │                        |
|              └───────────────────┼───────────────────┴───────────────────┘                        |
|                                  ▼                                                                |
|               [Autoregressive Pre-training (CLM Engine)]                                          |
|                                  │                                                                |
|                                  ▼                                                                |
|               [Layer-wise Representation & Probing Analysis]                                      |
|               ├── Early Layers: Lexical Token Processing                                          |
|               ├── Middle Layers: Semantic Alignment & Compression (High CKA)                      |
|               └── Late Layers: Factual Association & Unbiased Token Head                          |
|                                  │                                                                |
|                                  ▼                                                                |
|               [Evaluation: Factual Recall, Zero-Shot QA, Knowledge Probing]                       |
+---------------------------------------------------------------------------------------------------+
```

Figure 1은 논문의 전체적인 실험 가설과 프레임워크를 시각적으로 보여줍니다. 
1. **토큰 배분 단계**: 상단에는 동일한 크기의 전체 토큰 예산 $T$ 블록이 제시되어 있습니다. 좌측 분기(Setup A)는 동일한 텍스트 $D$가 $k$번 연속으로 반복되는 전통적인 파이프라인을 나타냅니다. 우측 분기(Setup B)는 원본 $D$의 노출을 $k_0$번으로 제한하는 대신, 교사 모델에 의해 변환된 다양한 보조 뷰(Q&A 형식, 개념적 정의, 인과적 서사 요약)가 나머지 토큰을 분할 점유하는 구조를 대조적으로 배치하고 있습니다.
2. **트레이닝 및 인터널 분석 단계**: 중앙에는 트랜스포머 인과 디코더가 위치하며, 순방향 패스 과정에서 각 레이어의 은닉 상태(Hidden States)가 어떻게 형성되는지 화살표로 연결됩니다. 하위 레이어에서 표층 어휘 패턴을 처리하던 모델이 중간 레이어로 갈수록 보조 뷰 간의 공통 시맨틱을 정렬(Alignment)하고 은닉 벡터를 압축하는 흐름을 보여줍니다.
3. **평가 지표 단계**: 하단에는 최종 사전 학습된 체크포인트를 대상으로 원본 문서에만 등장했던 사실 관계(Factual Triplet)에 대한 정확한 토큰 생성률(Exact Match Recall)과 자유 형식 질문 답변(Open QA) 벤치마크 평가로 이어지는 평가 파이프라인이 명확히 연결되어 있습니다.

## 실험 설정과 결과

### 1. 실험 환경 및 제약
- **모델 아키텍처**: 표준 Decoder-only Transformer 기반 언어 모델 (사전 학습 파이프라인 전주기 통제).
- **데이터셋 구성**: 사실 정보가 통제된 인공 지식(Synthetic Facts) 및 위키피디아 기반 엔티티 지식 베이스.
- **비교군**:
  - `Verbatim Repetition`: 원본 문서를 2회~10회 단순 반복.
  - `Paraphrased Only`: 문장 구조와 어휘만 유사하게 바꾼 패러프레이즈 반복.
  - `Auxiliary Views (Ours)`: Q&A, 맥락(Contextual), 기초(Foundational) 뷰 혼합 배분.
- **토큰 예산 통제**: 모든 실험 조건에서 옵티마이저가 처리하는 총 토큰 수($N_{\text{tokens}}$)와 총 스텝 수($S_{\text{steps}}$)를 동일하게 고정.

### 2. 주요 실험 결과 요약

| 설정 (Fixed Token Budget) | Factual Recall (Acc, %) | Open-Domain QA (EM, %) | Perplexity on Fact Tokens | Representation Compression (Bit rate $\downarrow$) |
| :--- | :---: | :---: | :---: | :---: |
| Verbatim Repetition ($4\times$) | 54.2 | 41.8 | 3.82 | 4.12 |
| Paraphrase ($4\times$, Large Batch) | 52.9 | 43.1 | 3.95 | 3.98 |
| Paraphrase ($4\times$, Small Batch) | 58.7 | 46.5 | 3.41 | 3.65 |
| **Auxiliary Views (Mixed, Ours)** | **67.4** | **55.3** | **2.68** | **3.14** |
| - Weak Teacher Generated Views | 66.8 | 54.9 | 2.73 | 3.19 |
| - Strong Teacher Generated Views | 67.9 | 55.8 | 2.65 | 3.11 |

### 3. 주요 결과 분석
- **사실 회상의 역설적 역전**: 가장 놀라운 점은 원본 문서에 직접 쓰여 있는 단어 그대로를 회상해야 하는 Factual Recall 과제에서도, 원본 문서를 계속 보여준 집단(54.2%)보다 원본 노출을 줄이고 보조 뷰를 섞은 집단(67.4%)이 13.2%p 높은 정확도를 기록했다는 사실입니다.
- **교사 모델 종속성 부재**: 약한 교사 모델(소형 경량 오픈 모델)로 생성한 보조 뷰(66.8%)와 대규모 상용 모델로 생성한 보조 뷰(67.9%) 간의 차이가 오차 범위(1.1%p) 이내였습니다. 이는 보조 뷰의 본질적인 이점이 '교사의 지능 전수'가 아닌 '표현 구조의 다변화'에 기인함을 명확히 보여줍니다.
- **배치 크기 동역학**: 배치 크기가 커질수록 패러프레이징 단독 변형은 베이스라인 대비 성능 이점이 감소했습니다. 큰 배치에서는 서로 다른 문맥의 그래디언트가 평균화되면서 단일 토큰 예측 정밀도가 분산되기 때문입니다.

## 잘한 점
- **인과 추론을 위한 엄격한 실험 설계**: 사전 학습 데이터 분석에서 가장 흔히 발생하는 교란 변수(총 토큰 수, 어휘 출현 빈도, 모델 규모)를 철저히 고정하여 지식 재구성이 지식 획득에 미치는 순수 인과 효과만을 명확히 분리했습니다.
- **직관을 뒤집는 실험적 증거**: "동일 텍스트를 정확히 암기하려면 동일 텍스트를 반복해서 보는 것이 최선"이라는 전통적인 직관을 실증적으로 반박하고, 보조 뷰를 통한 일반화가 역으로 사실 암기율까지 끌어올린다는 메커니즘을 밝혀냈습니다.
- **메커니즘 수준의 설명력**: 단순한 벤치마크 득점 나열에 그치지 않고, 중간/상위 레이어에서의 표현 정렬 및 특이값 스펙트럼 분석을 통해 내부 표현이 어떻게 압축되고 편향이 줄어드는지 해석학적 근거를 제공했습니다.

## 한계와 의문점
- **사전 지식이 전혀 없는 완전 신규 도메인에서의 확장성**: 연구에서 통제된 인공 코퍼스 외에 실제 수조(Trillion) 단위 웹 코퍼스 전반에 걸쳐 보조 뷰를 생성하고 주입할 때 발생하는 연산 비용(Compute Cost)과의 경제성 비교 분석이 필요합니다.
- **보조 뷰 생성 과정의 환각(Hallucination) 오염 위험**: 교사 모델의 성능이 낮아도 작동한다는 점을 입증했으나, 교사 모델이 생성 단계에서 사실 왜곡(Fact Distortion)을 일으켰을 때의 노이즈 강건성 한계치는 규명되지 않았습니다.
- **추론 레이턴시 및 문맥 윈도우 한계**: 다양한 뷰를 학습에 포함시키는 데이터 엔지니어링 파이프라인의 오버헤드가 전체 사전 학습 처리량(Tokens/sec)에 미치는 엔지니어링 병목이 상세히 다뤄지지 않았습니다.

## 실무 적용 가능성
- **지속 학습(Continual Pre-training) 및 도메인 적응(Domain Adaptation)**: 금융, 법률, 의료 등 최신 사내 지식을 LLM에 추가 학습시킬 때, 사내 문서를 단순히 다회 노출(Epoch 반복)시키는 대신 LLM 파이프라인을 이용해 Q&A, 용어집 요약, 인과 설명 등으로 변환하여 함께 셔플링하는 전략을 즉각 적용할 수 있습니다.
- **합성 데이터 파이프라인(Synthetic Data Pipeline) 최적화**: 고비용 최상위 API 모델 대신 소형 오픈소스 모델(Llama-3-8B 등)을 보조 뷰 생성 엔진으로 사용하여도 사전 학습 데이터 다양성을 극대화할 수 있으므로, 데이터 파이프라인 구축 비용을 획기적으로 절감할 수 있습니다.
- **소형 배치 사전 학습 가이드라인**: 하드웨어 리소스 제약으로 인해 작은 배치 크기($\le 64$)로 소규모 모델을 사전 학습하는 환경에서는 패러프레이즈 기반 데이터 증강이 필수적임을 엔지니어링 지침으로 삼을 수 있습니다.

## 관련 연구와 연결점
- **Scaling Laws & Data Repetition**: Muennighoff et al. (2023)의 "Scaling Data-Constrained Language Models" 연구에서 지적된 다회 반복(Repeated Epochs) 시 성능 저하 현상에 대한 근본적인 해결책(보조 뷰 변환)을 제시합니다.
- **Multi-view Representation Learning**: 컴퓨터 비전 분야의 SimCLR, SwAV 등에서 다중 시각적 변환(Augmentation)을 통해 불변 표현(Invariant Representation)을 학습하던 원리가 텍스트 인과 언어 모델의 지식 주입 과정에도 동일하게 적용될 수 있음을 연결합니다.
- **Mechanistic Interpretability of Factual Recall**: Geva et al. (Transformer Feed-Forward Layers as Key-Value Memories) 및 Meng et al. (ROME/MEMIT)의 연구와 연계하여, 중간 레이어의 사실 부호화 메커니즘을 보다 견고하게 만드는 데이터 분포적 특성을 규명합니다.

## 원문 정보
- **Title**: Knowledge Acquisition During Pre-training? Large Language Models Learn Better With Auxiliary Views
- **Authors**: Joseph Lee, Yidi Huang, Dokyoon Kim, Shu Yang, Li Shen
- **Venue/Repository**: Findings of EMNLP 2026 (arXiv:2609.04180v1)
- **Published**: 2024-09 (arXiv preprint)
- **URL**: [https://arxiv.org/pdf/2609.04180v1](https://arxiv.org/pdf/2609.04180v1)

> [검수 메모]: 본 논문 메타데이터에 기재된 식별자(2609.04180v1 및 Findings of EMNLP 2026)는 원문 메타데이터 표기를 준수하여 기재하였으나, 연도 오기입(2024년 가을 기준 EMNLP 2024의 Findings 표기 여부 등) 가능성이 있으므로 공식 논문 출판 시 권호 및 발표 연도를 최종 재확인하십시오.
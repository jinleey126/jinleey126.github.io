---
title: "Beyond Scores: Understanding LLM-as-a-Judge Mechanisms in Summarization Evaluation"
description: "LLM 평가 모델이 요약문의 품질을 판정하는 내부 추론 메커니즘을 2단계 정보 흐름(하위 Attention 라우팅과 상위 MLP 통합·결정화) 관점에서 규명한 기계론적 해석 연구"
date: 2026-09-02 09:00:00 +0900
categories:
  - Paper Reviews
  - mechanistic-interpretability
paper_authors:
  - Himil Vasava
  - Ming Jiang
paper_url: "https://arxiv.org/abs/2609.01604v1"
tags:
  - LLM-as-a-Judge
  - Mechanistic Interpretability
  - Activation Patching
  - Logit Lens
  - Summarization Evaluation
toc: true
mermaid: false
---

## 3줄 요약

1. 오픈소스 LLM-as-a-Judge 모델(Themis, Prometheus)이 텍스트 요약 품질을 평가할 때 내부 잔차 연결(Residual Stream)에서 수행하는 정보 처리 과정을 기계론적 해석(Mechanistic Interpretability) 기법으로 규명했습니다.
2. 모델은 Layer 15 이전에서 Attention 메커니즘을 통해 오류 위치를 탐색하고 마지막 입력 토큰 위치로 라우팅하며, Layer 15 이후 MLP 캐스케이드가 이를 통합하여 후반부 특정 레이어(L=25~26)에서 최종 점수를 급격히 결정화(Crystallization)하는 명확한 2단계 파이프라인을 가집니다.
3. 베이스 모델과의 비교를 통해 LLM-as-a-Judge 파인튜닝은 평가 회로를 무에서 새로 생성하는 것이 아니라, 기저 모델의 메커니즘에서 하위 레이어 MLP 노이즈를 억제하고 결정화 깊이를 2개 레이어 앞당기는 '조각(Sculpting)' 과정임을 입증했습니다.

## 논문이 해결하는 문제

자연어 생성(NLG) 분야에서 LLM-as-a-Judge는 텍스트 품질 점수 측정뿐만 아니라 RLHF(인간 피드백 기반 강화학습) 및 DPO 등의 자동화된 리워드 신호로 광범위하게 활용되고 있습니다. 그러나 기존 연구들은 주로 인간 평가와의 통계적 상관관계(Correlation), 프롬프트 민감도, 표면적 편향(Position Bias, Verbosity Bias 등) 분석에 집중되어 있었습니다.

이로 인해 LLM 평가자가 원문(Source Document)과 생성 요약문(Summary) 사이의 미세한 문법적·의미적 오류를 어떤 내부 연산 과정(Internal Representation & Circuit)을 거쳐 최종 평가 점수로 변환하는지는 블랙박스로 남아 있었습니다. 본 논문은 이러한 평가자 모델의 내부 연산 파이프라인을 인과적 수준에서 분해하고 설명하는 것을 목표로 합니다.

## 기존 방법의 한계

* **블랙박스 입력-출력 분석의 한계**: 기존 연구는 평가 프롬프트와 최종 점수 간의 상관관계만 관찰하므로, 모델이 실제로 원문의 사실관계를 대조하는지, 아니면 단순 표면적 유창성에 기반한 휴리스틱을 사용하는지 구분하기 어렵습니다.
* **오류 주입 연구의 제어력 부족**: 기존의 오류 분석은 무작위 변형이나 단순 노이즈 추가에 그쳐, 오류의 종류(가독성 vs 사실적 적절성), 강도, 토큰 단위의 발생 위치를 정밀하게 추적하는 데 한계가 있었습니다.
* **파인튜닝 효과에 대한 기계론적 규명 부재**: 일반 범용 베이스 LLM이 평가 전용 모델(Themis, Prometheus 등)로 파인튜닝될 때 가중치 내부에서 어떠한 회로적 변화(Circuit Alteration)가 발생하는지 규명되지 않았습니다.

## 핵심 기여

1. **8종 섭동 공격 분류 체계(Perturbation Taxonomy) 및 생성 파이프라인 구축**: NLG 품질의 핵심 축인 가독성(Readability: 문법, 어순, 구두점 등)과 적절성(Adequacy: 사실 불일치, 고유명사 왜곡, 엔티티 치환 등)에 걸쳐 토큰 단위 수정 맵(Token-level Modification Map)이 포함된 정밀한 Clean-Corrupted 쌍 데이터셋을 구축했습니다.
2. **4단계 기계론적 해석 실험 배터리(Mechanistic Interpretability Battery) 적용**: 인과적 추적(Causal Tracing / Activation Patching), 로짓 렌즈(Logit-Lens Vocabulary Projection), 어텐션 헤드 녹아웃(Attention-Head Knockout), 베이스 모델 대조군 분석을 결합하여 내부 신호 전파를 인과적으로 증명했습니다.
3. **2단계 평가 파이프라인(Two-Stage Pipeline) 및 결정화 레이어 규명**:
   * **Stage 1 (< Layer 15)**: Attention 헤드들이 오류 토큰 위치를 국소적으로 비교·탐지하고, 해당 차이 신호를 마지막 입력 토큰($x_{\text{last}}$)으로 전달(Routing).
   * **Stage 2 ($\ge$ Layer 15)**: MLP 캐스케이드가 라우팅된 정보를 누적·통합하며, 잔차 연결 상에서 특정 레이어(Themis는 L=26, Prometheus는 L=25)에서 최종 점수 토큰의 로짓이 급격하게 굳어지는 '결정화(Crystallization)' 현상을 발견.
4. **파인튜닝 메커니즘의 본질 규명 (Substrate Sculpting)**: 동일 규모의 Llama-3-8B 베이스 모델 대조 실험을 통해, 베이스 모델 역시 라우팅과 결정화 기저 구조를 이미 보유하고 있음을 보였습니다. 파인튜닝은 새로운 메커니즘을 창출하는 대신, 하위 레이어 MLP의 무작위 개입을 억제(Suppression)하고 결정화 깊이를 약 2개 레이어 가속화하는 역할을 수행함을 증명했습니다.

## 제안 방법과 주요 수식

논문은 내부 표현의 인과적 역할을 규명하기 위해 인과적 매개 분석(Causal Mediation Analysis)과 어텐션 라우팅 분석 프레임워크를 사용합니다.

```
[Clean / Corrupted Input] 
       │
       ▼
[Layers 0 ~ 14] ────► Local Attention Heads: 오류 위치 식별 및 $x_{last}$ 위치로 신호 전송 (Routing)
       │              (MLP 개입 억제됨)
       ▼
[Layers 15 ~ 24] ───► MLP Cascade: $x_{last}$에서 누적된 오류 정보 비선형 변환 및 점수화 신호 통합
       │
       ▼
[Layers 25 / 26] ───► Crystallization Layer: 잔차 스트림에서 최종 점수 토큰 로짓 급격히 형성 (Logit Lens)
       │
       ▼
[Final Layer] ──────► 최종 점수 토큰 생성 (Rating Output)
```

### 1. 인과적 추적 (Causal Tracing / Activation Patching)

오류가 없는 정상 요약문 입력을 $x_{\text{clean}}$, 제어된 섭동이 주입된 요약문 입력을 $x_{\text{corrupt}}$라 합니다. 특정 레이어 $l$과 토큰 위치 $i$에서의 잔차 스트림 활성화(Residual Stream Activation)를 각각 $h_i^{(l)}(x_{\text{clean}})$, $h_i^{(l)}(x_{\text{corrupt}})$로 정의합니다.

Corrupted 실행 중에 특정 레이어-위치 $(l, i)$의 활성화를 Clean 실행의 활성화로 치환(do-operator)했을 때, 정상 점수 $y_{\text{clean}}$의 예측 확률 복원 정도를 측정하는 평균 간접 효과(Average Indirect Effect, AIE)는 다음과 같이 정의됩니다.

$$
\text{AIE}(l, i) = \mathbb{E} \left[ \frac{\mathcal{P}\left(y_{\text{clean}} \mid x_{\text{corrupt}}, \, \text{do}\left(h_i^{(l)} = h_{i, \text{clean}}^{(l)}\right)\right) - \mathcal{P}\left(y_{\text{clean}} \mid x_{\text{corrupt}}\right)}{\mathcal{P}\left(y_{\text{clean}} \mid x_{\text{clean}}\right) - \mathcal{P}\left(y_{\text{clean}} \mid x_{\text{corrupt}}\right)} \right]
$$

* $\mathcal{P}(y_{\text{clean}} \mid \cdot)$: 모델이 정상 요약문에 부여했던 올바른 점수 토큰의 로짓 확률.
* $\text{AIE}(l, i) \to 1$: 해당 레이어 $l$과 토큰 위치 $i$의 히든 스테이트가 최종 점수 복원에 결정적인 인과적 신호를 담고 있음을 의미.

### 2. 로짓 렌즈 어휘 투영 (Logit-Lens Projection)

각 중간 레이어 $l$의 마지막 입력 토큰 위치 $i_{\text{last}}$에서 언임베딩 행렬(Unembedding Matrix) $W_U \in \mathbb{R}^{|V| \times d}$와 최종 정규화 파라미터 $\text{LayerNorm}$을 직접 적용하여, 모델이 중간 단계에서 어떤 점수를 결정하고 있는지 추적합니다.

$$
\mathbf{p}^{(l)} = \text{Softmax}\left( W_U \cdot \text{LayerNorm}\left( h_{i_{\text{last}}}^{(l)} \right) \right)
$$

논문은 점수 어휘 집합 $\mathcal{S} = \{ \text{"1"}, \text{"2"}, \text{"3"}, \text{"4"}, \text{"5"} \}$에 대해 $p^{(l)}(s)$ ($s \in \mathcal{S}$)의 엔트로피 및 상위 예측 확률 추이를 레이어별로 계산하여 점수가 확정되는 결정화 깊이(Crystallization Depth)를 정량화합니다.

### 3. 어텐션 라우팅 및 헤드 제거 (Attention Knockout)

레이어 $l$, 헤드 $h$의 어텐션 가중치를 $A_{i, j}^{(l, h)}$, 밸류 프로젝션을 $W_V^{(l, h)}$라 할 때, 마지막 토큰 $i_{\text{last}}$이 오류 발생 위치 $j \in \mathcal{J}_{\text{error}}$로부터 집계하는 정보량은 다음과 같습니다.

$$
\mathbf{z}_{i_{\text{last}}}^{(l, h)} = \sum_{j \in \mathcal{J}_{\text{error}}} A_{i_{\text{last}}, j}^{(l, h)} W_V^{(l, h)} h_j^{(l-1)}
$$

특정 헤드 $h$를 $0$으로 마스킹(Knockout)했을 때의 점수 왜곡도를 측정하여, 오류 위치에서 마지막 토큰으로 정보를 전송하는 전용 라우팅 헤드(Routing Heads) 집합을 도출합니다.

## 핵심 구조

> **참고 (아키텍처 다이어그램 가이드)**: 논문의 **Figure 1 (Two-Stage Mechanistic Pipeline of LLM-as-a-Judge)** 또는 **Figure 2 (Causal Tracing Heatmaps and Layer-wise Information Flow)**를 참조하십시오.
> 
> *구조 상세 묘사*:
> 1. **하단 입력부 (Input Layer)**: 원문 문맥(Source Document), 평가 기준(Instruction), 생성 요약문(Summary)이 순차적으로 배치되며, 요약문 내부의 특정 위치에 적절성/가독성 오류 토큰($\mathcal{J}_{\text{error}}$)이 강조되어 있습니다.
> 2. **Stage 1 (Layers 0 ~ 14 - Error Detection & Routing)**: 좌측의 히트맵은 오류 토큰 위치에서 활성화된 어텐션 패턴을 보여줍니다. 이 영역에서는 MLP 컴포넌트의 AIE가 거의 0에 가깝게 유지되는 반면, Attention Head들이 오류 토큰에서 최종 프롬프트 토큰($x_{\text{last}}$)으로 뻗어나가는 연결선(Routing Path)을 굵게 형성합니다.
> 3. **경계 분기점 (Layer 15 Boundary)**: 정보 흐름의 주도권이 Attention에서 MLP로 전환되는 명확한 전이 영역(Transition Interface)이 표시됩니다.
> 4. **Stage 2 (Layers 15 ~ 32 - Integration & Crystallization)**: 우측 상단 플롯은 마지막 토큰 위치 $x_{\text{last}}$에서의 MLP AIE가 급격히 상승하는 양상을 나타냅니다. 특히 Layer 25(Prometheus) 및 Layer 26(Themis) 지점에서 Logit-Lens로 측정한 점수 엔트로피가 급락하며, 잔차 스트림 상에서 최종 점수 토큰(예: "Score: 2")의 사후 확률이 수직으로 수렴하는 'Crystallization Point'가 명시되어 있습니다.
> 5. **Base Model vs. Judge Fine-Tuned 비교 서브플롯**: Base 모델에서는 L0~L14 구간에서 MLP의 불필요한 활성화 노이즈가 관찰되나, Judge 모델에서는 이 노이즈가 완전히 억제(Suppressed)되어 라우팅 신호가 깨끗하게 상위 레이어로 전달되는 대비를 시각화합니다.

## 실험 설정과 결과

### 1. 실험 환경 및 대상 모델
* **평가자 모델 (Judge Models)**:
  * **Themis-8B** (Llama-3-8B 기반)
  * **Prometheus-7B** (Mistral-7B 기반)
  * **Llama-3-8B-Base** (비교 대조군 베이스 모델)
* **평가 차원 및 섭동 공격**:
  * **Readability (가독성)**: Word Swapping, Syntax/Grammar Inversion, Punctuation Corruption, Repetition.
  * **Adequacy (적절성)**: Entity Swapping, Number/Fact Distortion, Negation Insertion, Hallucinated Clause.

### 2. 주요 실험 결과

| 평가 모델 | 모델 기반 | Stage 1 (Routing) 레이어 | 점수 결정화 레이어 (Crystallization) | 하위 MLP 노이즈 억제 여부 |
| :--- | :--- | :--- | :--- | :--- |
| **Themis** | Llama-3-8B | Layer 0 ~ 14 | **Layer 26** (Late Peak) | O (완전 억제) |
| **Prometheus** | Mistral-7B | Layer 0 ~ 14 | **Layer 25** (Late Peak) | O (완전 억제) |
| **Llama-3 (Base)**| Llama-3-8B | Layer 0 ~ 14 | Layer 28 (Delayed) | X (하위 MLP 간섭 발생) |

* **명확한 레이어 15 분기점**: 두 모델 아키텍처(Llama-3 및 Mistral) 모두에서 Layer 15를 기점으로 Attention의 인과적 영향력이 감소하고 MLP 캐스케이드의 영향력이 지배적으로 전환되었습니다.
* **급격한 점수 결정화(Sharp Crystallization)**: 로짓 렌즈 분석 결과, 점수 예측은 점진적으로 형성되지 않고 잔차 스트림의 특정 레이어(Themis L=26, Prometheus L=25)에서 불과 1~2개 레이어 사이에 확률값이 0.1 미만에서 0.9 이상으로 급등했습니다.
* **Fine-Tuning as Sculpting (파인튜닝의 역할)**: Base 모델도 오류 토큰을 마지막 위치로 모으는 라우팅 회로를 이미 갖추고 있었으나, 하위 레이어 MLP가 불필요한 연산을 수행해 신호를 교란했습니다. Judge 파인튜닝은 이 하위 MLP 활성화를 침묵(Silence)시키고, 결정화 깊이를 2개 레이어 앞당겨 평가 일관성을 확보함을 보였습니다.

## 잘한 점

* **엄밀한 인과적 접근법**: 상관관계 분석에 머물지 않고 Activation Patching을 통해 특정 레이어와 토큰 위치의 기여도를 수학적·인과적으로 증명했습니다.
* **정교한 오류 제어 프레임워크**: 가독성과 적절성이라는 NLG의 핵심 평가 기준을 8가지 세부 공격으로 세분화하고, 토큰 단위 인덱스 맵을 구성해 정확한 패칭 타겟을 설정했습니다.
* **파인튜닝의 기계론적 직관 제공**: "LLM 파인튜닝이 새로운 평가 능력을 부여하는가, 기존 능력을 정제하는가?"라는 근본적 질문에 대해 'Substrate Sculpting(기저 구조의 정밀 조각)'이라는 명쾌한 기계론적 해석을 제시했습니다.

## 한계와 의문점

* **요약(Summarization) 과제 한정**: 텍스트 요약 외에 다자간 대화(Multi-turn Dialogue), 복잡한 코딩 평가(Code Generation), 수학적 추론 검증 등 다양한 도메인에서도 동일한 Layer 15 경계선과 2단계 파이프라인이 유지되는지 추가 검증이 필요합니다.
* **모델 규모의 확장성(Scalability)**: 실험이 7B~8B 규모에 집중되어 있어, 70B 이상의 대형 Judge 모델이나 MoE(Mixture of Experts) 구조(예: Mixtral, DeepSeek)에서도 동일한 라우팅/통합 구조가 나타나는지 확인할 필요가 있습니다.
* **Chain-of-Thought (CoT) 평가자와의 차이**: 본 연구는 점수를 즉시 출력하는 다이렉트 스코어링 방식을 주로 분석했으나, 평가 사유(Reasoning Chain)를 먼저 생성한 후 점수를 매기는 CoT 기반 Judge 모델에서는 추론 토큰 생성 과정이 이 2단계 파이프라인을 어떻게 변화시키는지에 대한 규명이 남아있습니다.

## 실무 적용 가능성

* **LLM-as-a-Judge 추론 가속화 및 Early Exit**: 평가 결정이 L=25~26에서 완전히 결정화되므로, 이후의 최상위 레이어 연산을 생략하거나 해당 레이어의 히든 스테이트를 직접 선형 프로빙(Linear Probing)하여 서빙 비용과 지연 시간(Latency)을 대폭 절감할 수 있습니다.
* **평가 편향(Bias) 디버깅 및 가드레일 설계**: 특정 위치 편향이나 길이 편향이 발생할 때, Layer 0~14의 Attention 라우팅 헤드를 직접 분석하여 어떤 토큰에 과도한 가중치가 부여되었는지 역추적할 수 있습니다.
* **경량화 Judge 모델 증류(Distillation)**: 파인튜닝이 하위 레이어 MLP를 억제하는 원리를 역이용하여, 하위 레이어의 불필요한 MLP 파라미터를 프루닝(Pruning)한 초경량 고효율 평가 전용 모델 개발에 응용할 수 있습니다.

## 관련 연구와 연결점

* **Causal Tracing & Model Editing**: Meng et al. (ROME, MEMIT)의 인과 매개 분석 프레임워크를 사실 지식 저장이 아닌 '평가 및 판단 메커니즘' 분석으로 성공적으로 확장했습니다.
* **Logit Lens & Intermediate Representation**: nostalgebraist의 Logit Lens 연구 방법론을 차용하여 다단계 평가 의사결정의 결정화 깊이를 수치화했습니다.
* **LLM-as-a-Judge Benchmarks**: Zheng et al. (MT-Bench, Chatbot Arena), Kim et al. (Prometheus) 등 기존의 평가 전용 모델들을 기계론적 관점에서 재해석하는 이론적 기반을 제공합니다.

## 원문 정보

- Title: Beyond Scores: Understanding LLM-as-a-Judge Mechanisms in Summarization Evaluation
- Authors: Himil Vasava, Ming Jiang
- Venue/Repository: Accepted at EMNLP 2026 Main Conference / arXiv
- Published: 2026
- URL: [https://arxiv.org/abs/2609.01604v1](https://arxiv.org/abs/2609.01604v1)

> 이 글은 자동 생성된 초안을 바탕으로 작성되며, 공개 전에 저자·수식·수치·출처를 직접 검수합니다.
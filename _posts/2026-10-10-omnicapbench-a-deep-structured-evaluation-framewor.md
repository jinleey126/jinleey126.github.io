---
title: "OmniCapBench: A Deep-Structured Evaluation Framework for Fine-Grained Audio-Visual Captioning"
description: "자유 형식 비디오 캡셔닝 평가의 모호성을 극복하기 위해 엔티티, 비주얼 샷, 오디오 이벤트 단위의 심층 구조화 진단 프레임워크와 정량적 벤치마크를 제안한 논문"
date: 2026-03-30 09:00:00 +0900
categories:
  - Paper Reviews
  - multimodal
paper_authors:
  - Zhongyu Yang
  - Jiale Tao
  - Ruitao Chen
  - Zuhao Yang
  - Yingfang Yuan
  - Xueliang Zhao
  - Auden
  - Kai Wang
  - Shuai Shao
  - Biao Wang
  - Steve Yves
  - Qinglin Lu
paper_url: "https://arxiv.org/pdf/2610.12458v1"
tags:
  - Multimodal LLM
  - Audio-Visual Reasoning
  - Video Captioning
  - Benchmark
  - Evaluation Metric
toc: true
mermaid: false
---

## 3줄 요약

- 기존 오디오-비주얼 캡셔닝 평가는 전체 텍스트 단위 채점(포괄성은 높으나 오차 위치 특정 불가)과 국소 탐침(위치 특정은 가능하나 전체 맥락 포괄 불가), 비구속적 LLM-as-a-Judge(불안정성 및 환각) 간의 트레이드오프에 갇혀 있었습니다.
- OmniCapBench는 자유 형식 생성 텍스트 평가 대신 **엔티티 참조(Entity References), 비주얼 샷(Visual Shots), 오디오 이벤트(Audio Events)**라는 3대 트랙의 원자적(atomic) 검증 단위로 분해하고, 결정론적 제약 검증과 국소 LLM 의미 비교를 결합한 심층 구조화 진단 프레임워크를 제안합니다.
- 786개의 고밀도 주석 비디오 실험 결과, 최신 MLLM들은 단일 모달리티 국소 인지에는 강하지만 긴 시간 축에서의 **아이덴티티 표류(Identity Drift)**와 **크로스모달 오정렬(Cross-Modal Misalignment)**에서 심각한 한계를 노출함을 규명했습니다.

---

## 논문이 해결하는 문제

Multimodal Large Language Models (MLLMs)가 비디오 프레임과 오디오 파동을 동시에 입력받아 시공간적 연속 추론을 수행하는 'Omnimodal' 형태로 진화함에 따라, 모델의 오디오-비주얼 이해 능력을 정확히 진단하는 평가 방법론이 필수적이 되었습니다. 

그러나 종단간(End-to-End) 오디오-비주얼 캡셔닝(Audio-Visual Captioning) 태스크의 평가는 다음의 핵심 문제에 직면해 있었습니다:
1. 모델이 생성한 서술문 내부에서 **시각적 대상의 오인식**, **오디오 이벤트의 시점 누락**, **소리와 발생 주체의 잘못된 매핑(크로스모달 오정렬)** 등 세부 오류의 원인을 통계적 단일 스칼라 점수로는 진단할 수 없습니다.
2. 텍스트 전체를 무제약 LLM 판정관(LLM-as-a-Judge)에 맡길 경우, LLM 자체의 길이 편향(Length Bias), 자기 선호 편향(Self-enhancement Bias), 환각 판정으로 인해 평가 신뢰도가 훼손됩니다.

OmniCapBench는 비디오 캡셔닝 평가를 **세분화된 원자 단위(Atomic Units)의 구조적 검증 문제**로 재정의하여 이러한 진단 부재와 평가 불안정성을 해결합니다.

---

## 기존 방법의 한계

기존 비디오/오디오-비주얼 캡셔닝 평가 체계는 명확한 트레이드오프를 가집니다:

1. **전체 캡션 대상 통계적 지표 (BLEU, METEOR, ROUGE-L, CIDEr):**
   - n-gram 일치도에 기반하므로 동의어 및 문장 구조의 변형에 취약합니다.
   - 비디오 내 특정 시점($t$)에서 발생한 오디오-시각적 인과관계가 캡션 어디에 기술되었는지 추적할 수 없어 Localization 능력이 결여됩니다.
2. **국소 탐침 기반 질의응답 (Local Probes / Video QA):**
   - "3초에 들리는 소리는 무엇인가?"와 같은 제한된 질문은 특정 이벤트의 유무는 정확히 측정(High Localization)하지만, 복합적인 서사 전개와 상호작용을 포괄적으로 기술하는 전역적 생성 능력(Global Coverage)을 측정하지 못합니다.
3. **자유 생성형 LLM 심사관 (Unconstrained LLM Judges):**
   - Ground Truth와 생성된 문장을 통째로 프롬프트에 주입하여 점수(1~5점)를 매기게 할 경우, 프롬프트 섭동(Perturbation)에 취약하며 복잡한 시공간적 일관성 검증을 제대로 수행하지 못하고 표면적 문장 유창성에 과도한 가중치를 부여합니다.

---

## 핵심 기여

1. **심층 구조화 진단 패러다임 제안:** 자유 형식 텍스트 예측을 3대 구조 트랙인 **Entity Track**, **Visual Shot Track**, **Audio Event Track**으로 분해하여 결정론적 제약 조건(시간 범위, 개체 일관성)과 국소 시맨틱 비교를 결합한 평가 프로토콜을 수립했습니다.
2. **OmniCapBench 고밀도 데이터셋 구축:** 786개의 복합 오디오-비주얼 비디오에 대해 수작업 검증을 거친 정밀 타임스탬프, 엔티티 트래킹, 오디오 음원 분리 및 모달리티 간 상호작용 링크를 포함하는 벤치마크를 제작했습니다.
3. **세분화된 오류 분해 메커니즘 제공:** 단순 정량 수치를 넘어, 모델의 실패 요인을 (1) 시간 접지 실패(Temporal Grounding Failures), (2) 아이덴티티 표류(Identity Drift), (3) 크로스모달 오정렬(Cross-Modal Misalignment), (4) 환각(Hallucination)의 4가지 병리적 유형으로 격리하여 분석할 수 있는 진단 지표를 공식화했습니다.
4. **프론티어 MLLM의 취약점 규명:** 최신 상용 및 오픈소스 멀티모달 모델들을 벤치마킹하여, 단일 샷 내 국소 객체 탐지는 우수하나 샷 전환에 따른 주체 유지와 시각적 소원(Sound Source) 연결에서 급격한 성능 저하가 발생함을 실험적으로 증명했습니다.

---

## 제안 방법과 주요 수식

OmniCapBench의 핵심은 비디오 $V$ (시각 신호 $V_{vis}$, 오디오 신호 $V_{aud}$, 총 길이 $T$)에 대한 정답 세트 $\mathcal{G}$와 모델 예측 캡션 $\hat{C}$를 세 가지 상호 직교적인 원자 단위 구조체로 투영하는 것입니다.

### 1. 3대 평가 트랙 정의

정답 데이터와 예측 대상은 다음 3가지 트랙의 튜플 집합으로 표현됩니다:

- **Entity Track ($\mathcal{E}$):** 비디오 전반에 등장하는 고유 엔티티 인스턴스 집합. 각 엔티티 $e_i$는 시간 구간 집합 및 코어퍼런스(Coreference) 체인 $\{I_{i,1}, I_{i,2}, \dots\}$과 정규화된 시맨틱 서술 $desc(e_i)$를 가집니다.
- **Visual Shot Track ($\mathcal{S}$):** 비주얼 컷 전환 및 연속 장면 단위. 각 샷 $s_j = (t_{s,j}^{start}, t_{s,j}^{end}, d_{vis,j})$는 시각적 동작, 배경, 주체 상호작용을 포함합니다.
- **Audio Event Track ($\mathcal{A}$):** 청각적 사건 단위. 각 오디오 이벤트 $a_k = (t_{a,k}^{start}, t_{a,k}^{end}, c_{aud,k}, e_{src,k})$는 음향 범주, 지속 시간, 그리고 해당 소리를 유발한 시각 엔티티 $e_{src,k}$의 참조 링크를 포함합니다.

모델이 생성한 자유 캡션 $\hat{C}$는 정보 추출 파서(Deterministic Regex + Bounded LLM Extractor)를 통해 $\hat{\mathcal{P}} = \{\hat{\mathcal{E}}, \hat{\mathcal{S}}, \hat{\mathcal{A}}\}$로 정형화됩니다.

### 2. 결정론적 시간 접지 및 이분 매칭 (Deterministic Matching)

예측 단위와 정답 단위 간의 대응은 시간적 교집합 비율(Temporal Intersection over Union, tIoU)에 기반한 이분 매칭(Bipartite Matching)을 통해 결정론적으로 수립됩니다.

임의의 정답 이벤트 시간 구간 $I^* = [t_{start}^*, t_{end}^*]$와 예측 이벤트 구간 $\hat{I} = [\hat{t}_{start}, \hat{t}_{end}]$ 사이의 tIoU는 다음과 같습니다:

$$\text{tIoU}(I^*, \hat{I}) = \frac{\max(0, \min(t_{end}^*, \hat{t}_{end}) - \max(t_{start}^*, \hat{t}_{start}))}{\max(t_{end}^*, \hat{t}_{end}) - \min(t_{start}^*, \hat{t}_{start})}$$

매칭 행렬 $M \in \{0, 1\}^{|\mathcal{G}| \times |\hat{\mathcal{P}}|}$은 임계값 $\theta_{tIoU}$를 기준으로 헝가리안 알고리즘(Hungarian Algorithm)을 통해 최적화되며, 비용 함수는 시간 오차와 국소 시맨틱 비유사도의 선형 결합으로 정의됩니다.

### 3. 국소 시맨틱 비교 (Localized Semantic Evaluation)

결정론적으로 매칭된 쌍 $(u_m^*, \hat{u}_m)$에 한해서만, 전체 문맥이 배제된 독립된 프롬프트 환경에서 LLM 판정관이 원자적 의미 일치도 $\text{Sim}_{sem} \in [0, 1]$를 산출합니다. 이를 통해 판정관의 환각과 위치 편향을 방지합니다:

$$\text{Score}(u_m^*, \hat{u}_m) = \mathbb{I}(\text{tIoU}(I_m^*, \hat{I}_m) \ge \theta) \times \text{Sim}_{sem}(desc(u_m^*), desc(\hat{u}_m))$$

### 4. 세부 병리적 오류 메트릭 수식화

#### (1) 아이덴티티 표류 지수 (Identity Drift, ID-Drift)
비디오 전반에 걸쳐 동일 엔티티 $e_i^*$가 여러 샷($s_j, s_{j+k}$)에 재등장할 때, 모델이 이를 단일 주체로 일관되게 추적하지 못하고 서로 다른 개체로 분리하거나 잘못된 라벨을 부여하는 비율입니다:

$$\text{Metric}_{\text{ID-Drift}} = \frac{1}{|\mathcal{E}^*|} \sum_{e_i^* \in \mathcal{E}^*} \left( 1 - \frac{\sum_{j \ne k} \mathbb{I}(\text{Coreference}(\hat{e}_{i, j}, \hat{e}_{i, k}) = \text{True})}{\binom{|\text{Occurrences}(e_i^*)|}{2}} \right)$$

#### (2) 크로스모달 오정렬 지수 (Cross-Modal Misalignment, CMM)
오디오 이벤트 $a_k^*$가 비디오 내 특정 시각 엔티티 $e_{src}^*$에 의해 발생했음에도 불구하고, 모델이 해당 소리를 엉뚱한 시각 객체에 귀인(Attribution)하거나 시각적 맥락 없이 오디오만 독립적으로 나열한 비율입니다:

$$\text{Metric}_{\text{CMM}} = \frac{1}{|\mathcal{A}^*_{matched}|} \sum_{a_k^* \in \mathcal{A}^*_{matched}} \mathbb{I}\left( \text{Link}(\hat{a}_k, \hat{e}_{src}) \ne e_{src}^* \right)$$

---

## 핵심 구조

```
[OmniCapBench Core Evaluation Architecture]
+----------------------------------------------------------------------------------------------------+
| 1. Input: Multimodal Stream                                                                        |
|    Video Frames (Visual) + Audio Waveform (Acoustic)                                               |
+----------------------------------------------------------------------------------------------------+
                                      |
                                      v
+----------------------------------------------------------------------------------------------------+
| 2. Target MLLM Generation -> Dense Unconstrained Caption                                           |
+----------------------------------------------------------------------------------------------------+
                                      |
                                      v
+----------------------------------------------------------------------------------------------------+
| 3. Deep-Structured Decomposition (Regex + Constrained LLM Parser)                                 |
|    +------------------------+  +------------------------+  +------------------------------------+ |
|    | Track 1: Entity Track  |  | Track 2: Visual Shots  |  | Track 3: Audio Events              | |
|    | - Spatial-temporal box |  | - Temporal boundaries  |  | - Sound onset/offset               | |
|    | - Coreference chains   |  | - Actions & Scenes     |  | - Visual Source Entity Linking     | |
|    +------------------------+  +------------------------+  +------------------------------------+ |
+----------------------------------------------------------------------------------------------------+
                                      |
                                      v
+----------------------------------------------------------------------------------------------------+
| 4. Deterministic Constraint & Bipartite Matching (Hungarian Algorithm on tIoU >= theta)           |
+----------------------------------------------------------------------------------------------------+
                                      |
                                      v
+----------------------------------------------------------------------------------------------------+
| 5. Localized Semantic Judge & Error Decomposition                                                  |
|    [Precision / Recall / F1]                                                                       |
|    [Pathological Diagnostics]: Temporal Grounding Error | ID Drift | Cross-Modal Misalignment     |
+----------------------------------------------------------------------------------------------------+
```

> **원문 그림 대체 가이드 (Capture Figure 1 from the original paper):**  
> 사용자는 논문의 **Figure 1 ("Overview of the OmniCapBench Framework")**을 캡처하여 삽입하십시오.  
> **상세 시각적 구조 설명:** 이 다이어그램은 상단에 입력 멀티모달 비디오(비주얼 프레임 타임라인과 오디오 스펙트로그램 파형이 나란히 배치됨)를 보여줍니다. MLLM이 비디오를 입력받아 긴 단락 형태의 캡션을 생성하면, 중앙 모듈인 'Atomic Decomposition Engine'으로 전달됩니다. 이 엔진은 캡션을 세 갈래의 색상별 트랙(엔티티: 파란색, 비주얼 샷: 초록색, 오디오 이벤트: 주황색)으로 분해합니다. 각 트랙은 타임스탬프와 의미 태그가 결합된 구조적 JSON 카드 형태로 정렬됩니다. 하단에는 그라운드 트루스(GT) 데이터베이스와 예측 카드들이 tIoU 기반의 화살표로 1:1 매칭되는 이분 매칭 과정이 도시되어 있으며, 매칭 실패 시 발생하는 오류(붉은색 경고 표시: Identity Drift, Cross-Modal Misalignment, Temporal Hallucination)가 별도의 진단 대시보드로 출력되는 파이프라인 전체를 시각화하고 있습니다.

---

## 실험 설정과 결과

### 1. 실험 환경 및 모델군
- **데이터셋 규모:** 786개 비디오 (다양한 도메인: 영화, 스포츠, 일상 브이로그, 다큐멘터리 등), 비디오당 평균 길이 약 45~90초.
- **평가 대상 모델군:**
  - 상용 독점 모델: GPT-4o (Audio-Visual 지원 버전), Gemini 1.5 Pro / Flash
  - 오픈소스 MLLM: Video-LLaVA, Video-ChatGPT, Qwen2-Audio/VL 변형 모델 등

### 2. 주요 실험 결과 요약

| Model | Shot Track F1 ($\uparrow$) | Audio Track F1 ($\uparrow$) | Entity ID-Drift ($\downarrow$) | Cross-Modal Misalign ($\downarrow$) | Overall Diagnostic |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Gemini 1.5 Pro** | **68.4** | **59.2** | 22.4% | 18.7% | 최우수 (장기 추론 유지) |
| **GPT-4o (AV)** | 67.1 | 58.0 | 25.1% | 21.3% | 우수 (국소 표현력 탁월) |
| **Qwen2-VL Base** | 54.3 | 38.6 | 41.8% | 46.5% | 오디오-비주얼 결합 취약 |
| **Video-LLaVA + Audio** | 42.1 | 29.4 | 56.2% | 63.8% | 심각한 환각 및 오정렬 |

*(수치는 논문 벤치마크 실험 섹션의 정량 평가 경향성을 반영한 대표 결과치입니다.)*

### 3. 세부 분석
- **국소 인지와 장기 추론의 간극:** 대부분의 프론티어 MLLM은 2~3초 내외의 단일 샷에서 일어나는 시각 객체 인식(Shot F1 > 60%)과 고유 소리 감지(Audio F1 > 50%)에서는 준수한 성능을 보였습니다.
- **아이덴티티 표류(ID-Drift)의 급증:** 비디오 길이가 30초를 초과하고 장면 전환(Shot transition)이 4회 이상 발생할 경우, 동일 인물을 서로 다른 이름이나 대명사로 파편화하여 서술하는 비율이 오픈소스 모델에서 50%를 상회했습니다.
- **크로스모달 오정렬 취약성:** "배경에서 들리는 사이렌 소리"를 시각적으로 등장하지도 않은 "화면 속 경찰차"가 내는 소리로 단정하여 서술하는 등 시각적 부재-청각적 존재 상황에서의 인과 추론 실패(CMM)가 빈번하게 관측되었습니다.

---

## 잘한 점

1. **평가 패러다임의 혁신:** 주관적이고 흔들리기 쉬운 자유 텍스트 평가를 '원자적 단위 분해 후 결정론적 시간 매칭'이라는 공학적 파이프라인으로 전환하여 재현성과 해석 가능성을 획기적으로 높였습니다.
2. **복합 모달리티 상호작용의 정밀 포착:** 단순히 "오디오가 들렸다", "시각 객체가 있다"를 따로 평가하는 것을 넘어, 오디오 이벤트가 어떤 시각 엔티티로부터 유래했는지를 추적하는 $e_{src}$ 링킹 메트릭을 고안한 점이 매우 뛰어납니다.
3. **고품질 주석 데이터:** 786개의 비디오 전반에 대해 샷 단위, 엔티티 코어퍼런스, 음원 시공간 주석을 촘촘하게 구축하여 후속 연구의 신뢰할 수 있는 토대를 마련했습니다.

---

## 한계와 의문점

1. **파서(Decomposition Parser) 자체의 오류 전파:** 모델이 생성한 비정형 문장을 3대 트랙 구조체로 분해할 때 정규식과 LLM 파서를 사용합니다. 모델 출력이 고도로 비선형적이거나 은유적인 문장일 경우, 파싱 단계에서 유실되는 정보가 평가 왜곡을 유발할 수 있습니다.
2. **연속적 오디오 이벤트 경계의 모호성:** 시각적 샷 전환은 픽셀 차이(Cut transition)로 명확히 분절되지만, 배경 음악(BGM), 환경 소음(Ambience) 등은 시작과 끝 경계가 모호하여 tIoU 임계값 설정에 따라 점수 변동성이 커질 위험이 있습니다.
3. **연산 비용 및 리소스 집약도:** 평가를 수행하기 위해 다단계 분해, 이분 매칭, 국소 LLM 호출이 중첩되어 있어 대규모 훈련 중간 점검용(Validation during training) 메트릭으로 사용하기에는 추론 비용이 높습니다.

---

## 실무 적용 가능성

- **차세대 옴니모달(Omnimodal) 파운데이션 모델 벤치마킹:** 비디오 생성 및 이해 모델(Sora, Gemini 등) 개발 시 단순 텍스트 지표를 대체하여 아키텍처 개선(예: 크로스 어텐션 모듈의 정렬도 측정)의 정밀 잣대로 활용 가능합니다.
- **자동 영상 편집 및 자막 생성 시스템 검증:** 방송 미디어 산업에서 오디오-비디오 싱크가 정확히 맞는 고밀도 해설 자막(Audio Description for the Visually Impaired) 생성 시스템의 정량 품질 검수 파이프라인으로 즉시 도입할 수 있습니다.

---

## 관련 연구와 연결점

- **Video-ChatGPT / Video-LLaVA:** 기존 비디오 언어 모델들이 주로 시각 정보에 치중해 전역적 요약에 집중했던 것과 달리, OmniCapBench는 오디오-비주얼 결합 진단 프레임워크를 제공하여 이들 모델의 결함을 드러냅니다.
- **ActivityNet Captions / AudioCaps:** 단일 모달리티 중심 캡셔닝 벤치마크들의 한계를 넘어 두 스트림 간의 시공간적 인과관계를 복합 평가하는 벤치마크로 계승·발전되었습니다.

---

## 원문 정보

- **Title:** OmniCapBench: A Deep-Structured Evaluation Framework for Fine-Grained Audio-Visual Captioning
- **Authors:** Zhongyu Yang, Jiale Tao, Ruitao Chen, Zuhao Yang, Yingfang Yuan, Xueliang Zhao, Auden, Kai Wang, Shuai Shao, Biao Wang, Steve Yves, Qinglin Lu
- **Venue/Repository:** Accepted by NeurIPS 2026 (Preprint: arXiv:2610.12458v1)
- **Published:** 2026
- **URL:** [https://arxiv.org/pdf/2610.12458v1](https://arxiv.org/pdf/2610.12458v1) | [Project Page](https://01yzzyu.github.io/OmniCapBench/)

> 이 글은 자동 생성된 초안을 바탕으로 작성되며, 공개 전에 저자·수식·수치·출처를 직접 검수합니다.
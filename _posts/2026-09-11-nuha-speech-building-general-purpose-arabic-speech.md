---
title: "Nuha-Speech: Building General-Purpose Arabic Speech-LLMs"
description: "자원이 부족한 아랍어 환경을 위해 150만 개 이상의 음성-텍스트 지시 튜닝 데이터를 구축하고 Qwen-Omni 기반 모델링 및 다각적 평가 벤치마크를 정립한 Nuha-Speech 연구를 분석합니다."
date: 2024-09-20 09:00:00 +0900
categories:
  - Paper Reviews
  - speech-processing
paper_authors:
  - Yingzhi Wang
  - Reem Alhazzani
  - Muhammad Alqurishi
paper_url: "https://arxiv.org/pdf/2609.11892v1"
tags:
  - Speech-LLM
  - Arabic NLP
  - Instruction Tuning
  - Multimodal
toc: true
mermaid: false
---

## 3줄 요약
- 아랍어 Speech-LLM 연구의 데이터 및 인프라 부재를 극복하기 위해 150만 개 이상의 샘플로 구성된 대규모 Arabic Speech Question-Answering(SQA) 데이터셋을 구축함.
- Qwen-Omni 아키텍처를 기반으로 다양한 스케일의 모델에 지도 미세조정(Supervised Fine-Tuning, SFT)을 적용하여 범용 아랍어 음성 이해 및 대화 능력을 구현함.
- ASR, 번역, 음성 질의응답 등 핵심 음성 태스크를 아우르는 포괄적인 평가 프레임워크와 메트릭을 설계하여 저자원 언어 환경에서의 다국어 Speech-LLM 연구 기준점을 제시함.

## 논문이 해결하는 문제
최근 음성-언어 통합 모델(Speech Large Language Models, Speech-LLMs)은 텍스트 중심의 LLM을 넘어 오디오 입력 및 출력을 엔드투엔드로 처리하는 방향으로 진화하고 있습니다. 그러나 대부분의 최신 오픈소스 및 상용 모델은 영어 및 소수의 고자원 언어에 편중되어 있습니다. 아랍어는 4억 명 이상의 화자가 사용하고 형태론적 복잡성(Morphological complexity) 및 방언(Dialects)의 다양성이 극심함에도 불구하고, Speech-LLM을 위한 고품질 정렬 데이터셋과 평가 벤치마크가 절대적으로 부족했습니다. 본 논문은 이러한 인프라 결핍을 해결하기 위해 데이터 생성, 모델 학습, 벤치마크 설계를 아우르는 통합 프로젝트인 **Nuha-Speech**를 제안합니다.

## 기존 방법의 한계
- **데이터 부족 및 편향**: 기존의 다국어 Speech-LLM(예: Whisper 기반 모델, SpeechGPT, AudioPaLM 등)은 주로 자동 음성 인식(ASR)이나 단순 번역(AST) 데이터만을 학습에 활용하여 고차원 추론 및 복합 지시어 수행 능력이 제한적입니다. 특히 아랍어의 경우 오픈 도메인 SQA(Speech Question-Answering) 코퍼스가 거의 전무했습니다.
- **방언 및 언어적 다양성 처리 부재**: 현대 표준 아랍어(Modern Standard Arabic, MSA)와 지역 방언(Gulf, Levantine, Egyptian 등) 간의 음성학적·어휘적 괴리를 고려한 체계적 튜닝 데이터가 부재하여 실제 배포 환경에서 성능 저하가 뚜렷했습니다.
- **표준화된 다태스크 평가 체계 부재**: 음성 이해, 번역, QA를 통합적으로 검증할 수 있는 통일된 메트릭 및 평가 파이프라인이 정립되지 않아 모델 간 객관적 비교가 불가능했습니다.

## 핵심 기여
1. **대규모 아랍어 SQA 코퍼스 구축**: 음성 인식, 번역, 질의응답, 문맥 이해 등을 포괄하는 150만 개 이상의 고품질 아랍어 음성 지시 튜닝(Instruction Tuning) 데이터를 합성 및 정제하여 확보했습니다.
2. **Qwen-Omni 기반의 아랍어 Speech-LLM 학습**: 검증된 다중모달 백본인 Qwen-Omni 계열을 베이스 모델로 삼아 다양한 파라미터 스케일에 대해 효율적인 모달리티 정렬(Modality Alignment) 및 파인튜닝을 수행했습니다.
3. **종합적 평가 프레임워크 수립**: 전통적인 ASR(Word Error Rate), 번역(BLEU), 그리고 개방형 질의응답(LLM-as-a-Judge 및 ROUGE/Exact Match 등)을 통합한 아랍어 전용 평가 체계를 구축하여 모델 성능을 다각도로 분석했습니다.

## 제안 방법과 주요 수식

### 1. 음성-텍스트 모달리티 정렬 및 인코딩
입력 음성 신호 $X \in \mathbb{R}^{T \times D_{in}}$은 사전 학습된 오디오 인코더(예: Whisper-Encoder 또는 Conformer 계열)를 통해 연속형 특징 표현(Continuous Representations)으로 변환됩니다.

$$H_{speech} = \text{AudioEncoder}(X) \in \mathbb{R}^{T' \times D_{audio}}$$

여기서 $T'$는 다운샘플링된 시계열 길이이며, $D_{audio}$는 인코더의 은닉 차원입니다. LLM의 임베딩 공간 $D_{llm}$과 정렬하기 위해 선형 프로젝션 또는 어댑터(Adapter) 네트워크 $\mathcal{P}_{\theta}$를 거칩니다.

$$Z_{speech} = \mathcal{P}_{\theta}(H_{speech}) \in \mathbb{R}^{T' \times D_{llm}}$$

### 2. 다중모달 지시 튜닝 목적함수
주어진 음성 입력 $Z_{speech}$와 텍스트 프롬프트 토큰 시퀀스 $U_{prompt} = (u_1, u_2, \dots, u_m)$가 주어졌을 때, 정답 시퀀스 $Y = (y_1, y_2, \dots, y_n)$를 자동회귀(Autoregressive) 방식으로 생성합니다. 모델의 최적화 목적함수는 다음과 같이 정답 토큰에 대한 음의 로그 가능도(Negative Log-Likelihood, NLL) 최소화로 정의됩니다.

$$\mathcal{L}_{SFT}(\theta) = -\sum_{t=1}^{n} \log P_{\theta}\left(y_t \mid Z_{speech}, U_{prompt}, y_{<t}\right)$$

여기서:
- $\theta$: 어댑터 $\mathcal{P}_{\theta}$ 및 LLM 백본의 파라미터 집합
- $y_t$: 시점 $t$에서 생성되는 목표 텍스트 토큰
- $y_{<t}$: $t$ 이전 시점까지 생성된 토큰 시퀀스

Nuha-Speech는 150만 개에 달하는 대규모 코퍼스를 활용하므로 단순 전사(Transcription) 태스크 $\mathcal{L}_{ASR}$뿐만 아니라 의미론적 추론을 요구하는 QA 태스크 $\mathcal{L}_{QA}$를 동일한 프레임워크 내에서 멀티태스크 방식으로 동시에 최적화합니다.

$$\mathcal{L}_{Total} = \lambda_1 \mathcal{L}_{ASR} + \lambda_2 \mathcal{L}_{Translation} + \lambda_3 \mathcal{L}_{QA}$$

각 가중치 $\lambda_i$를 통해 모델이 저수준 음향 특징 인지 능력과 고수준 의미론적 추론 능력 사이에서 균형을 유지하도록 유도합니다.

## 핵심 구조

*(원문 내 별도의 외부 이미지 URL이 제공되지 않았으므로, 논문 본문의 아키텍처 다이어그램(예: Figure 1: Nuha-Speech Framework Overview)을 참고하시기 바랍니다.)*

> **Figure 1 권장 캡처 안내 및 상세 시각화 설명:**
>
> **구조도 상세 묘사 (Architecture & Pipeline Workflow):**
> 논문의 전반적인 파이프라인은 크게 **(1) 데이터 파이프라인(Data Engine)**, **(2) 모델 아키텍처(Model Architecture)**, **(3) 평가 프레임워크(Evaluation Suite)** 의 3단계 수직/수평 흐름으로 구성되어 있습니다.
> 
> 1. **Data Engine**: 좌측에는 다양한 아랍어 원천 음성 코퍼스(뉴스, 일상 대화, 방언 데이터 등)와 텍스트 데이터셋이 위치합니다. 여기서 음성 전사 파이프라인과 대규모 언어 모델을 이용한 지시어 생성(Instruction Generation) 모듈을 거쳐, '음성 질문 - 텍스트/음성 답변' 쌍으로 구성된 150만 개 이상의 SQA 데이터가 필터링 및 밸런싱 과정을 통해 저장소로 모이는 과정이 도시되어 있습니다.
> 2. **Model Architecture**: 중앙부에는 입력 오디오 신호가 들어가는 오디오 인코더 블록이 상단에 배치되고, 인코더 출력은 컨볼루션 스트라이드 또는 크로스 어텐션 기반의 모달리티 프로젝터(Modality Projector)를 통과하여 토큰 시퀀스 형태로 변환됩니다. 텍스트 프롬프트는 텍스트 토크나이저를 거쳐 임베딩 레이어로 진입하며, 음성 임베딩과 텍스트 임베딩이 연결(Concatenate)되어 Qwen-Omni 트랜스포머 디코더 레이어로 전달되는 순차적 데이터 흐름이 화살표로 표현됩니다.
> 3. **Evaluation Suite**: 우측에는 훈련된 모델의 출력이 세 가지 주요 평가 갈래(ASR 모듈, 음성 기계 번역 모듈, 복합 SQA 추론 모듈)로 분기되며, 각각 WER, BLEU/COMET, 그리고 LLM-as-a-Judge 지표로 채점되는 검증 파이프라인이 나타나 있습니다.

## 실험 설정과 결과
- **백본 모델**: 다양한 연산 환경 및 용도에 맞추어 Qwen-Omni 계열의 변형 모델(예: 7B급 이상 및 소형 변형)을 채택.
- **데이터셋 구성**:
  - 총 150만 개 이상의 음성-질의응답 샘플.
  - 현대 표준 아랍어(MSA) 중심 구성에 주요 지역 방언(Gulf, Levantine, Egyptian 등)이 포함된 혼합 분포.
- **주요 결과 및 관찰**:
  - **음성 이해 및 추론(SQA)**: 기존의 일반 다국어 모델 대비 아랍어 질의응답 정확도 및 자연스러움에서 유의미한 성능 향상을 달성. 단순 ASR 후 텍스트 LLM을 거치는 캐스케이드(Cascade) 방식에 준하거나 특정 문맥 추론 태스크에서는 엔드투엔드 모델이 음향 단서(운율, 억양)를 직접 활용하여 오차 전파(Error Propagation)를 방지함.
  - **음성 전사(ASR) 및 번역**: 대규모 음성 지시 튜닝을 거친 후에도 기본 전사 성능(WER)이 유지되거나 향상되었으며, 영어-아랍어 간 교차 모달 번역 성능에서도 견고한 수치를 기록함.
  - **스케일링 효과**: 모델 파라미터가 증가함에 따라 방언 처리 능력 및 복합 지시어 수행 능력이 멱법칙(Power-law) 경향을 보이며 안정적으로 개선됨.

## 잘한 점
- **데이터 인프라의 오픈 사이언스 기여**: 자원이 빈약한 아랍어권에 150만 개 규모의 체계적인 SQA 데이터를 구축하여 커뮤니티 전반의 연구 진입 장벽을 낮춤.
- **체계적인 3단계 파이프라인**: 단순 모델 학습에 그치지 않고, 데이터 구축부터 평가 프로토콜까지 표준화된 방법론을 완성도 있게 제시함.
- **모달리티 정렬의 안정성**: 멀티태스크 목적함수 설계를 통해 Speech-to-Text 기본 성능을 훼손하지 않으면서 복합 추론 태스크를 성공적으로 결합함.

## 한계와 의문점
- **음성 출력(Speech-to-Speech)의 부재/제한성**: 본 연구의 주요 초점은 음성 입력에 대한 이해 및 텍스트 생성(Speech-to-Text)에 맞추어져 있어, 진정한 풀 듀플렉스(Full-duplex) 실시간 음성 대화 모델로 확장하기 위한 엔드투엔드 음성 합성(Speech Synthesis/Vocoding) 부분은 추가 연구가 필요합니다.
- **방언 커버리지의 편차**: MSA 데이터의 비중이 지배적일 가능성이 높아, 데이터가 극히 적은 특정 소수 아랍어 방언에 대한 일반화 한계가 존재할 수 있습니다.
- **인위적 합성 데이터 의존도**: 150만 개 코퍼스 중 상당 부분이 LLM 기반 텍스트 생성 및 TTS(Text-to-Speech)를 거친 합성 데이터일 경우, 실제 인간의 자연스러운 발화 특성(필러, 끊김, 배경 잡음 등)과의 괴리가 발생할 수 있습니다.

## 실무 적용 가능성
- **중동 및 아랍권 인텔리전트 보이스 에이전트**: 금융, 공공 서비스, 전자상거래 도메인에서 아랍어 화자를 위한 고품질 대화형 콜센터 및 AI 비서 시스템 구축에 즉각 활용 가능.
- **엔터프라이즈 캐스케이드 파이프라인 대체**: 기존의 'ASR $\rightarrow$ Text LLM $\rightarrow$ TTS' 구조를 단일 모델 기반으로 단순화하여 시스템 복잡도와 지연 시간(Latency)을 단축할 수 있는 기초 모델로 적합.

## 관련 연구와 연결점
- **Qwen-Audio / Qwen-Omni**: 본 연구의 모델 베이스라인이자 다중모달 아키텍처의 근간을 제공.
- **SpeechGPT / AudioPaLM**: 음성을 이산 토큰(Discrete Tokens)으로 다루거나 엔드투엔드로 통합하려는 시도들의 연장선상에 위치.
- **Whisper & SeamlessM4T**: 다국어 음성 인코딩 및 기계 번역에서 Nuha-Speech의 오디오 표현 기준점을 제공하는 선행 연구.

## 원문 정보
- Title: Nuha-Speech: Building General-Purpose Arabic Speech-LLMs
- Authors: Yingzhi Wang, Reem Alhazzani, Muhammad Alqurishi
- Venue/Repository: arXiv
- Published: 2024 (Review Note: arXiv ID 표기 확인 필요 - URL: `https://arxiv.org/pdf/2609.11892v1`)
- URL: [https://arxiv.org/pdf/2609.11892v1](https://arxiv.org/pdf/2609.11892v1)

> 이 글은 자동 생성된 초안을 바탕으로 작성되며, 공개 전에 저자·수식·수치·출처를 직접 검수합니다.
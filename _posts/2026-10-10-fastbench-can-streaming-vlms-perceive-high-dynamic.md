---
title: "FastBench: Can Streaming VLMs Perceive High-Dynamic Real-World Streams?"
description: "제한된 컨텍스트 버짓 내에서 고역동적(High-Dynamic) 실시간 비디오 스트림을 처리하기 위한 벤치마크 FastBench와 적응형 프레임 레이트 조정 베이스라인 ProactiveFrame을 제안한 논문."
date: 2026-10-15 09:00:00 +0900
categories:
  - Paper Reviews
  - multimodal
paper_authors:
  - Yuxuan Hu
  - Weikang Shi
  - Yang Bo
  - Xudong Lu
  - Xintong Guo
  - Shuhan Li
  - Yuyang He
  - Huankang Guan
  - Peiwen Sun
  - Yunqiao Yang
  - Wenbo Li
  - Rui Liu
  - Hongsheng Li
paper_url: "https://arxiv.org/abs/2610.12427v1"
tags:
  - Video-LLM
  - Streaming-VLM
  - Video-Benchmark
  - High-Dynamic
toc: true
mermaid: false
---

## 3줄 요약
- 기존 비디오 스트리밍 벤치마크가 놓치고 있던 고역동적(High-dynamic) 순간 포착 능력을 체계적으로 측정하기 위해 306개 고정밀 QA 쌍과 증거 구간(evidence intervals)을 포함하는 **FastBench**를 구축함.
- 2 FPS 이하 저주기 샘플링으로 풀리는 질문을 엄격히 배제하고, SAM3 및 CoTracker3 기반의 객체 궤적 검증과 3단계 인간 검수를 결합한 생성 파이프라인을 제안함.
- 텍스트 토큰을 통해 능동적으로 입력 프레임 레이트를 조절하는 훈련 불필요(Training-free) 베이스라인 **ProactiveFrame**을 제시하고, 최신 SOTA 모델(Gemini-3.5-Flash 등)도 50.7%에 불과한 정확도를 보임을 밝힘.

## 논문이 해결하는 문제
기존 비디오 거대 언어 모델(Video-LLMs, Streaming VLMs)은 연속적인 스트리밍 입력을 처리할 때 제한된 컨텍스트 윈도우(Context window budget) 및 연산 한계로 인해 대개 1~2 FPS의 균일하고 희소한(Sparse uniform) 샘플링 방식을 채택합니다. 
그러나 자율주행, 스포츠 분석, 고속 객체 추적, 이상 감지 등 현실의 **고역동적(High-Dynamic) 실세계 비디오 스트림**에서는 찰나의 순간(수 프레임 내)에 결정적인 이벤트가 발생합니다. 기존 벤치마크(Video-ChatGPT, EgoSchema, StreamingBench 등)는 저역동적 정적 클립에 치중되어 있어, 스트리밍 VLM이 temporal history 길이, spatial resolution, temporal granularity 사이에서 어떻게 trade-off를 최적화해야 하는지, 그리고 모델이 빠른 이벤트를 놓치지 않고 인지할 수 있는지 평가하지 못했습니다.

## 기존 방법의 한계
1. **평가 데이터셋의 시간 해상도 결여**: 기존 데이터셋의 비디오 QA는 시간적 변화율이 낮아 1 FPS 수준으로 균일하게 다운샘플링해도 정답 유추가 가능한 문제들이 대다수였습니다.
2. **환각 및 궤적 오차 검증 미흡**: 고속 이동 객체의 미세 동작(fine-grained motion)을 설명하는 정답 라벨에 대해 자동화된 궤적 일관성 검증 도구가 부재하여 노이즈가 많았습니다.
3. **고정된 프레임 정책의 딜레마**: 고정된 24 FPS를 쓰면 컨텍스트 메모리가 순식간에 고갈되어 장기 기억(Temporal history)을 유지하지 못하고, 1~2 FPS를 쓰면 이벤트가 샘플링 프레임 사이로 누락(Temporal aliasing)되는 본질적 한계가 존재했습니다.

## 핵심 기여
1. **FastBench 벤치마크**: 8개 도메인, 6개 핵심 역량(동작 변화, 속도 추정, 세부 상호작용 등), 3가지 시간적 범위(Forward, Instant, Backward)를 아우르는 306개 고난도 QA 세트를 정립. 고속 이벤트 발생 시점(Evidence intervals)을 사람 검수를 거쳐 정밀 마킹함.
2. **Trajectory-Grounded 데이터 생성 파이프라인**: 
   - 고주기(High-FPS) 클립으로부터 초기 QA를 생성.
   - 2 FPS 희소 입력 조건에서 LLM/VLM이 정답을 맞출 수 있는 문제를 필터링하여 탈락시킴.
   - SAM3와 CoTracker3를 활용해 실제 객체 궤적의 시공간 연속성을 수학적으로 대조·검증하고, 3라운드 휴먼 인스펙션을 적용.
3. **ProactiveFrame (Training-free Baseline)**: VLM이 스트림을 모니터링하다가 복잡한 사건이 감지되면 텍스트 토큰(`[ACCELERATE]`, `[DECELERATE]`)을 생성하여 입력 FPS를 동적으로 스위칭하는 듀얼 티어 슬라이딩 윈도우(Dual-tier sliding window) 메커니즘을 제안.

## 제안 방법과 주요 수식

### 1. Dual-Tier Sliding Window 및 메모리 예산 공식
제한된 토큰 예산 $B$ 하에서 비디오 스트림을 관리하기 위해 모델은 최근 관측 구간과 과거 이력 구간을 계층적으로 분할합니다. 
시간 $t$에서 총 비디오 토큰 수 $\mathcal{T}(t)$는 다음과 같이 제약됩니다:

$$
\mathcal{T}(t) = \mathcal{T}_{\text{recent}}(t) + \mathcal{T}_{\text{history}}(t) \le B
$$

여기서 각 티어의 토큰 소비는 입력 프레임 레이트와 시각 토큰 압축률에 의해 결정됩니다:

$$
\mathcal{T}_{\text{recent}}(t) = N_{\text{recent}} \cdot f_{\text{high}} \cdot \kappa_v, \quad \mathcal{T}_{\text{history}}(t) = N_{\text{history}} \cdot f_{\text{low}} \cdot \kappa_v
$$

- $N_{\text{recent}}, N_{\text{history}}$: 각각 최근 윈도우와 과거 이력 윈도우의 시간 길이(초 단위).
- $f_{\text{high}}, f_{\text{low}}$: 고밀도 샘플링 주파수($\text{FPS}$) 및 저밀도 다운샘플링 주파수($f_{\text{low}} \ll f_{\text{high}}$).
- $\kappa_v$: 프레임당 인코딩되는 visual token의 개수.

새로운 프레임이 인입되면 최근 윈도우의 가장 오래된 프레임들은 균일 서브샘플링(Uniform subsampling) 비율 $r = \frac{f_{\text{low}}}{f_{\text{high}}}$에 따라 축약되어 이력 윈도우로 이동합니다.

### 2. Trajectory Grounding 기반 답안 검증
객체의 2차원 공간 궤적 $\mathbf{P} = \{ (x_i, y_i) \}_{i=1}^T$에 대해, CoTracker3 추적 결과를 바탕으로 운동 변위(Motion Displacement)와 곡률(Curvature)을 측정하여 동작의 일관성을 검증합니다:

$$
\mathcal{D}(\mathbf{P}) = \sum_{i=1}^{T-1} \|\mathbf{p}_{i+1} - \mathbf{p}_i\|_2
$$

$$
\mathcal{C}(\mathbf{P}) = \frac{1}{T-2} \sum_{i=2}^{T-1} \arccos \left( \frac{(\mathbf{p}_i - \mathbf{p}_{i-1}) \cdot (\mathbf{p}_{i+1} - \mathbf{p}_i)}{\|\mathbf{p}_i - \mathbf{p}_{i-1}\|_2 \|\mathbf{p}_{i+1} - \mathbf{p}_i\|_2} \right)
$$

자동 생성된 질문이 설명하는 고속 회전이나 급격한 가속도가 물리적 궤적 $\mathcal{D}(\mathbf{P})$ 및 각도 변화율 $\mathcal{C}(\mathbf{P})$의 임계값 조건을 충족할 때만 유효 QA로 승인하여, 텍스트 생성 환각(Hallucination)을 수치적으로 차단합니다.

## 핵심 구조

> **[아키텍처 다이어그램 확인 및 시각화 안내]**  
> *참고:* 원문에서 제공된 공개 이미지 URL이 없으므로, 독자는 논문의 **Figure 1 (FastBench Pipeline 및 ProactiveFrame Architecture)**을 참조하십시오.

### Figure 1 상세 구조 설명 (개념도)
해당 다이어그램은 상단과 하단의 2가지 핵심 파이프라인으로 구성되어 있습니다:
1. **FastBench Data Construction Pipeline (상단부)**:
   - **입력 비디오 스트림**: 60 FPS 이상의 고화질 실세계 영상(스포츠, 드론, 드라이빙 등).
   - **Trajectory Extraction & Filtering**: SAM3(세그멘테이션 마스크)와 CoTracker3(포인트 트래커)를 통해 빠른 객체의 좌표열 $\mathbf{P}$를 추출.
   - **2-FPS Filter**: 동일 클립을 2 FPS로 다운샘플링하여 소형 VLM에게 질의한 뒤, 저해상도에서도 맞출 수 있는 쉬운 질문(정적 맥락 기반)은 자동으로 탈락(Drop).
   - **Evidence Interval Annotation**: 실제 정답 판별에 필요한 최소 시간 윈도우 $[t_{\text{start}}, t_{\text{end}}]$를 인간 어노테이터가 라벨링.
2. **ProactiveFrame Inference Workflow (하단부)**:
   - **Streaming Ingestion**: 카메라/비디오에서 실시간 프레임이 유입됨.
   - **Dual-Tier Window Manager**: 직전 관측은 High-FPS 버퍼($f_{\text{high}}$)에 보관하고, 오래된 데이터는 Temporal Pooling을 거쳐 Low-FPS 버퍼($f_{\text{low}}$)로 전달.
   - **VLM Policy Generation**: VLM이 출력 텍스트 스트림 사이에 능동 제어 토큰(`[ACCELERATE]`)을 방출하면, 입력 프레임 취득단(Frame grabber)이 즉시 샘플링 레이트를 끌어올려 고역동적 순간을 놓치지 않도록 제어 루프를 형성.

## 실험 설정과 결과

### 평가 대상 모델
- **상용 폐쇄형 모델**: Gemini-3.5-Flash, GPT-4o 계열
- **오픈소스 스트리밍/비디오 모델**: Qwen3-VL-8B, VideoLLaMA 계열 등

### 주요 결과
- **Gemini-3.5-Flash 성능**: 현존 최강 모델임에도 FastBench에서 **50.7%**의 정확도에 그침. 이는 고역동적 비디오 스트림 이해가 현 세대 최상위 모델에게도 미지의 영역임을 시사함.
- **FPS 변화에 따른 Qwen3-VL-8B 추론 변화**:
  - 2 FPS 샘플링: **32.9%**
  - 24 FPS 샘플링: **44.6%** (+11.7%p 상승)
  - 그러나 24 FPS 환경에서는 메모리 제한으로 장기 컨텍스트(History)가 급격히 삭제되어 과거 문맥과의 연계 질문에서 점수 포화 및 저하 발생.
- **ProactiveFrame 효과**:
  - 고정된 희소 샘플링(Uniform Sparse) 대비 각각 **+5.4%p**, **+1.5%p** 향상 달성.
  - 하지만 사람이 완벽한 시점을 지정해주는 **Oracle-guided focusing** 방식의 성능에는 크게 미치지 못함.

## 잘한 점
1. **문제 정의의 정확성**: 비디오 스트리밍 모델의 아킬레스건인 "저주기 샘플링 vs 컨텍스트 길이"의 본질적 딜레마를 고역동성(High-dynamics)이라는 실제적 상황으로 정확히 짚어냄.
2. **엄격한 데이터 정제 절차**: 단순히 LLM으로 QA를 생성하는 것에 그치지 않고, 2 FPS 필터링과 기하학적 궤적 추적 도구(SAM3, CoTracker3), 인간 3단계 검수를 결합하여 벤치마크 신뢰도를 극대화함.
3. **경량 적응형 베이스라인 제안**: 대규모 파라미터 재학습 없이도 텍스트 토큰 인터페이스만으로 프레임 레이트를 가변 제어할 수 있음을 입증.

## 한계와 의문점
1. **데이터셋 규모**: 총 306개의 QA 쌍은 정밀한 검수를 거쳤으나, 모델의 도메인별 세부 역량을 대규모 통계적 유의성으로 검증하기에는 다소 작은 규모임.
2. **반응 지연(Latency) 문제**: ProactiveFrame은 모델이 이상 징후를 감지하고 텍스트 토큰(`[ACCELERATE]`)을 생성하기까지의 디코딩 레이턴시가 발생함. 초고속(수십 밀리초 단위)으로 지나가는 극단적 이벤트에서는 이미 사건이 종료된 후 프레임 레이트가 증가할 위험이 있음.
3. **하드웨어 대역폭 고려**: 입력 FPS를 동적으로 올리는 작업은 카메라 센서 및 비디오 디코더 인터페이스의 I/O 병목을 동반하므로, 실제 온디바이스 에지 환경에서의 실시간성 검증이 추가로 필요함.

## 실무 적용 가능성
- **지능형 관제 및 CCTV**: 평상시 1 FPS로 전력과 네트워크 대역폭을 절약하다가, 침입이나 낙상 등 급격한 모션이 포착될 때 자동으로 30~60 FPS로 전환하여 정밀 추론을 수행하는 시스템에 직접 활용 가능.
- **자율주행 및 로보틱스**: 예측 불가능한 보행자의 돌발 행동이나 고속 낙하물을 감지하기 위한 계층적 비전 버퍼(Dual-tier window) 설계에 참조할 수 있음.

## 관련 연구와 연결점
- **Streaming Video Understanding**: StreamingBench, Memory-augmented Video-LLMs와 연결되며, 이를 시간 해상도 극대화 관점으로 확장함.
- **Adaptive Frame Sampling**: 과거 컴퓨터 비전 분야의 AdaFrame, Frame-Exit 등 강화학습 기반 프레임 선택 연구를 최신 VLM 토큰 인터페이스로 재해석한 형태임.

## 원문 정보
- **Title**: FastBench: Can Streaming VLMs Perceive High-Dynamic Real-World Streams?
- **Authors**: Yuxuan Hu, Weikang Shi, Yang Bo, Xudong Lu, Xintong Guo, Shuhan Li, Yuyang He, Huankang Guan, Peiwen Sun, Yunqiao Yang, Wenbo Li, Rui Liu, Hongsheng Li
- **Venue/Repository**: arXiv
- **Published**: 2026-10-15 (v1 기준)
- **URL**: [https://arxiv.org/abs/2610.12427v1](https://arxiv.org/abs/2610.12427v1)

> 이 글은 자동 생성된 초안을 바탕으로 작성되며, 공개 전에 저자·수식·수치·출처를 직접 검수합니다.
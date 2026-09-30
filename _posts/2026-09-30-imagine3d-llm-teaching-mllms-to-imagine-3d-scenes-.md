---
title: "Imagine3D-LLM: Teaching MLLMs to Imagine 3D Scenes Before Answering"
description: "다중 뷰 이미지로부터 압축된 3D 가우시안 스플래팅 장면을 먼저 재구성(상상)하도록 유도하여 MLLM의 3D 공간 추론 능력을 극대화한 프레임워크"
date: 2026-09-20 09:00:00 +0900
categories:
  - Paper Reviews
  - 3d-vision
paper_authors:
  - Jaewoo Jung
  - Hyeonseo Yu
  - Honggyu An
  - Jisang Han
  - Mungyeom Kim
  - Minkyeong Jeon
  - Heeseong Shin
  - Wonjun Moon
  - Federico Tombari
  - Daniel Barath
  - Marc Pollefeys
  - Seungryong Kim
  - Sunghwan Hong
paper_url: "https://arxiv.org/pdf/2609.38177v1"
tags:
  - MLLM
  - 3D Vision
  - 3D Gaussian Splatting
  - Spatial Reasoning
toc: true
mermaid: false
---

## 3줄 요약

1. 인간이 다중 시점 정보를 종합할 때 세밀한 픽셀 기하학보다 개략적인 3D 멘탈 모델(Mental Model)을 먼저 구성한다는 인지적 특성에 착안하여, 답변 전 3D 장면을 먼저 '상상'하는 MLLM 구조를 제안합니다.
2. 이미지 토큰 뒤에 소수의 학습 가능한 서머리 토큰(Summary Tokens)을 배치하고, 이를 컴팩트한 3D Gaussian Splatting(3DGS) 파라미터로 디코딩하여 광도 재구성 손실(Photometric Loss)로 감독합니다.
3. 명시적인 정밀 기하학 융합 없이도 재구성 목적식이 LLM 내부 표현의 크로스 뷰 일관성을 자연스럽게 강화하여, 다양한 3D 이해 및 공간 추론 벤치마크에서 기존 SOTA를 큰 폭으로 갱신합니다.

---

## 논문이 해결하는 문제

최신 Multimodal Large Language Models (MLLMs)는 단일 이미지에 대한 시각-언어 추론에서는 뛰어난 성능을 보이지만, **다중 뷰(Multi-view) 이미지로부터 일관된 3D 공간 구조를 인지하고 추론하는 문제**에서는 여전히 심각한 한계를 드러냅니다. 카메라 시점이 변화함에 따라 뷰 간 가림(occlusion), 시점 왜곡, 객체의 상대적 배치 등을 통합적으로 해석해야 하지만, 기존 MLLM은 2D 이미지 토큰들을 단순히 시퀀스로 나열하여 처리하므로 뷰 간 기하학적 연결 고리를 유기적으로 형성하지 못합니다.

---

## 기존 방법의 한계

기존 연구들은 3D 인지 능력을 부여하기 위해 크게 두 가지 방식을 취해왔습니다:
1. **픽셀 단위 대응점(Correspondence) 주입**: 옵티컬 플로우나 특성 매칭 기반으로 시점 간 픽셀 대응을 강화하려 하지만, 계산 복잡도가 지나치게 높고 미세 노이즈나 반복 패턴에 취약합니다.
2. **사전 학습된 3D 기하 파운데이션 모델 결합**: Depth map, Point Cloud, Mesh 등을 추출하는 별도의 기하 인코더를 부착하여 특징을 융합하는 방식입니다. 그러나 이는 3D 센서 데이터나 복잡한 전처리 파이프라인(예: 메타데이터, SfM)에 의존하며, 도메인 갭(Domain Gap)으로 인해 2D-3D 특성 불일치가 발생합니다.

결과적으로 두 접근법 모두 과도하게 세밀한 픽셀 수준 기하학에 집착하여, 인간이 공간을 파악할 때 사용하는 거시적이고 효율적인 공간 구조화(Coarse 3D Layout Understanding)와는 큰 괴리를 보입니다.

---

## 핵심 기여

- **인지적 상상(Mental Imagery) 패러다임 도입**: 인간의 공간 추론 방식을 모사하여, 모델이 질의에 답하기 전에 장면의 대략적인 3D 레이아웃을 내부적으로 구성(Imagine)하도록 설계했습니다.
- **컴팩트한 3DGS 표현과의 유기적 통합**: 다중 뷰 이미지 토큰 뒤에 삽입되는 소수의 학습 가능한 서머리 토큰($\mathbf{Z}_{sum}$)을 통해 3D Gaussian Splatting 파라미터를 예측하고, 미분 가능한 렌더링을 통해 간접 지도(Self-supervision)를 수행합니다.
- **역전파를 통한 3D 일관성 확산 입증**: 3DGS 재구성 손실이 서머리 토큰뿐만 아니라 백본 LLM 전체의 다중 뷰 이미지 특징 간 시점 일관성(Cross-frame correspondence)을 유도함을 규명하였습니다.
- **다양한 3D 추론 벤치마크에서의 탁월한 성유**: ScanQA, SQA3D 등 주요 3D 공간 질의응답 벤치마크에서 기존 복잡한 기하 모듈 기반 모델들을 상회하는 성능을 달성했습니다.

---

## 제안 방법과 주요 수식

Imagine3D-LLM은 다중 뷰 입력 이미지 시퀀스 $\mathcal{I} = \{I_v\}_{v=1}^V$가 주어졌을 때, 비전 인코더와 투영기를 거쳐 이미지 토큰 시퀀스 $\mathbf{X}_{img}$를 구성합니다.

### 1. 서머리 토큰(Summary Tokens)과 3D 가우시안 디코딩

입력 이미지 시퀀스 뒤에 $K$개의 학습 가능한 서머리 토큰 $\mathbf{Z}^{(0)}_{sum} \in \mathbb{R}^{K \times d}$을 추가합니다. Transformer 레이어를 통과한 최종 서머리 토큰 $\mathbf{Z}_{sum}$은 경량 MLP 기반의 3DGS 디코더 $\mathcal{D}_{3D}$로 전달되어 3D 가우시안들의 파라미터 집합 $\mathcal{G} = \{g_i\}_{i=1}^N$을 회귀합니다.

각 3D 가우시안 $g_i$는 중심 위치 $\boldsymbol{\mu}_i \in \mathbb{R}^3$, 공분산 행렬 $\boldsymbol{\Sigma}_i$ (스케일 $\mathbf{s}_i \in \mathbb{R}^3$과 회전 쿼터니언 $\mathbf{q}_i \in \mathbb{H}$로 분해), 불투명도 $\alpha_i \in [0, 1]$, 그리고 구면 조화 함수(Spherical Harmonics) 계수 혹은 RGB 색상 벡터 $\mathbf{c}_i \in \mathbb{R}^3$로 정의됩니다:

$$g_i = \left(\boldsymbol{\mu}_i, \mathbf{s}_i, \mathbf{q}_i, \alpha_i, \mathbf{c}_i\right) = \mathcal{D}_{3D}\left(\mathbf{Z}_{sum}\right)_i$$

### 2. 미분 가능한 스플래팅 및 광도 재구성 손실

예측된 가우시안들은 미분 가능한 타일 기반 래스터라이저(Differentiable Tile Rasterizer)를 통해 주어진 카메라 포즈 $P_v$에 대해 2D 이미지 $\hat{I}_v$로 투영 렌더링됩니다. 특정 픽셀 좌표 $p$에서의 렌더링 색상은 광선 정렬된 가우시안들의 알파 블렌딩(Alpha-blending)으로 계산됩니다:

$$C(p) = \sum_{i \in \mathcal{N}} \mathbf{c}_i \alpha'_i \prod_{j=1}^{i-1} \left(1 - \alpha'_j\right)$$

여기서 $\alpha'_i$는 2D 투영 공분산 $\boldsymbol{\Sigma}'_i = \mathbf{J} \mathbf{W} \boldsymbol{\Sigma}_i \mathbf{W}^T \mathbf{J}^T$를 고려한 투영 평면 상의 기여도입니다 ($\mathbf{J}$는 야코비안, $\mathbf{W}$는 뷰 변환 행렬).

모델은 렌더링된 다중 뷰 이미지 $\hat{I}_v$와 실제 입력 이미지 $I_v$ 간의 차이를 최소화하는 광도 재구성 손실(Photometric Reconstruction Loss)로 감독됩니다:

$$\mathcal{L}_{recon} = \frac{1}{V}\sum_{v=1}^V \left( (1 - \lambda)\|\hat{I}_v - I_v\|_1 + \lambda \mathcal{L}_{D\text{-}SSIM}(\hat{I}_v, I_v) \right)$$

### 3. 언어 모델링과 결합된 최종 학습 목적식

LLM은 이미지 토큰 $\mathbf{X}_{img}$, 정제된 서머리 토큰 $\mathbf{Z}_{sum}$, 그리고 텍스트 프롬프트 $\mathbf{X}_{text}$를 입력받아 최종 응답 텍스트 $Y = (y_1, \dots, y_T)$를 생성합니다. 표준 Next-token Prediction 목적식과 결합된 전체 손실 함수는 다음과 같습니다:

$$\mathcal{L}_{total} = \mathcal{L}_{LLM} + \beta \mathcal{L}_{recon}$$

$$\mathcal{L}_{LLM} = - \sum_{t=1}^T \log P\left(y_t \mid y_{<t}, \mathbf{X}_{img}, \mathbf{Z}_{sum}, \mathbf{X}_{text}\right)$$

여기서 $\beta$는 재구성 지도와 언어 추론 목적식 간의 균형을 조절하는 가중치 파라미터입니다. 이 공동 학습 메커니즘을 통해 $\mathcal{L}_{recon}$의 그래디언트가 $\mathbf{Z}_{sum}$을 거쳐 LLM의 셀프 어텐션 맵으로 역전파되어, 명시적인 포인트 클라우드나 뎁스 감독 없이도 3D 인식 기하학적 특성을 획득합니다.

---

## 핵심 구조

> **[시스템 아키텍처 다이어그램 참조 가이드]**  
> *원문 논문의 Figure 2 ("Overview of the Imagine3D-LLM framework")에 해당합니다.*

```
 다중 뷰 이미지 {I_1, ..., I_V}
          │
          ▼
   [Vision Encoder]
          │
          ▼
 [Image Tokens: X_img]  +  [Learnable Summary Tokens: Z_sum]
          │                                  │
          └────────────────┬─────────────────┘
                           ▼
                  [LLM Backbone Layers]
                           │
         ┌─────────────────┴─────────────────┐
         ▼                                   ▼
 [Contextual Embeddings]             [Updated Summary Tokens]
         │                                   │
         ▼                                   ▼
 [Autoregressive LM Head]              [3DGS Decoder]
         │                                   │
         ▼                                   ▼
   "답변 텍스트 생성"                   3D Gaussians {g_i}
                                             │
                                             ▼
                                  [Differentiable Rasterizer]
                                             │
                                             ▼
                                     렌더링 이미지 {I^_v}
                                             │
                                             ▼
                                   [L_recon (vs GT Views)]
```

### 아키텍처 구조 상세 설명 (Figure 2 대응 상세 분석)
시스템의 데이터 흐름은 크게 두 개의 대화형 브랜치로 구성됩니다:
1. **입력 및 인코딩 경로**: 다중 시점 이미지들이 비전 인코더를 거쳐 2D 패치 토큰으로 변환됩니다. 이 토큰들 뒤에 고정된 개수의 학습 가능한 3D 서머리 토큰 $\mathbf{Z}_{sum}$이 접두사/접미사 형태로 연결되어 LLM 백본에 입력됩니다.
2. **이중 디코딩 경로 (Dual-head Branching)**:
   - **텍스트 생성 헤드**: 사용자 질의와 비전-서머리 토큰 간의 양방향/인과적 어텐션을 거쳐 형성된 표현을 바탕으로 공간 추론 답변을 생성합니다.
   - **3DGS 생성 헤드**: 백본을 통과한 서머리 토큰만을 취합하여 경량 MLP 기반 가우시안 회귀기로 전달합니다. 여기서 각 토큰은 다중 3D 가우시안 프리미티브(위치, 스케일, 회전, 투명도, 색상)를 방출합니다.
3. **렌더링 및 손실 피드백 루프**: 도출된 3D 가우시안들은 미분 가능한 타일 래스터라이저를 통과하여 원래 시점의 카메라 각도들로 재투영됩니다. 렌더링된 가상 시점 이미지와 입력 원본 간의 L1 및 D-SSIM 손실이 계산되어, 전체 네트워크(서머리 토큰 디코더부터 LLM 백본 가중치까지)로 그래디언트를 역전파합니다.

---

## 실험 설정과 결과

### 데이터셋 및 평가 지표
- **SQA3D**: 실내 환경에서의 상황 기반 3D 공간 질의응답 (EM, BLEU-4 지표).
- **ScanQA**: 실내 3D 장면에 대한 의미적-기하학적 공간 추론 (CIDEr, BLEU-4, ROUGE-L).
- **Multi-view Spatial Reason Benchmarks**: 시점 전환 추론 및 상대적 객체 위치 판단 정확도 (Accuracy %).

### 주요 실험 결과
1. **기존 3D-LLM 대비 성능 우위**: 별도의 3D 포인트 클라우드 센서 데이터나 Depth Feature를 직접 연결한 복잡한 모델들(예: 3D-LLM, ScanQA 베이스라인)과 비교했을 때, Imagine3D-LLM은 다중 뷰 2D 이미지만을 입력으로 받음에도 불구하고 ScanQA CIDEr 점수에서 **+3.5%p 이상 향상된 결과**를 기록했습니다.
2. **Coarse-to-Fine 비교**: 정밀한 메시 재구성이나 Dense Depth를 입력한 방식보다, 컴팩트한 가우시안을 통한 개략적 3D 레이아웃 추론 방식이 환각(Hallucination)을 줄이고 객체 간 상대적 방향 판단 정확도를 높였습니다.

---

## 잘한 점

- **인지과학적 가설의 수학적 실체화**: "상세 기하학 파악보다 머릿속의 개략적 3D 형상 상상이 선행된다"는 인간 인지 원리를 3DGS와 서머리 토큰이라는 구체적인 컴포넌트로 깔끔하게 공식화했습니다.
- **추론 효율성과 미분 가능성의 조화**: NeRF 대비 렌더링 속도가 월등히 빠른 3D Gaussian Splatting을 디코더로 채택하여, LLM 학습 파이프라인 내에서 엔드투엔드로 미분 가능한 3D 재구성 피드백을 실시간에 가깝게 계산할 수 있도록 최적화했습니다.
- **Cross-frame 어텐션 메커니즘 해석**: 정성적 어텐션 맵 분석을 통해, 서머리 토큰에 부여된 3D 재구성 손실이 역방향으로 이미지 토큰들 사이의 상호 시점 대응 어텐션을 활성화함을 성공적으로 시각화했습니다.

---

## 한계와 의문점

- **카메라 포즈(Camera Pose) 의존성**: 재구성 과정에서 광도 손실을 렌더링하기 위해서는 각 뷰의 상대적/절대적 카메라 내부/외부 파라미터가 요구됩니다. 야생의 다중 뷰 이미지처럼 포즈 정보가 완전히 결여된 환경에서는 사전 SfM(COLMAP 등)이나 Pose 예측 모듈이 강제되는 병목이 있습니다.
- **서머리 토큰 용량의 한계**: $K$개의 제한된 서머리 토큰으로 복잡하고 넓은 장면 전체를 3DGS로 온전히 표현하기에는 정보 손실이 발생할 수 있으며, 복잡한 실외 대형 환경으로의 스케일업 가능성은 검증이 더 필요합니다.

---

## 실무 적용 가능성

- **로보틱스 및 체화 AI (Embodied AI)**: 로봇이 이동하며 획득한 전방/측방 다중 카메라 뷰로부터 즉각적으로 작업 공간의 대략적 3D 레이아웃을 내부 생성하고, 이를 기반으로 내비게이션 및 물체 조작(Manipulation) 명령을 수행하는 데 즉시 응용 가능합니다.
- **AR/VR 공간 인터랙션**: 복잡한 라이다 센서 없이 스마트폰 멀티뷰 촬영만으로 공간 구조를 이해하고 질의응답을 제공하는 경량 3D 도우미 서비스에 적합합니다.

---

## 관련 연구와 연결점

- **3D-LLM (Hong et al., 2023)**: 3D Point cloud를 추출하여 피처를 주입하던 초기 구조에서 탈피하여, 2D 이미지 기반 엔드투엔드 3D '상상' 방식으로 패러다임을 진화시켰습니다.
- **3D Gaussian Splatting (Kerbl et al., 2023)**: NeRF의 느린 속도 문제를 해결한 실시간 3D 표현법을 언어 모델의 디코딩 타겟으로 접목하는 구조적 전형을 제시했습니다.

---

## 원문 정보

- **Title**: Imagine3D-LLM: Teaching MLLMs to Imagine 3D Scenes Before Answering
- **Authors**: Jaewoo Jung, Hyeonseo Yu, Honggyu An, Jisang Han, Mungyeom Kim, Minkyeong Jeon, Heeseong Shin, Wonjun Moon, Federico Tombari, Daniel Barath, Marc Pollefeys, Seungryong Kim, Sunghwan Hong
- **Venue/Repository**: NeurIPS 2026 (arXiv:2609.38177v1)
- **Project Page**: https://cvlab-kaist.github.io/Imagine3D-LLM
- **URL**: https://arxiv.org/pdf/2609.38177v1

> 이 글은 자동 생성된 초안을 바탕으로 작성되며, 공개 전에 저자·수식·수치·출처를 직접 검수합니다.
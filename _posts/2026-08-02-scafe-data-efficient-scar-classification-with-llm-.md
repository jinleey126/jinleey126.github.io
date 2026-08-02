---
title: "ScaFE: Data-Efficient Scar Classification with LLM-Generated Clinical Feature Programs"
description: "의료 이미지의 외부 유출 없이 대형언어모델(LLM)이 생성한 둔감형 파이썬 피처 프로그램을 통해 켈로이드와 비후성 흉터를 효율적이고 안전하게 분류하는 ScaFE 프레임워크를 설명합니다."
date: 2026-07-16 09:00:00 +0900
categories:
  - Paper Reviews
  - medical-ai
paper_authors:
  - Ruman Wang
  - Hangting Ye
paper_url: "https://arxiv.org/abs/2607.28538v1"
tags:
  - Paper Review
  - Medical AI
  - LLM
  - Feature Engineering
  - Data Efficiency
toc: true
mermaid: false
---

## 3줄 요약
1. 원본 환자 사진을 외부 호스팅 VLM/LLM에 직접 전송하지 않고, LLM이 의학 지식을 기반으로 실행 가능한 이미지 피처 추출 프로그램(Python 코드)을 작성하도록 설계했습니다.
2. 로컬 보안 환경에서 코드를 실행해 생성된 구조화 피처와 피처별 SHAP 기여도 요약만 LLM에 전달하여 추출 프로그램을 자율적으로 반복 개선(Iterative Refinement)합니다.
3. 3개 병원의 600장 흉터 이미지 대상 Leave-One-Site-Out 평가에서 BiomedCLIP 대비 10.0%p 높은 81.0% Balanced Accuracy를 달성했으며, 데이터의 10%만 사용할 때도 강력한 효율성을 입증했습니다.

---

## 논문이 해결하는 문제
병적 흉터(Pathological Scar)인 **켈로이드(Keloid)**와 **비후성 흉터(Hypertrophic Scar)**를 임상 사진만으로 정밀하게 구분하는 것은 적절한 치료 방침(주사, 수술, 방사선 치료 등)을 결정하기 위해 필수적입니다. 그러나 이 문제를 컴퓨터 비전 모델로 해결하려면 세 가지 큰 장벽에 직면합니다.

- **전문가 라벨링 데이터 부족**: 숙련된 피부과/성형외과 전문의의 정확한 라벨링을 거친 의료 사진 데이터셋의 규모가 매우 제한적입니다.
- **병원 간 높은 수집 변동성(Cross-Site Variation)**: 촬영 조명, 카메라 기종, 촬영 거리, 환자 피부색 등 병원별 외부 요인의 차이가 심해 모델의 일반화가 어렵습니다.
- **엄격한 데이터 거버넌스 및 개인정보 보호**: 환자의 생체 정보를 담은 임상 사진을 외부 Cloud/API 형태의 Vision-Language Model(VLM, 예: GPT-4V)에 직접 전송하는 것은 HIPAA, GDPR 등 로컬 의료 데이터 보호 규정과 상충됩니다.

---

## 기존 방법의 한계
1. **End-to-End 딥러닝 (CNN / Vision Transformer)**
   - 대규모 데이터 학습에 의존하기 때문에 데이터가 적은 경우 과적합(Overfitting)이 발생합니다.
   - 학습 데이터가 수집된 병원과 다른 타 병원(Out-of-Distribution) 데이터에 적용했을 때 일반화 성능이 급격히 저하됩니다.
2. **Hosted VLM (비전-언어 모델) 직접 추론**
   - 원본 사진을 외부 서버로 송신해야 하므로 데이터 거버넌스 및 환자 프라이버시 이슈를 유발합니다.
   - VLM의 추론 과정은 비결정론적(Non-deterministic)이며 "블랙박스" 형태로 작동하여 진단 근거를 임상적으로 검증하거나 감사(Audit)하기 어렵습니다.
3. **수동 특성 공학 (Manual Feature Engineering)**
   - 도메인 전문가와 컴퓨터 비전 엔지니어가 직접 규칙 기반 알고리즘을 작성하려면 막대한 시간과 비용이 소요됩니다.

---

## 핵심 기여
- **Zero Raw-Data Transfer 아키텍처**: 원본 사진을 로컬 보안 환경 내에 격리하고, LLM은 오직 의학 문헌 검색과 '파이썬 코드 형태의 피처 프로그램' 합성 역할만 담당하도록 분리했습니다.
- **SHAP 기반의 반복적 코드 개선 (Iterative Feature Program Repair)**: 로컬 실행 결과 발생하는 정적/동적 오류와 Feature-level SHAP 중요도 수치만 피드백으로 수집하여 LLM이 실행 가능성과 예측 성능이 우수한 피처 추출 함수를 스스로 정제하도록 구성했습니다.
- **높은 데이터 효율성 및 병원 간 일반화**: 10%의 소량 데이터만으로도 72.0%의 Balanced Accuracy를 보였으며, 3개 병원 간 교차 검증(Leave-One-Site-Out, LOSO)에서 기존 SOTA 비전-언어 파운데이션 모델(BiomedCLIP)을 크게 앞섰습니다.

---

## 제안 방법과 주요 수식

ScaFE(Scar Feature Engineering)의 동작 프로세스는 크게 **(1) 임상 지식 수집 및 프로그램 합성**, **(2) 로컬 실행 및 피처 행렬 구축**, **(3) SHAP 피드백 기반 피처 개선 루프**, **(4) 경량 분류기 학습**으로 구분됩니다.

```
+-------------------------------------------------------------------------+
| [Cloud / External LLM Environment]                                      |
|  1. Web Search & Clinical Evidence Retrieval                            |
|  2. Synthesize/Repair Executable Python Feature Programs (P_m)          |
+-------------------------------------------------------------------------+
                                 |  ^
          Generated Code (P_m)   |  | Aggregated Validation Stats &
                                 v  | SHAP Summaries (No Images)
+-------------------------------------------------------------------------+
| [Local Secure Environment]                                              |
|  3. Execute Feature Programs P_m on Local Images X_i                    |
|  4. Construct Feature Matrix F in R^{N x M}                             |
|  5. Train Random Forest Classifier g_\theta                             |
|  6. Calculate Feature-level SHAP Values \bar{\phi}_m                    |
+-------------------------------------------------------------------------+
```

### 1. 임상 지식 기반 프로그램 합성 (Clinical Feature Program Synthesis)
웹 검색 기능이 활성화된 LLM은 흉터 진단에 필요한 시각적 특성(경계 불규칙성, 색상 불균일성, 높이/홍반 프록시, 텍스처 등)에 대한 임상 지식을 수집합니다. 이후 이를 로컬 영상 처리 라이브러리(OpenCV, Scikit-Image, SciPy 등)를 사용하는 둔감형(Deterministic) 파이썬 함수 $P_m$으로 작성합니다.

$$ P_m \sim \text{LLM}(\text{Prompt}_{\text{evidence}}, \mathcal{D}_{\text{spec}}) $$

여기서 $\mathcal{D}_{\text{spec}}$은 함수 입출력 타입 및 보안 샌드박스 제약 조건 사양입니다.

### 2. 로컬 실행 및 특성 행렬(Feature Matrix) 추출
로컬 격리 환경에서 총 $M$개의 피처 프로그램 $\mathcal{P} = \{P_1, P_2, \dots, P_M\}$을 환자 이미지 $\mathbf{X}_i \in \mathcal{X}_{\text{local}}$ ($i=1, \dots, N$)에 적용합니다. 각 프로그램은 스칼라 형태의 시각적 특성값을 반환합니다.

$$ f_{i, m} = P_m(\mathbf{X}_i) $$

이를 통해 전체 로컬 데이터셋에 대해 다음과 같은 $N \times M$ 차원의 구조화된 특성 행렬 $\mathbf{F}$를 형성합니다.

$$ \mathbf{F} = \begin{bmatrix} P_1(\mathbf{X}_1) & \dots & P_M(\mathbf{X}_1) \\ \vdots & \ddots & \vdots \\ P_1(\mathbf{X}_N) & \dots & P_M(\mathbf{X}_N) \end{bmatrix} \in \mathbb{R}^{N \times M} $$

추출된 특성 행렬 $\mathbf{F}$와 라벨 $y_i \in \{0, 1\}$ (0: 비후성 흉터, 1: 켈로이드)을 사용하여 경량 앙상블 모델인 Random Forest $g_\theta$를 학습시킵니다.

$$ \hat{y}_i = g_\theta(\mathbf{f}_i), \quad \text{where } \mathbf{f}_i = [f_{i, 1}, f_{i, 2}, \dots, f_{i, M}]^\top $$

### 3. SHAP 요약 기반 피드백 및 자율 디버깅 Loop
로컬 모델 $g_\theta$에서 각 피처 $m$이 최종 분류 결정에 미치는 기여도를 측정하기 위해 Shapley additive explanations (SHAP) 값 $\phi_m$을 계산합니다. 특성 $m$의 평균 절대 SHAP 기여도 $\bar{\phi}_m$은 다음과 같습니다.

$$ \bar{\phi}_m = \frac{1}{N} \sum_{i=1}^N \left| \phi_m(g_\theta, \mathbf{f}_i) \right| $$

이때 Shapley Value 계산식은 다음과 같습니다:

$$ \phi_m(g_\theta, \mathbf{f}_i) = \sum_{S \subseteq \mathcal{M} \setminus \{m\}} \frac{|S|!(|\mathcal{M}| - |S| - 1)!}{|\mathcal{M}|!} \left[ g_\theta(S \cup \{m\}) - g_\theta(S) \right] $$

여기서 $\mathcal{M} = \{1, \dots, M\}$은 전체 특성 집합입니다.

LLM 서버로는 **오직** 피처 실행 성공 여부(Execution Status), 예외 메세지(Stacktrace), 그리고 각 특성의 평균 SHAP 기여도 $\bar{\phi}_m$ 요약 정보만 전달됩니다. LLM은 실행 오류가 발생한 코드($P_m$)를 수정하거나, $\bar{\phi}_m \approx 0$인 중요도가 낮은 피처 프로그램을 폐기하고 임상 지식 기반의 새로운 프로그램으로 대체하는 자율 수정을 반복합니다.

---

## 핵심 구조

```
+-----------------------------------------------------------------------------------+
|                        [ScaFE System Pipeline Architecture]                      |
+-----------------------------------------------------------------------------------+
|                                                                                   |
|  +-----------------------------------------------------------------------------+  |
|  |                     [EXTERNAL / CLOUD] LLM Agent Zone                       |  |
|  |  +---------------------------+       +-----------------------------------+  |  |
|  |  | Medical Literature Search | ----> | Feature Program Generator (Python)|  |  |
|  |  +---------------------------+       +-----------------------------------+  |  |
|  +-------------------------------------------------|---------------------------+  |
|                                                    | Code Deployment (P_m)        |
|                                                    v                              |
|  +-----------------------------------------------------------------------------+  |
|  |                     [LOCAL SECURE ENVIRONMENT]                              |  |
|  |  +-----------------------+      +----------------------------------------+  |  |
|  |  | Protected Image DB    | ---> | Restricted Python Sandbox Execution    |  |  |
|  |  | (Keloid / Hypertrophic)     | Extract Features: f_{i,m} = P_m(X_i)  |  |  |
|  |  +-----------------------+      +----------------------------------------+  |  |
|  |                                                     |                          |  |
|  |                                                     v                          |  |
|  |                                 +----------------------------------------+  |  |
|  |                                 | Feature Matrix F (N x M)               |  |  |
|  |                                 +----------------------------------------+  |  |
|  |                                                     |                          |  |
|  |                                                     v                          |  |
|  |                                 +----------------------------------------+  |  |
|  |                                 | Lightweight Classifier (Random Forest) |  |  |
|  |                                 +----------------------------------------+  |  |
|  |                                                     |                          |  |
|  |                                                     v                          |  |
|  |                                 +----------------------------------------+  |  |
|  |                                 | Local SHAP Explainer Engine            |  |  |
|  |                                 +----------------------------------------+  |  |
|  +-------------------------------------------------|---------------------------+  |
|                                                    |                              |
|                                                    | Aggregated SHAP Values &     |
|                                                    | Execution Status ONLY        |
|                                                    v (NO Patients' Images)        |
|  +-----------------------------------------------------------------------------+  |
|  |                     [ITERATIVE REFINEMENT LOOP]                             |  |
|  |  LLM analyzes error trace / low SHAP features and updates feature programs. |  |
|  +-----------------------------------------------------------------------------+  |
+-----------------------------------------------------------------------------------+
```

> **구조 설명**: 
> ScaFE 아키텍처는 크게 외부 Cloud 영역(LLM Agent Zone)과 로컬 보안 환경(Local Secure Environment)으로 명확히 구분되어 있습니다.
> 1. **외부 LLM 영역**: 의학 문헌 검색을 통해 흉터 분류에 필요한 임상적 특징(예: 비후성 경계 vs. 켈로이드 침윤 경계 등)을 식별하고, OpenCV 및 Scikit-Image 라이브러리로 작성된 실행 가능한 파이썬 코드($P_m$)를 생성합니다.
> 2. **로컬 보안 영역**: 전달받은 파이썬 피처 프로그램을 원본 환자 사진이 저장된 local sandbox에서 실행시킵니다. 이미지로부터 스칼라 특성값들을 추출해 $N \times M$ 차원의 특성 행렬 $\mathbf{F}$를 구성하고, 이를 경량 Random Forest 모델로 학습시킵니다.
> 3. **반복 정제 루프**: 학습된 Random Forest 모델의 Feature-level SHAP 값과 코드 실행 통계만 추출하여 외부 LLM으로 피드백을 전달합니다. 환자의 사진이나 개별 데이터 정보는 전혀 외부로 유출되지 않으며, LLM은 이 수치적 피드백을 활용해 특성 추출 알고리즘의 오류를 바로잡고 중요한 특성 위주로 프로그램을 고도화합니다.

---

## 실험 설정과 결과

### 1. 실험 환경 및 데이터셋
- **데이터 구성**: 3개 의료 기관(Hospital A, B, C)에서 수집한 총 600장의 임상 흉터 사진.
- **평가 방식**: **Leave-One-Site-Out (LOSO)** 교차 검증 (2개 병원 데이터로 프로그램 정제 및 학습 후, 미지의 1개 병원 데이터로 성능 테스트).
- **주요 평가 지표**: Site-Macro Balanced Accuracy, Executable Program Rate, Clinical Evidence Verification Rate.

### 2. 주요 실험 결과

| 모델 (Model) | 데이터 활용량 (Training Data) | Site-Macro Balanced Accuracy (%) | 비고 |
| :--- | :---: | :---: | :--- |
| ResNet-50 (Scratch/Fine-tuned) | 100% | 62.4% | 병원 간 도메인 이탈에 매우 취약 |
| BiomedCLIP (Zero-shot) | 0% (Pre-trained) | 68.5% | 의학 도메인 파운데이션 모델 |
| BiomedCLIP (Fine-tuned) | 100% | 71.0% | 데이터 부족으로 폭넓은 성능 향상 한계 |
| **ScaFE (Ours)** | **100%** | **81.0%** | **BiomedCLIP 대비 +10.0%p 우수** |
| **ScaFE (Ours)** | **10%** | **72.0%** | **10% 데이터만으로도 SOTA fine-tuned 모델 능가** |

### 3. Iterative Refinement 효율성 및 코드 검증
- **실행 가능 프로그램 비율 (Executable Rate)**: 초기 1회차 생성 시 66.7%에 불과했으나, SHAP/Trace 피드백 루프를 거치며 3차 반복 후 **95.0%**로 대폭 상승.
- **임상적 유효성 (Clinical Evidence Verification)**: 생성된 최종 파이썬 특성 프로그램의 **91.7%**가 실제 의학 문헌 및 피부과 전문의의 진단 가이드라인 지표와 직접적으로 부합함을 확인.

---

## 잘한 점
- **강력한 프라이버시 보존 설계**: 대형언어모델/VLM을 활용하면서도 원본 의료 이미지 유출 위험을 제로(Zero)화하여 실제 병원 데이터 거버넌스 규정을 완벽히 만족했습니다.
- **높은 데이터 효율성**: 단 10%의 로컬 데이터만으로 기존 대형 파운데이션 모델의 파인튜닝 성능을 뛰어넘는 뛰어난 극소량 데이터 적응력을 보였습니다.
- **투명성 및 감사 가능성 (Auditability)**: 블랙박스 신경망 대신 LLM이 생성한 파이썬 코드 및 Random Forest의 SHAP 기여도를 제시하므로, 의사가 진단 근거를 수학적/코드 레벨에서 직접 검증할 수 있습니다.

---

## 한계와 의문점
- **고차원 텍스처/3차원 정보 포착 한계**: 전통적 컴퓨터 비전 함수(OpenCV 코드) 기반이므로, 흉터의 미세한 3차원 입체감이나 복잡한 비선형적 질감 특성을 표현하는 데는 엔드투엔드 딥러닝 피처보다 한계가 존재할 수 있습니다.
- **파이썬 코드 실행의 안전성 이슈**: LLM이 작성한 파이썬 코드를 로컬 환경에서 실행할 때 발생할 수 있는 보안적 허점(예: 임의의 시스템 명령 실행 위험)을 막기 위해 철저히 격리된 샌드박스(Sandbox) 환경 구축이 전제되어야 합니다.
- **타 도메인 확장성**: 피부 질환 이외에 조직 병리(Pathology) 사진이나 CT/MRI 등 다중 슬라이스 3D 영상 데이터로도 동일한 수준의 코드 생성이 가능할지 추가 검증이 필요합니다.

---

## 실무 적용 가능성
- **의료 AI 제품화 및 온디바이스 적용**: 추론 단계에서는 LLM을 호출할 필요 없이, 로컬에 저장된 파이썬 피처 추출 함수와 가벼운 Random Forest 파일(.joblib)만 실행되므로 low-power 모바일/태블릿 장비 및 에지 디바이스에서도 즉각 동작이 가능합니다.
- **개인정보보호 규제 기관 도입**: HIPAA, GDPR 규정이 엄격한 다기관 공동 연구 프로젝트에서 병원 간 데이터 공유 없이 피처 프로그램 및 통계치만 교환하는 방식으로 신속하게 확장할 수 있습니다.

---

## 관련 연구와 연결점
- **Program Synthesis for Vision (VisProg, ViperGPT)**: 코드 작성을 통해 비전 문제를 해결하는 대반열의 연구 흐름을 의료 영상 분류 및 데이터 프라이버시 영역으로 확장 적용했습니다.
- **Interpretable Machine Learning**: SHAP 기여도를 단순히 모델 설명용으로 쓰지 않고, 코드 정제 루프(Code Refinement Loop)의 피드백 신호로 재활용했다는 점에서 자율형 AI 에이전트 연구와 연결됩니다.

---

## 원문 정보
- **Title**: ScaFE: Data-Efficient Scar Classification with LLM-Generated Clinical Feature Programs
- **Authors**: Ruman Wang, Hangting Ye
- **Venue/Repository**: arXiv
- **Published**: 2026
- **URL**: [https://arxiv.org/abs/2607.28538v1](https://arxiv.org/abs/2607.28538v1)

> 이 글은 자동 생성된 초안을 바탕으로 작성되며, 공개 전에 저자·수식·수치·출처를 직접 검수합니다.
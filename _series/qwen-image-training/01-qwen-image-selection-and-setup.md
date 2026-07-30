---
title: "Qwen-Image-2512 학습기 (1) - 모델 선정 배경 및 개발 환경 구축"
description: "멀티모달 프로젝트의 베이스 모델 선정 기준과 Qwen-Image 학습 환경 구축 과정을 정리합니다."
author: 이유진
date: 2026-07-07
category: series
subcategory: multimodal
series: qwen-image-training
series_order: 1
tags:
  - Multimodal
  - Qwen-Image
  - Fine-tuning
layout: post
mermaid: true
---

# Qwen-Image-2512 학습기 (1) - 모델 선정 배경 및 개발 환경 구축

새로운 이미지-텍스트 멀티모달 프로젝트를 준비하며, 오픈소스 VLM(Vision-Language Model) 중 가장 적합한 베이스 모델을 탐색하고 최종적으로 **Qwen-Image-2512** 모델을 선정하였다. 본 포스트에서는 타 모델과의 비교를 통한 선정 배경과, 본격적인 파인튜닝을 위한 개발 환경 구축 과정을 정리한다.

---

## 1. Qwen-Image-2512 선정 배경

멀티모달 프로젝트를 설계할 때 가장 핵심적인 요구사항은 **1) 고해상도 이미지 내의 미세 텍스트 인식(OCR) 성능**, **2) 한국어와 영어의 균형 있는 처리 능력**, 그리고 **3) 사내 GPU 인프라 내에서 학습 및 서빙이 가능한 효율성**이다.

시장조사 과정에서 후보군에 올랐던 대표적인 VLM들과의 비교 분석은 다음과 같다.

### VLM 모델 비교 분석

| 평가 항목 | LLaVA-NeXT | InternVL2 | Qwen2-VL / Qwen-Image-2512 |
| :--- | :--- | :--- | :--- |
| **OCR / 미세 텍스트** | 보통 (격자 분할의 한계) | 우수 | **최우수 (Dynamic Resolution)** |
| **다국어 (한국어) 지원** | 미흡 (영어 중심) | 보통 | **우수 (중국어/영어/한국어 코퍼스)** |
| **비전 토큰 효율성** | 낮음 (고정 패치) | 보통 | **높음 (유연한 패치 조절)** |
| **오픈소스 생태계** | 넓음 (활발함) | 보통 | **넓음 (Hugging Face / vLLM 연동 우수)** |

### Qwen-Image-2512를 선정한 3가지 결정적 요인

#### ① 동적 해상도 지원 (Naive Dynamic Resolution)
기존 LLaVA 등은 이미지를 강제로 고정된 격자 크기(예: $$336 \times 336$$)로 분할하여 미세한 텍스트나 표가 깨지는 문제가 자주 발생한다. 반면 Qwen 모델군은 원본 이미지의 종횡비를 보존하며 동적으로 토큰을 할당한다. 이미지 해상도($$H \times W$$)와 비전 인코더의 패치 크기($$P \times P$$)의 관계식은 다음과 같다.

$$ N_{\text{tokens}} = \lceil \frac{H}{P} \rceil \times \lceil \frac{W}{P} \rceil + N_{\text{learned\_query}} $$

이 방식을 통해 글자가 뭉개지는 현상을 방지하며, 복잡한 문서나 데이터 시트 분석에서 가장 압도적인 성능을 보인다고 한다.

#### ② 뛰어난 가성비와 경량화 가능성 (LoRA 친화도)
InternVL2 등 초대형 멀티모달 모델은 성능은 뛰어나지만 파인튜닝에 수많은 GPU 장비가 필요하다. Qwen-Image-2512 모델은 성능 대비 파라미터 구성이 효율적이며, `PEFT(LoRA/QLoRA)`와 `DeepSpeed`를 적용해 사내의 한정된 자원(VRAM 24GB~80GB대 장비)에서도 원활하게 풀-파이닝 혹은 어댑터 학습이 가능하다고 알려져 있다.

#### ③ 다국어 처리 능력 및 한국어 학습 과제
* Qwen2.5-VL 기반 백본을 공유하여 한국어가 포함된 이미지 이해 및 질의응답(VQA) 수준은 우수함.
* 그러나 이미지 내에 한글 텍스트를 직접 렌더링(글자 인쇄)하는 생성 태스크의 경우, 한글 학습 데이터 부족으로 인해 글자 깨짐 및 어색한 서체 표현 문제가 고질적으로 발생함.
* **본 프로젝트의 주 목표**: 이처럼 한글 렌더링이 깨지는 한계를 극복하기 위해, 베이스라인인 Qwen-Image-2512에 양질의 한글 텍스트 렌더링 데이터셋을 투입하여 커스텀 파인튜닝을 진행하고자 함.

---

## 2. 모델 선정을 위한 의사결정 흐름 (Decision Flow)

아래 다이어그램은 프로젝트 요구사항에 맞춰 최적의 모델을 선택했던 논리 구조를 나타낸다.

```mermaid
graph TD
    Start([프로젝트 VLM 후보군 탐색]) --> Q1{미세 OCR 및 표 인식이 중요한가?}
    Q1 -->|No| LLaVA[LLaVA-NeXT 고려]
    Q1 -->|Yes| Q2{단일 GPU 자원에서 파인튜닝이 가능한가?}
    Q2 -->|No (대규모 자원)| Intern[InternVL2 26B+ 고려]
    Q2 -->|Yes (VRAM 효율 중시)| Q3{다국어 및 한국어 자연어 처리가 우수한가?}
    Q3 -->|No| OtherVLM[기타 특화 모델 검토]
    Q3 -->|Yes| Qwen[최종 선정: Qwen-Image-2512]
```

---

## 3. 개발 환경 구축 (Environment Setup)

파인튜닝을 안전하게 진행하기 위해 standard PyTorch와 DeepSpeed 환경을 구축한다.

### 1) 가상환경 생성 및 PyTorch 설치
가상환경을 생성하고, CUDA 12.1 버전용 PyTorch를 설치한다.

```bash
# conda 환경 생성 및 활성화
conda create -n qwen_train python=3.10 -y
conda activate qwen_train

# PyTorch 설치 (CUDA 12.1 매칭)
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121
```

### 2) 필수 라이브러리 및 DeepSpeed 설치
멀티모달 모델 학습 및 어댑터 학습을 위한 필수 패키지를 설치한다.

```bash
# Transformers 및 PEFT 패키지 설치
pip install transformers accelerate peft modelscope sentencepiece

# 웹 데모 구성을 위한 추가 라이브러리
pip install gradio decord

# 분산 학습용 DeepSpeed 설치
pip install deepspeed
```

---

## 4. 사전 학습 모델(Pre-trained) 추론 맛보기

환경이 잘 구축되었는지 확인하기 위해 오픈소스 표준 코드를 활용하여 이미지를 입력하고 설명을 생성하는 기본 추론 테스트를 수행한다.

```python
import torch
from transformers import AutoProcessor, AutoModelForVision2Seq

device = "cuda" if torch.cuda.is_available() else "cpu"
model_id = "Qwen/Qwen-VL-Chat"

# 모델 및 프로세서 로드
processor = AutoProcessor.from_pretrained(model_id, trust_remote_code=True)
model = AutoModelForVision2Seq.from_pretrained(
    model_id, 
    torch_dtype=torch.float16 if device == "cuda" else torch.float32,
    device_map="auto",
    trust_remote_code=True
)

# 이미지 및 쿼리 준비
image_url = "https://images.cocodataset.org/val2017/000000039769.jpg"
query = "Describe this image in Korean."

# 입력을 위한 전처리
messages = [
    {"role": "user", "content": [
        {"type": "image", "image": image_url},
        {"type": "text", "text": query}
    ]}
]
text = processor.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
image_inputs, video_inputs = processor.image_processor(image_url, return_tensors="pt"), None

inputs = processor(
    text=[text],
    images=image_inputs,
    padding=True,
    return_tensors="pt"
).to(device)

# 생성
with torch.no_grad():
    generated_ids = model.generate(**inputs, max_new_tokens=100)
    generated_ids_trimmed = [
        out_ids[len(in_ids):] for in_ids, out_ids in zip(inputs.input_ids, generated_ids)
    ]
    output_text = processor.batch_decode(
        generated_ids_trimmed, skip_special_tokens=True, clean_up_tokenization_spaces=False
    )

print("모델 답변:", output_text[0])
```

---

## 5. 다음 단계 예고
개발 환경 구축과 모델 로드 검증을 마쳤다. 다음 2편에서는 **공개 이미지 데이터셋을 Qwen-Image 모델의 학습용 멀티모달 포맷으로 파싱하고 전처리하는 과정**을 자세히 다룰 예정이다.

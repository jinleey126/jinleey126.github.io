---
title: "TokTier: Exact Stateful Tokenization for Agentic LLM Serving"
description: "에이전틱 LLM 서빙 환경에서 상태 기반 증분 토큰화와 GPU 병렬 BPE 알고리즘을 결합하여, 기존 완전 토큰화 결과와의 100% 일치성을 보장하면서 TTFT 단축 및 처리량을 극대화하는 TokTier 기술 분석"
date: 2026-07-30 09:00:00 +0900
categories:
  - Paper Reviews
  - llm-serving
paper_authors:
  - Zhenyu Zhang
  - Zhichao Cao
paper_url: "https://arxiv.org/abs/2607.29678"
tags:
  - Paper Review
  - LLM Serving
  - Tokenization
  - BPE
  - Agentic LLM
toc: true
mermaid: false
---

## 3줄 요약
- **문제 정의**: 에이전틱(Agentic) LLM 서빙에서는 Prompt KV Cache를 통해 가중치 연산을 재사용함에도 불구하고, 프론트엔드가 매 요청마다 전체 트랜스크립트를 다시 토큰화(Re-tokenization)하여 TTFT(Time To First Token)의 최대 64%가 토큰화 오버헤드로 소모됨.
- **핵심 방법**: 이전 호출의 토큰화 상태를 유지하는 상태 기반 서비스(Stateful Service) 구조인 **TokTier**를 제안하여, 세션 연속 요청 시 경계 안정성 검증(Stable Boundary Check) 기반 증분 복구(Incremental Repair)를 수행하고, 세션 신규 생성 시 GPU 기반 병렬 전처리 및 BPE 알고리즘을 적용함.
- **주요 결과**: 17개 토크나이저 패밀리와 12.4TB 실제 말뭉치 검증에서 오차 0%(Zero Divergence)를 달성하며, 1M 캐릭터 기준 증분 복구 0.5~1.1ms(Gigatoken 대비 2.1배), GPU 토큰화 0.87ms(HuggingFace 대비 최대 491배)의 속도 향상과 함께 vLLM 연동 시 TTFT P99를 23% 개선함.

---

## 논문이 해결하는 문제

대화형 LLM 및 코딩 에이전트(Coding Agent) 서비스는 도구 실행 결과(Tool execution results)가 발생할 때마다 이전 대화 기록 전체(Full Transcript)를 백엔드 LLM 엔진으로 재전송하는 구조를 가집니다. 백엔드 서빙 엔진(예: vLLM, SGLang)은 Prompt KV Caching 기술을 활용하여 접두사(Prefix)에 대한 Key-Value 텐서 재계산을 피하지만, 프론트엔드 서빙 계층은 매 호출 시마다 전체 텍스트 룰에 대한 **전체 재토큰화(Full Re-tokenization)**를 수행합니다.

실제 Agent 트래픽 분석(153,951건 분석)에 따르면:
1. 중앙값(Median) 요청은 약 1.4K 자의 소규모 텍스트만 추가(Append)합니다.
2. 수백만 자의 신규 세션을 생성하거나 재구성하는 비율은 전체의 1.0~3.6%에 불과합니다.
3. Fleet 차원의 Prompt KV Cache 히트율이 94.1%에 달할 때, 전체 첫 토큰 생성 시간(TTFT)의 **최대 64%**가 CPU 기반 토큰화 과정에서 소비되는 병목 현상이 발생합니다.

---

## 기존 방법의 한계

1. **BPE 토큰 경계 변동성 (Token Boundary Shifts)**:
   Byte-Pair Encoding(BPE) 방식은 텍스트 끝에 단 몇 글자만 추가되더라도 기존 텍스트의 끝부분 토큰 경계가 결합 규칙(Merge Rules)에 따라 소급 변경될 수 있습니다. 단순 텍스트 이어붙이기(Concatenation) 방식은 참조 토크나이저(Reference Tokenizer)의 결과와 달라지는 토큰 불일치(Divergence)를 유발합니다.
2. **기존 Caching 기반 토크나이저의 한계 (예: Gigatoken)**:
   기존의 토큰화 캐싱 기법은 접두사 해시 기반 캐싱을 사용하지만, 텍스트 길이가 수백만 자로 늘어날 경우 캐시 룩업 및 경계 재계산 과정에서 메모리 오버헤드가 급증하며, 최대로 prewarm된 상태에서도 1M 자 기준 최적화 성능이 제한적입니다.
3. **CPU 병목 및 병렬화 실패**:
   HuggingFace Tokenizers나 Tiktoken 등 기존 구현은 기본적으로 CPU 단일/다중 스레딩에 의존하며, 정규표현식(Regex) 기반 Pre-tokenization 패시지가 CPU 코어 자원을 크게 점유하여 초당 처리량(RPS)의 한계를 결정짓습니다.

---

## 핵심 기여

1. **Exact Stateful Tokenization 보장**:
   참조 토크나이저(HuggingFace/Tiktoken)의 전체 토큰화 결과와 **100% 동일한 Token ID Sequence**를 보장하는 수학적 경계 안정성 검증 규칙 및 접합(Splicing) 메커니즘을 설계했습니다.
2. **2-Tier 토크나이저 파이프라인 (Incremental Repair & GPU Full BPE)**:
   - **Incremental Repair (Tier 1)**: 세션 연장 요청 시 추가된 텍스트 주변의 최소 윈도우만 재토큰화한 후 안전한 지점에서 Splice를 수행하여 0.5~1.1ms 이내에 토큰화 완료.
   - **GPU Parallel Tokenization (Tier 2)**: 신규 세션 호출 시 GPT 계열 Regex 전처리를 Run-local 규칙으로 분해하고, GPU 상에서 병렬 Pre-tokenization 및 BPE를 0.87ms(1M 자 기준) 만에 수행.
3. **엄격한 프로덕션 수준 검증**:
   17개 토크나이저 패밀리, 150억 회의 Split 검증, 12.4TB 실데이터 텍스트, 93,000개 이상의 Agent Step 리플레이 검증을 거쳐 Divergence 0을 증명하고 프로덕션 환경 vLLM 서빙 엔진에 성공적으로 통합했습니다.

---

## 제안 방법과 주요 수식

TokTier의 핵심 알고리즘은 **경계 안정성 검증 기반 증분 복구(Incremental Repair)**와 **GPU 기반 병렬 전처리 및 BPE 연산**으로 구성됩니다.

```
[Incoming Request]
       │
       ▼
Is Session Active & Cache Available?
       ├── Yes ──────────────────────────────────────────┐
       │                                                 │
       No                                                ▼
       │                                       [Tier 1: Incremental Repair]
       ▼                                       1. Extract Left Context Window L_left
[Tier 2: GPU Full Tokenization]                2. Re-tokenize Window (W = T_prev[-L_left:] + ΔT)
1. Regex Pre-tokenization (FST on GPU)         3. Perform Stable Boundary Check
2. Parallel BPE Pair Rank Merging                         │
3. Output Token Sequence                                  ├── Success ──> Splicing & Emit
       │                                                  │
       │                                                  └── Failure ──> Expand Window or Fallback
       └─────────────────────────┬────────────────────────┘
                                 ▼
                    [Output Token Sequence]
                                 │
                                 ▼ (Asynchronous)
                     [Sampled Shadow Verifier]
```

### 1. 상태 기반 증분 복구 및 경계 안정성 조건 (Stable Boundary Condition)

기존 텍스트 $T_{prev}$와 기존 토큰 열 $S_{prev} = \text{Tok}(T_{prev})$, 새로 추가된 텍스트 $\Delta T$가 주어졌을 때, 전체 토큰화 결과 $\text{Tok}(T_{prev} \mathbin{\parallel} \Delta T)$는 $T_{prev}$의 특정 안정 경계(Stable Boundary) 지점 전까지의 토큰 열과 완벽히 일치합니다.

텍스트 분할 지점 $p$가 **안정적(Stable)**이라는 것은 다음을 만족하는 경우입니다:

$$ \text{Tok}(T_1 \mathbin{\parallel} T_2) = \text{Tok}(T_1) \mathbin{\parallel} \text{Tok}(T_2) $$

TokTier는 $T_{prev}$의 끝부분에서 길이 $L_{left}$만큼의 좌측 컨텍스트 윈도우를 잘라내어 윈도우 텍스트 $W = T_{prev}[|T_{prev}| - L_{left}:] \mathbin{\parallel} \Delta T$를 구성합니다. 윈도우를 토큰화한 결과 $S_W = \text{Tok}(W)$에 대해, Original $S_{prev}$와의 일치성을 검증합니다.

접합(Splicing)이 유효하기 위한 안정 경계 매칭 조건식은 다음과 같습니다:

$$ \exists \, i, j \quad \text{s.t.} \quad T_{prev}[:p_i] \equiv W[:q_j] \quad \text{and} \quad S_{prev}[:i] \equiv S_W[:j] $$

이 조건이 충족되면, 소급 변경이 미치지 않는 안전 지점 $i$가 확인된 것이므로 최종 토큰 시퀀스는 다음과 같이 결합됩니다:

$$ S_{new} = S_{prev}[:i] \mathbin{\parallel} S_W[j:] $$

만약 안정 경계 검증에 실패할 경우, 윈도우 크기 $L_{left}$를 확장하거나 Tier 2(Full Tokenization)로 폴백(Fallback)합니다.

### 2. GPU 병렬 Pre-tokenization 및 BPE 연산

신규 요청에 대해 GPU를 활용한 병렬 토큰화를 수행하기 위해 정규표현식 분할을 유한 상태 트랜스듀서(FST) 및 Run-local 규칙으로 전환합니다.

BPE의 병렬 병합 단계에서는 각 토큰 쌍 $(t_k, t_{k+1})$의 우측 결합 순위(Rank)를 어휘집 테이블 $\text{VocabTable}$에서 동시 조회합니다:

$$ r_k = \text{VocabTable}[t_k][t_{k+1}] $$

전체 토큰 시퀀스에서 최소 결합 순위를 갖는 최우선 병합 대상 순위 $r_{min}$을 구합니다:

$$ r_{min} = \min_k r_k $$

동일한 최우선 순위 $r_{min}$을 가지며 서로 겹치지 않는(Non-overlapping) 모든 인접 토큰 쌍들을 GPU의 멀티스레드가 병렬로 동시에 병합(Parallel Merge)합니다. 이 과정은 $r_{min} = \infty$ (더 이상 병합 가능한 인접 쌍이 없음)가 될 때까지 반복됩니다.

---

## 핵심 구조

> 본 논문 검토 시 제공된 이미지 URL이 없으므로, 논문의 **Figure 1: TokTier System Architecture 및 전체 데이터 흐름도**를 상세히 서술합니다.

TokTier의 시스템 구조도는 크게 **(1) Client/Agent Frontend Interface**, **(2) Stateful Session Registry**, **(3) Tier 1: CPU Incremental Repair Pipeline**, **(4) Tier 2: GPU Parallel Tokenization Engine**, **(5) Background Sampled Shadow Verifier**의 5가지 핵심 모듈로 구성됩니다.

1. **Stateful Session Registry**:
   각 에이전트 세션의 식별자(Session ID)와 해당 세션의 이전 토큰화 결과 메타데이터($S_{prev}$, 텍스트 오프셋 마핑 정보)를 경량 메모리 저장소에 유지합니다.
2. **Tier 1: Incremental Repair Pipeline (CPU Fast Path)**:
   - **Context Slicing Module**: 입력 요청이 기존 세션의 연속일 경우, 이전 입력 $T_{prev}$의 접미사 $L_{left}$와 추가 텍스트 $\Delta T$를 잘라내어 최소 슬라이스 윈도우 $W$를 생성합니다.
   - **Stable Boundary Checker**: 슬라이스 윈도우의 토큰화 결과와 기존 세션 $S_{prev}$의 토큰 경계가 일치하는지 $O(1)$ 정밀 검증을 수행합니다.
   - **Splicer**: 경계 검증 성공 시, 기존 토큰의 안정 영역 $S_{prev}[:i]$와 새로 생성된 $S_W[j:]$를 인메모리 연산으로 단순 배열 결합하여 즉시 반환합니다.
3. **Tier 2: GPU Parallel Tokenization Engine (GPU Fast Path)**:
   - **Run-local Regex Engine**: GPT 계열 토크나이저의 전처리 정규식을 GPU 스레드 블록 단위로 병렬 실행할 수 있는 FST 규칙으로 실행하여 단어/문자 단위 스트림으로 분할합니다.
   - **GPU Parallel BPE Kernel**: 분할된 스트림에 대해 Shared Memory 기반의 Pair Rank Lookup 및 Parallel Non-overlapping Merge 커널을 수행하여 대용량 텍스트(예: 1M 자)를 밀리초 미만 단위로 완벽히 토큰화합니다.
4. **Background Sampled Shadow Verifier**:
   프로덕션 라우팅에 영향을 주지 않는 비동기 백그라운드 프로세스로, 라이브 트래픽의 일부분을 샘플링하여 오프라인 표준 HuggingFace/Tiktoken 토크나이저 연산 결과와 TokTier 반환 결과를 1:1 비교 검증하여 Divergence 발생 여부를 지속 모니터링합니다.

---

## 실험 설정과 결과

### 1. 실험 환경 및 비교 대상
- **Dataset / Workload**: 153,951개 라이브 에이전트 호출 데이터, 12.4TB 크기의 실세계 텍스트 코퍼스, 93,000+ Replayed Agent Steps.
- **Tokenizer Families**: Llama, Qwen, GPT-4(Tiktoken), Mistral 등 총 17개 주요 토크나이저 패밀리.
- **Baseline**: HuggingFace Fast Tokenizers, Tiktoken, Gigatoken (최신 토큰 캐싱 기반 프론트엔드).
- **LLM Serving Engine**: vLLM과 통합 연동 실험.

### 2. 주요 정량적 성능 지표

| 평가 항목 | 비교 대상 (Baseline) | TokTier 성능 | 성능 향상 폭 |
| :--- | :--- | :--- | :--- |
| **1M 자 Incremental Repair 속도** | Gigatoken (Fully Prewarmed) | **0.5 ~ 1.1 ms** | **2.1배 향상** |
| **1M 자 Full Tokenization 속도** | HuggingFace Tokenizer | **0.87 ms** | **최대 491배 향상** |
| **1M 자 Full Tokenization 속도** | 최신 CPU 병렬 토크나이저 | **0.87 ms** | **23.4배 향상** |
| **vLLM 연동 TTFT Median** | 기존 Stateless Front-end | - | **16% ~ 34% 감소** |
| **vLLM 연동 TTFT P99** | 기존 Stateless Front-end | - | **23% 감소** |
| **50ms P99 SLA 만족 최대 RPS** | 16-Core Stateless Front-end (40 RPS) | **4-Core + 1 GPU (1,821 RPS)** | **45.5배 수용량 증가** |
| **Token Divergence Rate** | Reference 기준 | **0.00% (Zero Divergence)** | **100% Exact Match** |

---

## 잘한 점

1. **결과 정확성(Exactness) 보장**:
   성능을 향상시키면서 토큰화 결과를 근사(Approximate)하지 않고, 참조 토크나이저와 100% 일치하도록 검증 메커니즘을 수학적으로 엄밀하게 구성했습니다.
2. **실제 Agentic 워크로드 특성 고찰**:
   대부분의 에이전트 호출이 소규모 Append 패턴을 보인다는 점에 착안하여, CPU 기반 증분 복구(Tier 1)와 GPU 기반 대용량 토큰화(Tier 2)를 계층화한 계층식 구조가 매우 효율적입니다.
3. **압도적인 엔지니어링 완성도**:
   150억 회의 Split 검증과 12.4TB에 달하는 초대형 데이터셋 검증을 통해 프로덕션 배포가 즉시 가능한 수준의 신뢰성을 입증했습니다.

---

## 한계와 의문점

1. **상태 관리(State Management) 오버헤드 및 복잡성**:
   Stateless한 프론트엔드 구조와 달리 각 세션별 $S_{prev}$ 메타데이터를 서빙 프론트엔드 메모리에 유지해야 하므로, 수십만 개의 동시 활성 세션(Concurrent Sessions)이 존재하는 대규모 분산 환경에서 세션 동기화 및 메모리 관리 복잡도가 증가할 수 있습니다.
2. **GPU 자원 할당의 경제성**:
   Tier 2(Full Tokenization)를 위해 GPU 자원을 별도로 할당하거나 LLM 추론 GPU의 일부 자원을 점유해야 합니다. 트래픽의 96% 이상이 Tier 1(CPU Incremental Repair)에서 처리된다면 극소수의 신규 세션을 위해 GPU를 유지하는 데 따른 비용 대비 효율성 검토가 요구됩니다.
3. **다양한 Pre-tokenizer 규칙 확장성**:
   GPT 계열 외에 정규식 구조가 독특하거나 비표준 전처리 로직을 사용하는 신규 토크나이저 패밀리가 등장할 경우, GPU FST 커널을 개별적으로 최적화해야 하는 구현상의 부담이 존재합니다.

---

## 실무 적용 가능성

- **즉시 적용 가능 분야**:
  vLLM, SGLang, TensorRT-LLM 등을 기반으로 에이전틱 코딩 서비스(예: Claude Code, Cursor, Devin 형태의 서비스)를 구축 중인 대규모 LLM 인프라 팀에 매우 유용합니다.
- **인프라 절감 효과**:
  기존에는 토큰화 병목을 해소하기 위해 프론트엔드 CPU 코어를 과도하게 확장(Scale-out)해야 했으나, TokTier 기법 적용 시 단 4개의 CPU 코어와 1개의 소형 GPU만으로도 기존 16코어 프론트엔드 대비 45배 이상의 RPS를 처리할 수 있어 TCO(총소유비용) 절감 효과가 큽니다.

---

## 관련 연구와 연결점

- **Prompt KV Caching (vLLM, SGLang, RadixAttention)**:
  LLM 추론 백엔드에서의 KV Cache 재사용 기술과 완벽한 짝을 이룹니다. 백엔드가 KV Caching으로 추론 시간을 단축할 때 프론트엔드의 토큰화 병목을 제거함으로써 시스템 전체의 TTFT 단축을 완성합니다.
- **Gigatoken / Fast Tokenizers**:
  기존 캐싱 기반 토크나이저들의 경계 변동성 및 메모리 급증 문제를 Exactness 보장과 GPU Parallel BPE 알고리즘을 통해 극복한 진화된 형태입니다.

---

## 원문 정보

- **Title**: TokTier: Exact Stateful Tokenization for Agentic LLM Serving
- **Authors**: Zhenyu Zhang, Zhichao Cao
- **Venue/Repository**: arXiv:2607.29678v1 [cs.DC / cs.CL]
- **Published**: 2026-07-29 (arXiv)
- **URL**: [https://arxiv.org/abs/2607.29678](https://arxiv.org/abs/2607.29678)

> 이 글은 자동 생성된 초안을 바탕으로 작성되며, 공개 전에 저자·수식·수치·출처를 직접 검수합니다.
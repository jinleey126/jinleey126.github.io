---
title: Research
description: 직접 수행한 AI 연구와 실험 기록
layout: post
order: 2
---

# Research

문제 정의, 가설, 실험 방법, 결과와 한계를 직접 검증한 연구 기록입니다.

{% assign documents = site.research | sort: "date" | reverse %}
{% for document in documents %}
- **{{ document.date | date: "%Y-%m-%d" }}** · [{{ document.title }}]({{ document.url | relative_url }})  
  {{ document.description | default: document.excerpt | strip_html | truncate: 140 }}
{% endfor %}


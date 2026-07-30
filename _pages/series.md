---
title: Learning Series
description: 하나의 기술을 단계별로 탐구하는 학습 연재
layout: post
order: 5
---

# Learning Series

환경 구축부터 내부 구조, 학습, 평가와 서빙까지 하나의 주제를 연속해서 탐구합니다.

{% assign documents = site.series | sort: "date" | reverse %}
{% for document in documents %}
- **{{ document.date | date: "%Y-%m-%d" }}** · [{{ document.title }}]({{ document.url | relative_url }})  
  {{ document.description | default: document.excerpt | strip_html | truncate: 140 }}
{% endfor %}


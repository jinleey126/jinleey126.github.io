---
title: Paper Reviews
description: AI 논문의 핵심 아이디어와 실무 적용 가능성을 분석한 리뷰
layout: post
order: 3
---

# Paper Reviews

논문의 문제 정의, 핵심 방법론, 실험 결과, 한계와 실무 적용 가능성을 분석합니다.

{% assign documents = site.papers | sort: "date" | reverse %}
{% for document in documents %}
- **{{ document.date | date: "%Y-%m-%d" }}** · [{{ document.title }}]({{ document.url | relative_url }})  
  {{ document.description | default: document.excerpt | strip_html | truncate: 140 }}
{% endfor %}


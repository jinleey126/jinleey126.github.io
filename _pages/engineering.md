---
title: Engineering
description: Production AI 시스템 구현과 문제 해결 기록
layout: post
order: 4
---

# Engineering

AI 시스템을 구현하고 운영하며 만난 문제, 원인, 대안과 검증 결과를 기록합니다.

{% assign documents = site.engineering | sort: "date" | reverse %}
{% if documents.size > 0 %}
{% for document in documents %}
- **{{ document.date | date: "%Y-%m-%d" }}** · [{{ document.title }}]({{ document.url | relative_url }})  
  {{ document.description | default: document.excerpt | strip_html | truncate: 140 }}
{% endfor %}
{% else %}
첫 번째 Engineering Note를 준비하고 있습니다.
{% endif %}


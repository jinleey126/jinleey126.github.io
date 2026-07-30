---
title: Archive
description: 기술 블로그 전체 글 목록
layout: post
order: 6
---

# Archive

## Research

{% assign research_docs = site.research | sort: "date" | reverse %}
{% for document in research_docs %}
- {{ document.date | date: "%Y-%m-%d" }} · [{{ document.title }}]({{ document.url | relative_url }})
{% endfor %}

## Paper Reviews

{% assign paper_docs = site.papers | sort: "date" | reverse %}
{% for document in paper_docs %}
- {{ document.date | date: "%Y-%m-%d" }} · [{{ document.title }}]({{ document.url | relative_url }})
{% endfor %}

## Engineering

{% assign engineering_docs = site.engineering | sort: "date" | reverse %}
{% for document in engineering_docs %}
- {{ document.date | date: "%Y-%m-%d" }} · [{{ document.title }}]({{ document.url | relative_url }})
{% endfor %}

## Learning Series

{% assign series_docs = site.series | sort: "date" | reverse %}
{% for document in series_docs %}
- {{ document.date | date: "%Y-%m-%d" }} · [{{ document.title }}]({{ document.url | relative_url }})
{% endfor %}

## Posts

{% for document in site.posts %}
- {{ document.date | date: "%Y-%m-%d" }} · [{{ document.title }}]({{ document.url | relative_url }})
{% endfor %}


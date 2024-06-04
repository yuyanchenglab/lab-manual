---
layout: default
title: Welcome
nav_order: 1
description: "Welcome"
permalink: /
---

# Welcome to the Cheng Molecular Opthalmology lab!

This is the internal website for the Cheng Molecular Opthalmology lab's onboarding and a repository for Standard Operating Procedures (SOP).

Most recent release: Updated basics.

<ul class="list-style-none">
{% for contributor in site.github.contributors %}
  <li class="d-inline-block mr-1">
     <a href="{{ contributor.html_url }}"><img src="{{ contributor.avatar_url }}" width="32" height="32" alt="{{ contributor.login }}"/></a>
  </li>
{% endfor %}
</ul>


This documentation website was created using [Jekyll and Github pages](https://help.github.com/en/github/working-with-github-pages/setting-up-a-github-pages-site-with-jekyll).
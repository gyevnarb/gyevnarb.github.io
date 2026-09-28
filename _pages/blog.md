---
layout: default
title: blog
permalink: /blog/
---

<header class="blog-head">
  <h1>{{ site.blog_name }}</h1>
  <p class="lede">{{ site.blog_description }}</p>
</header>

{% include posts.html full=true %}

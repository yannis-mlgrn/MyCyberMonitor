<template>
    <div class="card w-225 bg-base-100 card-md shadow-sm">
  <div class="card-body">
    <h2 class="card-title blog-title">{{ blog.title }}</h2>
    <p v-html="blog.description"> </p>
    <p> écrit par <strong>{{ blog.author }}</strong></p>
    <div class="justify-end card-actions">
    <a :href="blog.link" class="btn btn-primary">Read More →</a>
    </div>
  </div>
</div>
  </template>
  
  <script setup>

  defineProps({
    blog: Object
  });
  </script>
  
  <style scoped>

  .blog-card {
    background: #fff;
    padding: 1rem;
    border-radius: 0.75rem;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    width: 100%;
    margin-bottom: 1rem;
  }

.blog-title {
    font-family: 'SpecialGothicExpandedOne', sans-serif;
}
  
  .blog-summary {
    color: #555;
    margin-top: 0.5rem;
  }
  
  .blog-link {
    margin-top: 1rem;
    font-weight: 600;
    color: #3182ce;
    text-decoration: none;
  }
  
  .blog-link:hover {
    color: #2b6cb0;
  }
  </style>
  
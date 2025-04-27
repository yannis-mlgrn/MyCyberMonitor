<template>
  <div class="layout">
    <header class="header">
      <h1 class="title">My Cyber Monitor</h1>
    </header>

    <main class="content">
      <section class="blogs">
        <h2 class="section-title">Last Blog Articles</h2>
        <div class="section-body">
         <div v-for="(blog, index) in blogs" :key="index">
            <BlogPost :blog="blog" class="post" />
          </div>
        </div>
      </section>

      <aside class="cves">
        <h2 class="section-title">Trending CVE</h2>
        <ul class="list bg-base-100 rounded-box shadow-md">
          <li class="p-4 pb-2 text-xs opacity-60 tracking-wide">Most trending CVE by Vulmon website</li>
          <CveCard v-for="(cve, index) in cves" :index="index" :cve="cve" />
        </ul>
      </aside>
    </main>
  </div>
</template>

<script setup>
// Import des composants nécessaires
import CveCard from './components/CveCard.vue'
import BlogPost from './components/BlogPost.vue'
import { ref, onMounted } from 'vue'
import { getRecentCVEs, getLatestPosts } from './services/api.js'

const cves = ref([])
const blogs = ref([])

onMounted(async () => {
  try {
    blogs.value = await getLatestPosts();  // fetching blog posts
    cves.value = await getRecentCVEs(15) // fetching CVEs
  } catch (error) {
    console.error('Failed to fetch blog posts:', error);
  }
})
</script>

<style scoped>
/* Style global pour l'application */

:root {
  --gap: 2rem;
  --radius: 0.75rem;
  --shadow-light: 0 2px 8px rgba(0, 0, 0, 0.05);
  --shadow-strong: 0 4px 24px rgba(0, 0, 0, 0.1);
  --color-bg: #fafafa;
  --color-card: #ffffff;
  --color-text: #222;
  --font-sans: 'Inter', sans-serif;
  --max-width: 640px;
}

.layout {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background: var(--color-bg);
  font-family: var(--font-sans);
  color: var(--color-text);
  padding: var(--gap);
  box-sizing: border-box;
}

.header {
  margin-top: 1.5rem;
  padding: var(--gap) 0;
  text-align: center;
}

.title {
  font-family: 'SpecialGothicExpandedOne', sans-serif;
  margin: 0;
  font-size: 3rem;
  font-weight: 300;
  letter-spacing: -1px;
  line-height: 1.1;
}

.content {
  flex: 1;
  display: grid;
  grid-template-columns: 4fr 1fr;
  gap: var(--gap);
  margin-top: var(--gap);
}
.post {
  margin-bottom: 1rem;
}
.blogs, .cves {
  background: var(--color-card);
  border-radius: var(--radius);
  box-shadow: var(--shadow-light);
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: var(--gap);
  transition: box-shadow 0.2s;
}
.blogs:hover, .cves:hover {
  box-shadow: var(--shadow-strong);
}

.section-title {
  font-family: 'SpecialGothicExpandedOne', sans-serif;
  width: 100%;
  text-align: center;
  font-size: 1.5rem;
  font-weight: 400;
  margin: 4rem 0 1rem; /* Augmente l'espace au-dessus */
  border-bottom: 1px solid #e5e7eb;
  padding-bottom: 0.5rem;
}

.section-body {
  width: 100%;
  max-width: var(--max-width);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--gap);
}

.blog-card {
  background: var(--color-card);
  padding: 1rem;
  border-radius: var(--radius);
  box-shadow: var(--shadow-light);
  width: 100%;
}

.blog-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #333;
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

/* Responsive */
@media (max-width: 768px) {
  .content {
    grid-template-columns: 1fr;
  }
  .cves {
    order: -1;
  }
}
</style>

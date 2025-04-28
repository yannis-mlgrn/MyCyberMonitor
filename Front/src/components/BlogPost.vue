<template>
  <div class="card w-225 bg-base-100 card-md card-border shadow-sm ">
    <div class="card-body">
      <h2 class="card-title blog-title">{{ blog.title }}</h2>
      <p v-html="getShortDescription(blog.description)"></p>
      <br>
      <p>Written by <strong>{{ blog.author }}</strong></p>
      
      <div class="justify-end card-actions">
        <a :href="blog.link" target="_blank" class="btn btn-primary">Read More →</a>
      </div>
      <p class="publication-date"> <strong>{{ formatDate(blog.published) }}</strong></p>
    </div>
  </div>
</template>

<script setup>
defineProps({
  blog: Object
});

// Function to format the date
function formatDate(dateString) {
  const date = new Date(dateString);

  // Check if the date is valid
  if (isNaN(date)) {
    return "Invalid date";
  }

  return date.toLocaleString('en-US', {
    weekday: 'long',  // Nom du jour (par exemple "Saturday")
    year: 'numeric',  // Année (par exemple "2025")
    month: 'long',    // Mois (par exemple "April")
    day: 'numeric',   // Jour (par exemple "26")
    hour: '2-digit',  // Heure avec 2 chiffres (par exemple "04")
    minute: '2-digit',// Minute avec 2 chiffres (par exemple "08")
    second: '2-digit',// Seconde avec 2 chiffres (par exemple "00")
    hour12: true      // Affichage de l'heure au format AM/PM
  });
}

// Function to get a short description
function getShortDescription(description) {
  if (description.length > 2000) {
    return description.slice(0, 400) + '...';
  }
  return description;
}
</script>

<style scoped>

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


.publication-date {
  font-size: 0.9rem;
  position: absolute;
  bottom: 10px;
  left: 10px;
  margin: 0;
}
</style>

<template>
  <div class="card w-225 bg-base-100 card-md shadow-sm ">
    <div class="card-body">
      <h2 class="card-title blog-title">{{ blog.title }}</h2>
      <p v-html="blog.description"> </p>
      <br>
      <p>Written by <strong>{{ blog.author }}</strong></p>
      
      <div class="justify-end card-actions">
        <a :href="blog.link" class="btn btn-primary">Read More →</a>
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

/* Style pour positionner la date en bas à gauche */
.publication-date {
  color: #666;
  font-size: 0.9rem;
  position: absolute; /* Utilisation de position absolue */
  bottom: 10px; /* Positionné à 10px du bas */
  left: 10px;   /* Positionné à 10px de la gauche */
  margin: 0;    /* Enlever les marges pour éviter tout décalage */
}
</style>

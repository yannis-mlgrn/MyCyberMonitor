<template>
  <li class="list-row">
    <div class="text-4xl font-thin opacity-30 tabular-nums"> <strong>{{ index + 1 }}</strong></div>
    
    <div class="list-col-grow">
      <div> <strong>{{ cve.id }}</strong></div>
      <div class="text-xs uppercase font-semibold opacity-60">
        <strong v-if="cve.cvss != null"> CVSS : {{ cve.cvss }}</strong>
        <strong v-if="cve.cvss == null"> CVSS : NA </strong> <br>
        {{ cve.description }}
        <br>
        <a :href="cve.link" target="_blank" class="text-blue-500 underline">Learn more</a>
      </div>
    </div>
  </li>
</template>

<script setup>
// Component props: cve (the CVE object) and index (the formatted index)
defineProps({
  cve: Object,
  index: Number
});
</script>

<style scoped>
.list-row {
  display: flex;
  margin-bottom: 1rem;
  padding: 1rem;
  border-radius: 0.75rem;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.list-col-grow {
  flex-grow: 1;
}

.text-4xl {
  font-size: 2rem;
}

.text-xs {
  font-size: 0.75rem;
}
</style>

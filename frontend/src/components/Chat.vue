<template>
  <div>
    <input v-model="query" placeholder="Ask something..." />
    <button @click="ask">Ask</button>

    <div v-if="response">
      <h3>Answer:</h3>
      <p>{{ response }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const query = ref('')
const response = ref('')

const ask = async () => {
  const res = await fetch("http://localhost:8000/query", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({ query: query.value })
  });

  const data = await res.json();
  response.value = data.answer;
};
</script>
<template>
  <div>
    <input type="file" @change="uploadFile" />
    <div v-if="message">{{ message }}</div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const message = ref('')

const uploadFile = async (e) => {
  const file = e.target.files[0];
  if (!file) return;

  const formData = new FormData();
  formData.append("file", file);

  const res = await fetch("http://localhost:8000/api/reports/upload", {
    method: "POST",
    body: formData
  });

  const data = await res.json();
  message.value = res.ok ? data.message : data.detail;
};
</script>

<template>
  <div class="upload-panel">
    <input type="file" accept=".pdf" @change="uploadFile" />

    <div v-if="isLoading" class="loading-block">
      <div class="loading-text">Extracting report and structuring genetic findings...</div>
      <div class="progress-track">
        <div class="progress-bar"></div>
      </div>
    </div>

    <div v-if="message" class="message">{{ message }}</div>

    <div v-if="extractedJson" class="result-block">
      <h3>Extracted JSON</h3>
      <pre>{{ extractedJson }}</pre>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const message = ref('')
const extractedJson = ref('')
const isLoading = ref(false)

const uploadFile = async (e) => {
  const file = e.target.files[0];
  if (!file) return;

  isLoading.value = true;
  message.value = '';
  extractedJson.value = '';

  const formData = new FormData();
  formData.append("file", file);

  try {
    const res = await fetch("http://localhost:8000/api/reports/upload", {
      method: "POST",
      body: formData
    });

    const contentType = res.headers.get("content-type") || "";
    const data = contentType.includes("application/json")
      ? await res.json()
      : { detail: await res.text() };

    message.value = res.ok ? data.message : (data.detail || "Upload failed.");
    if (res.ok) {
      extractedJson.value = JSON.stringify(data.extracted_data, null, 2);
    }
  } catch (error) {
    message.value = 'Upload failed. Request could not be completed.';
  } finally {
    isLoading.value = false;
  }
};
</script>

<style scoped>
.upload-panel {
  display: grid;
  gap: 12px;
}

.loading-block {
  display: grid;
  gap: 8px;
}

.loading-text {
  font-size: 14px;
}

.progress-track {
  width: 100%;
  height: 10px;
  overflow: hidden;
  border-radius: 999px;
  background: #d9e4ec;
}

.progress-bar {
  width: 35%;
  height: 100%;
  border-radius: 999px;
  background: linear-gradient(90deg, #1f7a8c, #3fb0ac);
  animation: loading-slide 1.2s infinite ease-in-out;
}

.message {
  font-size: 14px;
}

.result-block pre {
  margin: 0;
  padding: 12px;
  overflow: auto;
  border-radius: 12px;
  background: #f3f7fa;
  font-size: 13px;
  line-height: 1.45;
}

@keyframes loading-slide {
  0% {
    transform: translateX(-120%);
  }
  100% {
    transform: translateX(320%);
  }
}
</style>

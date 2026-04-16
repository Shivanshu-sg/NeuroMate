<template>
  <div class="upload-panel">
    <label class="upload-label" for="report-file">Upload Genetic Report (PDF)</label>
    <input id="report-file" class="upload-input" type="file" accept=".pdf" @change="uploadFile" />
    <p v-if="message" class="message">{{ message }}</p>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const emit = defineEmits(['upload-start', 'upload-success', 'upload-error'])

const message = ref('')

const uploadFile = async (e) => {
  const file = e.target.files[0]
  if (!file) return;

  message.value = ''
  emit('upload-start')

  const formData = new FormData()
  formData.append('file', file)

  try {
    const res = await fetch('http://localhost:8000/api/reports/upload', {
      method: 'POST',
      body: formData
    })

    const contentType = res.headers.get('content-type') || ''
    const data = contentType.includes("application/json")
      ? await res.json()
      : { detail: await res.text() }

    message.value = res.ok ? data.message : (data.detail || 'Upload failed.')
    if (res.ok) {
      emit('upload-success', data)
    } else {
      emit('upload-error', data.detail || 'Upload failed.')
    }
  } catch (error) {
    const fallback = 'Upload failed. Request could not be completed.'
    message.value = fallback
    emit('upload-error', fallback)
  }
}
</script>

<style scoped>
.upload-panel {
  display: grid;
  gap: 10px;
}

.upload-label {
  font-size: 0.95rem;
  font-weight: 600;
  color: #2f4a5b;
}

.upload-input {
  border: 1px solid #c8d4de;
  border-radius: 10px;
  padding: 10px;
  background: #ffffff;
}

.message {
  margin: 0;
  color: #496476;
  font-size: 0.9rem;
}
</style>

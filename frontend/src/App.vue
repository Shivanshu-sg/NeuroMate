<template>
  <div class="page">
    <main class="container">
      <section class="hero">
        <p class="kicker">NeuroMate</p>
        <h1>Your Genetic Report, Explained Clearly</h1>
        <p class="subtitle">
          Private, local-first interpretation of genetic reports for rare neuromuscular conditions.
        </p>
      </section>

      <section v-show="stage === 'upload'" class="card">
        <Upload @upload-start="onUploadStart" @upload-success="onUploadSuccess" @upload-error="onUploadError" />
      </section>

      <section v-if="stage === 'loading'" class="card">
        <h2>Processing report</h2>
        <p>Extracting details and structuring genetic findings. This can take a few moments.</p>
        <div class="progress-track">
          <div class="progress-bar"></div>
        </div>
      </section>

      <section v-if="stage === 'ready'" class="layout">
        <article class="card">
          <h2>Patient Summary</h2>
          <div class="summary-grid">
            <div><strong>Name:</strong> {{ valueOrNA(extracted.patient_name) }}</div>
            <div><strong>Age:</strong> {{ valueOrNA(extracted.age) }}</div>
            <div><strong>Gender:</strong> {{ valueOrNA(extracted.gender) }}</div>
            <div><strong>Gene:</strong> {{ valueOrNA(extracted.gene_name) }}</div>
            <div><strong>Variant:</strong> {{ valueOrNA(extracted.variant) }}</div>
            <div><strong>Variant Type:</strong> {{ valueOrNA(extracted.variant_type) }}</div>
            <div><strong>Zygosity:</strong> {{ valueOrNA(extracted.zygosity) }}</div>
            <div><strong>Classification:</strong> {{ valueOrNA(extracted.classification) }}</div>
            <div><strong>Disease:</strong> {{ valueOrNA(extracted.disease_name) }}</div>
          </div>
        </article>

        <article class="card">
          <h2>Extracted JSON</h2>
          <pre>{{ formattedExtracted }}</pre>
        </article>

        <article class="card">
          <h2>Ask NeuroMate</h2>
          <Chat :report-id="currentReportId" />
        </article>
      </section>

      <section v-if="errorMessage" class="error">
        {{ errorMessage }}
      </section>
    </main>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import Upload from './components/Upload.vue'
import Chat from './components/Chat.vue'

const stage = ref('upload')
const extracted = ref({})
const currentReportId = ref('')
const errorMessage = ref('')

const formattedExtracted = computed(() => JSON.stringify(extracted.value, null, 2))

const onUploadStart = () => {
  stage.value = 'loading'
  errorMessage.value = ''
}

const onUploadSuccess = (payload) => {
  console.log('Upload successful, extracted data:', payload.extracted_data)
  currentReportId.value = payload.report_id || ''
  extracted.value = payload.extracted_data || {}
  stage.value = 'ready'
}

const onUploadError = (message) => {
  stage.value = 'upload'
  errorMessage.value = message
}

const valueOrNA = (value) => {
  if (value === null || value === undefined || value === '') return 'N/A'
  return value
}
</script>

<style scoped>
.page {
  min-height: 100vh;
  background: linear-gradient(155deg, #f6fbff 0%, #edf5fa 45%, #f8fbf6 100%);
  color: #1c2f3d;
}

.container {
  max-width: 980px;
  margin: 0 auto;
  padding: 30px 18px 50px;
  display: grid;
  gap: 18px;
}

.hero h1 {
  margin: 0;
  font-size: clamp(1.7rem, 2.8vw, 2.3rem);
}

.kicker {
  margin: 0 0 6px;
  font-size: 0.82rem;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: #35607a;
  font-weight: 700;
}

.subtitle {
  margin: 10px 0 0;
  color: #4b6678;
}

.card {
  background: #ffffff;
  border: 1px solid #d8e4ec;
  border-radius: 16px;
  padding: 18px;
  box-shadow: 0 8px 20px rgba(26, 52, 69, 0.06);
}

.layout {
  display: grid;
  gap: 14px;
}

.summary-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 8px 14px;
}

pre {
  margin: 0;
  background: #f4f8fb;
  border-radius: 12px;
  padding: 12px;
  overflow: auto;
  border: 1px solid #d9e4eb;
}

.progress-track {
  width: 100%;
  height: 10px;
  border-radius: 999px;
  background: #d9e4ec;
  overflow: hidden;
}

.progress-bar {
  width: 35%;
  height: 100%;
  border-radius: 999px;
  background: linear-gradient(90deg, #1f7a8c, #3fb0ac);
  animation: loading-slide 1.2s infinite ease-in-out;
}

.error {
  color: #9b2226;
  background: #fff1f2;
  border: 1px solid #f8c6ca;
  border-radius: 12px;
  padding: 10px 12px;
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

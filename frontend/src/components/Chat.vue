<template>
  <div class="chat-panel">
    <div class="row">
      <input v-model="query" placeholder="Ask something..." />
      <button :disabled="isLoading || !query.trim()" @click="ask">
        {{ isLoading ? 'Thinking...' : 'Ask' }}
      </button>
    </div>

    <div v-if="response" class="response-block">
      <h3>Answer:</h3>
      <p>{{ response }}</p>
    </div>

    <div v-if="citations.length" class="citations-block">
      <h3>Citations</h3>
      <div v-for="citation in citations" :key="citation.chunk_id" class="citation-card">
        <p class="citation-head">
          <strong>#{{ citation.rank }}</strong>
          <span>{{ citation.source_type }}</span>
          <span>score: {{ Number(citation.score).toFixed(4) }}</span>
        </p>
        <p class="citation-excerpt">{{ citation.excerpt }}</p>
        <p v-if="citation.source_url" class="citation-source">{{ citation.source_url }}</p>
        <button class="details-btn" @click="loadChunkDetail(citation.chunk_id)">View full context</button>
      </div>
    </div>

    <div v-if="selectedChunkDetail" class="detail-block">
      <h3>Full Citation Context</h3>
      <p><strong>Chunk ID:</strong> {{ selectedChunkDetail.chunk_id }}</p>
      <p><strong>Source Type:</strong> {{ selectedChunkDetail.source_type }}</p>
      <p v-if="selectedChunkDetail.source_url"><strong>Source URL:</strong> {{ selectedChunkDetail.source_url }}</p>
      <pre>{{ selectedChunkDetail.text }}</pre>
    </div>

    <p v-if="error" class="error">{{ error }}</p>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  reportId: {
    type: String,
    default: ''
  }
})

const query = ref('')
const response = ref('')
const citations = ref([])
const selectedChunkDetail = ref(null)
const error = ref('')
const isLoading = ref(false)

const ask = async () => {
  error.value = ''
  isLoading.value = true
  citations.value = []
  selectedChunkDetail.value = null

  try {
    const res = await fetch('http://localhost:8000/api/query', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        query_text: query.value,
        report_id: props.reportId || null,
        top_k: 5
      })
    })

    const contentType = res.headers.get('content-type') || ''
    const data = contentType.includes('application/json')
      ? await res.json()
      : { detail: await res.text() }

    if (!res.ok) {
      error.value = data.detail || 'Could not fetch answer right now.'
      return
    }

    response.value = data.answer || 'No answer returned.'
    citations.value = data.citations || []
  } catch (e) {
    error.value = 'Chat request failed. Please verify the chat backend endpoint.'
  } finally {
    isLoading.value = false
  }
}

const loadChunkDetail = async (chunkId) => {
  try {
    const res = await fetch(`http://localhost:8000/api/chunks/${chunkId}`)
    const contentType = res.headers.get('content-type') || ''
    const data = contentType.includes('application/json')
      ? await res.json()
      : { detail: await res.text() }

    if (!res.ok) {
      error.value = data.detail || 'Could not load chunk details.'
      return
    }
    selectedChunkDetail.value = data
  } catch (e) {
    error.value = 'Failed to load citation details.'
  }
}
</script>

<style scoped>
.chat-panel {
  display: grid;
  gap: 10px;
}

.row {
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 8px;
}

input {
  border: 1px solid #c9d8e1;
  border-radius: 10px;
  padding: 10px 12px;
}

button {
  border: 1px solid #1f7a8c;
  background: #1f7a8c;
  color: #fff;
  border-radius: 10px;
  padding: 10px 14px;
  cursor: pointer;
}

button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.response-block {
  padding: 12px;
  border-radius: 10px;
  background: #f3f8fb;
  border: 1px solid #d8e6ee;
}

.citations-block {
  display: grid;
  gap: 10px;
}

.citation-card {
  border: 1px solid #d8e6ee;
  border-radius: 10px;
  padding: 10px;
  background: #f8fbfd;
}

.citation-head {
  display: flex;
  gap: 10px;
  margin: 0 0 6px;
  font-size: 0.9rem;
}

.citation-excerpt {
  margin: 0 0 6px;
}

.citation-source {
  margin: 0 0 8px;
  color: #496476;
  font-size: 0.84rem;
}

.details-btn {
  border: 1px solid #2a6f97;
  background: #ffffff;
  color: #2a6f97;
  border-radius: 8px;
  padding: 6px 10px;
}

.detail-block {
  border: 1px solid #cfdde7;
  border-radius: 10px;
  padding: 12px;
  background: #f7fafc;
}

.detail-block pre {
  margin: 0;
  white-space: pre-wrap;
}

.response-block h3 {
  margin-top: 0;
}

.error {
  margin: 0;
  color: #9b2226;
}
</style>

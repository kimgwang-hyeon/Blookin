<!-- src/views/ThreadWriteView.vue -->
<template>
  <div class="p-6 max-w-xl mx-auto relative">
    <!-- ✅ 로딩 오버레이 추가 -->
    <div
      v-if="isSubmitting"
      class="fixed inset-0 z-50 bg-black bg-opacity-60 flex items-center justify-center"
    >
      <div class="text-center space-y-4">
        <div class="relative w-40 h-40 mx-auto flex items-end justify-center">
           <img
              src="@/assets/loading-rabbit.png"
              alt="달토끼"
              class="absolute bottom-0 max-w-[180px] h-auto animate-bounce"
            />
        </div>

        <!-- 텍스트 -->
        <p class="text-white text-lg font-semibold">감상글을 생성 중입니다...</p>

        <!-- 프로그레스 바 -->
        <div class="w-64 h-2 border border-white rounded overflow-hidden mx-auto bg-transparent relative">
          <div class="absolute h-full w-1/4 bg-white animate-slide-loop"></div>
        </div>
      </div>
    </div>

    <h1 class="text-2xl font-bold mb-4">감상글 작성</h1>

    <form @submit.prevent="submitThread" class="space-y-4">
      <p class="text-l font-bold mb-4">Title</p>
      <input v-model="title" type="text" placeholder="제목을 입력하세요" class="w-full border rounded p-2" />
      <p class="text-l font-bold mb-4">Contents</p>
      <textarea v-model="content" placeholder="내용을 입력하세요" class="w-full border rounded p-2 h-32"></textarea>
      <p class="text-l font-bold mb-4">Reading Date</p>
      <input v-model="reading_date" type="date" class="w-full border rounded p-2" />
      
      <p class="text-l font-bold mb-4">AI Assistant</p>
      <ThreadEditor @ai="getAIFeedback" />

      <div class="ai-section">
        <div v-if="loading">AI 피드백 처리 중...</div>
        <AiFeedbackApply
          v-if="aiFeedback.length"
          :original="content"
          :feedback="aiFeedback"
          @updateContent="handleAIApply"
        />
      </div>

      <!-- 도서 정보 카드 -->
      <div v-if="bookInfo" class="flex items-center gap-4 p-4 rounded shadow">
        <img
          :src="bookInfo.cover"
          alt="도서 표지"
          class="w-20 h-28 object-cover rounded"
        />
        <div>
          <p class="text-m font-semibold">{{ bookInfo.title.split('-')[0] }}</p>
          <p class="text-sm text-gray-400 mt-4 line-clamp-1">
            {{ bookInfo.author }} | {{ bookInfo.publisher }}
          </p>
        </div>
      </div>


      <!-- ✅ 등록 버튼에서 중복 등록 방지 조건 추가 -->
      <button
        type="submit"
        :disabled="aiFeedback.length > 0 && !aiApplied || threadSubmitted"
        class="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700 disabled:bg-gray-400"
      >
        등록하기
      </button>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useThreadStore } from '@/stores/threads'
import { useAccountStore } from '@/stores/account'
import ThreadEditor from '@/components/ThreadEditor.vue'
import AiFeedbackApply from '@/components/AiFeedbackApply.vue'
import axios from 'axios'

const route = useRoute()
const router = useRouter()

const title = ref('')
const content = ref('')
const reading_date = ref('')
const book = ref(route.query.book ? Number(route.query.book) : null)
const bookInfo = ref(null)
const aiFeedback = ref([])
const aiApplied = ref(false)
const loading = ref(false) // ✅ AI 피드백 로딩
const isSubmitting = ref(false) // ✅ 스레드 작성 중 로딩
const threadSubmitted = ref(false) // ✅ 중복 등록 방지를 위한 상태

const threadStore = useThreadStore()
const accountStore = useAccountStore()

const getAIFeedback = async () => {
  if (!content.value.trim()) return
  loading.value = true
  aiApplied.value = false

  try {
    const res = await fetch('https://api.openai.com/v1/chat/completions', {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${import.meta.env.VITE_OPENAI_API_KEY}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        model: 'gpt-4o',
        messages: [
          {
            role: 'system',
            content: `다음 JSON 형식을 반드시 지켜서 감상글 수정 제안을 반환하세요. \n[{"from": "", "to": "", "explanation": ""}]`,
          },
          {
            role: 'user',
            content: content.value,
          },
        ],
      }),
    })

    const data = await res.json()
    let raw = data.choices[0].message.content
    raw = raw.replace(/^```json\n?/, '').replace(/```$/, '').trim()
    aiFeedback.value = JSON.parse(raw)
  } catch (e) {
    console.error('AI 피드백 실패:', e)
    aiFeedback.value = []
  } finally {
    loading.value = false
  }
}

const handleAIApply = (updatedContent) => {
  content.value = updatedContent
  aiApplied.value = true
}

const submitThread = () => {
  if (aiFeedback.value.length && !aiApplied.value) return
  if (threadSubmitted.value) return

  const payload = {
    title: title.value,
    content: content.value,
    reading_date: reading_date.value,
    book: book.value,
  }

  threadSubmitted.value = true
  isSubmitting.value = true // ✅ 로딩 시작

  threadStore.createThread(payload, accountStore.token)
    .then(() => {
      alert('감상글이 작성되었습니다!')
      router.push('/threads')
    })
    .catch((err) => {
      console.error('작성 실패:', err)
      alert('감상글 작성에 실패했습니다.')
      threadSubmitted.value = false
    })
    .finally(() => {
      isSubmitting.value = false // ✅ 로딩 종료
    })
}

onMounted(() => {
  if (book.value) {
    axios
      .get(`/api/books/${book.value}/`)
      .then((res) => {
        bookInfo.value = res.data
      })
      .catch((err) => {
        console.error('도서 정보를 가져오는 데 실패했습니다:', err)
      })
  }
})
</script>

<style scoped>
@keyframes slide-loop {
  0% {
    transform: translateX(-100%);
  }
  100% {
    transform: translateX(400%);
  }
}

.animate-slide-loop {
  animation: slide-loop 1.5s linear infinite;
}

</style>

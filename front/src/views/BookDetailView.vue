<!-- BookDetailView.vue -->
<template>
  <div v-if="book" class="p-6 max-w-5xl mx-auto">
    <!-- 책 제목 -->
    <h1 class="text-2xl font-bold mb-4">{{ book.title.split('-')[0] }}</h1>

    <!-- 버튼 그룹 (상단 우측) -->
    <div class="flex flex-wrap justify-end gap-2 mb-6">
      <button
        @click="toggleLike"
        class="text-xs px-3 py-1 border rounded transition font-medium"
        :class="book.is_liked
          ? 'bg-red-100 text-red-700 border-red-300 hover:bg-red-200'
          : 'bg-blue-100 text-blue-700 border-blue-300 hover:bg-blue-200'"
      >
        {{ book.is_liked ? '💔 관심 도서에서 제거' : '❤️ 관심 도서에 추가' }}
      </button>

      <RouterLink
        :to="`/threads/write?book=${book.id}`"
        class="text-xs bg-blue-600 text-white px-3 py-1 rounded hover:bg-blue-700 transition"
      >
        ✏️ 감상글 작성
      </RouterLink>
    </div>

    <!-- 2단 구성: 좌측 표지 + 우측 정보 -->
    <div class="flex flex-col md:flex-row items-start gap-8">
      <!-- 왼쪽: 도서 표지 -->
      <div class="flex-shrink-0 w-full md:w-64">
        <img :src="book.cover" alt="cover" class="w-full object-contain rounded shadow" />
      </div>

      <!-- 오른쪽: 설명 및 정보 -->
      <div class="flex-1">
        <p class="whitespace-pre-line mb-4">{{ book.description }}</p>
          <!-- 책 부가 정보: 작은 글씨 + 회색 -->
          <div class="text-sm text-gray-500">
            <p class="mb-1">저자: {{ book.author }}</p>
            <p class="mb-1">출판사: {{ book.publisher }}</p>
            <p class="mb-1">출간일: {{ book.pub_date }}</p>
            <p class="mb-1" v-if="book.subTitle">소제목: {{ book.subTitle }}</p>
          </div>
        <!-- 작가 프로필 이미지 -->
        <div v-if="book.author_profile_img" class="mt-4">
          <img
            :src="`/media/${book.author_profile_img}`"
            alt="작가 이미지"
            class="w-40 rounded shadow"
          />
        </div>
      </div>
    </div>

    <!-- AI 생성 작가 정보 -->
    <div v-if="book.author_info" class="mt-8 p-4">
      <h2 class="text-lg font-semibold mb-2">작가 정보</h2>
      <p class="text-sm whitespace-pre-line">{{ book.author_info }}</p>
      
      <!-- 대표작 -->
      <div v-if="parsedWorks.length" class="mt-4">
        <h2 class="font-semibold text-lg">대표작</h2>
        <ul class="list-disc list-inside text-sm">
          <li v-for="work in parsedWorks" :key="work">{{ work }}</li>
        </ul>
      </div>


      <p class="text-xs text-gray-400 mt-2">
        * 작가 정보와 대표작은 AI가 생성한 정보로, 정확하지 않을 수 있습니다.
      </p>
    </div>

    <!-- 🎧 오디오 소개 카드 -->
    <div v-if="book.tts_audio" class="mt-10 bg-[#1e293b] text-white shadow-lg rounded-xl p-6 border border-gray-700">
      <h2 class="text-xl font-bold text-white mb-4 flex items-center gap-2">
        <svg xmlns="http://www.w3.org/2000/svg" class="w-6 h-6 text-cyan-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
            d="M9 19V6l-2 2H4a1 1 0 00-1 1v6a1 1 0 001 1h3l2 2zm7-2a3 3 0 003-3V9a3 3 0 00-6 0v5a3 3 0 003 3z" />
        </svg>
        오디오 소개
      </h2>
      <audio
        controls
        :src="`${book.tts_audio}`"
        class="w-full rounded-lg shadow-inner bg-gray-800"
      ></audio>
    </div>

    <!-- 감상글이 있는 경우 -->
    <div v-if="book.thread_set && book.thread_set.length" class="mt-12">
      <h2 class="text-xl font-semibold mb-4">📘 감상글</h2>

      <div class="grid grid-cols-1 sm:grid-cols-2 gap-6">
        <ThreadCard
          v-for="thread in book.thread_set"
          :key="thread.id"
          :thread="thread"
        />
      </div>
    </div>

    <!-- 감상글이 없는 경우 -->
    <div v-else class="mt-12 text-center text-gray-400">
      아직 감상글이 없습니다.
    </div>


    <!-- 지도 -->
    <div class="mt-6">
      <!-- ✅ 토글 버튼 -->
      <button
        @click="isOpen = !isOpen"
        class="flex items-center gap-2 text-white font-semibold hover:underline focus:outline-none"
      >
        <span>{{ isOpen ? '▼' : '▶' }}</span>
        지도 보기
      </button>

      <!-- ✅ 토글 내용 -->
      <div v-if="isOpen" class="mt-4">
        <MapViewer />
      </div>
    </div>
  </div>
</template>


<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, RouterLink } from 'vue-router'
import axios from 'axios'
import { useBookStore } from '@/stores/books'
import { useAccountStore } from '@/stores/account'
import MapViewer from '@/components/MapViewer.vue'
import ThreadCard from '@/components/ThreadCard.vue'

const route = useRoute()
const bookStore = useBookStore()
const book = computed(() => bookStore.selectedBook)
const works = ref([])
const account = useAccountStore()
const isOpen = ref(false)

const toggleLike = () => {
  if (!book.value) return
  axios.post(`/api/books/${book.value.id}/like/`, {}, {
    headers: {
      Authorization: `Token ${account.token}`,
    }
  })
  .then(res => {
    book.value.is_liked = res.data.liked
    book.value.likes_count = res.data.likes_count
  })
  .catch(err => {
    console.error('관심 도서 토글 실패:', err)
  })
}

onMounted(async () => {
  await bookStore.fetchBookDetail(route.params.bookId)
  console.log('[디버깅] author_works:', book.value.author_works)
  // ✅ author_works 문자열을 배열로 변환
  if (book.value.author_works) {
    works.value = book.value.author_works
      .split(/,|·|・|\n/)
      .map(w => w.trim())
      .filter(w => w.length > 0)
    console.log('[디버깅] works 배열:', works.value)
  }
})

const parsedWorks = computed(() => {
  if (!book.value?.author_works) return []

  // author_works가 문자열이면 → JSON.parse (단, 작은따옴표 처리 필요)
  if (typeof book.value.author_works === 'string') {
    try {
      const fixed = book.value.author_works.replace(/'/g, '"')  // 작은따옴표 → 큰따옴표
      return JSON.parse(fixed)
    } catch (e) {
      console.warn('author_works 파싱 실패:', e)
      return []
    }
  }

  // 이미 배열이면 그대로 반환
  return book.value.author_works
})
</script>


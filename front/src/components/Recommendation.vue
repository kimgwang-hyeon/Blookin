<!-- components/Recommendation.vue -->
<template>
  <div class="p-6 max-w-5xl mx-auto">
    <!-- 페이지 제목 -->
    <h2 class="text-2xl font-bold mb-4">추천 도서</h2>

    <!-- 추천 기준 선택 버튼 (좋아요 기반 / 감상글 기반) -->
    <div class="mb-6 flex gap-3 flex-wrap">
      <button
        class="text-white border px-4 py-2 rounded-lg font-semibold hover:bg-blue-200 transition"
        @click="changeType('likes')"
      >
        내가 좋아요한 책 기반
      </button>
      <button
        class="text-white border px-6 py-2 rounded-lg font-semibold hover:bg-blue-200 transition"
        @click="changeType('threads')"
      >
        내가 쓴 감상글 기반
      </button>
    </div>

    <!-- 추천 도서 목록 -->
    <div v-if="books.length" class="grid grid-cols-2 md:grid-cols-4 gap-6">
      <RouterLink
        v-for="book in books"
        :key="book.id"
        :to="`/books/${book.id}`"
        class="block rounded p-2 shadow hover:shadow-lg transition"
      >
        <img :src="book.cover" class="w-full h-80 object-cover mb-2 rounded" />
        <h3 class="text-sm font-semibold truncate">{{ book.title.split('-')[0] }}</h3>
        <p class="text-xs text-gray-500">{{ book.author }}</p>
      </RouterLink>
    </div>

    <!-- 추천 결과가 없을 경우 메시지 -->
    <p v-else class="text-gray-500">해당 기준으로 추천할 책이 없습니다.</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { RouterLink } from 'vue-router'
import { fetchPersonalRecommendations } from '@/services/recommend'

// 추천 도서 목록 상태
const books = ref([])

// 현재 선택된 추천 기준: 'likes' 또는 'threads'
const selectedType = ref('likes')

// 추천 도서 불러오기
const loadBooks = () => {
  fetchPersonalRecommendations(selectedType.value)
    .then(res => books.value = res.data)
    .catch(err => console.error('추천 실패', err))
}

// 버튼 클릭 시 추천 기준 변경
const changeType = (type) => {
  selectedType.value = type
  loadBooks()
}

// 컴포넌트 초기 렌더 시 도서 로딩
onMounted(() => {
  loadBooks()
})
</script>

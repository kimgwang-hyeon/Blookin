<!-- views/MbtiResultView.vue -->
<template>
  <div class="max-w-5xl mx-auto p-6 space-y-8">
    <!-- MBTI 제목 및 설명 -->
    <div class="text-center">
      <h2 class="text-3xl font-bold mb-2">{{ mbti }} 유형에게 추천하는 책</h2>
      <p class="text-gray-400 text-lg">"{{ reason }}"</p>
    </div>

    <!-- 추천 도서 목록 -->
    <div v-if="books.length" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-2 gap-x-6 gap-y-8">
      <BookCard
        v-for="book in books"
        :key="book.id"
        :book="book"
        class="my-2"
      />
    </div>

    <!-- 로딩/에러 메시지 -->
    <div v-else class="text-center text-gray-500">
      추천 도서를 불러오는 중이거나 결과가 없습니다.
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from '@/lib/axios'
import BookCard from '@/components/BookCard.vue'

const route = useRoute()
const mbti = route.query.mbti || ''

const books = ref([])
const reason = ref('')

onMounted(() => {
  if (!mbti) return

  axios.get(`/books/recommend/mbti/?mbti=${mbti}`)
    .then(res => {
      books.value = res.data.books
      reason.value = res.data.reason
    })
    .catch(err => {
      console.error('[MBTI 추천 실패]', err)
    })
})
</script>

<!-- BestsellerCarousel.vue -->
<template>
  <!-- 전체 캐러셀 섹션 -->
  <div class="my-12 px-4">
    <h2 class="text-3xl font-bold mb-6 text-center">베스트셀러</h2>

    <div class="relative overflow-hidden">
      <!-- 슬라이드 컨테이너: transform을 이용한 이동 구현 -->
      <div
        class="flex transition-transform duration-500 ease-in-out"
        :style="{ transform: `translateX(-${currentSlide * 100}%)` }"
      >
        <!-- 한 슬라이드에 4권씩 배치 -->
        <div
          v-for="chunk in chunkedBooks"
          :key="chunk[0].id"
          class="grid grid-cols-2 md:grid-cols-4 gap-4 flex-shrink-0 w-full"
        >
          <!-- 도서 카드 -->
          <div
            v-for="book in chunk"
            :key="book.id"
            @click="goToBookDetail(book.id)"
            class="bg-[#0f172a] text-white shadow rounded p-4 text-center cursor-pointer hover:shadow-lg transition"
          >
            <img
              :src="book.cover"
              alt="cover"
              class="mx-auto mb-2 w-[150px] h-[220px] object-cover"
            />
            <h3 class="font-semibold truncate">{{ book.title.split('-')[0] }}</h3>
            <p class="text-sm text-gray-500">{{ book.author }}</p>
          </div>
        </div>
      </div>

      <!-- 수동 제어 버튼: 이전 슬라이드 -->
      <button
        @click="prevSlide"
        class="absolute left-0 top-1/2 transform -translate-y-1/2 bg-[#0f172a] text-white bg-opacity-80 px-2 py-1 rounded-full shadow"
      >
        ◀
      </button>

      <!-- 수동 제어 버튼: 다음 슬라이드 -->
      <button
        @click="nextSlide"
        class="absolute right-0 top-1/2 transform -translate-y-1/2 bg-[#0f172a] text-white bg-opacity-80 px-2 py-1 rounded-full shadow"
      >
        ▶
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

// 클릭 시 도서 상세 페이지로 이동
const goToBookDetail = (bookId) => {
  router.push(`/books/${bookId}`)
}

// props: 외부에서 받은 도서 배열
const props = defineProps({
  books: {
    type: Array,
    required: true
  }
})

// 도서 목록을 4개씩 끊어서 슬라이드 페이지 구성
const chunkedBooks = computed(() => {
  const chunks = []
  for (let i = 0; i < props.books.length; i += 4) {
    chunks.push(props.books.slice(i, i + 4))
  }
  return chunks
})

// 현재 보여지는 슬라이드 인덱스
const currentSlide = ref(0)
const slideCount = computed(() => chunkedBooks.value.length)

// 다음 슬라이드로 이동
const nextSlide = () => {
  currentSlide.value = (currentSlide.value + 1) % slideCount.value
}

// 이전 슬라이드로 이동
const prevSlide = () => {
  currentSlide.value =
    (currentSlide.value - 1 + slideCount.value) % slideCount.value
}

// 자동 슬라이드 기능 설정
let intervalId
onMounted(() => {
  intervalId = setInterval(nextSlide, 4000) // 4초 간격 자동 이동
})
onUnmounted(() => {
  clearInterval(intervalId)
})
</script>

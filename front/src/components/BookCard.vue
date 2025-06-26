<!-- src/components/BookCard.vue -->
<template>
  <!-- 카드 전체 컨테이너 (배경색 및 테두리 적용) -->
  <div class="bg-gray-800 text-white rounded-lg">
    <!-- 클릭 시 도서 상세 페이지로 이동 -->
    <router-link :to="`/books/${book.id}`" class="block h-full">
      <!-- 카드 본문 레이아웃 (좌우 배치) -->
      <div class="h-full flex text-white dark:bg-gray-800 shadow hover:shadow-lg transition overflow-hidden">
        
        <!-- 표지 이미지 영역 -->
        <div
          class="w-28 md:w-32 lg:w-36 aspect-[2/3] flex-shrink-0
                flex items-center justify-center"
        >
          <img
            :src="book.cover"
            alt="cover"
            class="object-contain max-h-full max-w-full"
          />
        </div>

        <!-- 텍스트 정보 영역 -->
        <div class="flex flex-col justify-center p-4 w-full">
          <!-- 도서 제목 (앞부분만) -->
          <h3 class="text-base font-semibold break-words leading-snug line-clamp-2">
            {{ book.title.split('-')[0] }}
          </h3>

          <!-- 저자, 출판사, 출간일 -->
          <p class="text-sm text-gray-400 mt-1 line-clamp-1">
            {{ book.author }} | {{ book.publisher }} | {{ book.pub_date }}
          </p>

          <br />

          <!-- 도서 부제목 (title의 뒷부분) -->
          <p class="text-sm break-words leading-snug line-clamp-2">
            {{ book.title.split('-')[1] }}
          </p>
        </div>
      </div>
    </router-link>
  </div>
</template>

<script setup>
// 상위 컴포넌트로부터 도서 객체를 props로 전달받음
defineProps({
  book: {
    type: Object,
    required: true
  }
})
</script>

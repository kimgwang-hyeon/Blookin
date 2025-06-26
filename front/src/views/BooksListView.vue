<!-- views/BooksListView.vue -->
<template>
  <div class="flex justify-center px-8 xl:px-24 py-6 bg-[#0f172a] text-white">
    <!-- 컨테이너: 전체 레이아웃을 가운데 정렬 + 여백 -->
    <div class="flex gap-8 w-full max-w-screen-2xl">
      
      <!-- 왼쪽: 카테고리 목록 -->
      <div class="w-56 flex-shrink-0 self-start sticky top-6">
        <h2 class="text-lg font-bold mb-2">카테고리</h2>
        <ul class="space-y-2">
          <li>
            <button
              class="w-full text-left px-3 py-1 rounded transition-colors duration-200
                    hover:bg-white hover:text-blue-800"
              :class="selectedCategory === '' ? 'bg-blue-500 text-white' : 'text-white'"
              @click="selectCategory('')"
            >
              전체
            </button>
          </li>
          <li v-for="cat in bookStore.categories" :key="cat.id">
            <button
              class="w-full text-left px-3 py-1 rounded transition-colors duration-200
                    hover:bg-white hover:text-blue-800"
              :class="selectedCategory === cat.id.toString() ? 'bg-blue-500 text-white' : 'text-white'"
              @click="selectCategory(cat.id)"
            >
              {{ cat.name }}
            </button>
          </li>
        </ul>
      </div>

      <!-- 오른쪽: 검색 + 정렬 + 도서 목록 -->
      <div class="flex-1">
        <!-- 검색 + 정렬 -->
        <form @submit.prevent="onSearch" class="flex flex-col md:flex-row md:items-center md:justify-between gap-2 mb-6">
          <div class="flex w-full md:w-2/3 gap-2">
            <input
              v-model="query"
              @keyup.enter="onSearch"
              class="border px-4 py-2 rounded flex-1"
              placeholder="도서 제목을 입력하세요"
            />
            <button type="submit" class="px-4 py-2 bg-blue-500 text-white rounded whitespace-nowrap">
              검색
            </button>
          </div>

          <select
            v-model="ordering"
            @change="onSearch" 
            class="w-full md:w-48 px-3 py-2 rounded border border-gray-600
                  bg-[#0f172a] text-white focus:outline-none focus:ring-2 focus:ring-blue-500
                  transition-colors"
          >
            <option value="-pub_date">최신순</option>
            <option value="pub_date">오래된순</option>
            <option value="-customer_review_rank">평점높은순</option>
          </select>
        </form>

        <!-- 도서 리스트 -->
        <div v-if="bookStore.books.length" class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-2 gap-x-6 gap-y-8">
          <BookCard
            v-for="book in bookStore.books"
            :key="book.id"
            :book="book"
          />
        </div>
        <div v-else class="text-center text-gray-500 mt-8">
          아직 등록된 도서가 없습니다.
        </div>
      </div>
    </div>
  </div>
</template>


<script setup>
import { ref, watch, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useBookStore } from '@/stores/books'
import BookCard from '@/components/BookCard.vue'

const bookStore = useBookStore()
const route = useRoute()
const router = useRouter()

const query = ref('')
const selectedCategory = ref('')
const ordering = ref('-pub_date')

// ✅ 최초 진입 시 query가 비어있다면 기본값으로 세팅
onMounted(() => {
  if (!route.query.q && !route.query.ordering && !route.query.category) {
    router.replace({
      path: '/books',
      query: {
        q: '',
        ordering: '-pub_date',
        category: '',
      },
    })
  }

  bookStore.fetchCategories()
})

// ✅ query가 바뀔 때마다 서버에서 다시 도서 목록 불러오기
watch(() => route.query, () => {
  query.value = route.query.q || ''
  ordering.value = route.query.ordering || '-pub_date'
  selectedCategory.value = route.query.category || ''

  bookStore.fetchBooks({
    q: query.value,
    ordering: ordering.value,
    category: selectedCategory.value,
  })
})

// ✅ 카테고리 선택 시 직접 router push (selectedCategory.value 갱신은 watch에서 함)
const selectCategory = (categoryId) => {
  router.push({
    path: '/books',
    query: {
      q: query.value,
      ordering: ordering.value,
      category: categoryId,
    },
  })
}

// ✅ 검색 or 정렬 시 직접 push
const onSearch = () => {
  router.push({
    path: '/books',
    query: {
      q: query.value,
      ordering: ordering.value,
      category: selectedCategory.value,
    },
  })
}
</script>


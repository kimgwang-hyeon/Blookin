<!-- views/ThreadsListView.vue -->
<template>
  <div class="flex justify-center px-8 xl:px-24 py-6 bg-[#0f172a] text-white">
    <!-- 전체 컨테이너: 가운데 정렬 + 최대 너비 제한 -->
    <div class="flex gap-8 w-full max-w-screen-2xl">

      <!-- 왼쪽: 카테고리 필터만 -->
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
          <li v-for="cat in threadStore.categories" :key="cat.id">
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

      <!-- 오른쪽: 검색 + 정렬 + 감상글 목록 -->
      <div class="flex-1">
        <!-- 검색 + 정렬 -->
        <form @submit.prevent="onSearch" class="flex flex-col md:flex-row md:items-center md:justify-between gap-2 mb-6">
          <div class="flex w-full md:w-2/3 gap-2">
            <input
              v-model="query"
              @keyup.enter="onSearch"
              class="border px-4 py-2 rounded flex-1"
              placeholder="감상글을 검색하세요."
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
            <option value="-created_at">최신순</option>
            <option value="created_at">오래된순</option>
            <option value="-likes">좋아요순</option>
          </select>
        </form>

        <!-- 감상글 목록 -->
        <div v-if="threadStore.threads.length" class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-2 gap-x-6 gap-y-8">
          <ThreadCard
            v-for="thread in threadStore.threads"
            :key="thread.id"
            :thread="thread"
          />
        </div>

        <div v-else class="text-center text-gray-500 mt-12">
          아직 작성된 감상글이 없습니다.
        </div>
      </div>
    </div>
  </div>
</template>




<script setup>
import { ref, watch, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useThreadStore } from '@/stores/threads'
import ThreadCard from '@/components/ThreadCard.vue'

const threadStore = useThreadStore()
const route = useRoute()
const router = useRouter()

// 상태
const query = ref('')
const selectedCategory = ref('')
const ordering = ref('-created_at')

// ✅ URL → 상태 초기화
onMounted(() => {
  if (!route.query.q && !route.query.ordering && !route.query.category) {
    router.replace({
      path: '/threads',
      query: {
        q: '',
        ordering: '-created_at',
        category: '',
      },
    })
  }
  threadStore.fetchCategories()  // ✅ 반드시 있어야 함
})



// ✅ URL query 변경 감지 → 다시 fetch
watch(() => route.query, () => {
  query.value = route.query.q || ''
  ordering.value = route.query.ordering || '-created_at'
  selectedCategory.value = route.query.category || ''

  threadStore.fetchThreads({
    q: query.value,
    ordering: ordering.value,
    category: selectedCategory.value,
  })
})

// ✅ form submit 혹은 카테고리 선택 시 URL 변경만 하면 끝
const onSearch = () => {
  router.push({
    path: '/threads',
    query: {
      q: query.value,
      ordering: ordering.value,
      category: selectedCategory.value,
    },
  })
}

const selectCategory = (categoryId) => {
  selectedCategory.value = categoryId
  onSearch()
}


</script>

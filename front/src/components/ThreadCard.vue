<!-- components/ThreadCard.vue -->
<template>
  <div class="bg-gray-800 rounded-lg px-3">
    <router-link
      :to="`/threads/${thread.id}`"
      class="block rounded overflow-hidden shadow hover:shadow-md transition"
    >
     <div class="p-3">
      @{{ thread.user_info.full_name }}
     </div>
      <!-- 커버 이미지 -->
      <img
        v-if="thread.cover_img"
        :src="thread.cover_img.startsWith('http') 
          ? thread.cover_img 
          : `http://localhost:8000${thread.cover_img.replace(/\\/g, '/')}`"
        alt="커버 이미지"
        class="h-48 w-full object-cover"
      />

      <!-- 텍스트 내용 -->
      <div class="p-3">
        <h4 class="mb-2">
          ❤️ {{ thread.likes_count }} 
        </h4>
        <h3 class="font-semibold text-base mb-1 line-clamp-1">
          {{ thread.title }}
        </h3>
        <p class="text-sm text-gray-400 mb-1 line-clamp-2">
          {{ thread.content }}
        </p>
        <br>
        <p class="text-right text-xs text-gray-400 line-clamp-1">
          "{{ thread.book_info?.title.split("-")[0] || '제목 없음' }}"
        </p>
      </div>
    </router-link>
  </div>
</template>

<script setup>
defineProps({
  thread: {
    type: Object,
    required: true
  }
})
</script>



<style scoped>
/* line-clamp은 tailwind 플러그인 또는 수동 스타일로도 가능 */
.line-clamp-1 {
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>

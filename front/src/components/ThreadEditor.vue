<!-- src/components/ThreadEditor.vue -->
<template>    
    <p class="text-sm text-gray-500">AI가 감상글을 자연스럽게 다듬어줄 수 있어요.</p>
    <button
      type="button"
      class="text-white border px-4 py-2 rounded-lg font-semibold hover:bg-gray-500 transition"
      @click="$emit('ai')"
    >
      ✨ AI 피드백 받기 ✨
    </button>
  
</template>

<script setup>
defineEmits(['ai'])
</script>
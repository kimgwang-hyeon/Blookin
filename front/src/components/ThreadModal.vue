<!-- components/ThreadModal.vue -->
<template>
  <div class="fixed inset-0 bg-black/50 flex justify-center items-center z-50">
    <div class="bg-white text-black p-6 rounded-xl shadow max-w-lg w-full">
      <h2 class="text-xl font-semibold mb-4">
        {{ mode === 'edit' ? '스레드 수정' : '스레드 삭제' }}
      </h2>

      <!-- 수정 모드 -->
      <template v-if="mode === 'edit'">
        <input v-model="localTitle" class="border w-full mb-2 p-2 rounded" placeholder="제목" />
        <textarea v-model="localContent" class="border w-full p-2 rounded h-32" placeholder="내용" />
      </template>

      <!-- 삭제 모드 -->
      <template v-else>
        <p class="text-lg mb-4">정말 이 스레드를 삭제하시겠습니까?</p>
      </template>

      <div class="flex justify-end gap-2 mt-4">
        <button @click="$emit('cancel')" class="text-gray-600">취소</button>
        <button
          @click="handleConfirm"
          :class="mode === 'edit' ? 'bg-blue-500 hover:bg-blue-600' : 'bg-red-500 hover:bg-red-600'"
          class="text-white px-4 py-1 rounded"
        >
          {{ mode === 'edit' ? '저장' : '삭제' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  mode: {
    type: String,
    required: true,
    validator: value => ['edit', 'delete'].includes(value),
  },
  title: String,
  content: String,
})
const emit = defineEmits(['confirm', 'cancel'])

const localTitle = ref('')
const localContent = ref('')

// 초기값 설정
watch(
  () => [props.title, props.content],
  ([newTitle, newContent]) => {
    localTitle.value = newTitle || ''
    localContent.value = newContent || ''
  },
  { immediate: true }
)

const handleConfirm = () => {
  if (props.mode === 'edit') {
    emit('confirm', {
      title: localTitle.value,
      content: localContent.value
    })
  } else {
    emit('confirm')
  }
}

</script>

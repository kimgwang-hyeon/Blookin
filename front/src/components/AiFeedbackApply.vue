<!-- src/components/AiFeedbackApply.vue -->
<template>
  <!-- 변경 사항이 있을 경우에만 렌더링 -->
  <div v-if="changes.length">
    <!-- 각 피드백 항목을 반복 렌더링 -->
    <div v-for="(item, i) in changes" :key="i" class="mb-2">
      <label>
        <!-- 선택 적용 여부를 체크박스로 입력 -->
        <input type="checkbox" v-model="item.applied" />
        <span class="font-medium text-blue-600">{{ item.from }}</span>
        →
        <span class="font-medium text-green-700">{{ item.to }}</span>
      </label>
      <!-- 설명 표시 -->
      <p class="text-xs text-gray-500">- {{ item.explanation }}</p>
    </div>

    <!-- 선택 적용 / 전체 적용 버튼 -->
    <div class="flex gap-2 mt-2">
      <button
        type="button"
        @click="applySelected"
        class="text-sm bg-blue-500 text-white px-3 py-1 rounded"
      >
        선택 적용
      </button>
      <button
        type="button"
        @click="applyAll"
        class="text-sm bg-purple-600 text-white px-3 py-1 rounded"
      >
        전체 적용
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'

// props: 원본 텍스트와 AI 피드백 배열
const props = defineProps({
  original: String, // 감상글 원본 텍스트
  feedback: Array    // [{ from, to, explanation }]
})

// content를 업데이트하는 부모 컴포넌트 이벤트 정의
const emit = defineEmits(['updateContent'])

// 내부 상태로 피드백 변경사항 관리 (applied 여부 포함)
const changes = ref([])

// feedback prop이 변경되면 changes에 반영하고 applied를 false로 초기화
watch(
  () => props.feedback,
  (newVal) => {
    changes.value = newVal.map(item => ({ ...item, applied: false }))
  },
  { immediate: true }
)

// 선택한 항목만 적용
const applySelected = () => {
  let updated = props.original
  changes.value.forEach(c => {
    if (c.applied) {
      updated = updated.replace(c.from, c.to)
    }
  })
  emit('updateContent', updated)
}

// 전체 항목 일괄 적용
const applyAll = () => {
  let updated = props.original
  changes.value.forEach(c => {
    updated = updated.replace(c.from, c.to)
  })
  emit('updateContent', updated)
}
</script>

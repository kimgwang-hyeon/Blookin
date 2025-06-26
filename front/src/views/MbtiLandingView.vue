<template>
  <div class="max-w-xl mx-auto py-10 space-y-8">
    <h1 class="text-3xl font-bold text-center">나의 MBTI 유형을 찾아보세요</h1>

    <!-- 질문 1 -->
    <div>
      <p class="font-semibold mb-2">에너지는 어디에서 얻나요?</p>
      <div class="flex gap-4">
        <button @click="selectedIorE = 'I'" :class="buttonClass(selectedIorE, 'I')">I (내향)</button>
        <button @click="selectedIorE = 'E'" :class="buttonClass(selectedIorE, 'E')">E (외향)</button>
      </div>
    </div>

    <!-- 질문 2 -->
    <div>
      <p class="font-semibold mb-2">정보를 어떻게 받아들이나요?</p>
      <div class="flex gap-4">
        <button @click="selectedSorN = 'S'" :class="buttonClass(selectedSorN, 'S')">S (감각)</button>
        <button @click="selectedSorN = 'N'" :class="buttonClass(selectedSorN, 'N')">N (직관)</button>
      </div>
    </div>

    <!-- 질문 3 -->
    <div>
      <p class="font-semibold mb-2">결정은 어떻게 내리나요?</p>
      <div class="flex gap-4">
        <button @click="selectedTorF = 'T'" :class="buttonClass(selectedTorF, 'T')">T (사고)</button>
        <button @click="selectedTorF = 'F'" :class="buttonClass(selectedTorF, 'F')">F (감정)</button>
      </div>
    </div>

    <!-- 질문 4 -->
    <div>
      <p class="font-semibold mb-2">생활 방식은 어떤가요?</p>
      <div class="flex gap-4">
        <button @click="selectedJorP = 'J'" :class="buttonClass(selectedJorP, 'J')">J (계획적)</button>
        <button @click="selectedJorP = 'P'" :class="buttonClass(selectedJorP, 'P')">P (즉흥적)</button>
      </div>
    </div>

    <!-- 완료 버튼 -->
    <div class="text-center mt-6">
      <button
        :disabled="!isComplete"
        @click="goToResult"
        class="px-6 py-3 bg-blue-800 text-white font-semibold rounded hover:bg-blue-700 disabled:opacity-50"
      >
        나의 MBTI로 추천받기
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const selectedIorE = ref('')
const selectedSorN = ref('')
const selectedTorF = ref('')
const selectedJorP = ref('')

const isComplete = computed(() =>
  selectedIorE.value && selectedSorN.value && selectedTorF.value && selectedJorP.value
)

const goToResult = () => {
  const mbti = selectedIorE.value + selectedSorN.value + selectedTorF.value + selectedJorP.value
  router.push({ name: 'MbtiResultView', query: { mbti } })
}

const buttonClass = (current, value) => {
  return `px-4 py-2 rounded border font-semibold ${
    current === value ? 'bg-blue-600 text-white' : 'bg-white text-gray-800'
  }`
}
</script>

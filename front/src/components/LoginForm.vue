<!-- src/components/LoginForm.vue -->
<template>
  <!-- 로그인 폼 전체 컨테이너 -->
  <form @submit.prevent="handleLogin" class="max-w-md mx-auto mt-10 p-6 bg-[#0f172a] text-white shadow-md rounded">
    <h2 class="text-2xl font-bold mb-4 text-center">로그인</h2>

    <!-- 아이디 입력 필드 -->
    <div class="mb-4">
      <label for="username" class="block mb-1 font-semibold">아이디</label>
      <input
        id="username"
        v-model="username"
        placeholder="아이디"
        class="w-full border border-gray-300 rounded px-3 py-2"
      />
    </div>

    <!-- 비밀번호 입력 필드 -->
    <div class="mb-6">
      <label for="password" class="block mb-1 font-semibold">비밀번호</label>
      <input
        id="password"
        type="password"
        v-model="password"
        placeholder="비밀번호"
        class="w-full border border-gray-300 rounded px-3 py-2"
      />
    </div>

    <!-- 로그인 버튼 -->
    <button
      type="submit"
      class="w-full bg-blue-500 text-white py-2 rounded hover:bg-blue-600 transition"
    >
      로그인
    </button>

    <!-- 회원가입으로 이동하는 링크 -->
    <p class="mt-4 text-sm text-center">
      아직 계정이 없으신가요?
      <RouterLink to="/auth/signup" class="text-blue-600 hover:underline ml-1">회원가입</RouterLink>
    </p>
  </form>
</template>

<script setup>
import { ref } from 'vue'
import { useAccountStore } from '@/stores/account'
import { useRouter } from 'vue-router'

// 사용자 입력 상태
const username = ref('')
const password = ref('')

// Pinia 사용자 계정 스토어 및 라우터 객체
const account = useAccountStore()
const router = useRouter()

// 로그인 요청 처리 함수
const handleLogin = () => {
  account.logIn({ username: username.value, password: password.value })
    .then(() => {
      // 로그인 성공 시 홈으로 이동
      router.push('/')
    })
    .catch(() => {
      // 실패 시 별도 처리 없음 (에러 메시지 출력은 생략됨)
    })
}
</script>

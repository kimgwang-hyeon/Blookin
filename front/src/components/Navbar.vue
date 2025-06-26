<!-- src/components/Navbar.vue -->
<template>
  <!-- 내비게이션 바 전체 영역 -->
  <nav class="bg-[#0f172a] text-white shadow-md px-6 py-3 flex justify-between items-center">
    
    <!-- 왼쪽: 로고 및 사이트명 링크 -->
    <RouterLink to="/" class="flex items-center">
      <img src="/src/assets/rabbit-logo.png" alt="로고" class="h-28 w-32 mr-3" />
      <span class="text-3xl font-bold text-white">Blookin</span>
    </RouterLink>

    <!-- 오른쪽: 메뉴 항목들 -->
    <div class="flex items-center gap-6">
      <RouterLink to="/books" class="hover:text-blue-300 text-white">도서</RouterLink>
      <RouterLink to="/threads" class="hover:text-blue-300 text-white">감상글</RouterLink>
      <RouterLink to="/recommend/personal" class="hover:text-blue-300 text-white">추천 도서</RouterLink>

      <!-- 로그인 상태일 때: 프로필 및 로그아웃 버튼 표시 -->
      <template v-if="account.user">
        <RouterLink :to="`/users/${account.user.username}`" class="hover:text-blue-300 text-white">프로필</RouterLink>
        <button
          @click="handleLogout"
          class="border border-white text-white text-sm px-3 py-1 rounded hover:bg-white hover:text-[#0f172a] transition"
        >
          로그아웃
        </button>
      </template>

      <!-- 비로그인 상태일 때: 로그인 버튼 표시 -->
      <template v-else>
        <RouterLink
          to="/auth/login"
          class="border border-white text-white text-sm px-3 py-1 rounded hover:bg-white hover:text-[#0f172a] transition"
        >
          로그인
        </RouterLink>
      </template>
    </div>
  </nav>
</template>

<script setup>
import { useRouter, RouterLink } from 'vue-router'
import { useAccountStore } from '@/stores/account'

// Pinia 계정 스토어 및 라우터 인스턴스 사용
const account = useAccountStore()
const router = useRouter()

// 로그아웃 처리 후 홈으로 이동
const handleLogout = () => {
  account.logout().then(() => {
    router.push('/')
  })
}
</script>

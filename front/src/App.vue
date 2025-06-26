<!-- App.vue -->

<template>
  <div class="flex flex-col min-h-screen">
    <!-- 고정된 상단 네비게이션 -->
    <Navbar />
    
    <main class="flex-grow">
    <!-- 라우터에 따라 바뀌는 화면 -->
      <RouterView />
    </main>

    <!-- 고정된 하단 푸터 -->
    <Footer />
  </div>
</template>

<script setup>
  import Navbar from '@/components/Navbar.vue'
  import Footer from '@/components/Footer.vue'
  import { RouterView } from 'vue-router'
  import { onMounted } from 'vue'
  import { useBookStore } from '@/stores/books'
  import { useThreadStore } from '@/stores/threads'
  import { useAccountStore } from '@/stores/account'

  const bookStore = useBookStore()
  const threadStore = useThreadStore()
  const accountStore = useAccountStore()

  onMounted(() => {
    bookStore.fetchBooks()
    threadStore.fetchThreads()
    accountStore.initAuth()
  })
</script>

<style scoped>
/* 공통 레이아웃에 대한 스타일 */
</style> 

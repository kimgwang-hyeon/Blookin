<!-- src/components/Footer.vue -->
<template>
  <!-- 푸터 영역 전체 배경 및 텍스트 색상 지정 -->
  <footer class="bg-[#0f172a] text-white py-12 px-6 shadow-inner">
    <!-- 최대 너비 제한 및 반응형 컬럼 레이아웃 -->
    <div class="max-w-6xl mx-auto grid grid-cols-1 md:grid-cols-2 gap-8">
      
      <!-- 왼쪽: 회사 소개 및 연락처 -->
      <div>
        <h2 class="text-xl font-semibold mb-3">Blookin</h2>
        <p class="text-sm leading-relaxed text-gray-300">
          감성과 연결되는 책 추천, <br />
          Blookin은 당신의 독서 여정을 함께합니다.
        </p>
        <p class="text-sm mt-4 text-gray-400">이메일: contact@blookin.com</p>
        <p class="text-sm text-gray-400">주소: 서울특별시 어디구 어디로 123</p>
      </div>

      <!-- 오른쪽: 내부 페이지 및 약관 링크 -->
      <div class="text-sm space-y-3">
        <h3 class="font-semibold mb-2">바로가기</h3>
        <ul class="space-y-1 text-gray-300">
          <li><RouterLink to="/" class="hover:underline">홈</RouterLink></li>
          <li><RouterLink to="/mbti" class="hover:underline">MBTI 추천</RouterLink></li>
          <li><RouterLink to="/books" class="hover:underline">도서 목록</RouterLink></li>
          <li><RouterLink to="/threads" class="hover:underline">감상글</RouterLink></li>
          <li>개인정보 처리방침</li>
          <li>이용약관</li>
        </ul>
      </div>
    </div>

    <!-- 하단 카피라이트 표시 -->
    <div class="text-center text-xs text-gray-500 mt-8">
      ⓒ 2025 Blookin. All rights reserved.
    </div>
  </footer>
</template>

<script setup>
// 현재 별도 로직 없음 (정적 컴포넌트)
</script>

<style scoped>
/* scoped 스타일 없음 */
</style>

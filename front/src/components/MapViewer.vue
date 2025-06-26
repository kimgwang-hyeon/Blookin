<!-- src/components/MapViewer.vue -->
<template>
  <div class="map-wrapper">
    <!-- 제목 표시 -->
    <h2><strong>현재 위치 주변 도서관</strong></h2>
    <br>

    <!-- 위치 정보가 확보되면 구글 지도 iframe 표시 -->
    <iframe
      v-if="lat && lng"
      :src="`https://maps.google.com/maps?q=도서관&ll=${lat},${lng}&z=14&output=embed`"
      width="50%"
      height="350"
      style="border:0;"
      allowfullscreen
      loading="lazy"
    ></iframe>

    <!-- 위치 정보가 아직 없는 경우 -->
    <p v-else>현재 위치를 불러오는 중입니다...</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

// 위도, 경도 상태 초기화
const lat = ref(null)
const lng = ref(null)

// 컴포넌트가 마운트되면 브라우저의 위치 정보 API 호출
onMounted(() => {
  navigator.geolocation.getCurrentPosition(
    (pos) => {
      // 성공 시 위도, 경도 저장
      lat.value = pos.coords.latitude
      lng.value = pos.coords.longitude
    },
    (err) => {
      // 실패 시 콘솔에 에러 출력
      console.error('위치 접근 거부:', err)
    }
  )
})
</script>

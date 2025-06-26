<template>
  <div class="bg-[#0f172a] text-white">
    <!-- ✅ Hero 섹션: 배경 이미지 + 왼쪽 배치 큰 텍스트 -->
    <section class="relative w-full h-[600px] overflow-hidden">
      <!-- 어두운 배경 이미지 -->
      <img
        src="/src/assets/background_img.png"
        alt="배경 이미지"
        class="absolute inset-0 w-full h-full object-cover brightness-50 z-0"
      />

      <!-- ⭐️ 별 컨테이너 -->
      <div class="absolute inset-0 z-0 pointer-events-none">
        <div class="star" style="top: 10%; left: 20%;"></div>
        <div class="star" style="top: 30%; left: 80%;"></div>
        <div class="star" style="top: 50%; left: 40%;"></div>
        <div class="star" style="top: 70%; left: 60%;"></div>
        <div class="star" style="top: 85%; left: 15%;"></div>
      </div>


      <!-- 텍스트 + 버튼 -->
      <div class="relative z-10 h-full flex flex-col justify-center pl-16 animate-fade">
        <h1 class="text-white text-[64px] leading-tight font-extrabold tracking-tight drop-shadow-glow">
          Dive into<br />
          Stories<br />
          that See You
        </h1>

        <!-- 버튼 영역 -->
        <div v-if="!account.user" class="mt-8 flex gap-4">
          <!-- SIGN IN: 투명한 흰 테두리 버튼 -->
          <RouterLink to="/auth/login">
            <button class="border border-white text-white text-lg font-semibold px-6 py-3 rounded-lg hover:bg-white hover:text-blue-900 transition">
              로그인
            </button>
          </RouterLink>

          <!-- SIGN UP: 남색 배경 버튼 -->
          <RouterLink to="/auth/signup">
            <button class="border border-white bg-blue-1000 text-white text-lg font-semibold px-6 py-3 rounded-lg shadow-md hover:bg-blue-800 transition">
              회원가입
            </button>
          </RouterLink>
        </div>
      </div>
    </section>

    <!-- ✅ MBTI 추천 배너 -->
    <section class="max-w-5xl mx-auto mt-16 px-4 animate-fade">
      <div class="bg-blue-1000 text-white p-8 rounded-xl shadow-lg flex flex-col md:flex-row items-center justify-between gap-6">
        <div>
          <h2 class="text-2xl font-bold mb-2">MBTI로 책을 추천받아보세요!</h2>
          <p class="text-sm opacity-90">당신의 성격에 꼭 맞는 책을 큐레이션해드립니다.</p>
        </div>
        <RouterLink to="/mbti">
          <button class="text-white border px-6 py-3 rounded-lg font-semibold hover:bg-blue-200 transition">
            MBTI 테스트 시작하기 →
          </button>
        </RouterLink>
      </div>
    </section>

    <!-- 베스트셀러 -->
    <section class="max-w-5xl mx-auto my-16 px-4 animate-fade">
      <BestsellerCarousel :books="bestsellers" />
    </section>

    <!-- 좋아요를 많이 받은 스레드 -->
    <section v-if="topLikedThreads.length" class="max-w-5xl mx-auto my-16 px-4 animate-fade">
    <h2 class="text-3xl font-bold mb-6 text-center">인기글</h2>
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
      <ThreadCard
        v-for="thread in topLikedThreads"
        :key="thread.id"
        :thread="thread"
      />
      </div>
    </section>

    <!-- 장르별 도서 목록 -->
    <section class="max-w-5xl mx-auto px-4 animate-fade">
      <h2 class="text-3xl font-bold mb-6 text-center">카테고리</h2>
      <div class="grid grid-cols-2 md:grid-cols-4 gap-6">
        <div
          v-for="category in categories"
          :key="category.id"
          @click="goToCategory(category.id)"
          class="cursor-pointer rounded-lg overflow-hidden shadow hover:shadow-lg transition"
        >
          <img
            :src="getCategoryImagePath(category.id)"
            alt="카테고리 이미지"
            class="w-full h-40 object-cover"
          />
        </div>
      </div>
    </section>


  </div>
</template>

<script setup>
import Navbar from '@/components/Navbar.vue'
import { useAccountStore } from '@/stores/account'
import BestsellerCarousel from '@/components/BestsellerCarousel.vue'
import { ref, onMounted, computed } from 'vue'
import axios from '@/lib/axios'
import { useRouter } from 'vue-router'
import { useThreadStore } from '@/stores/threads'
import ThreadCard from '@/components/ThreadCard.vue'

const account = useAccountStore()
const threadStore = useThreadStore()

const router = useRouter()
const bestsellers = ref([])

const categories = ref([
  { id: 1, name: '문학·에세이·만화', image: '/src/assets/categories/literature.jpg' },
  { id: 2, name: '경제·경영', image: '/src/assets/categories/economy.jpg' },
  { id: 3, name: '자기계발', image: '/src/assets/categories/selfdev.jpg' },
  { id: 4, name: '인문·사회', image: '/src/assets/categories/humanities.jpg' },
  { id: 5, name: '과학·IT', image: '/src/assets/categories/science.jpg' },
  { id: 6, name: '어린이·청소년', image: '/src/assets/categories/kids.jpg' },
  { id: 7, name: '취미·실용·여행', image: '/src/assets/categories/hobby.jpg' },
  { id: 8, name: '학습·참고서', image: '/src/assets/categories/study.jpg' },
])

const goToCategory = (id) => {
  router.push({
    path: '/books',
    query: {
      q: '',
      ordering: '-pub_date',
      category: String(id),
    },
  })
}


const getCategoryImagePath = (id) => {
  const paddedId = String(id).padStart(2, '0')
  return new URL(`../assets/category_img/cate_${paddedId}.png`, import.meta.url).href
}


onMounted(() => {
  axios.get('/books/?ordering=-customer_review_rank').then(res => {
    bestsellers.value = res.data.slice(0, 12)
  })
})

const topLikedThreads = computed(() => {
  return [...threadStore.threads]
    .sort((a, b) => Number(b.likes_count || 0) - Number(a.likes_count || 0))
    .slice(0, 6)
})
</script>

<style scoped>
/* 텍스트에 빛나는 느낌의 그림자 */
.drop-shadow-glow {
  text-shadow: 0 0 10px rgba(255, 255, 255, 0.9),
               0 0 30px rgba(255, 255, 255, 0.7);
}

/* 부드러운 진입 애니메이션 */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
.animate-fade {
  animation: fadeInUp 1.2s ease-out forwards;
}

/* ⭐️ 반짝이는 별 효과 */
.star {
  position: absolute;
  width: 3px;
  height: 3px;
  background-color: white;
  border-radius: 50%;
  opacity: 0.7;
  animation: twinkle 2s infinite ease-in-out;
}

/* ⭐️ 반짝임 애니메이션 */
@keyframes twinkle {
  0%, 100% { opacity: 0.2; transform: scale(1); }
  50% { opacity: 1; transform: scale(1.4); }
}
</style>

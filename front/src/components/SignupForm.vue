<!-- components.SignupForm.vue -->
 
<template>
  <form @submit.prevent="handleSignup" class="max-w-md mx-auto mt-10 p-6 bg-[#0f172a] text-white shadow-md rounded">
    <h2 class="text-2xl font-bold mb-2 text-center">회원가입</h2>

    <p class="text-sm text-gray-300 text-center mb-6">
      아이디, 비밀번호, 비밀번호 확인을 제외한 모든 항목은 선택 입력입니다.
    </p>

    <div class="mb-4">
      <label for="username" class="block mb-1 font-semibold">아이디</label>
      <input id="username" v-model="form.username" class="w-full border rounded px-3 py-2" />
    </div>

    <div class="mb-4">
      <label for="password1" class="block mb-1 font-semibold">비밀번호</label>
      <input id="password1" v-model="form.password1" type="password" class="w-full border rounded px-3 py-2" />
    </div>

    <div class="mb-4">
      <label for="password2" class="block mb-1 font-semibold">비밀번호 확인</label>
      <input id="password2" v-model="form.password2" type="password" class="w-full border rounded px-3 py-2" />
    </div>

    <div class="mb-4">
      <label for="email" class="block mb-1 font-semibold">
        이메일 <span class="font-normal text-gray-300">(선택)</span>
      </label>
      <input id="email" v-model="form.email" type="email" class="w-full border rounded px-3 py-2" />
    </div>

    <div class="mb-4">
      <label for="first_name" class="block mb-1 font-semibold">
        이름 <span class="font-normal text-gray-300">(선택)</span>
      </label>
      <input id="first_name" v-model="form.first_name" class="w-full border rounded px-3 py-2" />
    </div>

    <div class="mb-4">
      <label for="last_name" class="block mb-1 font-semibold">
        성 <span class="font-normal text-gray-300">(선택)</span>
      </label>
      <input id="last_name" v-model="form.last_name" class="w-full border rounded px-3 py-2" />
    </div>

    <div class="mb-4">
      <label class="block mb-1 font-semibold">
        성별 <span class="font-normal text-gray-300">(선택)</span>
      </label>
      <select v-model="form.gender" class="w-full border rounded px-3 py-2 bg-[#0f172a] text-white">
        <option value="">선택 안 함</option>
        <option value="M">남성</option>
        <option value="F">여성</option>
      </select>
    </div>

    <div class="mb-4">
      <label class="block mb-1 font-semibold">
        나이 <span class="font-normal text-gray-300">(선택)</span>
      </label>
      <input v-model="form.age" type="number" class="w-full border rounded px-3 py-2" />
    </div>

    <div class="mb-4">
      <label class="block mb-1 font-semibold">
        주간 평균 독서 시간 (분) <span class="font-normal text-gray-300">(선택)</span>
      </label>
      <input v-model="form.weekly_reading_time" type="number" class="w-full border rounded px-3 py-2" />
    </div>

    <div class="mb-4">
      <label class="block mb-1 font-semibold">
        연간 독서량 <span class="font-normal text-gray-300">(선택)</span>
      </label>
      <input v-model="form.yearly_reading_volume" type="number" class="w-full border rounded px-3 py-2" />
    </div>

    <div class="mb-4">
      <label class="block mb-1 font-semibold">
        프로필 이미지 <span class="font-normal text-gray-300">(선택)</span>
      </label>
      <input
        type="file"
        accept="image/*"
        @change="onFileChange"
        class="w-full border rounded px-3 py-2"
      />
    </div>
    <div class="mb-4">
      <label class="block mb-1 font-semibold">
        관심 장르 (다중 선택) <span class="font-normal text-gray-300">(선택)</span>
      </label>
      <p class="text-sm text-gray-300 mb-2">도서 추천을 위해 선택해주시길 권장합니다.</p>
      <div class="flex flex-wrap gap-3">
        <label v-for="genre in bookStore.categories" :key="genre.id" class="flex items-center space-x-1">
          <input
            type="checkbox"
            :value="genre.id"
            v-model="form.interested_genres"
            class="accent-blue-500"
          />
          <span>{{ genre.name }}</span>
        </label>
      </div>
    </div>

    <button type="submit" class="w-full bg-blue-500 text-white py-2 rounded hover:bg-blue-600">
      회원가입
    </button>
  </form>
</template>


<script setup>
import { reactive, ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { useAccountStore } from '@/stores/account'
import { useBookStore } from '@/stores/books'

const router = useRouter()
const account = useAccountStore()
const bookStore = useBookStore()

// 관심 장르 선택 옵션
const genreOptions = ref([])

// 회원가입 입력 폼 상태
const form = reactive({
  username: '',
  email: '',
  password1: '',
  password2: '',
  first_name: '',
  last_name: '',
  gender: '',
  age: null,
  weekly_reading_time: null,
  yearly_reading_volume: null,
  interested_genres: [],   // [1, 3, 4]
  profile_image: null,
})

const onFileChange = (e) => {
  const file = e.target.files[0]
  if (file) {
    form.profile_image = file
    console.log('선택된 프로필 이미지:', file.name)
  }
}

const handleSignup = () => {
  account.signUp(form)
    .then(() => {
      router.push('/')
    })
    .catch((err) => {
      console.error('회원가입 실패:', err.response?.data)
      alert('회원가입에 실패했습니다.')
    })
}


onMounted(() => {
  if (!bookStore.categories.length) {
    bookStore.fetchCategories()
  }
})

</script>

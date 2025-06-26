<!-- components/ProfileEditModal.vue -->
<template>
  <!-- 모달 창 전체 (가운데 정렬된 고정 위치) -->
  <div class="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2
              bg-black z-50 w-[600px] h-[1000px] rounded-lg
              flex items-center justify-center">
    <div class="p-6 rounded-xl shadow max-w-lg w-full">
      <h2 class="text-xl font-semibold mb-4 text-center">회원정보 수정</h2>

      <!-- 이름 입력 -->
      <div class="mb-3">
        <label class="block mb-1 font-semibold">이름</label>
        <input v-model="localUser.first_name" class="w-full border rounded px-3 py-2" />
      </div>

      <!-- 성 입력 -->
      <div class="mb-3">
        <label class="block mb-1 font-semibold">성</label>
        <input v-model="localUser.last_name" class="w-full border rounded px-3 py-2" />
      </div>

      <!-- 이메일 입력 -->
      <div class="mb-3">
        <label class="block mb-1 font-semibold">이메일</label>
        <input v-model="localUser.email" class="w-full border rounded px-3 py-2" />
      </div>

      <!-- 성별 선택 -->
      <div class="mb-3">
        <label class="block mb-1 font-semibold">성별</label>
        <select v-model="localUser.gender" class="w-full border rounded px-3 py-2 bg-black text-white">
          <option value="">선택 안 함</option>
          <option value="M">남성</option>
          <option value="F">여성</option>
        </select>
      </div>

      <!-- 나이 입력 -->
      <div class="mb-3">
        <label class="block mb-1 font-semibold">나이</label>
        <input type="number" v-model.number="localUser.age" class="w-full border rounded px-3 py-2" />
      </div>

      <!-- 주간 평균 독서 시간 입력 -->
      <div class="mb-3">
        <label class="block mb-1 font-semibold">주간 평균 독서 시간 (분)</label>
        <input type="number" v-model.number="localUser.weekly_reading_time" class="w-full border rounded px-3 py-2" />
      </div>

      <!-- 연간 독서량 입력 -->
      <div class="mb-3">
        <label class="block mb-1 font-semibold">연간 독서량</label>
        <input type="number" v-model.number="localUser.yearly_reading_volume" class="w-full border rounded px-3 py-2" />
      </div>

      <!-- 프로필 이미지 업로드 -->
      <div class="mb-3">
        <label class="block mb-1 font-semibold">프로필 이미지</label>
        <input type="file" @change="handleImageUpload" class="w-full border rounded px-3 py-2" />
      </div>

      <!-- 저장 / 취소 버튼 -->
      <div class="flex justify-end gap-2 mt-4">
        <button @click="$emit('cancel')" class="bg-red-500 hover:bg-red-600 text-white px-4 py-1 rounded">취소</button>
        <button @click="handleConfirm" class="bg-blue-500 hover:bg-blue-600 text-white px-4 py-1 rounded">저장</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
import axios from '@/lib/axios'

// props: 외부에서 전달받은 사용자 정보
const props = defineProps({
  user: {
    type: Object,
    required: true,
  }
})

// confirm(저장), cancel(취소) 이벤트 전달
const emit = defineEmits(['confirm', 'cancel'])

const localUser = ref({})
const categories = ref([])

// props.user가 변경되면 localUser에 복사
watch(
  () => props.user,
  (newUser) => {
    localUser.value = { ...newUser }
  },
  { immediate: true, deep: true }
)

// 이미지 선택 시 파일 객체 저장
const handleImageUpload = (e) => {
  localUser.value.profile_image = e.target.files[0]
}

// 저장 버튼 클릭 시 실행되는 함수
const handleConfirm = () => {
  const formData = new FormData()
  formData.append('username', localUser.value.username)

  for (const key in localUser.value) {
    if (key === 'username') continue

    if (key === 'interested_genres') {
      // 배열로 전송해야 하는 필드는 반복 append
      localUser.value[key].forEach(id => {
        formData.append('interested_genres', id)
      })
    } else if (key === 'profile_image') {
      if (localUser.value.profile_image instanceof File) {
        formData.append('profile_image', localUser.value.profile_image)
      }
    } else {
      formData.append(key, localUser.value[key])
    }
  }

  axios.patch(`/accounts/${localUser.value.username}/edit/`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
  .then(() => {
    alert('회원 정보가 수정되었습니다.')
    emit('confirm')
    emit('cancel')  // 수정 완료 후 모달 닫기
  })
  .catch((err) => {
    console.error('[회원정보 수정 실패]', err.response?.data || err)
    alert('수정 중 오류가 발생했습니다.')
  })
}

// 컴포넌트 로딩 시 카테고리 목록 불러오기
onMounted(() => {
  axios.get('/books/categories/')
    .then(res => categories.value = res.data)
})
</script>

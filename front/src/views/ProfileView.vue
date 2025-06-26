<template>
  <div class="min-h-screen flex flex-col items-center bg-[#0f172a] text-white px-4 py-10">
    <div class="w-full max-w-7xl grid grid-cols-1 lg:grid-cols-3 gap-8 bg-[#0f172a] text-white shadow-lg rounded-xl p-8">
      <!-- 프로필 카드 -->
      <div class="flex items-start justify-center">
        <div class="max-w-md p-6 text-center relative ">
          <img
            :src="profileUser.profile_image ? profileUser.profile_image : 'http://127.0.0.1:8000/media/profile_image/default.png'"
            class="w-40 h-40 rounded-full mx-auto mb-4 object-cover"
          />
          <h2 class="text-xl font-bold mb-1">{{ profileUser.full_name }}</h2>
          <p class="text-sm text-gray-500 mb-2">@{{ profileUser.username }}</p>
          <p class="text-sm text-gray-600 mb-1">{{ profileUser.email }}</p>
          <p class="text-sm">성별: {{ profileUser.gender === 'M' ? '남성' : profileUser.gender === 'F' ? '여성' : '비공개' }}</p>
          <p class="text-sm">나이: {{ profileUser.age }}</p>
          <p class="text-sm">주간 독서 시간: {{ profileUser.weekly_reading_time }}시간</p>
          <p class="text-sm">연간 독서량: {{ profileUser.yearly_reading_volume }}권</p>
          <p class="text-sm mt-2 text-gray-600">관심 장르: {{ profileUser.interested_genres?.join(', ') }}</p>

          <div class="mt-4 text-sm">
            <p>팔로워: {{ followersCount }}</p>
            <p>팔로잉: {{ profileUser.followings_count }}</p>
          </div>

          <button
            v-if="account.isLoggedIn && isOtherUser"
            @click="toggleFollow"
            class="mt-4 px-4 py-2 rounded text-white w-full"
            :class="isFollowing ? 'bg-gray-500' : 'bg-blue-500'"
          >
            {{ isFollowing ? '언팔로우' : '팔로우' }}
          </button>
          <br>
          <button
            v-if="account.isLoggedIn && !isOtherUser"
            @click="openEditModal"
            class="text-sm text-blue-600 border border-blue-600 px-6 py-2 rounded hover:bg-blue-50"
          >
            회원정보 수정
          </button>
        </div>
      </div>

      <!-- 오른쪽: 서재 + 스레드 -->
      <div class="lg:col-span-2 flex flex-col gap-8">
        <div class="flex items-center justify-between">
          <h2 class="text-xl font-semibold mb-3">내 서재</h2>

        </div>
        <div v-if="likedBooks.length" class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-2 gap-x-6 gap-y-8">
          <BookCard
            v-for="book in likedBooks"
            :key="book.id"
            :book="book"
          />
        </div>


        <div>
          <h2 class="text-xl font-semibold mb-3">작성한 감상글</h2>
          <ul class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-2 gap-4">
            <li
              v-for="thread in threads"
              :key="thread.id"
              class="bg-white shadow rounded-lg overflow-hidden hover:shadow-md transition"
            >
              <router-link :to="`/threads/${thread.id}`" class="block h-full">
                <img
                  v-if="thread.cover_img"
                  :src="`http://localhost:8000${thread.cover_img.replace(/\\/g, '/')}`"
                  alt="cover"
                  class="w-full h-40 object-cover"
                />
                <div class="p-4 space-y-1">
                  <h3 class="text-lg font-semibold truncate">{{ thread.title }}</h3>
                  <p class="text-sm text-gray-600 line-clamp-2">{{ thread.content }}</p>
                  <p class="text-xs text-gray-400 mt-1">{{ new Date(thread.created_at).toLocaleDateString() }}</p>
                </div>
              </router-link>
            </li>
          </ul>
        </div>
      </div>
    </div>

    <div v-if="account.isLoggedIn && !isOtherUser" class="mt-12">
      <button
        @click="deleteAccount"
        class="text-sm text-red-600 border border-red-600 px-6 py-2 rounded hover:bg-red-50"
      >
        회원 탈퇴
      </button>
    </div>

    <ProfileEditModal
      v-if="isEditModalOpen"
      :user="profileUser"
      @confirm="handleAfterEdit"
      @cancel="isEditModalOpen = false"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from '@/lib/axios'
import { useAccountStore } from '@/stores/account'
import ProfileEditModal from '@/components/ProfileEditModal.vue'
import BookCard from '@/components/BookCard.vue'

const route = useRoute()
const router = useRouter()
const account = useAccountStore()

const profileUser = ref({})
const threads = ref([])
const isFollowing = ref(false)
const followersCount = ref(0)
const likedBooks = ref([])
const isEditModalOpen = ref(false)

const isOtherUser = computed(() => {
  return profileUser.value.username && profileUser.value.username !== account.user?.username
})

const fetchProfile = () => {
  axios.get(`/accounts/${route.params.userId}/`)
    .then(res => {
      profileUser.value = res.data.user
      threads.value = res.data.threads
      isFollowing.value = res.data.user.is_following
      followersCount.value = res.data.user.followers_count
      likedBooks.value = res.data.liked_books
    })
    .catch(err => console.error('프로필 API 오류:', err))
}

const toggleFollow = () => {
  axios.post(`/accounts/${route.params.userId}/follow/`)
    .then(res => {
      isFollowing.value = res.data.followed
      followersCount.value = res.data.followers_count
    })
    .catch(err => console.error('팔로우 요청 오류:', err))
}

const openEditModal = () => {
  isEditModalOpen.value = true
}

const handleUpdate = (updatedUser) => {
  profileUser.value = updatedUser  // 바로 반영
  isEditModalOpen.value = false
  alert('회원정보가 수정되었습니다.')
}

const fetchCurrentUser = () => {
  axios.get('/accounts/user/').then(res => {
    account.user = res.data
  })
}


const deleteAccount = () => {
  if (!confirm('정말로 탈퇴하시겠습니까? 이 작업은 되돌릴 수 없습니다.')) return

  account.deleteAccount(profileUser.value.username)
    .then(() => {
      router.push('/')
    })
    .catch(() => {
      // 실패 시 메시지는 store에 있으므로 생략 가능
    })
}

const handleAfterEdit = () => {
  fetchProfile()
  fetchCurrentUser() 
  isEditModalOpen.value = false
}

onMounted(fetchProfile)
</script>

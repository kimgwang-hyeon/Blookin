<!-- views/ThreadDetailView.vue -->
<template>
  <div class="p-6 max-w-3xl mx-auto">
    <div v-if="thread">
      <div class="bg-gray-800 rounded-xl mt-8 p-4 bg-gray- rounded-xl shadow gap-4 items-start">
        <h1 class="text-3xl font-bold mb-2">{{ thread.title }}</h1>
        <img
          v-if="thread.cover_img"
          :src="`http://localhost:8000${thread.cover_img.replace(/\\/g, '/')}`"
          alt="스레드 커버 이미지"
          class="w-full max-h-96 object-cover rounded-lg mb-4 shadow"
        />
        <!-- 좋아요 버튼 -->
        <div class="mt-4">
          <button @click="toggleLike" class="text-red-500 hover:text-red-600">
            ❤️ 좋아요 {{ thread.likes_count }}
          </button>
        </div>
        <div class="bg-[#0f172a] rounded-xl my-4 p-4 bg-gray- rounded-xl shadow gap-4 items-start">
          <p class="my-2 text-white whitespace-pre-line">{{ thread.content }}</p>
        </div>
      </div>

      <!-- 스레드 수정/삭제 버튼 -->
      <div class="mt-4 flex gap-2" v-if="thread.user_info?.username === currentUser">
        <button @click="isEditModalOpen = true" class="text-sm text-blue-600 hover:underline">수정</button>
        <button @click="isDeleteModalOpen = true" class="text-sm text-red-600 hover:underline">삭제</button>
      </div>

      <ThreadModal
        v-if="isEditModalOpen"
        mode="edit"
        :title="thread.title"
        :content="thread.content"
        @cancel="isEditModalOpen = false"
        @confirm="submitEdit"
      />

      <ThreadModal
        v-if="isDeleteModalOpen"
        mode="delete"
        @cancel="isDeleteModalOpen = false"
        @confirm="submitDelete"
      />

      <!-- 댓글 목록 및 작성 -->
      <div class="mt-8">
        <h2 class="text-lg font-semibold mb-2">댓글</h2>
        <ul class="space-y-2">
          <li
            v-for="comment in thread.comments"
            :key="comment.id"
            class="border p-2 rounded flex justify-between items-center"
          >
            <p class="text-sm">{{ comment.user }}: {{ comment.content }}</p>
            <!-- 댓글 삭제 버튼 (본인 댓글일 경우에만 표시) -->
            <button
              v-if="comment.user === currentUser"
              @click="openDeleteCommentModal(comment.id)"
              class="text-xs text-red-500 hover:underline ml-2"
            >
              삭제
            </button>
          </li>
        </ul>

        <form @submit.prevent="submitComment" class="mt-4 flex gap-2">
          <input
            v-model="newComment"
            type="text"
            placeholder="댓글을 입력하세요"
            class="flex-1 border rounded px-2 py-1"
          />
          <button class="bg-blue-500 text-white px-4 py-1 rounded hover:bg-blue-600">작성</button>
        </form>
      </div>

      <!-- 작성자 정보 영역 -->
      <div class="mt-6 p-4 bg-gray-800 rounded-xl shadow flex items-center justify-between">
        <div class="flex items-center gap-4">
          <img
          :src="thread.user_info.profile_image 
            ? `http://127.0.0.1:8000${thread.user_info.profile_image}` 
            : 'http://127.0.0.1:8000/media/profile_image/default.png'"
            alt="작성자 프로필"
            class="w-12 h-12 rounded-full object-cover"
          />
          <span class="text-lg font-semibold text-white">{{ thread.user_info.username }}</span>
        </div>

        <div class="flex gap-2">
          <button
            v-if="thread.user_info?.username !== currentUser"
            @click="toggleFollow"
            class="text-white-500 px-3 py-1 rounded hover:bg-blue-500 hover:text-white transition"
          >
            {{ isFollowing ? '언팔로우' : '+ 팔로우' }}
          </button>
          <router-link
            :to="`/users/${thread.user_info.username}`"
            class="bg-[#0f172a] text-white px-3 py-1 rounded hover:bg-gray-500"
          >
            프로필가기
          </router-link>
        </div>
      </div>

      <router-link
        :to="`/books/${thread.book_info.id}`"
        class="text-white hover:underline"
      >
        <div class="mt-8 p-4 bg-gray- rounded-xl shadow flex gap-4 items-start">
          <img
            :src="thread.book_info.cover"
            alt="책 표지"
            class="w-28 h-40 object-cover rounded-md shadow-md"
          />
          <div class="flex flex-col justify-between">
            <h3 class="text-xl font-bold mb-1">{{ thread.book_info.title.split('-')[0] }}</h3>
            <p class="text-m text-gray-400 mb-1">"{{ thread.book_info.title.split('-')[1] }}""</p>
            <p class="text-gray-400 mb-1 mt-3">{{ thread.book_info.author }} | {{ thread.book_info.publisher }}</p>

          </div>
        </div>
      </router-link>
    </div>

    <div v-else class="text-center text-gray-500">로딩 중...</div>

    <!-- 댓글 삭제 확인 모달 -->
    <div
      v-if="isCommentDeleteModalOpen"
      class="fixed inset-0 z-50 bg-black bg-opacity-50 flex items-center justify-center"
    >
      <div class="bg-white p-6 rounded shadow max-w-sm w-full space-y-4 text-center">
        <p class="text-gray-800 text-lg font-semibold">댓글을 삭제하시겠습니까?</p>
        <div class="flex justify-center gap-4">
          <button
            @click="isCommentDeleteModalOpen = false"
            class="px-4 py-2 bg-gray-300 rounded hover:bg-gray-400"
          >
            취소
          </button>
          <button
            @click="confirmDeleteComment"
            class="px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600"
          >
            삭제
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref, watch, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useThreadStore } from '@/stores/threads'
import { useAccountStore } from '@/stores/account'
import ThreadModal from '@/components/ThreadModal.vue'
import axios from '@/lib/axios'

// route, router
const route = useRoute()
const router = useRouter()

// 스토어
const threadStore = useThreadStore()
const accountStore = useAccountStore()

// 상태 변수
const thread = computed(() => threadStore.selectedThread)
const currentUser = computed(() => accountStore.user?.username)
const newComment = ref('')
const isEditModalOpen = ref(false)
const isDeleteModalOpen = ref(false)

// 댓글 삭제 모달 상태
const isCommentDeleteModalOpen = ref(false)
const commentToDeleteId = ref(null)

// 팔로우 상태
const isFollowing = ref(false)

// fetch thread
const fetchThread = () => {
  const threadId = route.params.threadId
  if (threadId) threadStore.fetchThreadDetail(threadId)
}

// 좋아요
const toggleLike = () => {
  const threadId = route.params.threadId
  threadStore.toggleLike(threadId)
}

// 댓글 작성
const submitComment = () => {
  const threadId = route.params.threadId
  if (newComment.value.trim()) {
    threadStore.createComment(threadId, newComment.value)
    newComment.value = ''
  }
}

// 댓글 삭제 모달 열기
const openDeleteCommentModal = (commentId) => {
  commentToDeleteId.value = commentId
  isCommentDeleteModalOpen.value = true
}

// 댓글 삭제 확정 요청
const confirmDeleteComment = () => {
  if (!commentToDeleteId.value) return

  axios
    .delete(`/threads/comments/${commentToDeleteId.value}/`)
    .then(() => {
      isCommentDeleteModalOpen.value = false
      commentToDeleteId.value = null
      fetchThread()
    })
    .catch((err) => {
      console.error('댓글 삭제 실패:', err)
      isCommentDeleteModalOpen.value = false
    })
}

// 스레드 수정
const submitEdit = (data) => {
  threadStore.updateThread(route.params.threadId, data)
    .then(() => {
      isEditModalOpen.value = false
      fetchThread()
    })
}

// 스레드 삭제
const submitDelete = () => {
  threadStore.deleteThread(route.params.threadId)
    .then(() => {
      isDeleteModalOpen.value = false
      router.push('/threads')
    })
}

// 팔로우 토글
const toggleFollow = () => {
  const username = thread.value.user_info.username
  axios.post(`/accounts/${username}/follow/`)
    .then(res => {
      isFollowing.value = res.data.is_following
    })
    .catch(err => {
      console.error('팔로우 토글 실패:', err)
    })
}

// 날짜 포맷
const formatDate = (iso) => {
  return new Date(iso).toLocaleDateString('ko-KR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

// 최초 진입 및 threadId 변경 시 fetch
onMounted(fetchThread)
watch(() => route.params.threadId, fetchThread)
</script>

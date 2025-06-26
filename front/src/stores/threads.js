// stores/thread.js

import { ref, watch } from 'vue'
import { defineStore } from 'pinia'
import axios from '../lib/axios'

export const useThreadStore = defineStore('thread', () => {
  const THREAD_API_URL = 'threads'

  const threads = ref([])
  const selectedThread = ref(null)
  const categories = ref([])
  const selectedCategory = ref('')
  const sortOption = ref('-created_at')

  const CACHE_DURATION = 1000 * 60 * 5  // 5분
  
  // 감상글 목록 가져오기

  const fetchThreads = ({ q = '', category = '', ordering = '-created_at' } = {}) => {
    console.log('[fetchThreads] 호출됨 with:', { q, category, ordering })

    return axios.get('threads', {
      params: { q, category, ordering },
    })
      .then((res) => {
        console.log('[fetchThreads] 성공:', res.data)
        threads.value = res.data
      })
      .catch((err) => {
        console.error('[fetchThreads] 실패:', err)
        throw err
      })
  }


  const fetchCategories = () => {
    console.log('[fetchCategories] 호출됨')
    return axios.get('books/categories')  // 🔁 책 카테고리와 공유하는 API
      .then((res) => {
        console.log('[fetchCategories] 성공:', res.data)
        categories.value = res.data
      })
      .catch((err) => {
        console.error('[fetchCategories] 실패:', err)
        throw err
      })
  }


  // 감상글 작성
  const createThread = (payload, token) => {
    console.log('[createThread] payload:', payload)
    return axios.post(`${THREAD_API_URL}/`, payload, {
      headers: {
        Authorization: `Token ${token}`,
      }
    })
      .then(res => {
        const newThread = res.data          // ← ① 서버가 새 쓰레드 반환한다고 가정
      // 1) 현재 메모리 목록에 추가
      threads.value.unshift(newThread)

      // 2) 해당 카테고리 캐시 key 무효화
      const catKey = `threads_${newThread.book_info?.category?.id || 'all'}_*`
      Object.keys(localStorage)
        .filter(k => k.startsWith(catKey))
        .forEach(k => localStorage.removeItem(k))

      // 3) 전체(all) 캐시도 무효화
      Object.keys(localStorage)
        .filter(k => k.startsWith('threads_all'))
        .forEach(k => localStorage.removeItem(k))

        console.log('[createThread] 성공:', newThread)
        return newThread               // 필요하면 라우터에서 await
      })

      .catch(err => {
        console.error('[createThread] 실패:', err)
        throw err
      })
  }

  // 감상글 상세 정보
  const fetchThreadDetail = (threadId) => {
    console.log('[fetchThreadDetail] threadId:', threadId)
    return axios.get(`${THREAD_API_URL}/${threadId}/`)
      .then(res => {
        console.log('[fetchThreadDetail] 성공:', res.data)
        selectedThread.value = res.data
      })
      .catch(err => {
        console.error('[fetchThreadDetail] 실패:', err)
        throw err
      })
  }

  // 좋아요 토글
  const toggleLike = (threadId) => {
    console.log('[toggleLike] threadId:', threadId)
    return axios.post(`${THREAD_API_URL}/${threadId}/like/`)
      .then(res => {
        console.log('[toggleLike] 성공:', res.data)
        selectedThread.value.likes_count = res.data.likes_count
      })
      .catch(err => {
        console.error('[toggleLike] 실패:', err)
        throw err
      })
  }

  // 댓글 생성
  const createComment = (threadId, content) => {
    console.log('[createComment] threadId:', threadId, 'content:', content)
    return axios.post(`${THREAD_API_URL}/${threadId}/comments/`, { content })
      .then(res => {
        console.log('[createComment] 성공:', res.data)
        selectedThread.value.comments.push(res.data)
      })
      .catch(err => {
        console.error('[createComment] 실패:', err)
        throw err
      })
  }

  // 감상글 수정
  const updateThread = (threadId, data) => {
    console.log('[updateThread] 호출됨:', threadId, data)
    return axios.put(`${THREAD_API_URL}/${threadId}/`, data)
      .then(res => {
        console.log('[updateThread] 성공:', res.data)
        selectedThread.value = res.data
      })
      .catch(err => {
        console.error('[updateThread] 실패:', err)
        throw err
      })
  }

  // 감상글 삭제
  const deleteThread = (threadId) => {
    console.log('[deleteThread] 호출됨:', threadId)
    return axios.delete(`${THREAD_API_URL}/${threadId}/`)
      .then(res => {
        console.log('[deleteThread] 성공:', res.data)
      })
      .catch(err => {
        console.error('[deleteThread] 실패:', err)
        throw err
      })
  }

  return {
    threads,
    selectedThread,
    categories,
    fetchCategories,
    fetchThreads,
    createThread,
    fetchThreadDetail,
    toggleLike,
    createComment,
    updateThread,
    selectedCategory,
    deleteThread
  }
}, {
  persist: true
})

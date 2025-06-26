// stores/books.js

import { ref } from 'vue'
import { defineStore } from 'pinia'
import axios from '../lib/axios'

export const useBookStore = defineStore('books', () => {
  const BOOK_API_URL = 'books'
  const CATEGORY_API_URL = 'books/categories'

  // 상태
  const books = ref([])
  const categories = ref([])
  const selectedBook = ref(null)
  const initialized = ref(false)

  // 도서 목록 가져오기
  const fetchBooks = ({ q = '', category = '', ordering = '-pub_date' } = {}) => {
    console.log('[fetchBooks] 호출됨 with:', { q, category, ordering })

    return axios.get(BOOK_API_URL, {
      params: { q, category, ordering }
    })
      .then((res) => {
        console.log('[fetchBooks] 성공:', res.data)
        books.value = res.data
      })
      .catch((err) => {
        console.error('[fetchBooks] 실패:', err)
        throw err
      })
  }



  // 도서 상세 정보 가져오기 (+ 작가 AI 정보, 이미지, TTS 포함)

  const fetchBookDetail = (bookId) => {
    console.log('[fetchBookDetail] 호출됨 with bookId:', bookId)
    return axios.get(`${BOOK_API_URL}/${bookId}/`)
      .then((res) => {
        console.log('[fetchBookDetail] 성공:', res.data)
        selectedBook.value = {
          ...res.data,
          // media 경로가 상대경로일 경우 Vue에서 사용할 수 있게 처리
          author_profile_img_url: res.data.author_profile_img ? `/media/${res.data.author_profile_img}` : null,
          tts_audio_url: res.data.tts_audio ? `/media/${res.data.tts_audio}` : null,
        }
      })
      .catch((err) => {
        console.error('[fetchBookDetail] 실패:', err)
        throw err
      })
  }

  // 카테고리 목록 가져오기
  const fetchCategories = () => {
    console.log('[fetchCategories] 호출됨')
    return axios.get(CATEGORY_API_URL)
      .then((res) => {
        console.log('[fetchCategories] 성공:', res.data)
        categories.value = res.data
      })
      .catch((err) => {
        console.error('[fetchCategories] 실패:', err)
        throw err
      })
  }

  // MBTI 도서 추천 함수
  const fetchBooksByMbti = (mbti) => {
    return axios.get(`/books/recommend/mbti/?mbti=${mbti}`)
      .then(res => {
        books.value = res.data
      })
      .catch(err => {
        console.error('[MBTI 추천 실패]', err)
        throw err
      })
  }

  return {
    books,
    categories,
    selectedBook,
    fetchBooks,
    fetchBookDetail,
    fetchCategories,
    initialized, 
    fetchBooksByMbti,
  }
}, {
  persist: true
})

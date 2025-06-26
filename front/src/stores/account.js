// stores/account.js

import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from '../lib/axios'

export const useAccountStore = defineStore('account', () => {
  const ACCOUNT_API_URL = 'accounts'

  // 상태
  const token = ref('')
  const user = ref(null)

  // 회원가입
  const signUp = (userData) => {
    console.log('[signUp] 호출됨:', userData)

    const formData = new FormData()
    formData.append('username', userData.username)
    formData.append('email', userData.email)
    formData.append('password1', userData.password1)
    formData.append('password2', userData.password2)

    if (userData.first_name) formData.append('first_name', userData.first_name)
    if (userData.last_name) formData.append('last_name', userData.last_name)
    if (userData.gender) formData.append('gender', userData.gender)
    if (userData.age !== null) formData.append('age', userData.age)
    if (userData.weekly_reading_time !== null) formData.append('weekly_reading_time', userData.weekly_reading_time)
    if (userData.yearly_reading_volume !== null) formData.append('yearly_reading_volume', userData.yearly_reading_volume)

    if (userData.profile_image) formData.append('profile_image', userData.profile_image)

    if (userData.interested_genres?.length > 0) {
      userData.interested_genres.forEach(id => {
        formData.append('interested_genres', id)
      })
    }

    return axios.post(`${ACCOUNT_API_URL}/signup/`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
      .then(() => {
        console.log('[signUp] 성공! 자동 로그인 시작')
        alert('회원가입 성공! 이제 자동 로그인됩니다.')
        return logIn({
          username: userData.username,
          password: userData.password1
        })
      })
      .catch((err) => {
        console.error('[signUp] 실패:', err.response?.data)
        alert('회원가입에 실패했습니다.')
        throw err
      })
  }



  // 프로필 이미지 업로드
  const updateProfileImage = (file) => {
    const formData = new FormData()
    formData.append('profile_image', file)

    return axios.patch('/accounts/user/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
      .then(() => {
        console.log('[updateProfileImage] 성공')
      })
      .catch((err) => {
        console.error('[updateProfileImage] 실패:', err.response?.data)
        alert('프로필 이미지 업로드에 실패했습니다.')
        throw err
      })
  }



  const updateUser = (username, updatedData) => {
    return axios.put(`${ACCOUNT_API_URL}/${username}/edit/`, updatedData)
      .then((res) => {
        console.log('[updateUser] 성공:', res.data)
        user.value = res.data  // ✅ 수정된 내용으로 상태 갱신
      })
      .catch((err) => {
        console.error('[updateUser] 실패:', err.response?.data)
        throw err
      })
  }


  // 로그인
  const logIn = ({ username, password }) => {
    console.log('[logIn] 호출됨:', { username })
    return axios.post(`${ACCOUNT_API_URL}/login/`, {
      username,
      password
    })
      .then((res) => {
        console.log('[logIn] 성공:', res.data)
        token.value = res.data.key
        axios.defaults.headers.common['Authorization'] = `Token ${token.value}`
        return fetchUser()
      })
      .catch((err) => {
        console.error('[logIn] 실패:', err)
        alert('로그인에 실패했습니다.')
        throw err
      })
  }

  // 사용자 정보 가져오기
  const fetchUser = () => {
    console.log('[fetchUser] 호출됨')
    return axios.get(`${ACCOUNT_API_URL}/user/`)
      .then((res) => {
        console.log('[fetchUser] 성공:', res.data)
        user.value = res.data
      })
      .catch((err) => {
        console.error('[fetchUser] 실패:', err)
        logout()
      })
  }

  // 로그아웃
  const logout = () => {
    console.log('[logout] 호출됨')
    return axios.post(`${ACCOUNT_API_URL}/logout/`)
      .catch((err) => {
        console.warn('[logout] 실패 또는 이미 만료된 토큰:', err)
      })
      .finally(() => {
        console.log('[logout] 상태 초기화')
        token.value = ''
        user.value = null
        delete axios.defaults.headers.common['Authorization']
        localStorage.removeItem('token')
      })
  }

  // 회원 탈퇴 추가
  const deleteAccount = (username) => {
    console.log('[deleteAccount] 요청됨:', username)
    return axios.delete(`${ACCOUNT_API_URL}/${username}/delete/`)
      .then(() => {
        console.log('[deleteAccount] 성공')
        logout()
        alert('회원 탈퇴가 완료되었습니다.')
      })
      .catch((err) => {
        console.error('[deleteAccount] 실패:', err.response?.data)
        alert('회원 탈퇴에 실패했습니다.')
        throw err
      })
  }



  // 새로고침 후 인증 복구용
  const initAuth = () => {
    if (token.value) {
      console.log('[initAuth] 저장된 토큰으로 인증 복구 시도')
      axios.defaults.headers.common['Authorization'] = `Token ${token.value}`
      fetchUser()
    }
  }

  // 로그인 되어있나 확인
  const isLoggedIn = computed(() => user.value !== null)

  return {
    token,
    user,
    signUp,
    updateProfileImage,
    logIn,
    updateUser,
    fetchUser,
    logout,
    deleteAccount,
    initAuth,
    isLoggedIn
  }
}, { persist: true })

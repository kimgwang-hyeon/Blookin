<!-- LoginView.vue  -->
<template>
  <form @submit.prevent="login">
    <input v-model="username" placeholder="아이디" />
    <input v-model="password" type="password" placeholder="비밀번호" />
    <button type="submit">로그인</button>
  </form>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const username = ref('')
const password = ref('')

const login = async () => {
  try {
    const res = await axios.post('http://localhost:8000/accounts/login/', {
      username: username.value,
      password: password.value
    })
    const token = res.data.key
    localStorage.setItem('token', token)
    axios.defaults.headers.common['Authorization'] = `Token ${token}`
    alert('로그인 성공')
  } catch (err) {
    console.error(err)
    alert('로그인 실패')
  }
}
</script>

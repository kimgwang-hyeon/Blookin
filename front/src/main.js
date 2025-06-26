import { createApp } from 'vue'
import { createPinia } from 'pinia'
import piniaPersistedState from 'pinia-plugin-persistedstate'

import App from './App.vue'
import router from './router'
import axios from '@/lib/axios'


import './assets/tailwind.css'

const pinia = createPinia()
pinia.use(piniaPersistedState)

const app = createApp(App)

app.use(pinia)
app.use(router)

app.mount('#app')

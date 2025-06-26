import { createRouter, createWebHistory } from 'vue-router'
import AuthViews from '@/views/AuthViews.vue'
import LoginForm from '@/components/LoginForm.vue'
import SignupForm from '@/components/SignupForm.vue'
import MainView from '../views/MainView.vue'
import BooksListView from '@/views/BooksListView.vue'
import BookDetailView from '@/views/BookDetailView.vue'
import ThreadsListView from '@/views/ThreadsListView.vue'
import ThreadDetailView from '@/views/ThreadDetailView.vue'
import ThreadWriteView from '@/views/ThreadWriteView.vue'
import ProfileView from '@/views/ProfileView.vue'
import Recommendation from '@/components/Recommendation.vue'
import MbtiLandingView from '@/views/MbtiLandingView.vue'
import MbtiResultView from '@/views/MbtiResultView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'main',
      component: MainView,
    },
    {
      path: '/auth',
      component: AuthViews,
      children: [
        { path: 'login', component: LoginForm },
        { path: 'signup', component: SignupForm }
      ]
    },
    {
      path: '/books',
      name: 'BooksListView',
      component: BooksListView
    },
    {
      path: '/books/:bookId',
      name: 'BookDetailView',
      component: BookDetailView,
      props: true
    },
    {
      path: '/threads',
      name: 'ThreadsListView',
      component: ThreadsListView,
    },
    {
      path: '/threads/:threadId',
      name: 'ThreadDetailView',
      component: ThreadDetailView,
    },
    {
      path: '/threads/write',
      name: 'ThreadWriteView',
      component: ThreadWriteView,
    },
    {
      path: '/users/:userId',
      name: 'ProfileView',
      component: ProfileView,
    },
    {
      path: '/recommend/personal',
      name: 'Recommendation',
      component: Recommendation
    },
    {
      path: '/mbti',
      name: 'MbtiLandingView',
      component: MbtiLandingView
    },
    {
      path: '/mbti/result',
      name: 'MbtiResultView',
      component: MbtiResultView
    }
  ],
  scrollBehavior(to, from, savedPosition) {
    return { top: 0 }
  }
})

export default router

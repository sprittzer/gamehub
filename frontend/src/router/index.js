import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  { path: '/', component: () => import('@/views/Games.vue') },
  { path: '/games', component: () => import('@/views/Games.vue') },
  { path: '/games/:id', component: () => import('@/views/GameDetail.vue'), name: 'game-detail' },
  { path: '/reviews', component: () => import('@/views/Reviews.vue') },
  { path: '/admin', component: () => import('@/views/Admin.vue') }
]

export default createRouter({
  history: createWebHistory(),
  routes
})

const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export const api = {
  games: {
    list: (page = 1, pageSize = 20) => `${BASE_URL}/games?page=${page}&page_size=${pageSize}`,
    get: (id) => `${BASE_URL}/games/${id}`,
    delete: (id) => `${BASE_URL}/games/${id}`,
    create: () => `${BASE_URL}/games`,
    update: (id) => `${BASE_URL}/games/${id}`,
  },
  reviews: {
    list: (page = 1, pageSize = 20) => `${BASE_URL}/reviews?page=${page}&page_size=${pageSize}`,
    gameReviews: (gameId) => `${BASE_URL}/reviews?game_id=${gameId}`,
    create: () => `${BASE_URL}/reviews`,
    update: (id) => `${BASE_URL}/reviews/${id}`,
    delete: (id) => `${BASE_URL}/reviews/${id}`,
  }
}

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api'

export const api = {
  games: {
    list: (page = 1, pageSize = 20) => 
      `${API_BASE}/games?page=${page}&page_size=${pageSize}`,
    
    top: (limit = 10) => `${API_BASE}/games/top?limit=${limit}`,
    recent: (limit = 10) => `${API_BASE}/games/recent?limit=${limit}`,
    genres: () => `${API_BASE}/games/genres`,
    platforms: () => `${API_BASE}/games/platforms`,
    get: (id) => `${API_BASE}/games/${id}`,
    create: () => `${API_BASE}/games`,
    update: (id) => `${API_BASE}/games/${id}`,
    delete: (id) => `${API_BASE}/games/${id}`,
    cover: (id) => `${API_BASE}/games/${id}/cover`
  },
  reviews: {
    list: (page = 1, pageSize = 10) => `${API_BASE}/reviews?page=${page}&page_size=${pageSize}`,
    recent: (limit = 10) => `${API_BASE}/reviews/recent?limit=${limit}`,
    gameReviews: (gameId) => `${API_BASE}/reviews/game/${gameId}`,
    create: () => `${API_BASE}/reviews`,
    update: (id) => `${API_BASE}/reviews/${id}`,
    delete: (id) => `${API_BASE}/reviews/${id}`,
    myReviews: (page = 1, pageSize = 10) => `${API_BASE}/reviews/me?page=${page}&page_size=${pageSize}`
  }
}

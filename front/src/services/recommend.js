// src/services/recommend.js
import axios from '../lib/axios'


export const fetchPersonalRecommendations = (type = 'likes') => {
  return axios.get(`/books/recommend/personal/?type=${type}`)
}
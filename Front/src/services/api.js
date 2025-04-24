// src/services/api.js

import axios from 'axios'

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000',
  headers: {
    'Accept': 'application/json',
    'Content-Type': 'application/json'
  },
  timeout: 5000
})

export async function getRecentCVEs(n = 5) {
  try {
    const response = await apiClient.get('/cve/recent', {
      params: { n }
    })
    return response.data
  } catch (error) {
    console.error('Error fetching recent CVEs:', error)
    throw error
  }
}

export async function getLatestPosts() {
  try {
    const response = await apiClient.get('/blogs/latest', {
      headers: {
        'accept': 'application/json'
      }
    });
    return response.data;
  } catch (error) {
    console.error('Error fetching latest blog posts:', error);
    throw error;
  }
}

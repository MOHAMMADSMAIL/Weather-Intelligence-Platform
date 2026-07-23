import axios from 'axios'

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000'

export async function fetchWeather(locationOrCoords) {
  if (typeof locationOrCoords === 'object' && locationOrCoords !== null) {
    const { latitude, longitude } = locationOrCoords
    const response = await axios.get(`${API_BASE}/weather`, {
      params: { latitude, longitude },
    })
    return response.data
  }

  const response = await axios.get(`${API_BASE}/weather/${encodeURIComponent(locationOrCoords)}`)
  return response.data
}

export async function createRequest(payload) {
  const response = await axios.post(`${API_BASE}/requests`, payload)
  return response.data
}

export async function getRequests() {
  const response = await axios.get(`${API_BASE}/requests`)
  return response.data
}

export async function updateRequest(id, payload) {
  const response = await axios.put(`${API_BASE}/requests/${id}`, payload)
  return response.data
}

export async function deleteRequest(id) {
  const response = await axios.delete(`${API_BASE}/requests/${id}`)
  return response.data
}

export async function assistant(payload) {
  const response = await axios.post(`${API_BASE}/assistant`, payload)
  return response.data
}

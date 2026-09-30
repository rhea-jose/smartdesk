import axios from "axios"

const API_BASE = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";
export const api = axios.create({baseURL: API_BASE})

export const createTicket = (data) => api.post('/tickets',data)
export const listTickets = (params) => api.get('/tickets',{params})

export const updateTicket=(id,data) => api.patch(`/tickets/${id}`,data)
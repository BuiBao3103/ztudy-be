import api from './axiosInstance';

// Authentication APIs
export const login = async (email, password) => {
  const response = await api.post('/api/v1/auth/login/', { email, password });
  return response.data;
};

export const register = async (username, email, password1, password2) => {
  const response = await api.post('/api/v1/auth/register/', {
    username,
    email,
    password1,
    password2
  });
  return response.data;
};

export const logout = async () => {
  const response = await api.post('/api/v1/auth/logout/');
  return response.data;
};

export const getCurrentUser = async () => {
  const response = await api.get('/api/v1/auth/user/');
  return response.data;
};

// Room APIs
export const joinRoom = async (roomCode) => {
  const response = await api.post(`/api/v1/rooms/${roomCode}/join/`);
  response.data.status = response.status;
  return response.data;
};

export const approveRequest = async (roomCode, requestId) => {
  const response = await api.post(`/api/v1/rooms/${roomCode}/approve/${requestId}/`);
  return response.data;
};

// Thêm các API khác nếu cần

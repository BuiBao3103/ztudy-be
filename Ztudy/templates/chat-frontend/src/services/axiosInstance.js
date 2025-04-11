import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000',  // Thay đổi URL API của bạn
  withCredentials: true  // Quan trọng để gửi và nhận cookie
});

// Response interceptor
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    // Kiểm tra nếu lỗi là token hết hạn và chưa thử refresh
    if (
      error.response?.data?.code === 'token_not_valid' && 
      !originalRequest._retry
    ) {
      originalRequest._retry = true;

      try {
        // Gọi API refresh token
        await axios.post(
          '/api/v1/auth/token/refresh/',
          {},
          {
            baseURL: 'http://localhost:8000',
            withCredentials: true
          }
        );

        // Thử lại request ban đầu
        return api(originalRequest);
      } catch (refreshError) {
        // Nếu refresh token cũng hết hạn, chuyển về trang login
        window.location.href = '/login';
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

export default api;

import axios from 'axios';

// Set default base URL for axios
axios.defaults.baseURL = 'http://localhost:8000';
axios.defaults.withCredentials = true;

const API_BASE_URL = 'http://localhost:8000';

export const login = async (email, password) => {
  return await axios.post('/api/v1/auth/login/', {
    email,
    password,
  });
};

export const getCurrentUser = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/v1/auth/user/`, {
      headers: {
        'accept': 'application/json',
      },
      credentials: 'include',
    });

    if (!response.ok) {
      throw new Error('Failed to get current user');
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Get current user error:', error);
    throw error;
  }
};

export const logout = async () => {
  return await axios.post('/api/v1/auth/logout/');
};

export const register = async (username, email, password1, password2) => {
  return await axios.post('/api/v1/auth/registration/', {
    username,
    email,
    password1,
    password2
  });
}; 
const API_BASE_URL = 'http://localhost:8000/api/v1';

// Login user
export const login = async (email, password) => {
  const response = await fetch(`${API_BASE_URL}/auth/login/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
    },
    credentials: 'include',
    body: JSON.stringify({ email, password }),
  });

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.detail || 'Login failed');
  }

  const data = await response.json();
  return data;
};

// Get current user info
export const getCurrentUser = async () => {
  const response = await fetch(`${API_BASE_URL}/auth/user/`, {
    credentials: 'include',
  });
  if (!response.ok) {
    throw new Error('Failed to get user info');
  }
  return response.json();
};

// Join a room
export const joinRoom = async (roomCode) => {
  const response = await fetch(`${API_BASE_URL}/rooms/join/${roomCode}/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    credentials: 'include',
    body: JSON.stringify({})
  });

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.detail || 'Failed to join room');
  }

  return response.json();
}; 
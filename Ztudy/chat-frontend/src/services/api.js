import axios from "axios";

// Set default base URL for axios
axios.defaults.baseURL = "http://localhost:8000";
axios.defaults.withCredentials = true;

const API_BASE_URL = "http://localhost:8000";

export const login = async (email, password) => {
  return await axios.post("/api/v1/auth/login/", {
    email,
    password,
  });
};

export const getCurrentUser = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/v1/auth/user/`, {
      headers: {
        accept: "application/json",
      },
      credentials: "include",
    });

    if (!response.ok) {
      throw new Error("Failed to get current user");
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error("Get current user error:", error);
    throw error;
  }
};

export const logout = async () => {
  return await axios.post("/api/v1/auth/logout/");
};

export const register = async (username, email, password1, password2) => {
  const response = await axios.post("/api/v1/auth/registration/", {
    username,
    email,
    password1,
    password2,
  });
  if (response.status === 201) {
    return await login(email, password1);
  }
};

export const joinRoom = async (roomCode) => {
  try {
    const response = await fetch(
      `http://localhost:8000/api/v1/rooms/${roomCode}/join/`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        credentials: "include", // Để gửi cookies
      }
    );

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || "Failed to join room");
    }
    data.status = response.status;
    return data;
  } catch (error) {
    throw error;
  }
};

export const approveRequest = async (roomCode, requestId) => {
  try {
    const response = await fetch(
      `http://localhost:8000/api/v1/rooms/${roomCode}/approve/${requestId}/`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        credentials: "include",
      }
    );

    if (!response.ok) {
      throw new Error("Failed to approve request");
    }

    return await response.json();
  } catch (error) {
    throw error;
  }
};

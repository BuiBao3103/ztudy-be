import React, { useContext } from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { UserContext } from './context/UserContext';
import Login from './components/Login';
import ChatRoom from './components/ChatRoom';
import Header from './components/Header';
import Register from './components/Register';

const App = () => {
  const { currentUser, isLoading } = useContext(UserContext);

  if (isLoading) {
    return (
      <div className="h-screen flex items-center justify-center bg-[#111111]">
        <div className="text-gray-400">Loading...</div>
      </div>
    );
  }

  return (
    <div className="h-screen flex flex-col bg-[#111111]">
      <Header />
      <div className="flex-1 overflow-hidden">
        <Routes>
          <Route
            path="/login"
            element={currentUser ? <Navigate to="/" replace /> : <Login />}
          />
          <Route
            path="/"
            element={currentUser ? <ChatRoom /> : <Navigate to="/login" replace />}
          />
          <Route path="/register" element={<Register />} />
        </Routes>
      </div>
    </div>
  );
};

export default App; 
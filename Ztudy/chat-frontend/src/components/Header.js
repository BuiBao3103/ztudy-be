import React, { useContext } from 'react';
import { UserContext } from '../context/UserContext';
import { useNavigate } from 'react-router-dom';
import { logout } from '../api';

const Header = () => {
  const { currentUser, setCurrentUser } = useContext(UserContext);
  const navigate = useNavigate();

  const handleLogout = async () => {
    try {
      await logout();
      setCurrentUser(null);
      navigate('/login');
    } catch (error) {
      console.error('Logout failed:', error);
      setCurrentUser(null);
      navigate('/login');
    }
  };

  if (!currentUser) return null;

  return (
    <header className="h-16 bg-[#111111] border-b border-[#2a2a2a] shadow-xl">
      <div className="h-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex items-center justify-between">
        {/* Logo và Brand */}
        <div className="flex items-center">
          <div className="text-2xl font-bold text-gray-200">
            Ztudy Chat
          </div>
        </div>

        {/* User Profile và Actions */}
        <div className="flex items-center space-x-4">
          {/* User Profile */}
          <div className="flex items-center space-x-3">
            <div className="relative">
              <img
                src={currentUser.avatar}
                alt={currentUser.username}
                className="h-9 w-9 rounded-full object-cover border-2 border-[#2a2a2a] hover:border-[#3a3a3a] transition-colors duration-200"
              />
              <div className="absolute bottom-0 right-0 h-3 w-3 rounded-full bg-green-500 border-2 border-[#111111]"></div>
            </div>
            <div className="flex flex-col">
              <span className="text-sm font-medium text-gray-200">
                {currentUser.username}
              </span>
              <span className="text-xs text-gray-500">
                Online
              </span>
            </div>
          </div>

          {/* Logout Button */}
          <button
            onClick={handleLogout}
            className="px-4 py-2 bg-[#1a1a1a] text-gray-300 rounded-lg hover:bg-[#2a2a2a] hover:text-gray-200 focus:outline-none focus:ring-2 focus:ring-[#3a3a3a] transition-all duration-200 flex items-center space-x-2"
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
            </svg>
            <span>Logout</span>
          </button>
        </div>
      </div>
    </header>
  );
};

export default Header; 
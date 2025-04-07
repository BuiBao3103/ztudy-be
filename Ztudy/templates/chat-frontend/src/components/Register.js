import React, { useState, useContext } from 'react';
import { UserContext } from '../context/UserContext';
import { useNavigate } from 'react-router-dom';
import { register } from '../services/api';

const Register = () => {
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password1: '',
    password2: ''
  });
  const [error, setError] = useState('');
  const { setCurrentUser, isLoading, setIsLoading } = useContext(UserContext);
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setIsLoading(true);

    // Validate passwords match
    if (formData.password1 !== formData.password2) {
      setError('Passwords do not match');
      setIsLoading(false);
      return;
    }

    try {
      const response = await register(
        formData.username,
        formData.email,
        formData.password1,
        formData.password2
      );
      setCurrentUser(response.data);
      navigate('/');
    } catch (err) {
      const errorMessage = err.response?.data;
      let errorText = 'Registration failed. Please try again.';
      
      if (typeof errorMessage === 'object') {
        // Convert error object to readable message
        errorText = Object.entries(errorMessage)
          .map(([key, value]) => `${key}: ${value.join(', ')}`)
          .join('\n');
      }
      
      setError(errorText);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-[#111111] py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        {/* Header Section */}
        <div className="text-center">
          <h2 className="mt-6 text-3xl font-extrabold text-gray-200">
            Create your account
          </h2>
          <p className="mt-2 text-sm text-gray-400">
            Join our chat community today
          </p>
        </div>

        {/* Form Section */}
        <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
          <div className="rounded-md shadow-sm space-y-4">
            <div>
              <label htmlFor="username" className="block text-sm font-medium text-gray-400 mb-1">
                Username
              </label>
              <input
                id="username"
                name="username"
                type="text"
                required
                value={formData.username}
                onChange={handleChange}
                className="appearance-none relative block w-full px-3 py-3 border 
                border-[#2a2a2a] placeholder-gray-500 text-gray-200 rounded-lg 
                bg-[#1a1a1a] focus:outline-none focus:ring-2 focus:ring-blue-500 
                focus:border-transparent transition-colors duration-200"
                placeholder="Choose a username"
              />
            </div>

            <div>
              <label htmlFor="email" className="block text-sm font-medium text-gray-400 mb-1">
                Email
              </label>
              <input
                id="email"
                name="email"
                type="email"
                required
                value={formData.email}
                onChange={handleChange}
                className="appearance-none relative block w-full px-3 py-3 border 
                border-[#2a2a2a] placeholder-gray-500 text-gray-200 rounded-lg 
                bg-[#1a1a1a] focus:outline-none focus:ring-2 focus:ring-blue-500 
                focus:border-transparent transition-colors duration-200"
                placeholder="Enter your email"
              />
            </div>

            <div>
              <label htmlFor="password1" className="block text-sm font-medium text-gray-400 mb-1">
                Password
              </label>
              <input
                id="password1"
                name="password1"
                type="password"
                required
                value={formData.password1}
                onChange={handleChange}
                className="appearance-none relative block w-full px-3 py-3 border 
                border-[#2a2a2a] placeholder-gray-500 text-gray-200 rounded-lg 
                bg-[#1a1a1a] focus:outline-none focus:ring-2 focus:ring-blue-500 
                focus:border-transparent transition-colors duration-200"
                placeholder="Create a password"
              />
            </div>

            <div>
              <label htmlFor="password2" className="block text-sm font-medium text-gray-400 mb-1">
                Confirm Password
              </label>
              <input
                id="password2"
                name="password2"
                type="password"
                required
                value={formData.password2}
                onChange={handleChange}
                className="appearance-none relative block w-full px-3 py-3 border 
                border-[#2a2a2a] placeholder-gray-500 text-gray-200 rounded-lg 
                bg-[#1a1a1a] focus:outline-none focus:ring-2 focus:ring-blue-500 
                focus:border-transparent transition-colors duration-200"
                placeholder="Confirm your password"
              />
            </div>
          </div>

          {error && (
            <div className="rounded-md bg-red-900/50 p-4">
              <div className="flex">
                <div className="flex-shrink-0">
                  <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                  </svg>
                </div>
                <div className="ml-3">
                  <p className="text-sm text-red-400 whitespace-pre-line">{error}</p>
                </div>
              </div>
            </div>
          )}

          <div>
            <button
              type="submit"
              disabled={isLoading}
              className="group relative w-full flex justify-center py-3 px-4 border 
              border-transparent text-sm font-medium rounded-lg text-white 
              bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 
              focus:ring-offset-2 focus:ring-blue-500 transition-colors duration-200
              disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isLoading ? (
                <svg className="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
              ) : (
                'Create Account'
              )}
            </button>
          </div>
        </form>

        {/* Footer Section */}
        <div className="text-center mt-4">
          <p className="text-sm text-gray-500">
            Already have an account?{' '}
            <a 
              href="/login" 
              className="font-medium text-blue-500 hover:text-blue-400"
            >
              Sign in
            </a>
          </p>
        </div>
      </div>
    </div>
  );
};

export default Register; 
import React, { createContext, useState, useEffect } from 'react';
import { getCurrentUser } from '../api';

export const UserContext = createContext({
  currentUser: null,
  setCurrentUser: () => {},
  isLoading: true,
  setIsLoading: () => {},
});

export const UserProvider = ({ children }) => {
  const [currentUser, setCurrentUser] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const checkAuth = async () => {
      try {
        const userData = await getCurrentUser();
        setCurrentUser(userData);
      } catch (error) {
        console.error('Auth check failed:', error);
        setCurrentUser(null);
      } finally {
        setIsLoading(false);
      }
    };

    checkAuth();
  }, []);

  return (
    <UserContext.Provider value={{ 
      currentUser, 
      setCurrentUser, 
      isLoading,
      setIsLoading
    }}>
      {children}
    </UserContext.Provider>
  );
}; 
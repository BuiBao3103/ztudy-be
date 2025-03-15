import React, { createContext, useState } from 'react';

export const ChatContext = createContext({
  messages: [],
  setMessages: () => {},
  participants: [],
  setParticipants: () => {},
  isConnected: false,
  setIsConnected: () => {},
  currentRoom: null,
  setCurrentRoom: () => {},
  typingUsers: new Set(),
  setTypingUsers: () => {},
});

export const ChatProvider = ({ children }) => {
  const [messages, setMessages] = useState([]);
  const [participants, setParticipants] = useState([]);
  const [isConnected, setIsConnected] = useState(false);
  const [currentRoom, setCurrentRoom] = useState(null);
  const [typingUsers, setTypingUsers] = useState(new Set());

  const value = {
    messages,
    setMessages,
    participants,
    setParticipants,
    isConnected,
    setIsConnected,
    currentRoom,
    setCurrentRoom,
    typingUsers,
    setTypingUsers,
  };

  return (
    <ChatContext.Provider value={value}>
      {children}
    </ChatContext.Provider>
  );
}; 
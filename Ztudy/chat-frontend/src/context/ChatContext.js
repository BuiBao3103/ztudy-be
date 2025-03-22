import React, { createContext, useState } from "react";

export const ChatContext = createContext({
  messages: [],
  setMessages: () => { },
  participants: [],
  setParticipants: () => { },
  isConnected: false,
  setIsConnected: () => { },
  currentRoom: null,
  setCurrentRoom: () => { },
  typingUsers: new Set(),
  setTypingUsers: () => { },
  pendingRequests: [],
  setPendingRequests: () => { },
  role: "USER",
  setRole: () => { },
  isPending: false,
  setIsPending: () => { },
});

export const ChatProvider = ({ children }) => {
  const [messages, setMessages] = useState([]);
  const [participants, setParticipants] = useState([]);
  const [isConnected, setIsConnected] = useState(false);
  const [currentRoom, setCurrentRoom] = useState(null);
  const [typingUsers, setTypingUsers] = useState(new Set());
  const [pendingRequests, setPendingRequests] = useState([]);
  const [role, setRole] = useState(false);
  const [isPending, setIsPending] = useState(false);

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
    pendingRequests,
    setPendingRequests,
    role,
    setRole,
    isPending,
    setIsPending,
  };

  return <ChatContext.Provider value={value}>{children}</ChatContext.Provider>;
};

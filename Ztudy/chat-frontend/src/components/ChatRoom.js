import React, { useState, useContext } from 'react';
import { WebSocketContext } from '../context/WebSocketContext';
import { ChatContext } from '../context/ChatContext';
import ChatArea from './ChatArea';
import RoomControls from './RoomControls';
import UserList from './UserList';

const ChatRoom = () => {
  const [roomCode, setRoomCode] = useState('');
  const { connectChatSocket, disconnectChatSocket } = useContext(WebSocketContext);
  const { currentRoom, setCurrentRoom, isConnected } = useContext(ChatContext);

  const handleJoinRoom = (e) => {
    e.preventDefault();
    if (roomCode.trim()) {
      connectChatSocket(roomCode.trim());
      setCurrentRoom(roomCode.trim());
    }
  };

  const handleLeaveRoom = () => {
    disconnectChatSocket();
    setCurrentRoom(null);
  };

  if (!currentRoom || !isConnected) {
    return (
      <div className="h-full flex items-center justify-center p-4">
        <div className="bg-[#1a1a1a] p-8 rounded-xl w-full max-w-md shadow-2xl border border-[#2a2a2a]">
          <h2 className="text-2xl font-bold text-gray-200 mb-6">Join a Room</h2>
          <form onSubmit={handleJoinRoom} className="space-y-4">
            <div>
              <label htmlFor="roomCode" className="block text-gray-300 mb-2">
                Room Code
              </label>
              <input
                type="text"
                id="roomCode"
                value={roomCode}
                onChange={(e) => setRoomCode(e.target.value)}
                className="w-full px-4 py-3 bg-[#222222] border border-[#2a2a2a] rounded-lg text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-[#3a3a3a] focus:border-transparent"
                placeholder="Enter room code"
              />
            </div>
            <button
              type="submit"
              className="w-full px-6 py-3 bg-[#2a2a2a] text-white rounded-lg hover:bg-[#3a3a3a] focus:outline-none focus:ring-2 focus:ring-[#3a3a3a] transition-colors duration-200"
            >
              Join Room
            </button>
          </form>
        </div>
      </div>
    );
  }

  return (
    <div className="h-full flex">
      {/* Sidebar */}
      <div className="w-64 bg-[#1a1a1a] border-r border-[#2a2a2a] flex flex-col">
        <div className="p-4 border-b border-[#2a2a2a]">
          <h2 className="text-lg font-semibold text-gray-200">Room: {currentRoom}</h2>
        </div>
        <UserList />
        <div className="mt-auto p-4 border-t border-[#2a2a2a]">
          <button
            onClick={handleLeaveRoom}
            className="w-full px-4 py-2 bg-[#2a2a2a] text-white rounded-lg hover:bg-[#3a3a3a] focus:outline-none focus:ring-2 focus:ring-[#3a3a3a] transition-colors duration-200"
          >
            Leave Room
          </button>
        </div>
      </div>

      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col bg-[#111111]">
        <ChatArea />
        <RoomControls />
      </div>
    </div>
  );
};

export default ChatRoom; 
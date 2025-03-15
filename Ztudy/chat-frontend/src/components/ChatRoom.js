import React, { useState, useContext } from "react";
import { WebSocketContext } from "../context/WebSocketContext";
import { ChatContext } from "../context/ChatContext";
import { joinRoom } from "../services/api";
import ChatArea from "./ChatArea";
import RoomControls from "./RoomControls";
import UserList from "./UserList";
import RequestList from "./RequestList";

const ChatRoom = () => {
  const [roomCode, setRoomCode] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");
  const { connectChatSocket, disconnectChatSocket } =
    useContext(WebSocketContext);
  const {
    currentRoom,
    setCurrentRoom,
    isConnected,
    isAdmin,
    setIsAdmin,
    isPending,
    setIsPending,
  } = useContext(ChatContext);

  const handleJoinRoom = async (e) => {
    e.preventDefault();
    if (!roomCode.trim()) return;

    setIsLoading(true);
    setError("");

    try {
      const data = await joinRoom(roomCode.trim());

      if (data.status === 202) {
        setIsPending(true);
      }
      setCurrentRoom({
        id: data.room.id,
        code: data.room.code_invite,
        name: data.room.name,
        type: data.room.type,
        category: data.room.category,
        maxParticipants: data.room.max_participants,
        isActive: data.room.is_active,
        creatorUser: data.room.creator_user,
      });
      setIsAdmin(data.participant.is_admin);
      connectChatSocket(data.room.code_invite);
    } catch (err) {
      setError(err.message || "Failed to join room. Please try again.");
      console.error("Join room error:", err);
    } finally {
      setIsLoading(false);
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
                disabled={isLoading}
                className="w-full px-4 py-3 bg-[#222222] border border-[#2a2a2a] rounded-lg 
                text-white placeholder-gray-500 focus:outline-none focus:ring-2 
                focus:ring-[#3a3a3a] focus:border-transparent disabled:opacity-50"
                placeholder="Enter room code"
              />
            </div>

            {error && (
              <div className="bg-red-900/50 text-red-400 p-3 rounded-lg text-sm">
                {error}
              </div>
            )}

            <button
              type="submit"
              disabled={isLoading}
              className="w-full px-6 py-3 bg-[#2a2a2a] text-white rounded-lg 
              hover:bg-[#3a3a3a] focus:outline-none focus:ring-2 focus:ring-[#3a3a3a] 
              transition-colors duration-200 disabled:opacity-50 flex items-center justify-center"
            >
              {isLoading ? (
                <svg
                  className="animate-spin h-5 w-5 text-white"
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                >
                  <circle
                    className="opacity-25"
                    cx="12"
                    cy="12"
                    r="10"
                    stroke="currentColor"
                    strokeWidth="4"
                  ></circle>
                  <path
                    className="opacity-75"
                    fill="currentColor"
                    d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                  ></path>
                </svg>
              ) : (
                "Join Room"
              )}
            </button>
          </form>
        </div>
      </div>
    );
  }

  if (isPending) {
    return (
      <div className="h-full flex items-center justify-center p-4">
        <div className="bg-[#1a1a1a] p-8 rounded-xl w-full max-w-md shadow-2xl border border-[#2a2a2a] text-center">
          <div className="flex justify-center mb-4">
            <svg
              className="animate-spin h-12 w-12 text-blue-500"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
            >
              <circle
                className="opacity-25"
                cx="12"
                cy="12"
                r="10"
                stroke="currentColor"
                strokeWidth="4"
              />
              <path
                className="opacity-75"
                fill="currentColor"
                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
              />
            </svg>
          </div>
          <h2 className="text-2xl font-bold text-gray-200 mb-4">
            Waiting for Approval
          </h2>
          <p className="text-gray-400">
            Your request to join this room is pending approval from an admin.
          </p>
          <button
            onClick={() => {
              disconnectChatSocket();
              setIsPending(false);
              setRoomCode("");
            }}
            className="mt-6 px-6 py-2 bg-[#2a2a2a] text-white rounded-lg 
            hover:bg-[#3a3a3a] focus:outline-none focus:ring-2 focus:ring-[#3a3a3a] 
            transition-colors duration-200"
          >
            Cancel Request
          </button>
        </div>
      </div>
    );
  }
  return (
    <div className="h-full flex">
      {/* Sidebar */}
      <div className="w-64 bg-[#1a1a1a] border-r border-[#2a2a2a] flex flex-col">
        <div className="p-4 border-b border-[#2a2a2a]">
          <h2 className="text-lg font-semibold text-gray-200">
            Room: {currentRoom.name} ({currentRoom.type})
          </h2>
          <p className="text-sm text-gray-400 mt-1">Code: {currentRoom.code}</p>
          {isAdmin && (
            <span className="mt-2 inline-block px-2 py-1 bg-green-600 text-white text-xs rounded">
              Admin
            </span>
          )}
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
      <div className="flex-1 flex">
        <div className="flex-1 flex flex-col bg-[#111111]">
          <ChatArea />
          <RoomControls />
        </div>

        {/* Request List - Only show for admin */}
        {isAdmin && (
          <div className="w-72 border-l border-[#2a2a2a]">
            <RequestList />
          </div>
        )}
      </div>
    </div>
  );
};

export default ChatRoom;

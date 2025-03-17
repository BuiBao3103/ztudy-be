import React, { useContext, useState } from 'react';
import { ChatContext } from '../context/ChatContext';
import { UserContext } from '../context/UserContext';
import { assignAdmin } from '../services/api';

const UserList = () => {
  const { participants, currentRoom, isAdmin } = useContext(ChatContext);
  const { currentUser } = useContext(UserContext);
  const [hoveredUser, setHoveredUser] = useState(null);

  const handleAssignAdmin = async (userId) => {
    try {
      await assignAdmin(currentRoom.code, userId);
    } catch (error) {
      console.error("Error assigning admin:", error);
    }
  };

  return (
    <div className="flex-1 overflow-y-auto bg-[#1a1a1a]">
      <div className="p-4 border-b border-[#2a2a2a]">
        <h3 className="text-sm font-medium text-gray-400">
          Participants ({participants?.length || 0})
        </h3>
      </div>
      <div className="p-2">
        {participants?.map((participant) => {
          if (!participant?.user) return null;

          return (
            <div
              key={participant.user.id}
              className={`flex items-center space-x-3 p-2 rounded-lg mb-1 
                ${participant.user.id === currentUser?.id ? 'bg-[#2a2a2a]' : 'hover:bg-[#222222]'}
                transition-colors duration-200 relative group`}
              onMouseEnter={() => setHoveredUser(participant.user.id)}
              onMouseLeave={() => setHoveredUser(null)}
            >
              <div className="relative">
                <img
                  src={participant.user.avatar || '/default-avatar.png'}
                  alt={participant.user.username}
                  className="w-8 h-8 rounded-full object-cover border-2 border-[#2a2a2a]"
                />
                {participant.user.is_online && (
                  <div className="absolute bottom-0 right-0 h-2.5 w-2.5 rounded-full bg-green-500 border-2 border-[#1a1a1a]" />
                )}
              </div>
              <div className="flex-1 min-w-0">
                <div className="flex items-center justify-between">
                  <p className={`text-sm font-medium truncate ${
                    participant.user.id === currentUser?.id ? 'text-gray-200' : 'text-gray-300'
                  }`}>
                    {participant.user.username}
                    {participant.user.id === currentUser?.id && (
                      <span className="ml-2 text-xs text-gray-500">(You)</span>
                    )}
                    {participant.is_admin && (
                      <span className="ml-2 text-xs text-green-500">(Admin)</span>
                    )}
                  </p>
                </div>
                {participant.user.is_typing && (
                  <p className="text-xs text-gray-500">
                    typing...
                  </p>
                )}
              </div>

              {/* Assign Admin Button */}
              {isAdmin && 
               !participant.is_admin && 
               hoveredUser === participant.user.id && 
               participant.user.id !== currentUser?.id && (
                <button
                  onClick={() => handleAssignAdmin(participant.user.id)}
                  className="absolute right-2 px-2 py-1 text-xs bg-green-600 text-white rounded
                    hover:bg-green-700 transition-colors duration-200 opacity-0 group-hover:opacity-100"
                >
                  Make Admin
                </button>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default UserList; 
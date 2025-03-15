import React, { useContext } from 'react';
import { ChatContext } from '../context/ChatContext';
import { UserContext } from '../context/UserContext';

const UserList = () => {
  const { participants } = useContext(ChatContext);
  const { currentUser } = useContext(UserContext);

  return (
    <div className="flex-1 overflow-y-auto bg-[#1a1a1a]">
      <div className="p-4 border-b border-[#2a2a2a]">
        <h3 className="text-sm font-medium text-gray-400">
          Participants ({participants.length})
        </h3>
      </div>
      <div className="p-2">
        {participants.map((user) => (
          <div
            key={user.id}
            className={`flex items-center space-x-3 p-2 rounded-lg mb-1 
              ${user.id === currentUser?.id ? 'bg-[#2a2a2a]' : 'hover:bg-[#222222]'}
              transition-colors duration-200`}
          >
            <div className="relative">
              <img
                src={user.avatar}
                alt={user.username}
                className="w-8 h-8 rounded-full object-cover border-2 border-[#2a2a2a]"
              />
              {user.is_online && (
                <div className="absolute bottom-0 right-0 h-2.5 w-2.5 rounded-full bg-green-500 border-2 border-[#1a1a1a]" />
              )}
            </div>
            <div className="flex-1 min-w-0">
              <div className="flex items-center justify-between">
                <p className={`text-sm font-medium truncate ${
                  user.id === currentUser?.id ? 'text-gray-200' : 'text-gray-300'
                }`}>
                  {user.username}
                  {user.id === currentUser?.id && (
                    <span className="ml-2 text-xs text-gray-500">(You)</span>
                  )}
                </p>
              </div>
              {user.is_typing && (
                <p className="text-xs text-gray-500">
                  typing...
                </p>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default UserList; 
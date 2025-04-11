import React, { useContext, useEffect, useRef } from 'react';
import { ChatContext } from '../context/ChatContext';
import { UserContext } from '../context/UserContext';
import TypingIndicator from './TypingIndicator';

const ChatArea = () => {
  const { messages, typingUsers } = useContext(ChatContext);
  const { currentUser } = useContext(UserContext);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  console.log('Typing users:', typingUsers); // Debug log

  return (
    <div className="flex-1 relative overflow-hidden">
      <div className="h-full overflow-y-auto p-4 pb-14">
        <div className="space-y-4">
          {messages.map((message, index) => {
            const isCurrentUser = message.user.id === currentUser?.id;
            
            return (
              <div
                key={index}
                className={`flex items-start gap-3 ${
                  isCurrentUser ? 'flex-row-reverse' : 'flex-row'
                }`}
              >
                {/* Avatar */}
                <div className="flex-shrink-0">
                  <img
                    src={message.user.avatar || '/default-avatar.png'}
                    alt={message.user.username}
                    className="w-10 h-10 rounded-full object-cover border-2 border-gray-700"
                  />
                </div>

                {/* Message Content */}
                <div
                  className={`flex flex-col ${
                    isCurrentUser ? 'items-end' : 'items-start'
                  } flex-1`}
                >
                  {/* Username */}
                  <span className="text-sm text-gray-400 mb-1">
                    {message.user.username}
                  </span>

                  {/* Message Bubble */}
                  <div
                    className={`max-w-[95%] px-4 py-2 rounded-lg ${
                      isCurrentUser
                        ? 'bg-blue-600 text-white'
                        : 'bg-gray-700 text-gray-100'
                    }`}
                  >
                    <p className="break-words whitespace-pre-wrap">
                      {message.content || message.message}
                    </p>
                  </div>

                  {/* Timestamp */}
                  <span className="text-xs text-gray-500 mt-1">
                    {new Date(message.timestamp).toLocaleTimeString()}
                  </span>
                </div>
              </div>
            );
          })}
          <div ref={messagesEndRef} />
        </div>
      </div>

      {typingUsers.size > 0 && (
        <div className="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-gray-900 to-transparent">
          <div className="px-4 py-2">
            <TypingIndicator />
          </div>
        </div>
      )}
    </div>
  );
};

export default ChatArea; 
import React, { useState, useContext, useEffect } from 'react';
import { WebSocketContext } from '../context/WebSocketContext';

const RoomControls = () => {
  const [message, setMessage] = useState('');
  const { chatSocket, sendTypingStatus } = useContext(WebSocketContext);
  const [typingTimeout, setTypingTimeout] = useState(null);

  const handleTyping = () => {
    console.log('Sending typing status: true'); // Debug log
    sendTypingStatus(true);
    
    // Clear previous timeout
    if (typingTimeout) {
      clearTimeout(typingTimeout);
    }
    
    // Set new timeout
    const timeout = setTimeout(() => {
      console.log('Sending typing status: false'); // Debug log
      sendTypingStatus(false);
    }, 1000);
    
    setTypingTimeout(timeout);
  };

  useEffect(() => {
    return () => {
      if (typingTimeout) {
        clearTimeout(typingTimeout);
      }
    };
  }, [typingTimeout]);

  const handleChange = (e) => {
    setMessage(e.target.value);
    handleTyping();
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (message.trim() && chatSocket) {
      chatSocket.send(JSON.stringify({
        type: 'message',
        message: message.trim()
      }));
      setMessage('');
      sendTypingStatus(false);
    }
  };

  return (
    <div className="bg-[#1a1a1a] p-4 border-t border-[#2a2a2a]">
      <form onSubmit={handleSubmit} className="flex space-x-3">
        <input
          type="text"
          value={message}
          onChange={handleChange}
          placeholder="Type a message..."
          className="flex-1 px-4 py-2 bg-[#222222] border border-[#2a2a2a] rounded-lg text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-[#3a3a3a] focus:border-transparent"
        />
        <button
          type="submit"
          className="px-6 py-2 bg-[#2a2a2a] text-white rounded-lg hover:bg-[#3a3a3a] focus:outline-none focus:ring-2 focus:ring-[#3a3a3a] transition-colors duration-200"
        >
          Send
        </button>
      </form>
    </div>
  );
};

export default RoomControls; 
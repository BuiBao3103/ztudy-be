import React, { useContext } from 'react';
import { ChatContext } from '../context/ChatContext';

const RequestList = () => {
  const { pendingRequests } = useContext(ChatContext);

  return (
    <div className="w-64 bg-gray-800 border-l border-gray-700">
      <div className="p-4 border-b border-gray-700">
        <h2 className="text-lg font-semibold text-white">Join Requests</h2>
      </div>
      <div className="p-4 space-y-2">
        {pendingRequests.map((request) => (
          <div key={request.id} className="bg-gray-700 rounded-lg p-3">
            <div className="flex items-center justify-between">
              <span className="text-gray-300 text-sm font-medium">
                {request.username}
              </span>
              <button
                onClick={() => {/* Handle approve */}}
                className="px-3 py-1 bg-green-600 text-white text-sm rounded-md hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2 focus:ring-offset-gray-800 transition-colors duration-200"
              >
                Approve
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default RequestList; 
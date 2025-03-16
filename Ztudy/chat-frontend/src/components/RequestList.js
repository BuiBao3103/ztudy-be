import React, {useContext} from "react";
import {ChatContext} from "../context/ChatContext";
import {approveRequest, rejectRequest} from "../services/api";

const RequestList = () => {
    const {pendingRequests, setPendingRequests, currentRoom} =
        useContext(ChatContext);

    const handleApprove = async (requestId) => {
        try {
            await approveRequest(currentRoom.code, requestId);
        } catch (error) {
            console.error("Error approving request:", error);
        }
    };

    const handleReject = async (requestId) => {
        console.log(requestId)
        try {
            await rejectRequest(currentRoom.code, requestId);
        } catch (error) {
            console.error("Error declining request:", error);
        }
    }

    return (
        <div className="h-full bg-[#1a1a1a]">
            <div className="p-4 border-b border-[#2a2a2a]">
                <h2 className="text-lg font-semibold text-gray-200">Join Requests</h2>
                <p className="text-sm text-gray-400 mt-1">
                    {pendingRequests?.length || 0} pending
                </p>
            </div>

            <div className="p-2 space-y-2 overflow-y-auto">
                {!pendingRequests || pendingRequests.length === 0 ? (
                    <div className="text-gray-400 text-center p-4">
                        No pending requests
                    </div>
                ) : (
                    pendingRequests.map((request) => (
                        <div
                            key={request.id}
                            className="bg-[#222222] rounded-lg p-3 space-y-3"
                        >
                            <div className="flex items-center space-x-3">
                                <img
                                    src={request.avatar}
                                    alt={request.username}
                                    className="w-10 h-10 rounded-full object-cover border-2 border-[#2a2a2a]"
                                />
                                <div className="flex-1">
                                    <p className="text-gray-200 font-medium">
                                        {request.username}
                                    </p>
                                </div>
                            </div>

                            <div className="flex gap-2">
                                <button
                                    onClick={() => handleApprove(request.id)}
                                    className="w-full px-4 py-2 bg-green-600 text-white text-sm rounded-lg
                                        hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500
                                        transition-colors duration-200"
                                >
                                    Approve
                                </button>
                                <button
                                    onClick={() => handleReject(request.id)}
                                    className="w-full px-4 py-2 bg-red-600 text-white text-sm rounded-lg
                                        hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-500
                                        transition-colors duration-200"
                                >
                                    Decline
                                </button>
                            </div>
                        </div>
                    ))
                )}
            </div>
        </div>
    );
};

export default RequestList;

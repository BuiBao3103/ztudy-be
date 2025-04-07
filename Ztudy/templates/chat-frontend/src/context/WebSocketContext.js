import React, {
    createContext,
    useContext,
    useEffect,
    useState,
    useCallback,
} from "react";
import { UserContext } from "./UserContext";
import { ChatContext } from "./ChatContext";

export const WebSocketContext = createContext({
    onlineSocket: null,
    chatSocket: null,
    connectOnlineSocket: () => {
    },
    connectChatSocket: () => {
    },
    disconnectChatSocket: () => {
    },
    sendMessage: () => {
    },
    sendTypingStatus: () => {
    },
});

export const WebSocketProvider = ({ children }) => {
    const [onlineSocket, setOnlineSocket] = useState(null);
    const [chatSocket, setChatSocket] = useState(null);
    const { currentUser } = useContext(UserContext);
    const {
        setMessages,
        setParticipants,
        setCurrentRoom,
        setIsConnected,
        setTypingUsers,
        setIsPending,
        setPendingRequests,
        setRole,
    } = useContext(ChatContext);

    const connectChatSocket = (roomCode) => {
        if (!roomCode) return;

        const ws = new WebSocket(`ws://localhost:8000/ws/chat/${roomCode}/`);

        ws.onopen = () => {
            console.log("Chat WebSocket Connected");
            setIsConnected(true);
        };

        ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            console.log("Received message:", data);

            switch (data.type) {
                case "chat_message":
                    setMessages((prev) => [
                        ...prev,
                        {
                            content: data.message,
                            user: data.user,
                            timestamp: new Date().toISOString(),
                        },
                    ]);
                    // Khi có tin nhắn mới, xóa trạng thái typing của người gửi
                    setTypingUsers((prev) => {
                        const newSet = new Set(prev);
                        newSet.delete(data.user.id);
                        return newSet;
                    });
                    break;

                case "user_joined":
                    setParticipants((prev) => {
                        if (!prev.find((p) => p.id === data.user.id)) {
                            return [...prev, data.user];
                        }
                        return prev;
                    });
                    break;

                case "user_left":
                    setParticipants((prev) =>
                        prev.filter((user) => user.id !== data.user.id)
                    );
                    break;

                case "user_list":
                    setParticipants(data.users);
                    break;

                case "typing_status":
                    console.log("Typing status received:", data); // Debug log
                    if (data.user.id !== currentUser?.id) {
                        if (data.is_typing) {
                            setTypingUsers((prev) => {
                                const newSet = new Set(prev);
                                newSet.add(data.user.id);
                                return newSet;
                            });
                            // Tự động xóa trạng thái typing sau 3 giây
                            setTimeout(() => {
                                setTypingUsers((prev) => {
                                    const newSet = new Set(prev);
                                    newSet.delete(data.user.id);
                                    return newSet;
                                });
                            }, 3000);
                        } else {
                            setTypingUsers((prev) => {
                                const newSet = new Set(prev);
                                newSet.delete(data.user.id);
                                return newSet;
                            });
                        }
                    }
                    break;

                case "error":
                    console.error("WebSocket Error:", data.message);
                    setIsConnected(false);
                    ws.close();
                    break;

                case "pending_requests":
                    console.log("Received pending requests:", data.requests);
                    setPendingRequests(data.requests);
                    setIsConnected(true);
                    break;

                case "user_approved":
                    console.log("Received user approved:", data.user);
                    setIsConnected(true);
                    setIsPending(false);
                    break;

                case "user_rejected":
                    console.log("Received user rejected:", data.user);
                    setCurrentRoom(null)
                    setIsPending(false);
                    ws.close()
                    alert("You have been rejected from the room.");
                    break;

                case "participant_list":
                    setParticipants(data.participants);
                    break;

                case "user_assigned_moderator":
                    setRole("MODERATOR");
                    break;

                case "user_revoked_moderator":
                    setRole("USER");
                    break;
                case "room_ended":
                    setCurrentRoom(null);
                    setIsConnected(false);
                    break;
                default:
                    console.log("Unhandled message type:", data.type);
            }
        };

        ws.onclose = () => {
            console.log("Chat WebSocket Disconnected");
            setChatSocket(null);
            setIsConnected(false);
        };

        ws.onerror = (error) => {
            console.error("Chat WebSocket Error:", error);
            setChatSocket(null);
            setIsConnected(false);
        };

        setChatSocket(ws);
    };

    const connectOnlineSocket = () => {
        if (currentUser && !onlineSocket) {
            const ws = new WebSocket("ws://localhost:8000/ws/online/");

            ws.onopen = () => {
                console.log("Online Status WebSocket Connected");
            };

            ws.onclose = () => {
                console.log("Online Status WebSocket Disconnected");
                setOnlineSocket(null);
            };

            ws.onerror = (error) => {
                console.error("Online Status WebSocket Error:", error);
                setOnlineSocket(null);
            };

            setOnlineSocket(ws);
        }
    };

    const disconnectChatSocket = () => {
        if (chatSocket) {
            chatSocket.close();
            setChatSocket(null);
            setIsConnected(false);
            setCurrentRoom(null);
            setMessages([]);
            setParticipants([]);
            setTypingUsers(new Set());
        }
    };

    const sendTypingStatus = (isTyping) => {
        if (chatSocket) {
            chatSocket.send(
                JSON.stringify({
                    type: "typing",
                    is_typing: isTyping,
                })
            );
        }
    };

    useEffect(() => {
        return () => {
            if (onlineSocket) onlineSocket.close();
            if (chatSocket) chatSocket.close();
        };
    }, []);

    return (
        <WebSocketContext.Provider
            value={{
                onlineSocket,
                chatSocket,
                connectOnlineSocket,
                connectChatSocket,
                disconnectChatSocket,
                sendTypingStatus,
            }}
        >
            {children}
        </WebSocketContext.Provider>
    );
};

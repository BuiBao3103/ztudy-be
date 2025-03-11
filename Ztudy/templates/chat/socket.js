// socket.js

let chatSocket = null;
let currentRoom = null;

// socket.js - Improve connection handling
function connectWebSocket(codeInvite) {
    if (chatSocket !== null) {
        chatSocket.close();
    }

    currentRoom = codeInvite;
    document.getElementById('current-room').textContent = `Room: ${codeInvite}`;

    const protocol = window.location.protocol === 'https:' ? 'wss://' : 'ws://';
    const wsUrl = `${protocol}${window.location.host}/ws/chat/${codeInvite}/`;

    console.log(`Connecting to WebSocket at: ${wsUrl}`);

    chatSocket = new WebSocket(wsUrl);

    chatSocket.onopen = function () {
        console.log("WebSocket connected successfully");
    };

    chatSocket.onmessage = function (event) {
        const data = JSON.parse(event.data);
        console.log("Received message:", data);
        handleWebSocketMessage(data);
    };

    chatSocket.onclose = function (event) {
        console.log("WebSocket disconnected", event);
        if (!event.wasClean) {
            // If connection was not closed cleanly, try to reconnect after a delay
            setTimeout(() => {
                console.log("Attempting to reconnect...");
                connectWebSocket(codeInvite);
            }, 3000);
        }
    };

    chatSocket.onerror = function (error) {
        console.error("WebSocket error:", error);
    };
}

// Handle WebSocket messages
function handleWebSocketMessage(data) {
    console.log("Received message type:", data.type, data);

    if (data.type === "user_list") {
        updateUserList(data.users);
    } else if (data.type === "waiting_for_approval") {
        console.log(data.message);
        alert(data.message);
    } else if (data.type === "user_approved") {
        console.log(`User approved: ${data.user.username}`);
        if (data.user.id === currentUser.id) {
            alert(`You have been approved and joined the room!`);
            enableChatInterface();
        }
    } else if (data.type === "user_joined") {
        addUserToList(data.user);
    } else if (data.type === "user_left") {
        removeUserFromList(data.user);
    } else if (data.type === "chat_message") {
        displayMessage(data.user, data.message);
    } else if (data.type === "typing_status") {
        showTypingIndicator(data.is_typing, data.user);
    } else if (data.type === "pending_requests" || data.type === "update_pending_requests") {
        console.log("Updating pending requests:", data.requests);
        updateRequestList(data.requests);
    } else {
        console.log("Unknown message type:", data.type);
    }
}


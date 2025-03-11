// socket.js

let chatSocket = null;
let currentRoom = null;

// Connect WebSocket
function connectWebSocket(codeInvite) {
    if (chatSocket !== null) {
        chatSocket.close();
    }

    currentRoom = codeInvite;
    document.getElementById('current-room').textContent = `Room: ${codeInvite}`;

    const protocol = window.location.protocol === 'https:' ? 'wss://' : 'ws://';
    chatSocket = new WebSocket(`${protocol}${window.location.host}/ws/chat/${codeInvite}/`);

    chatSocket.onopen = function () {
        console.log("WebSocket connected");
    };

    chatSocket.onmessage = function (event) {
        const data = JSON.parse(event.data);
        handleWebSocketMessage(data);
    };

    chatSocket.onclose = function () {
        console.log("WebSocket disconnected");
    };

    chatSocket.onerror = function (error) {
        console.error("WebSocket error:", error);
    };
}

// Handle WebSocket messages
function handleWebSocketMessage(data) {
    if (data.type === "user_list") {
        updateUserList(data.users);
    } else if (data.type === "user_joined") {
        addUserToList(data.user);
    } else if (data.type === "user_left") {
        removeUserFromList(data.user);
    } else if (data.type === "chat_message") {
        console.log(data)
        displayMessage(data.user, data.message);
    } else if (data.type === "typing_status") {
        showTypingIndicator(data.is_typing, data.user);
    }
}
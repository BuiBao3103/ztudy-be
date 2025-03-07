let chatSocket = null;
let currentRoom = null;
let typingTimer = null;
let isTyping = false;
const TYPING_TIMEOUT = 2000; // 2 seconds
let user = {}

// Initialize UI state
function initUI() {
    const messageInput = document.getElementById('message-input');
    const sendButton = document.getElementById('send-btn');

    // Disable chat functionality when not in a room
    messageInput.disabled = true;
    sendButton.disabled = true;
}

// Get room code from input
function joinRoom() {
    const codeInvite = document.getElementById('room-code').value.trim();
    if (!codeInvite) {
        alert("Vui lòng nhập mã phòng!");
        return;
    }

    // Call API `join` to enter room
    fetch(`/api/v1/rooms/join/${codeInvite}/`, {method: "POST"})
        .then(response => response.json())
        .then(data => {
            if (data.message === "Joined room successfully!") {
                // Get the username from the server response if available
                connectWebSocket(codeInvite);
                enableChatInterface();
            } else {
                alert("Bạn cần chờ admin xét duyệt để vào phòng!");
            }
        })
        .catch(error => console.error("Lỗi khi vào phòng:", error));
}

// Enable chat interface elements
function enableChatInterface() {
    const messageInput = document.getElementById('message-input');
    const sendButton = document.getElementById('send-btn');

    messageInput.disabled = false;
    sendButton.disabled = false;
    messageInput.focus();
}

// Disable chat interface elements
function disableChatInterface() {
    const messageInput = document.getElementById('message-input');
    const sendButton = document.getElementById('send-btn');

    messageInput.disabled = true;
    sendButton.disabled = true;
    messageInput.value = "";
}

// Connect WebSocket
function connectWebSocket(codeInvite) {
    if (chatSocket !== null) {
        chatSocket.close();
    }

    currentRoom = codeInvite;
    document.getElementById('current-room').textContent = `Room: ${codeInvite}`;

    // Use secure WebSocket if the page is served over HTTPS
    const protocol = window.location.protocol === 'https:' ? 'wss://' : 'ws://';
    chatSocket = new WebSocket(`${protocol}${window.location.host}/ws/chat/${codeInvite}/`);

    chatSocket.onopen = function () {
        console.log("WebSocket connected");
    };

    chatSocket.onmessage = function (event) {
        const data = JSON.parse(event.data);
        console.log("Received message:", data); // Debug received messages

        if (data.type === "user_list") {
            updateUserList(data.users);
        } else if (data.type === "user_joined") {
            addUserToList(data.username);
        } else if (data.type === "user_left") {
            removeUserFromList(data.username);
        } else if (data.type === "chat_message") {
            displayMessage(data.username, data.message);
        } else if (data.type === "typing_status") {
            console.log("Received typing status:", data.is_typing, "for user:", data.username); // Debug typing status
            showTypingIndicator(data.is_typing, data.username);
        }
    };

    chatSocket.onclose = function () {
        console.log("WebSocket disconnected");
    };

    chatSocket.onerror = function (error) {
        console.error("WebSocket error:", error);
    };
}

// Send message via WebSocket
function sendMessage() {
    const messageInput = document.getElementById('message-input');
    const message = messageInput.value.trim();

    if (message && chatSocket !== null) {
        chatSocket.send(JSON.stringify({
            type: "message",
            message: message
        }));
        messageInput.value = "";
        // Reset typing status after sending a message
        isTyping = false;
        sendTypingStatus(false);
        clearTimeout(typingTimer);
    }
}

// Send typing status
function sendTypingStatus(status) {
    if (chatSocket !== null && chatSocket.readyState === WebSocket.OPEN) {
        console.log("Sending typing status:", status, "for user:", user.username); // Debug typing status
        chatSocket.send(JSON.stringify({
            'type': 'typing',
            'is_typing': status,
            'username': user.username
        }));
    }
}

// Display user list in room
function updateUserList(users) {
    const userListContainer = document.getElementById("user-list");
    userListContainer.innerHTML = "";

    users.forEach(user => {
        const userElement = document.createElement("li");
        userElement.textContent = user;
        userListContainer.appendChild(userElement);
    });

    console.log("🟢 Users in room:", users);
}

// Add user to list
function addUserToList(user) {
    const userListContainer = document.getElementById("user-list");
    // Check if user already exists in the list
    if (!Array.from(userListContainer.children).some(child => child.textContent === user)) {
        const userElement = document.createElement("li");
        userElement.textContent = user;
        userListContainer.appendChild(userElement);
    }
}

// Remove user from list
function removeUserFromList(user) {
    const userListContainer = document.getElementById("user-list");
    Array.from(userListContainer.children).forEach(child => {
        if (child.textContent === user) {
            userListContainer.removeChild(child);
        }
    });
}

// Display message in interface
function displayMessage(username, message) {
    const chatBox = document.getElementById("chat-box");
    const messageElement = document.createElement("p");
    messageElement.textContent = `${username}: ${message}`;
    chatBox.appendChild(messageElement);
    chatBox.scrollTop = chatBox.scrollHeight;
}

// Show typing indicator
function showTypingIndicator(isTyping, typingUsername) {
    const typingIndicator = document.getElementById("typing-indicator");
    if (isTyping && typingUsername !== user.username) {
        typingIndicator.style.display = "flex";
    } else {
        typingIndicator.style.display = "none";
    }
}

// Handle leaving room
function leaveRoom() {
    if (currentRoom) {
        fetch(`/api/v1/rooms/leave/${currentRoom}/`, {method: "POST"})
            .then(response => response.json())
            .then(() => {
                if (chatSocket) {
                    chatSocket.close();
                    chatSocket = null;
                }
                document.getElementById("user-list").innerHTML = "";
                document.getElementById("chat-box").innerHTML = "";
                document.getElementById("current-room").textContent = "Room: Not connected";
                currentRoom = null;
                disableChatInterface();
                alert("Bạn đã rời phòng thành công!");
            })
            .catch(error => console.error("Lỗi khi rời phòng:", error));
    }
}

// Get user information
function getUserInfo() {
    fetch("/api/v1/auth/user/")
        .then(response => response.json())
        .then(data => {
            user = data;
            console.log(user)
        })
        .catch(error => console.error("Lỗi khi lấy thông tin người dùng:", error));
}

// Event listeners
document.addEventListener("DOMContentLoaded", function () {
    // Initialize UI state on page load
    initUI();
    getUserInfo();
    // Listen for input events in message input (detects typing)
    document.getElementById("message-input").addEventListener("input", function () {
        if (currentRoom && chatSocket && chatSocket.readyState === WebSocket.OPEN) {
            if (!isTyping) {
                isTyping = true;
                sendTypingStatus(true);
            }

            // Reset timer on each key press
            clearTimeout(typingTimer);
            typingTimer = setTimeout(() => {
                isTyping = false;
                sendTypingStatus(false);
            }, TYPING_TIMEOUT);
        }
    });

    // Send message on Enter key press
    document.getElementById("message-input").addEventListener("keydown", function (event) {
        if (event.key === "Enter" && !event.shiftKey && !this.disabled) {
            event.preventDefault();
            sendMessage();
        }
    });

    // Add click handler for send button
    document.getElementById("send-btn").addEventListener("click", sendMessage);
});
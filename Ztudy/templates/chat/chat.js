// chat.js

let isTyping = false;
let typingTimer = null;
const TYPING_TIMEOUT = 2000; // 2 seconds

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
        isTyping = false;
        sendTypingStatus(false);
        clearTimeout(typingTimer);
    }
}

// Send typing status
function sendTypingStatus(status) {
    if (chatSocket !== null && chatSocket.readyState === WebSocket.OPEN) {
        chatSocket.send(JSON.stringify({
            'type': 'typing',
            'is_typing': status,
            'username': user.username
        }));
    }
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

// Display message in interface
function displayMessage(username, message) {
    const chatBox = document.getElementById("chat-box");
    const messageElement = document.createElement("p");
    messageElement.textContent = `${username}: ${message}`;
    chatBox.appendChild(messageElement);
    chatBox.scrollTop = chatBox.scrollHeight;
}

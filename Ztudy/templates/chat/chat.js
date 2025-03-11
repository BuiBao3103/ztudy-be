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
            message: message,
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
        }));
    }
}

// Show typing indicator
function showTypingIndicator(isTyping, user) {
    const typingIndicator = document.getElementById("typing-indicator");
    if (isTyping && user.id !== currentUser.id) {
        typingIndicator.style.display = "flex";
    } else {
        typingIndicator.style.display = "none";
    }
}

// Display message in interface
function displayMessage(user, message) {
    const chatBox = document.getElementById("chat-box");
    const messageElement = document.createElement("p");
    messageElement.textContent = `${user.id}-${user.username}: ${message}`;  // Bạn có thể thay đổi thành userId ở đây
    chatBox.appendChild(messageElement);
    chatBox.scrollTop = chatBox.scrollHeight;
}

function updateRequestList(requests) {
    const requestListContainer = document.getElementById("request-list");
    requestListContainer.innerHTML = "";

    requests.forEach(user => {
        const userElement = document.createElement("li");
        userElement.textContent = `${user.id} - ${user.username}`;

        const approveButton = document.createElement("button");
        approveButton.textContent = "Approve";
        approveButton.onclick = function () {
            approveUser(user.id);
        };

        userElement.appendChild(approveButton);
        requestListContainer.appendChild(userElement);
    });
}

// Gửi yêu cầu phê duyệt người dùng
function approveUser(userId) {
    fetch(`/api/v1/rooms/${currentRoom}/approve/${userId}/`, {method: "POST"})
        .then(response => response.json())
        .then(data => {
            alert(data.message);
        })
        .catch(error => console.error("Error approving user:", error));
}

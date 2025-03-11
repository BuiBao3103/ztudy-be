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

// Make sure the handleWebSocketMessage function properly handles pending requests
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

// Update the request list display function
function updateRequestList(requests) {
    console.log("Updating request list with:", requests);
    const requestListContainer = document.getElementById("request-list");
    requestListContainer.innerHTML = "";

    if (!requests || requests.length === 0) {
        const emptyMessage = document.createElement("li");
        emptyMessage.textContent = "No pending requests";
        requestListContainer.appendChild(emptyMessage);
        return;
    }

    requests.forEach(user => {
        const userElement = document.createElement("li");
        userElement.textContent = `${user.username} (ID: ${user.id})`;

        const approveButton = document.createElement("button");
        approveButton.textContent = "Approve";
        approveButton.className = "approve-button";
        approveButton.onclick = function() {
            approveUser(user.id);
        };

        userElement.appendChild(approveButton);
        requestListContainer.appendChild(userElement);
    });
}

// Gửi yêu cầu phê duyệt người dùng
function approveUser(userId) {
    fetch(`/api/v1/rooms/${currentRoom}/approve/${userId}/`, {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        console.log("User approved:", data);
        alert(data.message);
    })
    .catch(error => {
        console.error("Error approving user:", error);
        alert("Error approving user: " + error.message);
    });
}

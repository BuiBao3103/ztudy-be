// ui.js

// Initialize UI state
function initUI() {
    const messageInput = document.getElementById('message-input');
    const sendButton = document.getElementById('send-btn');

    // Disable chat functionality when not in a room
    messageInput.disabled = true;
    sendButton.disabled = true;
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

// Update user list in room
function updateUserList(users) {
    const userListContainer = document.getElementById("user-list");
    userListContainer.innerHTML = "";

    users.forEach(user => {
        const userElement = document.createElement("li");
        userElement.textContent = user.id + "-" + user.username;
        userListContainer.appendChild(userElement);
    });
}

// Add user to list
function addUserToList(user) {
    const userListContainer = document.getElementById("user-list");
    if (!Array.from(userListContainer.children).some(child => child.textContent === user.id + "-" + user.username)) {
        const userElement = document.createElement("li");
        userElement.textContent = user.id + "-" + user.username
        userListContainer.appendChild(userElement);
    }
}

// Remove user from list
function removeUserFromList(user) {
    const userListContainer = document.getElementById("user-list");
    Array.from(userListContainer.children).forEach(child => {
        if (child.textContent === user.id + "-" + user.username) {
            userListContainer.removeChild(child);
        }
    });
}

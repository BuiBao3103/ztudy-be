// app.js

document.addEventListener("DOMContentLoaded", function () {
    // Initialize UI and user info
    initUI();
    getUserInfo();

    // Connect WebSocket online
    connectOnlineSocket();

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
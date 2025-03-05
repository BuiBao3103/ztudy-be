let chatSocket = null;
let currentRoom = null;
let typingTimer = null;
let isTyping = false;
const TYPING_TIMEOUT = 2000; // 2 seconds
let userId = generateUserId(); // Generate a unique ID for this user session

// Generate a random user ID for the current session
function generateUserId() {
    return 'user_' + Math.random().toString(36).substr(2, 9);
}

// Lấy code_invite từ URL
const codeInvite = window.location.pathname.split('/')[3]; // Lấy phần cuối của URL

// Join the chat room based on code_invite
function joinRoom(codeInvite) {
    if (chatSocket !== null) {
        chatSocket.close();
    }

    currentRoom = codeInvite;
    document.getElementById('current-room').textContent = `Room: ${codeInvite}`;
    chatSocket = new WebSocket('ws://' + window.location.host + '/ws/chat/' + codeInvite + '/');

    // Khi WebSocket kết nối thành công
    chatSocket.onopen = function(e) {
        console.log('WebSocket connected');
    };

    // Khi nhận được tin nhắn mới
    chatSocket.onmessage = function(e) {
        const data = JSON.parse(e.data);

        // Xử lý thông báo typing
        if (data.type === 'typing_status') {
            const typingIndicator = document.getElementById('typing-indicator');

            // Only show typing indicator if it's not from the current user
            if (data.is_typing && data.user_id !== userId) {
                typingIndicator.style.display = 'flex';
            } else {
                typingIndicator.style.display = 'none';
            }
        }
        // Xử lý tin nhắn thông thường
        else if (data.message) {
            const message = data.message;
            const chatBox = document.getElementById('chat-box');

            // Tạo phần tử cho tin nhắn mới
            const newMessage = document.createElement('p');
            newMessage.textContent = message;

            // Thêm tin nhắn vào đầu chat-box để tin nhắn mới xuất hiện dưới cùng
            chatBox.insertBefore(newMessage, chatBox.firstChild);

            // Cuộn xuống dưới cùng của chat-box
            chatBox.scrollTop = chatBox.scrollHeight;

            // Ẩn typing indicator khi có tin nhắn mới
            document.getElementById('typing-indicator').style.display = 'none';
        }
    };

    // Khi WebSocket bị đóng
    chatSocket.onclose = function(e) {
        console.log('WebSocket disconnected');
    };
}

// Gửi tin nhắn tới WebSocket
function sendMessage() {
    const messageInput = document.getElementById('message-input');
    const message = messageInput.value;
    if (message && chatSocket !== null) {
        chatSocket.send(JSON.stringify({
            'message': message
        }));
        messageInput.value = ''; // Xóa ô input sau khi gửi

        // Reset typing status when sending a message
        isTyping = false;
        sendTypingStatus(false);
        clearTimeout(typingTimer);
    }
}

// Gửi trạng thái typing
function sendTypingStatus(status) {
    if (chatSocket !== null) {
        chatSocket.send(JSON.stringify({
            'type': 'typing',
            'is_typing': status,
            'user_id': userId  // Include the user ID with the typing status
        }));
    }
}

// Lắng nghe sự kiện phím khi gõ tin nhắn
document.getElementById('message-input').addEventListener('input', function(event) {
    if (!isTyping) {
        // Set typing status to true
        isTyping = true;
        sendTypingStatus(true);
    }

    // Reset the timer
    clearTimeout(typingTimer);
    typingTimer = setTimeout(function() {
        isTyping = false;
        sendTypingStatus(false);
    }, TYPING_TIMEOUT);
});

// Lắng nghe sự kiện phím Enter để gửi tin nhắn
document.getElementById('message-input').addEventListener('keydown', function(event) {
    if (event.key === 'Enter') {
        event.preventDefault(); // Ngăn chặn hành vi mặc định của Enter (ngắt dòng)
        sendMessage(); // Gửi tin nhắn khi nhấn Enter
    }
});

// Bắt đầu join room
joinRoom(codeInvite);
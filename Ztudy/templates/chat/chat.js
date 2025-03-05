let chatSocket = null;
let currentRoom = null;

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
        const message = data['message'];
        const chatBox = document.getElementById('chat-box');

        // Tạo phần tử cho tin nhắn mới
        const newMessage = document.createElement('p');
        newMessage.textContent = message;

        // Thêm tin nhắn vào đầu chat-box để tin nhắn mới xuất hiện dưới cùng
        chatBox.insertBefore(newMessage, chatBox.firstChild);

        // Cuộn xuống dưới cùng của chat-box
        chatBox.scrollTop = chatBox.scrollHeight;
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
    }
}

// Lắng nghe sự kiện phím Enter để gửi tin nhắn
document.getElementById('message-input').addEventListener('keydown', function(event) {
    if (event.key === 'Enter') {
        event.preventDefault(); // Ngăn chặn hành vi mặc định của Enter (ngắt dòng)
        sendMessage(); // Gửi tin nhắn khi nhấn Enter
    }
});

// Bắt đầu join room
joinRoom(codeInvite);

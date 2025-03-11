// user.js

let user = {};

// Get user information
function getUserInfo() {
    fetch("/api/v1/auth/user/")
        .then(response => response.json())
        .then(data => {
            user = data;
            console.log(user);
        })
        .catch(error => console.error("Lỗi khi lấy thông tin người dùng:", error));
}

// Join room
function joinRoom() {
    const codeInvite = document.getElementById('room-code').value.trim();
    if (!codeInvite) {
        alert("Vui lòng nhập mã phòng!");
        return;
    }

    fetch(`/api/v1/rooms/join/${codeInvite}/`, {method: "POST"})
        .then(response => response.json())
        .then(data => {
            if (data.message === "Joined room successfully!") {
                connectWebSocket(codeInvite);
                enableChatInterface();
            } else {
                alert("Bạn cần chờ admin xét duyệt để vào phòng!");
            }
        })
        .catch(error => console.error("Lỗi khi vào phòng:", error));
}

// Leave room
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

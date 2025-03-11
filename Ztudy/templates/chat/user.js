// user.js

let currentUser = {};

// Get user information
function getUserInfo() {
    fetch("/api/v1/auth/user/")
        .then(response => response.json())
        .then(data => {
            currentUser = data;
            console.log(currentUser);
        })
        .catch(error => console.error("Lỗi khi lấy thông tin người dùng:", error));
}

// Revised JoinRoom function
function joinRoom() {
    const codeInvite = document.getElementById('room-code').value.trim();
    if (!codeInvite) {
        alert("Please enter a room code!");
        return;
    }


    // Then send join request to the API
    fetch(`/api/v1/rooms/join/${codeInvite}/`, {method: "POST"})
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log("Join room response:", data);

            if (data.message === "Joined room successfully!") {
                // User has been approved, enable chat interface
                enableChatInterface();
            } else if (data.message === "Waiting for admin approval") {
                // User is waiting for approval
                disableChatInterface();
                alert("You need to wait for admin approval to join the room!");
            }
            connectWebSocket(codeInvite);

        })
        .catch(error => {
            console.error("Error joining room:", error);
            alert("Error joining room: " + error.message);
        });
}

// Updated leaveRoom function to handle disconnection properly
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
                document.getElementById("request-list").innerHTML = "";
                document.getElementById("chat-box").innerHTML = "";
                document.getElementById("current-room").textContent = "Room: Not connected";
                currentRoom = null;
                disableChatInterface();
                alert("You have successfully left the room!");
            })
            .catch(error => console.error("Error leaving room:", error));
    }
}
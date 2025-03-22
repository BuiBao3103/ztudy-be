const protocolOnlineSocket =
  window.location.protocol === "https:" ? "wss://" : "ws://";
let onelineSocket = new WebSocket(
  `${protocolOnlineSocket}${window.location.host}/ws/online/`
);

onelineSocket.onmessage = function (event) {
  const data = JSON.parse(event.data);
  console.log(data);
  if (data.type === "online_count") {
    console.log(`Số người online hiện tại: ${data.online_count}`);
    updateOnlineCount(data.online_count);
  }

  if (data.type === "send_achievement") {
    console.log(`Cập nhật level mới: ${data.level}`);
  }
};

onelineSocket.onclose = function () {
  console.log("Mất kết nối online WebSocket!");
};

onelineSocket.onerror = function (error) {
  console.error("WebSocket error:", error);
};

// Cập nhật số lượng người online trên giao diện
function updateOnlineCount(count) {
  const onlineCountElement = document.getElementById("online-count");
  if (onlineCountElement) {
    onlineCountElement.textContent = `Số người online: ${count}`;
  }
}

// Hàm để mở kết nối WebSocket
function connectOnlineSocket() {
  if (onelineSocket.readyState === WebSocket.CLOSED) {
    onelineSocket = new WebSocket(
      `${protocolOnlineSocket}${window.location.host}/ws/online/`
    );
  }
}

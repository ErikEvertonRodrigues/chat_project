const roomName = JSON.parse(document.getElementById('room-name').textContent);  

const chatSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/chat/'
    + roomName
    + '/'
);

chatSocket.onopen = function(e) {
    console.log("WebSocket connection opened!");
};

chatSocket.onmessage = function(e) {
    data = JSON.parse(e.data);
    if (data.type == "chat.history") {
        appendMessage(data.sender, data.message, data.timestamp, true);
    } else {
        appendMessage(data.sender, data.message, data.timestamp, false);
    }
};

function appendMessage(sender, message, timestamp, isHistory) {
    const container = document.getElementById("chat-log");
    const div = document.createElement("div");
    //After: Add logic with isHistory, but for now let's make it simple

    div.innerHTML = `${sender}: ${message} <br> ${formatTimeStamp(timestamp)}`
    div.classList.add("bg-room-base", "inline-block", "w-fit", "rounded-lg", "p-2", "text-white");
    container.appendChild(div)
}

chatSocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
};

document.querySelector('#chat-message-input').focus();
document.querySelector('#chat-message-input').onkeyup = function(e) {
    if (e.key == 'Enter') {
        document.querySelector('#chat-message-submit').click();
    }
};

document.querySelector('#chat-message-submit').onclick = function(e) {
    const messageInputDom = document.querySelector('#chat-message-input');
    const message = messageInputDom.value;  
    chatSocket.send(JSON.stringify({
        'message': message
    }));
    messageInputDom.value = '';
};

function formatTimeStamp(isoString) {
    const date = new Date(isoString);

    const options = {
        timeZone: 'America/Sao_Paulo',
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
        hour12: false,
    };

    const formatter = new Intl.DateTimeFormat('pt-BR', options);
    const formatted = formatter.format(date);

    return formatted + 'h';
}

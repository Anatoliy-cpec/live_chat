

const roomName = JSON.parse(document.getElementById('room-id').textContent);
const authorFrom = JSON.parse(document.getElementById('author').textContent);



const websocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/chat/room/'
    + roomName
    + '/'
);

output = document.getElementById('personel-messages')
input = document.getElementById('chat-message-input')
btnSend = document.getElementById('chat-message-submit')

websocket.onopen = function(e) {
    console.log('Chat socket open');
};

websocket.onmessage = function(e) {
    console.log(e.data)
    const data = JSON.parse(e.data);
    element = document.createElement('div')
    element.className = 'messages-message my-message'
    element.innerHTML = `<img class="message-avatar" src="${data.avatar_url}" alt="avatar">
                    <span class="message-text"><p class="message-author">${data.message.author}</p><p class="message-date">${data.message.creation_date}</p>${data.message.text}</span>`
    
    output.prepend(element);

    if (data.message.author == authorFrom) {
        element.className = 'messages-message my-message'
    } else {
        element.className = 'messages-message'
    }
};

websocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
};

input.focus();

btnSend.onclick = function(e) {
    e.preventDefault();  // prevent form from submitting
    const messageInputDom = input;
    const message = messageInputDom.value;
    websocket.send(JSON.stringify({
        'message': message,
        'author': authorFrom,
        'command': 'new_message',
    }));
    messageInputDom.value = '';
};
const socket = io();

document.getElementById('join-btn').addEventListener('click', () => {
    const username = document.getElementById('username').value;
    if (!username) {
        alert("Username cannot be empty");
        return;
    }
    document.getElementById('username').disabled = true;
    document.getElementById('join-btn').disabled = true;

    socket.emit('join_chat', { username });

    // Show the "Connected Successfully" message
    document.getElementById('success-message').textContent = `Connected Successfully [${username}]`;
    document.getElementById('success-message').style.display = 'block';

    socket.emit('user_joined', { username });

    // Optionally, display a "connected" message on the client
    const messagesDiv = document.getElementById('messages');
    const joinMessageElement = document.createElement('div');
    joinMessageElement.classList.add('join-message');
    joinMessageElement.textContent = `You have entered the chat as ${username}`;
    messagesDiv.appendChild(joinMessageElement);
});

document.getElementById('send-icon').addEventListener('click', () => {
    const message = document.getElementById('message').value;
    const username = document.getElementById('username').value;
    if (!message) {
        alert("Message cannot be empty");
        return;
    }
    socket.emit('send_message', { username, message });
    document.getElementById('message').value = '';
});

socket.on('user_joined', (data) => {
    const messagesDiv = document.getElementById('messages');
    const joinMessageElement = document.createElement('div');
    joinMessageElement.classList.add('join-message');
    joinMessageElement.textContent = `${data.username} has entered the chat`;
    messagesDiv.appendChild(joinMessageElement);
});

socket.on('receive_message', (data) => {
    const messagesDiv = document.getElementById('messages');
    const messageElement = document.createElement('div');
    const username = data.username;
    const message = data.message;
    
    // Check if the message is sent by the current user or another user
    if (username === document.getElementById('username').value) {
        messageElement.classList.add('message', 'sent');  // Style for the current user's message
    } else {
        messageElement.classList.add('message', 'received');  // Style for other users' messages
    }

    
    messageElement.textContent = `[${data.username}] ${data.message} (${data.classification})`;
    messagesDiv.appendChild(messageElement);
});

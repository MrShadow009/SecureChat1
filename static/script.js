const socket = io();
let currentRoom = null;
let username = null;

document.getElementById('create-room-btn').addEventListener('click', () => {
    document.getElementById('create-room-modal').classList.add('show');
});

document.getElementById('join-room-btn').addEventListener('click', () => {
    document.getElementById('join-room-modal').classList.add('show');
});

document.querySelectorAll('.close-modal').forEach(btn => {
    btn.addEventListener('click', () => {
        btn.closest('.modal').classList.remove('show');
    });
});

document.getElementById('submit-create').addEventListener('click', async () => {
    const name = document.getElementById('room-name').value;
    const algorithm = document.getElementById('algorithm-select').value;
    const passphrase = document.getElementById('passphrase').value;
    const creator = document.getElementById('creator').value;

    const response = await fetch('/create-room', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, algorithm, passphrase, creator })
    });

    const data = await response.json();
    alert(`Room created! ID: ${data.room_id}, Token: ${data.token}`);
    document.getElementById('create-room-modal').classList.remove('show');
});

document.getElementById('submit-join').addEventListener('click', async () => {
    const room_id = document.getElementById('join-room-id').value;
    const passphrase = document.getElementById('join-passphrase').value;
    const joinUsername = document.getElementById('join-username').value;

    const response = await fetch('/join-room', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ room_id, passphrase })
    });

    if (response.ok) {
        const data = await response.json();
        currentRoom = room_id;
        username = joinUsername;
        document.getElementById('room-title').textContent = data.room_name;
        document.getElementById('algorithm').textContent = `Algorithm: ${data.algorithm}`;
        socket.emit('join', { username, room_id });
        document.getElementById('join-room-modal').classList.remove('show');
    } else {
        alert('Failed to join room');
    }
});

document.getElementById('send-btn').addEventListener('click', () => {
    const message = document.getElementById('message-input').value;
    if (message && currentRoom) {
        socket.emit('message', { room_id: currentRoom, username, message });
        document.getElementById('message-input').value = '';
    }
});

socket.on('message', (data) => {
    const msgDiv = document.createElement('div');
    msgDiv.className = 'message';
    msgDiv.textContent = `${data.username}: ${data.message}`;
    document.getElementById('messages').appendChild(msgDiv);
});

socket.on('status', (data) => {
    const msgDiv = document.createElement('div');
    msgDiv.className = 'message';
    msgDiv.textContent = data.msg;
    document.getElementById('messages').appendChild(msgDiv);
});

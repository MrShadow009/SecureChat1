document.addEventListener('DOMContentLoaded', () => {
    let currentRoom = null;
    let username = null;
    let lastMessageId = -1;
    let messageInterval = null;
    let participantInterval = null;

    document.getElementById('createRoomBtn').addEventListener('click', async () => {
    // Fetch algorithms list from backend
    try {
        const response = await fetch('/api/algorithms');
        const data = await response.json();
        const algorithmSelect = document.getElementById('algorithm');
        algorithmSelect.innerHTML = ''; // Clear existing options
        data.algorithms.forEach((alg) => {
            const option = document.createElement('option');
            option.value = alg;
            option.textContent = alg;
            algorithmSelect.appendChild(option);
        });
    } catch (error) {
        console.error('Failed to load algorithms:', error);
    }
    document.getElementById('createModal').classList.add('show');
});

document.getElementById('joinRoomBtn').addEventListener('click', () => {
    document.getElementById('joinModal').classList.add('show');
});

document.getElementById('createClose').addEventListener('click', () => {
    document.getElementById('createModal').classList.remove('show');
});
document.getElementById('joinClose').addEventListener('click', () => {
    document.getElementById('joinModal').classList.remove('show');
});

document.getElementById('createSubmit').addEventListener('click', async () => {
    const name = document.getElementById('roomName').value;
    const algorithm = document.getElementById('algorithm').value;
    const passphrase = document.getElementById('passphrase').value;
    const creator = 'unknown'; // No creator input in HTML, set default or add input if needed

    const response = await fetch('/api/create-room', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ room_name: name, algorithm, passphrase, creator })
    });

    const data = await response.json();
    if (data.room_id) {
        alert(`Room created! ID: ${data.room_id}`);
        document.getElementById('createModal').classList.remove('show');
        // Optionally auto-fill Join modal
        document.getElementById('joinRoomId').value = data.room_id;
    } else {
        alert('Error: ' + JSON.stringify(data));
    }
});

document.getElementById('joinSubmit').addEventListener('click', async () => {
    const room_id = document.getElementById('joinRoomId').value;
    const passphrase = document.getElementById('joinPass').value;
    const joinUsername = document.getElementById('joinName').value || ('user-' + Math.floor(Math.random() * 1000));

    const response = await fetch('/api/join-room', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ room_id, passphrase, username: joinUsername })
    });

    const data = await response.json();
    if (data.error) {
        alert('Join failed: ' + data.error);
    } else {
        currentRoom = room_id;
        username = joinUsername;
        document.getElementById('roomHeader').textContent = `Room: ${room_id}`;
        // Assuming algorithm display is in roomInfo div
        document.getElementById('roomInfo').textContent = `Algorithm: ${data.algorithm}`;
        document.getElementById('joinModal').classList.remove('show');
        appendMessage(`You joined room ${room_id} as ${username}`, 'meta');
        // Start polling
        startPolling();
    }
});

document.getElementById('sendBtn').addEventListener('click', () => {
    sendMessage();
});

document.getElementById('msgInput').addEventListener('keydown', (event) => {
    if (event.key === 'Enter') {
        event.preventDefault();
        sendMessage();
    }
});

function sendMessage() {
    const message = document.getElementById('msgInput').value.trim();
    if (message && currentRoom && username) {
        fetch('/api/send-message', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ room_id: currentRoom, username, message })
        });
        document.getElementById('msgInput').value = '';
    }
}

function appendMessage(text, cls = '') {
    const msgDiv = document.createElement('div');
    msgDiv.className = 'message ' + cls;
    msgDiv.textContent = text;
    document.getElementById('messages').appendChild(msgDiv);
    document.getElementById('messages').scrollTop = document.getElementById('messages').scrollHeight;
}

function startPolling() {
    pollMessages();
    pollParticipants();
    messageInterval = setInterval(pollMessages, 2000);
    participantInterval = setInterval(pollParticipants, 5000);
}

async function pollMessages() {
    if (!currentRoom) return;
    try {
        const response = await fetch(`/api/get-messages?room_id=${currentRoom}`);
        const data = await response.json();
        if (data.messages) {
            data.messages.forEach(msg => {
                if (msg.id > lastMessageId) {
                    appendMessage(`${msg.username}: ${msg.message}`);
                    lastMessageId = msg.id;
                }
            });
        }
    } catch (e) {
        console.error('Poll messages error:', e);
    }
}

async function pollParticipants() {
    if (!currentRoom) return;
    try {
        const response = await fetch(`/api/get-participants?room_id=${currentRoom}`);
        const data = await response.json();
        if (data.participants) {
            const membersList = document.getElementById('participantsList');
            membersList.innerHTML = '';
            data.participants.forEach(p => {
                const li = document.createElement('li');
                li.textContent = p;
                membersList.appendChild(li);
            });
        }
    } catch (e) {
        console.error('Poll participants error:', e);
    }
}
});

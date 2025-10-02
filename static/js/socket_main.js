let currentRoomId = null;
let myUsername = null;
let lastMessageId = -1;
let messageInterval = null;
let participantInterval = null;

// UI elements
const createBtn = document.getElementById('createRoomBtn');
const createModal = document.getElementById('createModal');
const joinBtn = document.getElementById('joinRoomBtn');
const joinModal = document.getElementById('joinModal');

const messagesEl = document.getElementById('messages');
const participantsList = document.getElementById('participantsList');
const roomTitle = document.getElementById('roomTitle');
const leaveRoomBtn = document.getElementById('leaveRoomBtn');

// small helper
function appendMessage(text, cls='') {
  const p = document.createElement('div');
  p.className = 'msg ' + cls;
  p.textContent = text;
  messagesEl.appendChild(p);
  messagesEl.scrollTop = messagesEl.scrollHeight;
}

// Toggle modals
createBtn.onclick = ()=> createModal.style.display = 'flex';
document.getElementById('createClose').onclick = ()=> createModal.style.display = 'none';
joinBtn.onclick = ()=> joinModal.style.display = 'flex';
document.getElementById('joinClose').onclick = ()=> joinModal.style.display = 'none';

// Create room
document.getElementById('createSubmit').onclick = async ()=>{
  const room_name = document.getElementById('roomName').value;
  const algorithm = document.getElementById('algorithm').value;
  const passphrase = document.getElementById('passphrase').value;
  if(!room_name || !passphrase) return alert('name+pass required');
  const res = await fetch('/api/create-room', {
    method:'POST', headers:{'Content-Type':'application/json'},
    body: JSON.stringify({room_name, algorithm, passphrase, creator:'web'})
  });
  const data = await res.json();
  if(data.room_id) {
    alert('Room created: ' + data.room_id);
    createModal.style.display = 'none';
    // Optionally auto-fill Join modal
    document.getElementById('joinRoomId').value = data.room_id;
  } else {
    alert('Error: ' + JSON.stringify(data));
  }
};

// Join room
document.getElementById('joinSubmit').onclick = async ()=>{
  const room_id = document.getElementById('joinRoomId').value;
  const passphrase = document.getElementById('joinPass').value;
  const username = document.getElementById('joinName').value || ('user-' + Math.floor(Math.random() * 1000));
  if(!room_id || !passphrase) return alert('room id + pass required');

  try {
    const res = await fetch('/api/join-room', {
      method:'POST', headers:{'Content-Type':'application/json'},
      body: JSON.stringify({room_id, passphrase, username})
    });
    const data = await res.json();
    if(data.error) {
      return alert('Join failed: ' + data.error);
    }
    myUsername = username;
    currentRoomId = room_id;
    lastMessageId = -1;
    roomTitle.textContent = `Room: ${room_id} (${data.algorithm})`;
    leaveRoomBtn.style.display = 'block';
    joinModal.style.display = 'none';
    appendMessage(`You joined room ${room_id} as ${username}`, 'meta');
    // Start polling
    startPolling();
  } catch (error) {
    console.error('Join fetch error:', error);
    alert('Network error during join');
  }
};

// Sending messages
document.getElementById('sendBtn').onclick = async ()=>{
  const input = document.getElementById('msgInput');
  const msg = input.value.trim();
  if(!msg || !currentRoomId || !myUsername) return;
  await fetch('/api/send-message', {
    method:'POST', headers:{'Content-Type':'application/json'},
    body: JSON.stringify({room_id: currentRoomId, username: myUsername, message: msg})
  });
  input.value = '';
};

function leaveRoom() {
  currentRoomId = null;
  myUsername = null;
  lastMessageId = -1;
  roomTitle.textContent = 'Select or create a room to begin';
  leaveRoomBtn.style.display = 'none';
  messagesEl.innerHTML = '';
  participantsList.innerHTML = '';
  appendMessage('You left the room', 'meta');
  if (messageInterval) clearInterval(messageInterval);
  if (participantInterval) clearInterval(participantInterval);
  messageInterval = null;
  participantInterval = null;
}

leaveRoomBtn.onclick = leaveRoom;

// Polling functions
function startPolling() {
  pollMessages();
  pollParticipants();
  messageInterval = setInterval(pollMessages, 2000);
  participantInterval = setInterval(pollParticipants, 5000);
}

async function pollMessages() {
  if (!currentRoomId) return;
  try {
    const res = await fetch(`/api/get-messages?room_id=${currentRoomId}`);
    const data = await res.json();
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
  if (!currentRoomId) return;
  try {
    const res = await fetch(`/api/get-participants?room_id=${currentRoomId}`);
    const data = await res.json();
    if (data.participants) {
      participantsList.innerHTML = '';
      data.participants.forEach(p => {
        const li = document.createElement('li');
        li.textContent = p;
        participantsList.appendChild(li);
      });
    }
  } catch (e) {
    console.error('Poll participants error:', e);
  }
}

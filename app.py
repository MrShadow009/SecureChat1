from flask import Flask, render_template, request, jsonify
from passlib.hash import pbkdf2_sha256
import uuid

app = Flask(__name__)
app.config['SECRET_KEY'] = 'replace-with-a-secure-secret'

# In-memory room store (prototype). Replace with DB for production.
# Structure: rooms[room_id] = {name, algorithm, pass_hash, participants: {username: True}, messages: []}
rooms = {}

@app.route('/')
def index():
    return render_template('index_socketio.html')

# Create a room (HTTP POST)
@app.route('/api/create-room', methods=['POST'])
def create_room():
    data = request.json or {}
    room_name = data.get('room_name')
    algorithm = data.get('algorithm', 'RSA')
    passphrase = data.get('passphrase')
    creator = data.get('creator', 'unknown')

    if not room_name or not passphrase:
        return jsonify({'error': 'room_name and passphrase required'}), 400

    room_id = str(uuid.uuid4())
    pass_hash = pbkdf2_sha256.hash(passphrase)
    rooms[room_id] = {
        'name': room_name,
        'algorithm': algorithm,
        'pass_hash': pass_hash,
        'creator': creator,
        'participants': {},  # username -> True
        'messages': [],  # list of {'id':, 'username':, 'message':}
        'next_message_id': 0
    }
    return jsonify({'room_id': room_id, 'message': 'room created', 'algorithm': algorithm})

# Join-check (HTTP POST) - verifies passphrase, returns success
@app.route('/api/join-room', methods=['POST'])
def join_room_http():
    data = request.json or {}
    room_id = data.get('room_id')
    passphrase = data.get('passphrase')
    username = data.get('username') or 'guest'

    room = rooms.get(room_id)
    if not room:
        return jsonify({'error': 'room not found'}), 404

    if not pbkdf2_sha256.verify(passphrase, room['pass_hash']):
        return jsonify({'error': 'invalid passphrase'}), 403

    # Add participant
    room['participants'][username] = True
    return jsonify({'room_id': room_id, 'message': 'ok', 'algorithm': room['algorithm']})

# Polling endpoints for real-time simulation

@app.route('/api/send-message', methods=['POST'])
def send_message():
    data = request.json or {}
    room_id = data.get('room_id')
    username = data.get('username')
    message = data.get('message')
    room = rooms.get(room_id)
    if not room or username not in room['participants']:
        return jsonify({'error': 'unauthorized'}), 403
    msg_id = room['next_message_id']
    room['next_message_id'] += 1
    room['messages'].append({'id': msg_id, 'username': username, 'message': message})
    return jsonify({'success': True})

@app.route('/api/get-messages', methods=['GET'])
def get_messages():
    room_id = request.args.get('room_id')
    room = rooms.get(room_id)
    if not room:
        return jsonify({'error': 'room not found'}), 404
    return jsonify({'messages': room['messages'], 'next_id': room['next_message_id']})

@app.route('/api/get-participants', methods=['GET'])
def get_participants():
    room_id = request.args.get('room_id')
    room = rooms.get(room_id)
    if not room:
        return jsonify({'error': 'room not found'}), 404
    return jsonify({'participants': list(room['participants'])})

@app.route('/api/leave-room', methods=['POST'])
def leave_room():
    data = request.json or {}
    room_id = data.get('room_id')
    username = data.get('username')
    room = rooms.get(room_id)
    if room and username in room['participants']:
        del room['participants'][username]
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001, debug=True)

from flask_socketio import SocketIO, send, emit, join_room, leave_room
from flask import Flask, render_template, session, request
import poker

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

active_connections = []

@app.route('/')
def index():
    return render_template('index.html')

def check_for_capacity():
    num_players = len(active_connections)
    if num_players < 3:
        return
    
    poker.main_handler(active_connections, num_players)

@socketio.on('connect')
def connect():
    emit('my response', {'data': 'Connected'})

@socketio.on('register username')
def register_username(data):

    session['identifier'] = data
    username = data['username']
    active_connections.append(data)
    print(active_connections)
    check_for_capacity()
    send('Registered ' + data['username'], broadcast=True)

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected.')

@socketio.on('start game')
def start_game(data):
    print('Starting game!')
    print(data)

@socketio.on('message')
def handle_message(message):
    print('Received message: ', message)
    send(message, broadcast=True)

@socketio.on('check')
def on_check(data):
    username = session['username']
    send(username + ' has checked!', broadcast=True)

@socketio.on('fold')
def on_fold(data):
    username = session['username']
    send(username + ' has folded!', broadcast=True)

@socketio.on('raise')
def on_raise(data):
    username = session['username']
    send(username + ' has raised!', broadcast=True)

if __name__ == '__main__':
    socketio.run(app)
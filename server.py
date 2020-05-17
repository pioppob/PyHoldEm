from flask_socketio import SocketIO, send, emit, join_room, leave_room
from flask import Flask, render_template, session, request
import logging
import os
from Player import Player
from Table import Table
import time
import json
from maps import best_hand_map, rank_map, cpu_aggressiveness_map

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
socketio = SocketIO(app)

active_connections = []

def main_handler(connections, num_players):
    print('Starting game!')

    try:
        table = Table.instances[0]
    except:
        table = Table()

    if table.active_game:
        emit('wait-notif')
        send('Chat is temporarily disabled until next game.')
        return
    else:
        table.active_game = True


    while table.active_game:
        table.instantiate_players(connections)

        table.deal()

        for player in Player.instances:
            emit('deal', {
                'attributes': player.__dict__
            }, room=player.id)

        table.turn_action_handler(True)
        table.turn_action_handler(False)
        table.turn_action_handler(False)

        return table.determine_winner()

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def connect():
    print('Request SID: ', request.sid)

@socketio.on('backend handshake')
def handshake(user_data):
    user_data['sid'] = request.sid
    emit('frontend handshake', user_data)

@socketio.on('register user')
def register_username(data):

    session['identifier'] = data
    username = data['username']
    room = data['sid']
    join_room(room)
    active_connections.append(data)
    send(username + ' has joined the chat!', broadcast=True)
    check_for_capacity()

def check_for_capacity():
    num_players = len(active_connections)
    if num_players < 2:
        emit('queue-add', {
            'active_connections': ', '.join([connection['username'] for connection in active_connections]),
            'num_connections': len(active_connections)
        }, broadcast=True)
        return

    main_handler(active_connections, num_players)

@socketio.on('restart-game')
def restart():
    time.sleep(2)
    game_cleanup()
    time.sleep(3)
    check_for_capacity()

def game_cleanup():
    Table.instances = []
    Player.instances = []
    emit('game-cleanup', broadcast=True)

@socketio.on('disconnect')
def disconnect():
    connection = request.sid

    for entry in active_connections:
        if connection == entry['sid']:
            active_connections.remove(entry)

@socketio.on('start game')
def start_game(data):
    print('Starting game!')
    print(data)

@socketio.on('message')
def handle_message(message):
    player = Player.get_player(id=request.sid)
    body = f'{player.name}: {message}'
    send(body, broadcast=True)


@socketio.on('check')
def on_check(data):
    username = session['identifier']['username']

    table = Table.instances[0]
    player = Player.get_player(name=username)

    player._check(table)

    emit('toggle-display', {
        'display_type': 'three',
        'attributes': player.__dict__
    }, room=player.id)

    send(username + ' has checked!', broadcast=True)

@socketio.on('fold')
def on_fold(data):
    username = session['identifier']['username']

    table = Table.instances[0]
    player = Player.get_player(name=username)

    player._fold(table)

    emit('toggle-display', {
        'display_type': 'three',
        'attributes': player.__dict__
    }, room=player.id)

    send(username + ' has folded!', broadcast=True)

@socketio.on('timeout')
def on_timeout(data):
    username = session['identifier']['username']

    table = Table.instances[0]
    player = Player.get_player(name=username)

    player._fold(table)

    emit('toggle-display', {
        'display_type': 'three',
        'attributes': player.__dict__
    }, room=player.id)

    send(username + ' took too long!', broadcast=True)
    send(username + ' folded!', broadcast=True)


@socketio.on('raise')
def on_raise(data):
    username = session['identifier']['username']
    amount_to_raise = data['raise_amount']

    table = Table.instances[0]
    player = Player.get_player(name=username)

    player._raise(table, int(amount_to_raise))

    emit('toggle-display', {
        'display_type': 'three',
        'attributes': player.__dict__
    }, room=player.id)

    send(username + ' has raised ' + amount_to_raise + '!', broadcast=True)

@socketio.on('call')
def on_call(data):
    username = session['identifier']['username']

    table = Table.instances[0]
    player = Player.get_player(name=username)

    player._call(table)

    emit('toggle-display', {
        'display_type': 'three',
        'attributes': player.__dict__
    }, room=player.id)

    send(username + ' called!', broadcast=True)

if __name__ == '__main__':
    socketio.run(app)
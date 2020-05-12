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
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

active_connections = []

def main_handler(connections, num_players):
    print('Starting game!')

    table = Table()

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
    # print(request.__dict__['sid'])
    return render_template('index.html')

def check_for_capacity():
    num_players = len(active_connections)
    if num_players < 3:
        return
    
    main_handler(active_connections, num_players)

@socketio.on('connect')
def connect():
    print('Request SID: ', request.sid)

@socketio.on('backend handshake')
def handshake(user_data):
    print('Request SID 2: ', request.sid)
    user_data['sid'] = request.sid
    emit('frontend handshake', user_data)


@socketio.on('register user')
def register_username(data):

    session['identifier'] = data
    username = data['username']
    room = data['sid']
    join_room(room)
    
    active_connections.append(data)
    check_for_capacity()
    send('Registered ' + username + ' with room ' + room)

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
    username = session['identifier']['username']

    table = Table.instances[0]
    player = Player.get_player(name=username)

    player._check(table)

    emit('toggle-display', {
        'display_type': 'three'
    }, room=player.id)

    send(username + ' has checked!', broadcast=True)

@socketio.on('fold')
def on_fold(data):
    username = session['identifier']['username']

    table = Table.instances[0]
    player = Player.get_player(name=username)

    player._fold(table)

    emit('toggle-display', {
        'display_type': 'three'
    }, room=player.id)

    send(username + ' has folded!', broadcast=True)

@socketio.on('raise')
def on_raise(data):
    username = session['identifier']['username']
    amount_to_raise = data['raise_amount']

    table = Table.instances[0]
    player = Player.get_player(name=username)

    player._raise(table, int(amount_to_raise))

    emit('toggle-display', {
        'display_type': 'three'
    }, room=player.id)

    send(username + ' has raised!', broadcast=True)

@socketio.on('call')
def on_call(data):
    username = session['identifier']['username']

    table = Table.instances[0]
    player = Player.get_player(name=username)

    player._call(table)

    emit('toggle-display', {
        'display_type': 'three'
    }, room=player.id)

    send(username + ' has called!', broadcast=True)

if __name__ == '__main__':
    socketio.run(app)
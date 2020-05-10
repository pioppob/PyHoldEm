import itertools
import random
from collections import namedtuple
import logging
import os
from Player import Player
from maps import best_hand_map, rank_map, cpu_aggressiveness_map

class Table:

    SUITS=['DIAMONDS', 'SPADES', 'HEARTS', 'CLUBS']
    RANKS=list(range(2, 11)) + list('JQKA')

    def __init__(self):
        self.deck = list(itertools.product(self.RANKS, self.SUITS))
        self.available_cards = self.deck[:]
        self.community_cards = []
        self.pot = 0
        self.current_stake = 0
        self.active_players = []
        self.unfulfilled_action = []
        self.total_turns = 0
        self.active_game = True
        self.last_move = None

    def draw_card(self):
        card = random.choice(self.available_cards)
        self.available_cards.remove(card)
        return card

    def reset_stakes(self):

        for player in self.active_players:
            player.stake = 0

        if not self.unfulfilled_action:
            self.current_stake = 0
            return
        
        print('There are players that still need to take action.')

    def deal(self):
        for player in Player.instances:
            player.hand = [self.draw_card(), self.draw_card()]
            self.active_players.append(player)
            player.chips -= 50
            self.pot += 50

    def flop(self, initial=False):

        if initial:
            for x in range(3):
                card = self.draw_card()
                self.community_cards.append(card)
        else:
            card = self.draw_card()
            self.community_cards.append(card)

    def instantiate_players(self, players, username):

        if players > 8:
            raise Exception('This game supports a maximum of 8 players.')

        for x in range(players):
            if x == 0:
                name = username
                player = Player(name, 1000000)
            else:
                name = f'CPU {x}'
                player = Player(name, 1000000)

    def determine_turn_order(self):

        turn_order = []

        if not self.last_move:
            return Player.instances

        idx = Player.instances.index(self.last_move)
        idx += 1

        for x in range(idx, idx+len(Player.instances)):
            player = Player.instances[x % len(Player.instances)]

            if player in self.active_players:

                if not player == self.last_move:

                    if player in self.unfulfilled_action:
                        continue

                    turn_order.append(player)

        return turn_order

    def turn_action_handler(self, initial):

        user = Player.get_player(id=0)

        self.flop(initial=initial)
        
        turn_order = self.determine_turn_order()

        for player in turn_order:
            self.unfulfilled_action.append(player)

        while self.unfulfilled_action:

            # Never modify a list while iterating
            copy_of_ua_list = self.unfulfilled_action[:]

            for player in copy_of_ua_list:

                if player == user:
                    player.user_take_turn(self)
                else:
                    player.simulate_cpu_turn(self)

        self.reset_stakes()
                


    def determine_winner(self):

        winner = None
        best_hand = None

        for player in self.active_players:
            player._determine_best_hand(self)
            try:
                if winner is None and best_hand is None:
                    winner = player
                    best_hand = player.best_hand
                    continue

                elif player.best_hand < best_hand:
                    winner = player
                    best_hand = player.best_hand
                    continue

                elif player.best_hand == best_hand:
                    # print(self.community_cards)
                    winner = self.tie_break(winner, player)
                    continue
            except Exception as e:
                print('Error.', e),
                    

        user = Player.get_player(id=0)
        players = self._get_active_players()

        winning_hand = self.community_cards[:] + winner.hand
 
        if winner in players and not winner == user:
            print(f'{winner} won the pot! Winnings: {self.pot}. Best Hand: {best_hand_map[winner.best_hand]}.')
            print(f'Winning hand: {winning_hand}!')
        elif winner in players and winner == user:
            print(f'You won the pot! Winnings: {self.pot}. Best Hand: {best_hand_map[user.best_hand]}.')
            print(f'Winning hand: {winning_hand}!')
        elif len(winner) == 2:
            half_pot = self.pot // 2
            winner[0].chips += half_pot
            winner[1].chips += half_pot
            self.pot = 0
            print(f'Tie! {winner[0]} and {winner[1]} will split the pot at {half_pot} chips each.')

        self._end_game()

    def _end_game(self):
        self.unfulfilled_action = None
        self.active_players = None
        self.active_game = False

    def _get_active_players(self):
        return self.active_players

    def tie_break(self, player_one, player_two):
        p1_hand = sorted([rank_map[item[0]] for item in player_one.hand])
        # print('Tie break: ', player_one.name, p1_hand, best_hand_map[player_one.best_hand])
        p1_high_card = p1_hand[-1]

        p2_hand = sorted([rank_map[item[0]] for item in player_two.hand])
        # print('Tie break: ', player_two.name, p2_hand, best_hand_map[player_two.best_hand])
        p2_high_card = p2_hand[-1]

        if p1_high_card > p2_high_card:
            return player_one
        elif p2_high_card > p1_high_card:
            return player_two
        else:
            # print('Double tiebreaker')
            p1_high_card = p1_hand[-2]
            p2_high_card = p2_hand[-2]

            if p1_high_card > p2_high_card:
                return player_one
            elif p2_high_card > p1_high_card:
                return player_two
            else:
                winners = [player_one, player_two]
                return winners
from maps import best_hand_map, rank_map, cpu_aggressiveness_map
import random
import logging
import time
import itertools
from helpers import (
    is_royal, is_four_of_a_kind, is_full_house, is_flush,
    is_straight, is_three_of_a_kind, is_two_pair, is_one_pair,
    determine_flush_suit, is_game_over
)

class Player:
    
    id_counter = itertools.count()
    instances = []

    def __init__(self, name, chips):
        self.id = next(Player.id_counter)
        self.name = name
        self.chips = chips
        self.hand = None
        self.active = True
        self.best_hand = None
        self.aggressiveness = 0
        self.calculated_bet = 0
        self.stake = 0
        Player.instances.append(self)

    def __str__(self):
        return f'<{self.name}>'

    def __repr__(self):
        return f'Player(Name: {self.name}, Active: {self.active})'

    @classmethod
    def get_player(cls, **kwargs):
        if kwargs.get('name'):
            for player in Player.instances:
                if player.name == kwargs['name']:
                    return player
        elif kwargs.get('id') is not None:
            for player in Player.instances:
                if player.id == kwargs['id']:
                    return player

    def _call(self, table):

        amount_to_call = (table.current_stake - self.stake)
        self.chips -= amount_to_call
        self.stake += amount_to_call
        table.pot += amount_to_call
        table.unfulfilled_action.remove(self)
        table.total_turns += 1
        table.last_move = self

        print(f'{self} called {amount_to_call} chips!')

        return

    def _raise(self, table, amount_to_raise):

        self.chips -= amount_to_raise
        self.stake += amount_to_raise
        table.pot += amount_to_raise
        table.current_stake = amount_to_raise
        table.total_turns += 1
        table.last_move = self
        table.unfulfilled_action.remove(self)

        turn_order = table.determine_turn_order()
        table.unfulfilled_action.extend(turn_order)

        print(f'{self} raised {amount_to_raise} chips!')

        return

    def _fold(self, table):

        self.active = False
        self.stake = 0
        table.unfulfilled_action.remove(self)
        table.active_players.remove(self)
        table.total_turns += 1
        table.last_move = self

        print(f'{self} folded!')

        return

    def _check(self, table):

        table.unfulfilled_action.remove(self)
        table.total_turns += 1
        table.last_move = self

        print(f'{self} checked!')
        return

    def _determine_aggressiveness(self):

        if self.best_hand <= 2:
            self.aggressiveness = 5
        elif self.best_hand <= 3:
            self.agressiveness = 4
        elif self.best_hand <= 5:
            self.aggressiveness = 3
        elif self.best_hand <= 7:
            self.aggressiveness = 2
        elif self.best_hand <= 9:
            self.aggressiveness = 1
        else:
            self.aggressiveness = 0

    def _determine_best_hand(self, table):

        all_playable = set(table.community_cards).union(set(self.hand))
        sorted_hand = sorted(all_playable, key=lambda x: rank_map[x[0]])
        sorted_hand_ranked = [(rank_map[card[0]], card[1]) for card in sorted_hand]

        ranks = [card[0] for card in sorted_hand_ranked]
        suits = [card[1] for card in sorted_hand_ranked]

        if is_royal(ranks) and is_flush(suits[-5:]):
            self.best_hand = 1
            logging.critical('Royal Flush')

        elif is_flush(suits) and is_straight(ranks):
            suit = determine_flush_suit(suits)
            flush_hand = []
            for card in sorted_hand_ranked:
                if card[1] == suit:
                    flush_hand.append(card)

            if is_straight(list(card[0] for card in flush_hand)):
                self.best_hand = 2
                logging.critical('Straight Flush')

        elif is_four_of_a_kind(ranks):
            self.best_hand = 3
            logging.warning('Four of a Kind')
        elif is_full_house(ranks):
            self.best_hand = 4
            logging.info('Full House')
        elif is_flush(suits):
            self.best_hand = 5
            logging.info('Flush')
        elif is_straight(ranks):
            self.best_hand = 6
            logging.debug('Straight')
        elif is_three_of_a_kind(ranks):
            self.best_hand = 7
        elif is_two_pair(ranks):
            self.best_hand = 8
        elif is_one_pair(ranks):
            self.best_hand = 9
        else:
            self.best_hand = 10

    def _determine_bet_amount(self, table):

        self._determine_best_hand(table)
        self._determine_aggressiveness()

        percentage_bet = random.choice(cpu_aggressiveness_map[self.aggressiveness])
        decimal_bet = percentage_bet / 100

        bet = int(round(self.chips * decimal_bet, -3))

        self.calculated_bet = bet

    def simulate_cpu_turn(self, table):

        if is_game_over(table):
            return

        self._determine_best_hand(table)
        self._determine_aggressiveness()
        self._determine_bet_amount(table)

        time.sleep(1)

        # print(f'--------{self.name} TURN-------')
        # print('Turns: ', table.total_turns)
        # print('Table Cards: ', table.community_cards)
        # print('Table Pot: ', table.pot)
        # print('Table Stake: ', table.current_stake)
        # print('--------')
        # print('CPU Hand: ', self.hand)
        # print('CPU Best Hand: ', self.best_hand)
        # print('CPU Calc Aggro: ', self.aggressiveness)
        # print('CPU Total Chips: ', self.chips)
        # print('CPU Calc Bet: ', self.calculated_bet)
        # print('CPU Stake: ', self.stake)

        if self.stake >= table.current_stake:

            if self.calculated_bet > table.current_stake:
                self._raise(table, self.calculated_bet)

            elif self.calculated_bet == table.current_stake:
                self._check(table)

            else:  
                self._fold(table)

        elif self.stake < table.current_stake:

            if self.calculated_bet > table.current_stake:
                self._raise(table, self.calculated_bet)

            elif self.calculated_bet == table.current_stake:
                self._call(table)

            else:
                difference = (table.current_stake - self.calculated_bet)
                if difference < 60000:
                    self._call(table)
                else:
                    self._fold(table)


    def user_take_turn(self, table):

        if is_game_over(table):
            return

        print('--------YOUR TURN-------')
        print('Active Players: ', [player.name for player in table.active_players])
        # print('Turns: ', table.total_turns)
        print('Table Pot: ', table.pot, ' | Table Stake: ', table.current_stake)
        # print('Table Stake: ', table.current_stake)
        print('Table Cards: ', table.community_cards)
        # print('--------')
        print('Your Hand: ', self.hand)
        # print('Your Best Hand: ', self.best_hand)
        # print('Your Calc Aggro: ', self.aggressiveness)
        print('Your Total Chips: ', self.chips, ' | Your Stake: ', self.stake)
        # print('Your Calc Bet: ', self.calculated_bet)
        # print('Your Stake: ', self.stake)

        if self.stake >= table.current_stake:

            response = input('Would you like to check, raise, or fold? >> ')
            responses = ['check', 'raise', 'fold']
            if not response in responses:
                self.user_take_turn(table)

            if response == 'check':
                self._check(table)
                return

            elif response == 'raise':
                raise_amount = self.prompt_for_raise_amount(table)
                self._raise(table, raise_amount)
                return

            elif response == 'fold':
                self._fold(table)
                return
        
        elif self.stake < table.current_stake:
            response = input('Would you like to call, raise, or fold? >> ')
            responses = ['call', 'raise', 'fold']
            if not response in responses:
                self.user_take_turn(table)

            if response == 'call':
                self._call(table)
                return

            elif response == 'raise':
                raise_amount = self.prompt_for_raise_amount(table)
                self._raise(table, raise_amount)
                return

            elif response == 'fold':
                self._fold(table)
                return
    

    def prompt_for_raise_amount(self, table):
        try:
            response = int(input('How much would you like to raise? >> '))
            if response > self.chips:
                print('You do not have enough chips.')
                self.prompt_for_raise_amount(table)
            elif (self.stake + response) < table.current_stake:
                print('You did not stake enough chips.')
                self.prompt_for_raise_amount(table)
        except Exception as e:
            print(e)
            self.prompt_for_raise_amount(table)
        return response
import logging
import os
from Player import Player
from Table import Table
from maps import best_hand_map, rank_map, cpu_aggressiveness_map

def main_handler():

    table = Table()

    PLAYERS = 4
    USERNAME = 'User'

    while table.active_game:

        table.instantiate_players(PLAYERS, USERNAME)

        table.deal()

        table.turn_action_handler(True)
        table.turn_action_handler(False)
        table.turn_action_handler(False)

        return table.determine_winner()


if __name__ == '__main__':

    os.system('clear')

    logging.basicConfig(
        format='%(asctime)s %(levelname)s %(message)s', 
        datefmt='%m-%d-%Y %I:%M:%S',  
        filename='./games.log', 
        level=logging.DEBUG
    )

    main_handler()




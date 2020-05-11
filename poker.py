import logging
import os
from Player import Player
from Table import Table
import time
from maps import best_hand_map, rank_map, cpu_aggressiveness_map

def main_handler(connections, players):
    print('Starting game!')

    table = Table()

    print(connections)
    print(players)
    print(table)


if __name__ == '__main__':

    os.system('clear')

    PLAYERS = 4
    USERNAME = 'User'

    logging.basicConfig(
        format='%(asctime)s %(levelname)s %(message)s', 
        datefmt='%m-%d-%Y %I:%M:%S',  
        filename='./games.log', 
        level=logging.DEBUG
    )

    main_handler(PLAYERS, USERNAME)




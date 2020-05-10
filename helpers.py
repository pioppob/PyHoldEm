def is_royal(sorted_iterable):

    unique = False
    royal = False

    relevant_chunk = sorted_iterable[-5:]
    available_cards = set(relevant_chunk)

    if sum(relevant_chunk) == 60:
        royal = True

    if len(available_cards) == 5:
        unique = True
    
    if royal and unique:
        return True
    else:
        return False

def is_four_of_a_kind(sorted_iterable):

    available_cards = set(sorted_iterable)

    for card in available_cards:
        if sorted_iterable.count(card) >= 4:
            return True
    
    return False

def is_full_house(sorted_iterable):

    triple = False
    double = False

    available_cards = set(sorted_iterable)

    for card in available_cards:
        if sorted_iterable.count(card) == 3:
            triple = True
        elif sorted_iterable.count(card) == 2:
            double = True

    if double and triple:
        return True
    else:
        return False

def is_flush(sorted_iterable):
    
    available_suits = set(sorted_iterable)

    for suit in available_suits:
        if sorted_iterable.count(suit) >= 5:
            return True

    return False

         
def is_straight(sorted_iterable):

    straight_counter = 0
    cards = []
    for i in range(len(sorted_iterable) - 1):
        cards.append(sorted_iterable[i])
        if straight_counter == 4:
            break
        if sorted_iterable[i+1] - sorted_iterable[i] == 1:
            straight_counter += 1
        else:
            straight_counter = 0

    if straight_counter >= 4:
        return True
    else:
        return False

def is_three_of_a_kind(sorted_iterable):

    triple = False
    double = False

    available_cards = set(sorted_iterable)

    for card in available_cards:
        if sorted_iterable.count(card) == 3:
            triple = True
        elif sorted_iterable.count(card) == 2:
            double = True
    
    if triple and not double:
        return True
    else:
        return False

def is_two_pair(sorted_iterable):

    first = False
    second = False

    available_cards = set(sorted_iterable)

    for card in available_cards:
        if not first:
            if sorted_iterable.count(card) == 2:
                first = True
                continue

        if first:
            if sorted_iterable.count(card) == 2:
                second = True

    if first and second:
        return True
    else:
        return False

def is_one_pair(sorted_iterable):

    pairs = 0
    larger = False

    available_cards = set(sorted_iterable)

    for card in available_cards:
        if sorted_iterable.count(card) == 2:
            pairs += 1
        elif sorted_iterable.count(card) >= 2:
            larger = True

    if pairs == 1 and not larger:
        return True
    else:
        return False

def determine_flush_suit(sorted_iterable):

    available_suits = set(sorted_iterable)

    for suit in available_suits:
        if sorted_iterable.count(suit) == 5:
            return suit

def is_game_over(table):
    if len(table.active_players) == 1:
        table.unfulfilled_action = []
        return True
    return False

def print_table(player, table):

    for row in range(12):

        if row in [0, 11]:
            print('*' + '-'*98 + '*')
            continue
        elif row == 1:
            line_to_print = str([player.name for player in table.active_players])
        elif row == 5:
            line_to_print = str(table.community_cards)
        elif row == 6:
            line_to_print = str(table.pot) + ' | ' + str(table.current_stake)
        elif row == 9:
            line_to_print = str(player.hand)
        elif row == 10:
            line_to_print = str(player.chips) + ' | ' + str(player.stake)
        else:
            print('|' + ' '*98 + '|')
            continue
        
        print_line(line_to_print)

def print_line(text_to_print):
    filled_space = len(text_to_print)
    unused_space = 100 - (filled_space + 2)
    left_space = right_space = unused_space // 2
    if not left_space + right_space + 2 + filled_space == 100:
        right_space += 1
    print('|'*1 + ' '*left_space + text_to_print + ' '*right_space + '|'*1)



if __name__ == '__main__':
    player_instances = ['p0', 'p1', 'p2', 'p3', 'p4', 'p5', 'p6']
    active_players = ['p0', 'p1', 'p2', 'p3', 'p4', 'p5', 'p6']
    last_move = 'p5'
    unfulfilled = []

    final_list = []

    idx = player_instances.index(last_move)
    idx += 1

    for x in range(idx, idx+len(player_instances)):
        player = player_instances[x % len(player_instances)]

        if player in active_players:

            if not player == last_move:

                if player in unfulfilled:
                    continue

                final_list.append(player)

    print(final_list)


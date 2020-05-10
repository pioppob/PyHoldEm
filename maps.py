rank_map = {
    2: 2,
    3: 3,
    4: 4,
    5: 5,
    6: 6,
    7: 7,
    8: 8,
    9: 9,
    10: 10,
    'J': 11,
    'Q': 12,
    'K': 13,
    'A': 14
}

best_hand_map = {
    1: 'Royal Flush',
    2: 'Straight Flush',
    3: 'Four of a Kind',
    4: 'Full House',
    5: 'Flush',
    6: 'Straight',
    7: 'Three of a Kind',
    8: 'Two Pair',
    9: 'One Pair',
    10: 'High Card'
}

# Maps the CPU aggresiveness level to bet probability. 
# List items are percentages of a CPU's total chips.
cpu_aggressiveness_map = {
    5: [ 80, 80, 80, 80, 80, 80, 80, 80, 100, 100 ],
    4: [ 60, 60, 60, 60, 60, 60, 70, 70, 80, 80 ],
    3: [ 40, 40, 40, 40, 40, 40, 30, 30, 50, 50 ],
    2: [ 30, 30, 30, 30, 30, 20, 20, 40, 40, 10 ],
    1: [ 10, 10, 10, 5, 5, 5, 5, 0, 0, 15 ],
    0: [ 5, 5, 5, 5, 0, 0, 0, 0, 0, 10 ]
}
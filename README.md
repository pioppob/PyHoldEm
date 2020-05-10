# PyHoldEm
A Texas Hold'Em Game built in Python

How to play:
1. Clone this repository to your local machine. (git clone https:// ...)
2. Change directory (cd) to the PyHoldEm directory.
3. Run python3 poker.py

# Understanding the table
The poker table is displayed during your turn sequence. At the top, the active players are displayed. In the center of the table, the community cards are displayed with the current table pot and the current stake. If the current stake is not zero, you'll be prompted to call, raise or fold. You cannot check when the table stake is not zero.

Your hand is displayed at the bottom of the table, along with your chips and your current stake. Most times, your current stake will display at zero. The only time you'll see your current stake at a number other than zero is when you raise and another player re-raises you.

With every turn, the table will refresh, updating all of the values mentioned above.
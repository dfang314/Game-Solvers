# a knight starts in a random square on a 8x8 board
# two players take turns moving it
# the same square cannot be used twice
# whoever cannot move loses, and the other player wins

board = []
for i in range(8):
  board.append([])
  for j in range(8):
    board[i].append(False)

curri = -1 # CHANGE THIS
currj = -1 # CHANGE THIS

board[curri][currj] = True

# TODO
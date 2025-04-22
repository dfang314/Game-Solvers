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

di = [-2, -2, -1, -1, 1, 1, 2, 2]
dj = [-1, 1, -2, 2, -2, 2, -1, 1]

di2 = []
dj2 = []
for i in range(8):
  for j in range(8):
    di2.append(di[i] + di[j])
    dj2.append(dj[i] + dj[j])

while True:
    for i in range(8):
      candi = curri + di[i]
      candj = currj + dj[i]

      if candi < 0 or candi >= 8 or candj < 0 or candj >= 8 or board[candi][candj]:
        continue

      # winning move
      deadmove = True
      for j in range(8):
        oppi = candi + di[j]
        oppj = candj + dj[j]
        if oppi < 0 or oppi >= 8 or oppj < 0 or oppj >= 8 or board[oppi][oppj]:
          continue
      
        deadmove = False
      
      if deadmove:
        print(f"You should move to {candi},{candj}, there's no moves to go from there!")

      # losing move
      for j in range(8):
        oppi = candi + di[j]
        oppj = candj + dj[j]
        if oppi < 0 or oppi >= 8 or oppj < 0 or oppj >= 8 or board[oppi][oppj]:
          continue
      
        deadmove = True
        for k in range(8):
          checki = oppi + di[k]
          checkj = oppj + dj[k]
          if checki < 0 or checki >= 8 or checkj < 0 or checkj >= 8 or board[checki][checkj]:
            continue

          deadmove = False

        if deadmove:
          print(f"You should NOT move to {candi},{candj}, since the opponent can move to {oppi},{oppj} and you will lose.")

    # moves in format x,y , 0 indexed
    s = input("Your move:")
    curri = int(s[0])
    currj = int(s[1])
    board[curri][currj] = True
    s = input("Opponent move:")
    curri = int(s[0])
    currj = int(s[1])
    board[curri][currj] = True


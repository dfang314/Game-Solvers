board = [[0, 6, 0, 3, 0, 0, 8, 0, 4],
          [5, 3, 7, 0, 9, 0, 0, 0, 0],
          [0, 4, 0, 0, 0, 6, 3, 0, 7],
          [0, 9, 0, 0, 5, 1, 2, 3, 8],
          [0, 0, 0, 0, 0, 0, 0, 0, 0],
          [7, 1, 3, 6, 2, 0, 0, 4, 0],
          [3, 0, 6, 4, 0, 0, 0, 1, 0],
          [0, 0, 0, 0, 6, 0, 5, 2, 3],
          [1, 0, 2, 0, 0, 9, 0, 8, 0]]

def solve(board, i, j):
    if not check_board(board):
        return
    if i >= 9:
        print_board(board)
        return
    newi = i
    newj = j + 1
    if newj >= 9:
        newj -= 9
        newi += 1
    if board[i][j] != 0:
        return solve(board, newi, newj)
    for guess in range(1, 10):
        board[i][j] = guess
        solve(board, newi, newj)
    board[i][j] = 0

def check_board(board):
    for row in board:
        digits = set()
        for ele in row:
            if ele not in digits:
                digits.add(ele)
            elif ele != 0:
                return False
    for col in range(9):
        digits = set()
        for ele in [board[i][col] for i in range(9)]:
            if ele not in digits:
                digits.add(ele)
            elif ele != 0:
                return False
    startis = [0, 3, 6]
    startjs = [0, 3, 6]
    for starti in startis:
        for startj in startjs:
            digits = set()
            for i in range(starti, starti+3):
                for j in range(startj, startj+3):
                    if board[i][j] not in digits:
                        digits.add(board[i][j])
                    elif board[i][j] != 0:
                        return False
    return True

def print_board(board):
    print("Solution found")
    for row in board:
        print(row)

solve(board, 0, 0)
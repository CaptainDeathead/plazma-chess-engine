import copy

class Board:
    def __init__(self):
        self.board = [[10, 8, 9, 11, 12, 9, 8, 10],
                      [7, 7, 7, 7, 7, 7, 7, 7],
                      [0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0],
                      [1, 1, 1, 1, 1, 1, 1, 1],
                      [4, 2, 3, 5, 6, 3, 2, 4]]
        
        self.whiteCastling = [True, True]
        self.blackCastling = [True, True]
        
    def pieceAt(self, pos):
        if pos[0] < 0 or pos[0] > 7 or pos[1] < 0 or pos[1] > 7: return (False, 0)
        piece = self.board[pos[1]][pos[0]]
        if piece != 0: return (True, piece)
        else: return (False, 0)

class Engine:
    def __init__(self):
        self.TURN_STR = {0: "white", 1: "black"}
        self.board = Board()
        self.turn = 0

    def move(self, pos, newPos):
        moves = self.generateMoves(pos)

        # castling
        if pos == (4, 0) or pos == (4, 7):
            if (12, 17) in moves or (16, 17) in moves:
                if newPos == (2, 7): newPos = (12, 17)
                elif newPos == (6, 7): newPos = (16, 17)
            elif (12, 10) in moves or (16, 10) in moves:
                if newPos == (2, 0): newPos = (12, 10)
                elif newPos == (6, 0): newPos = (16, 10)

        if newPos in moves:
            if newPos[1] == 17:
                if newPos[0] == 12:
                    yRank = abs(self.turn-1)*7
                    self.board.board[yRank][4] = 0 # king empty
                    self.board.board[yRank][3] = 4 # rook
                    self.board.board[yRank][2] = 6 # king
                    self.board.board[yRank][0] = 0 # rook empty
                elif newPos[0] == 16:
                    yRank = abs(self.turn-1)*7
                    self.board.board[yRank][4] = 0 # king empty
                    self.board.board[yRank][5] = 4 # rook
                    self.board.board[yRank][6] = 6 # king
                    self.board.board[yRank][7] = 0 # rook empty
            elif newPos[1] == 10:
                if newPos[0] == 12:
                    yRank = abs(self.turn-1)*7
                    self.board.board[yRank][4] = 0 # king empty
                    self.board.board[yRank][3] = 10 # rook
                    self.board.board[yRank][2] = 12 # king
                    self.board.board[yRank][0] = 0 # rook empty
                elif newPos[0] == 16:
                    yRank = abs(self.turn-1)*7
                    self.board.board[yRank][4] = 0 # king empty
                    self.board.board[yRank][5] = 10 # rook
                    self.board.board[yRank][6] = 12 # king
                    self.board.board[yRank][7] = 0 # rook empty
            else:
                piece = self.board.pieceAt((pos[0], pos[1]))

                # set castling states
                if piece == 4:
                    if pos[0] == 0: self.board.whiteCastling[0] = False
                    elif pos[0] == 7: self.board.whiteCastling[1] = False

                elif piece == 6: self.board.whiteCastling = [False, False]

                elif piece == 10:
                    if pos[0] == 0: self.board.blackCastling[0] = False
                    elif pos[0] == 7: self.board.blackCastling[1] = False

                elif piece == 11: self.board.blackCastling = [False, False]

                self.board.board[newPos[1]][newPos[0]] = self.board.board[pos[1]][pos[0]]
                self.board.board[pos[1]][pos[0]] = 0
            
        else: raise Exception("Illegal move!")

        # check detection
        self.turn = not self.turn
        
        moves = []

        for y in range(8):
            for x in range(8):
                if self.board.board[y][x] == 0: continue
                elif self.board.board[y][x] < 7 and self.turn == 0: moves.append(self.generateMoves((x, y)))
                elif self.board.board[y][x] > 6 and self.turn == 1: moves.append(self.generateMoves((x, y)))

        self.turn = not self.turn

        newMoves = []
        for move in moves:
            if move != (): newMoves.append(move)

        if newMoves == []: return 1
        else: return 0

    def __moveWithoutCheck(self, pos, newPos):
        self.board.board[newPos[1]][newPos[0]] = self.board.board[pos[1]][pos[0]]
        self.board.board[pos[1]][pos[0]] = 0

    def inCheck(self, turn, square=None):
        if square == None:
            king = None
            for y in range(8):
                for x in range(8):
                    piece = self.board.board[y][x]
                    if turn == 0 and self.board.board[y][x] == 6: king = (x, y)
                    elif turn == 1 and self.board.board[y][x] == 12: king = (x, y)
        else: king = square

        diagonal = self.generateDiagonalMoves(king)
        for pos in diagonal:
            piece = self.board.board[pos[1]][pos[0]]
            if (piece == 9 or piece == 11) and turn == 0: return True
            elif (piece == 3 or piece == 5) and turn == 1: return True

        sliding = self.generateSlidingMoves(king)
        for pos in sliding:
            piece = self.board.board[pos[1]][pos[0]]
            if (piece == 10 or piece == 11) and turn == 0: return True
            elif (piece == 4 or piece == 5) and turn == 1: return True

        # pawn
        if turn == 0:
            if self.board.pieceAt((king[0]-1, king[1]-1))[1] == 7: return True
            elif self.board.pieceAt((king[0]+1, king[1]-1))[1] == 7: return True
        else:
            if self.board.pieceAt((king[0]-1, king[1]+1))[1] == 1: return True
            elif self.board.pieceAt((king[0]+1, king[1]+1))[1] == 1: return True

        # knight
        if turn == 0:
            if self.board.pieceAt((king[0]-1, king[1]-2))[1] == 8: return True
            elif self.board.pieceAt((king[0]+1, king[1]-2))[1] == 8: return True
            elif self.board.pieceAt((king[0]+2, king[1]-1))[1] == 8: return True
            elif self.board.pieceAt((king[0]+2, king[1]+1))[1] == 8: return True
            elif self.board.pieceAt((king[0]+1, king[1]+2))[1] == 8: return True
            elif self.board.pieceAt((king[0]-1, king[1]+2))[1] == 8: return True
            elif self.board.pieceAt((king[0]-2, king[1]+1))[1] == 8: return True
            elif self.board.pieceAt((king[0]-2, king[1]-1))[1] == 8: return True
        elif turn == 1:
            if self.board.pieceAt((king[0]-1, king[1]-2))[1] == 2: return True
            elif self.board.pieceAt((king[0]+1, king[1]-2))[1] == 2: return True
            elif self.board.pieceAt((king[0]+2, king[1]-1))[1] == 2: return True
            elif self.board.pieceAt((king[0]+2, king[1]+1))[1] == 2: return True
            elif self.board.pieceAt((king[0]+1, king[1]+2))[1] == 2: return True
            elif self.board.pieceAt((king[0]-1, king[1]+2))[1] == 2: return True
            elif self.board.pieceAt((king[0]-2, king[1]+1))[1] == 2: return True
            elif self.board.pieceAt((king[0]-2, king[1]-1))[1] == 2: return True

        # king
        if turn == 0:
            for y in range(-1, 2):
                for x in range(-1, 2):
                    if self.board.pieceAt((king[0]+x, king[1]+y))[1] == 12: return True
        elif turn == 1:
            for y in range(-1, 2):
                for x in range(-1, 2):
                    if self.board.pieceAt((king[0]+x, king[1]+y))[1] == 6: return True

    def generatePawnMoves(self, pos):
        moves = []

        if self.turn == 0:
            if pos[1] == 6 and not self.board.pieceAt((pos[0], 4))[0]: moves.append((pos[0], 4)) # 2 spaces forward

            if pos[1] > 0:
                if not self.board.pieceAt((pos[0], pos[1]-1))[0]: moves.append((pos[0], pos[1]-1)) # 1 space forward
                
                if pos[0] > 0:
                    col = self.board.pieceAt((pos[0]-1, pos[1]-1))
                    if col[0] and col[1] > 6: moves.append((pos[0]-1, pos[1]-1)) # 1 capture forward-left
                if pos[0] < 7:
                    col = self.board.pieceAt((pos[0]+1, pos[1]-1))
                    if col[0] and col[1] > 6: moves.append((pos[0]+1, pos[1]-1)) # 1 capture forward-right
        else:
            if pos[1] == 1 and not self.board.pieceAt((pos[0], 3))[0]: moves.append((pos[0], 3)) # 2 spaces forward

            if pos[1] < 7:
                if not self.board.pieceAt((pos[0], pos[1]+1))[0]: moves.append((pos[0], pos[1]+1)) # 1 space forward
                
                if pos[0] > 0:
                    col = self.board.pieceAt((pos[0]-1, pos[1]+1))
                    if col[0] and col[1] < 7: moves.append((pos[0]-1, pos[1]+1)) # 1 capture forward-left
                if pos[0] < 7:
                    col = self.board.pieceAt((pos[0]+1, pos[1]+1))
                    if col[0] and col[1] < 7: moves.append((pos[0]+1, pos[1]+1)) # 1 capture forward-right
        
        return moves

    def generateKnightMoves(self, pos):
        moves = []

        moves.append((pos[0]-1, pos[1]-2))
        moves.append((pos[0]+1, pos[1]-2))
        moves.append((pos[0]+2, pos[1]-1))
        moves.append((pos[0]+2, pos[1]+1))
        moves.append((pos[0]+1, pos[1]+2))
        moves.append((pos[0]-1, pos[1]+2))
        moves.append((pos[0]-2, pos[1]+1))
        moves.append((pos[0]-2, pos[1]-1))

        newMoves = []
        for move in moves:
            if move[0] < 0 or move[0] > 7 or move[1] < 0 or move[1] > 7: continue
            
            piece = self.board.pieceAt(move)[1]
            if self.turn == 0 and piece > 6: newMoves.append(move)
            elif self.turn == 1 and piece < 7: newMoves.append(move)
            elif piece == 0: newMoves.append(move)
        
        return newMoves

    def generateSlidingMoves(self, pos):
        moves = []
        # forward
        for y in range(pos[1]-1, -1, -1):
            col = self.board.pieceAt((pos[0], y))
            if col[0]:
                if self.turn == 0 and col[1] > 6: moves.append((pos[0], y))
                elif self.turn == 1 and col[1] < 7: moves.append((pos[0], y))
                break
            else: moves.append((pos[0], y))

        # back
        for y in range(pos[1]+1, 8):
            col = self.board.pieceAt((pos[0], y))
            if col[0]:
                if self.turn == 0 and col[1] > 6: moves.append((pos[0], y))
                elif self.turn == 1 and col[1] < 7: moves.append((pos[0], y))
                break
            else: moves.append((pos[0], y))
            
        # left
        for x in range(pos[0]-1, -1, -1):
            col = self.board.pieceAt((x, pos[1]))
            if col[0]:
                if self.turn == 0 and col[1] > 6: moves.append((x, pos[1]))
                elif self.turn == 1 and col[1] < 7: moves.append((x, pos[1]))
                break
            else: moves.append((x, pos[1]))

        # right
        for x in range(pos[0]+1, 8):
            col = self.board.pieceAt((x, pos[1]))
            if col[0]:
                if self.turn == 0 and col[1] > 6: moves.append((x, pos[1]))
                elif self.turn == 1 and col[1] < 7: moves.append((x, pos[1]))
                break
            else: moves.append((x, pos[1]))

        return moves
    
    def generateDiagonalMoves(self, pos):
        moves = []
        # forward-left
        x = pos[0]
        y = pos[1]
        while True:
            x-=1
            y-=1
            if x < 0 or x > 7 or y < 0 or y > 7: break
            col = self.board.pieceAt((x, y))
            if col[0]:
                if self.turn == 0 and col[1] > 6: moves.append((x, y))
                elif self.turn == 1 and col[1] < 7: moves.append((x, y))
                break
            else: moves.append((x, y))
        # forward-right
        x = pos[0]
        y = pos[1]
        while True:
            x+=1
            y-=1
            if x < 0 or x > 7 or y < 0 or y > 7: break
            col = self.board.pieceAt((x, y))
            if col[0]:
                if self.turn == 0 and col[1] > 6: moves.append((x, y))
                elif self.turn == 1 and col[1] < 7: moves.append((x, y))
                break
            else: moves.append((x, y))
        # back-left
        x = pos[0]
        y = pos[1]
        while True:
            x-=1
            y+=1
            if x < 0 or x > 7 or y < 0 or y > 7: break
            col = self.board.pieceAt((x, y))
            if col[0]:
                if self.turn == 0 and col[1] > 6: moves.append((x, y))
                elif self.turn == 1 and col[1] < 7: moves.append((x, y))
                break
            else: moves.append((x, y))

        # back-right
        x = pos[0]
        y = pos[1]
        while True:
            x+=1
            y+=1
            if x < 0 or x > 7 or y < 0 or y > 7: break
            col = self.board.pieceAt((x, y))
            if col[0]:
                if self.turn == 0 and col[1] > 6: moves.append((x, y))
                elif self.turn == 1 and col[1] < 7: moves.append((x, y))
                break
            else: moves.append((x, y))

        return moves

    def generateKingMoves(self, pos):
        moves = []
        if self.turn == 0:
            for y in range(-1, 2):
                if pos[1]+y > 7 or pos[1]+y < 0: continue
                for x in range(-1, 2):
                    if pos[0]+x > 7 or pos[0]+x < 0: continue
                    piece = self.board.pieceAt((pos[0]+x, pos[1]+y))[1]
                    if piece == 0 or piece > 6: moves.append((pos[0]+x, pos[1]+y))

            # castling
            if self.board.whiteCastling[0]:
                check = False
                for i in range(2, 4): # only go to index 2
                    check = self.inCheck(self.turn, (i, 7))
                    if self.board.pieceAt((i, 7))[0]: check = True
                    if check: break

                if not check: moves.append((12, 17))

            if self.board.whiteCastling[1]:
                check = False
                for i in range(5, 7): # only go to index 2
                    check = self.inCheck(self.turn, (i, 7))
                    if self.board.pieceAt((i, 7))[0]: check = True
                    if check: break

                if not check: moves.append((16, 17))

        elif self.turn == 1:
            for y in range(-1, 2):
                if pos[1]+y > 7 or pos[1]+y < 0: continue
                for x in range(-1, 2):
                    if pos[0]+x > 7 or pos[0]+x < 0: continue
                    piece = self.board.pieceAt((pos[0]+x, pos[1]+y))[1]
                    if piece == 0 or piece < 7: moves.append((pos[0]+x, pos[1]+y))

            # castling
            if self.board.blackCastling[0]:
                check = False
                for i in range(2, 4): # only go to index 2
                    check = self.inCheck(self.turn, (i, 0))
                    if self.board.pieceAt((i, 0))[0]: check = True
                    if check: break

                if not check: moves.append((12, 10))

            if self.board.blackCastling[1]:
                check = False
                for i in range(5, 7): # only go to index 2
                    check = self.inCheck(self.turn, (i, 0))
                    if self.board.pieceAt((i, 0))[0]: check = True
                    if check: break

                if not check: moves.append((16, 10))

        return moves

    def generateMoves(self, pos):
        moves = []
        piece = self.board.board[pos[1]][pos[0]]

        if piece == 0: raise Exception(f"No valid piece found at ({pos[0]}, {pos[1]})!")

        elif piece == 1 or piece == 7: # pawn
            moves.extend(self.generatePawnMoves(pos))

        elif piece == 2 or piece == 8: # knight
            moves.extend(self.generateKnightMoves(pos))

        elif piece == 3 or piece == 9: # bishop
            moves.extend(self.generateDiagonalMoves(pos))

        elif piece == 4 or piece == 10: # rook
            moves.extend(self.generateSlidingMoves(pos))

        elif piece == 5 or piece == 11: # queen
            moves.extend(self.generateSlidingMoves(pos))
            moves.extend(self.generateDiagonalMoves(pos))

        elif piece == 6 or piece == 12: # king
            moves.extend(self.generateKingMoves(pos))

        ogBoard = copy.deepcopy(self.board.board)

        newMoves = []
        for move in moves:
            # castling
            if move[1] > 7:
                newMoves.append(move)
                continue

            self.__moveWithoutCheck(pos, move)
            if not self.inCheck(self.turn): newMoves.append(move)
            self.board.board = copy.deepcopy(ogBoard)
        
        moves = newMoves.copy()
        del newMoves

        return tuple(moves)
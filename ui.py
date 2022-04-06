class GameState:
    def __init__(self):
        # Board is 8x8 2d list
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],
        ]

        self.whiteToMove = True
        # self.blackToMove = False
        self.moveLog = []
        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)
        self.checkMate = False
        self.staleMate = False

    # not castling and en-passand not work
    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove
        # self.blackToMove = not self.blackToMove
        if move.pieceMoved == 'wK':
            self.whiteKingLocation = (move.endRow, move.endCol)
        elif move.pieceMoved == 'bK':
            self.blackKingLocation = (move.endRow, move.endCol)

        # pawn promotion
        if move.isPawnPromotion:
            self.board[move.endRow][move.endCol] = move.pieceMoved[0] + 'Q'

    # click Z to undo the moves
    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            if move.pieceMoved == 'wK':
                self.whiteKingLocation = (move.startRow, move.startCol)
            elif move.pieceMoved == 'bK':
                self.blackKingLocation = (move.startRow, move.startCol)
        self.whiteToMove = not self.whiteToMove
        # reverse check mate or stalemate
        self.checkMate = False
        self.staleMate = False

    def getValidMoves(self):
        # 1.) generate all possible moves
        moves = self.getAllPossibleMoves()
        # 2.) for each move, make the move
        for i in range(len(moves) - 1, -1, -1):
            self.makeMove(moves[i])
            # 3.) generate all the opponent moves.
            # oppMoves = self.getAllPossibleMoves()
            self.whiteToMove = not self.whiteToMove
            if self.inCheck():
                moves.remove(moves[i])
            self.whiteToMove = not self.whiteToMove
            self.undoMove()

        if len(moves) == 0:
            if self.inCheck():
                self.checkMate = True
            else:
                self.staleMate = True
        else:
            self.checkMate = False
            self.staleMate = False
        return moves

    # used to check weather kink is in check or not.
    def inCheck(self):
        if self.whiteToMove:
            return self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
        else:
            return self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])

    def squareUnderAttack(self, r, c):
        self.whiteToMove = not self.whiteToMove
        oppMoves = self.getAllPossibleMoves()
        self.whiteToMove = not self.whiteToMove
        for move in oppMoves:
            if move.endRow == r and move.endCol == c:  # square under attack
                return True
        return False

    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):  # number of rows
            for c in range(len(self.board[r])):  # number of cols in given row
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    if piece == 'P':
                        self.getPawnMoves(r, c, moves)
                    if piece == 'R':
                        self.getRookMoves(r, c, moves)
                    if piece == 'B':
                        self.getBishopMoves(r, c, moves)
                    if piece == 'N':
                        self.getKnightMoves(r, c, moves)
                    if piece == 'K':
                        self.getKingMoves(r, c, moves)
                    if piece == 'Q':
                        self.getQueenMoves(r, c, moves)
        return moves

    def getPawnMoves(self, r, f, moves):

        if self.board[r][f][0] == 'b':
            if r != 1 and r < 7:
                if self.board[r + 1][f] == '--':
                    moves.append(Move((r, f), (r + 1, f), self.board))
                if (f - 1) >= 0 and self.board[r + 1][f - 1][0] == 'w':
                    moves.append(Move((r, f), (r + 1, f - 1), self.board))
                if (f + 1) <= 7 and self.board[r + 1][f + 1][0] == 'w':
                    moves.append(Move((r, f), (r + 1, f + 1), self.board))

            if r == 1:
                if self.board[r + 1][f] == '--':
                    moves.append(Move((r, f), (r + 1, f), self.board))
                if (f - 1) >= 0 and self.board[r + 1][f - 1][0] == 'w':
                    moves.append(Move((r, f), (r + 1, f - 1), self.board))
                if (f + 1) <= 7 and self.board[r + 1][f + 1][0] == 'w':
                    moves.append(Move((r, f), (r + 1, f + 1), self.board))
                if self.board[r + 1][f] == '--' and self.board[r + 2][f] == '--':
                    moves.append(Move((r, f), (r + 2, f), self.board))

        elif self.board[r][f][0] == 'w':
            if r != 6:
                if self.board[r - 1][f] == '--':
                    moves.append(Move((r, f), (r - 1, f), self.board))
                if (f - 1) >= 0 and self.board[r - 1][f - 1][0] == 'b':
                    moves.append(Move((r, f), (r - 1, f - 1), self.board))
                if (f + 1) <= 7 and self.board[r - 1][f + 1][0] == 'b':
                    moves.append(Move((r, f), (r - 1, f + 1), self.board))

            if r == 6:
                if self.board[r - 1][f] == '--':
                    moves.append(Move((r, f), (r - 1, f), self.board))
                if (f - 1) >= 0 and self.board[r - 1][f - 1][0] == 'b':
                    moves.append(Move((r, f), (r - 1, f - 1), self.board))
                if (f + 1) <= 7 and self.board[r - 1][f + 1][0] == 'b':
                    moves.append(Move((r, f), (r - 1, f + 1), self.board))
                if self.board[r - 1][f] == '--' and self.board[r - 2][f] == '--':
                    moves.append(Move((r, f), (r - 2, f), self.board))

            # if r == 1:
            #     pass

        # return moves

    def getRookMoves(self, r, c, moves):
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else:  # friendly piece
                        break
                else:
                    break

    def getBishopMoves(self, r, c, moves):
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))
        enemyColor = 'b' if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else:
                        break
                else:
                    break

    def getQueenMoves(self, r, c, moves):
        self.getBishopMoves(r, c, moves)
        self.getRookMoves(r, c, moves)

    def getKnightMoves(self, r, c, moves):
        KnightMove = ((2, 1), (2, -1), (-2, 1), (-2, -1), (1, -2), (1, 2), (-1, 2), (-1, -2))
        allyColor = 'w' if self.whiteToMove else "b"
        for i in range(8):
            rowEnd = r + KnightMove[i][0]
            colEnd = c + KnightMove[i][1]
            if 0 <= rowEnd < 8 and 0 <= colEnd < 8:
                endPiece = self.board[rowEnd][colEnd]
                if endPiece[0] != allyColor:
                    moves.append(Move((r, c), (rowEnd, colEnd), self.board))

    def getKingMoves(self, r, c, moves):
        kingMoves = ((-1, -1), (-1, 1), (1, -1), (1, 1), (-1, 0), (0, -1), (1, 0), (0, 1))
        allyColor = "w" if self.whiteToMove else "b"
        for i in range(8):
            endRow = r + kingMoves[i][0]
            endCol = c + kingMoves[i][1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:
                    moves.append(Move((r, c), (endRow, endCol), self.board))


class Move:
    # maps keys to values
    # key : value
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4,
                   "5": 3, "6": 2, "7": 1, "8": 0}
    rowToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCol = {"a": 0, "b": 1, "c": 2, "d": 3,
                  "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCol.items()}

    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.isPawnPromotion = False
        if (self.pieceMoved == 'wP' and self.endRow == 0) or (self.pieceMoved == 'bP' and self.endRow == 7):
            self.isPawnPromotion = True
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol

    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowToRanks[r]

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False
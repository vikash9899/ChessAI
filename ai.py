import random

pieceScore = {"K": 0, "Q": 20, "R": 12, "B": 7, "N": 6, "P": 2}

CHECKMATE = 2000
DREW = 0
level = 3


# random move generator valid possible moves
def findRandomMove(validMoves):
    return validMoves[random.randint(0, len(validMoves) - 1)]


# greedy algorithm for chess
def greedyAlgo(gs, validMoves):
    turnMultiplier = 1 if gs.whiteToMove else -1
    opponentMinMaxScore = CHECKMATE
    # maxScore = -CHECKMATE
    bestPlayerMove = None
    random.shuffle(validMoves)
    for playerMove in validMoves:
        gs.makeMove(playerMove)
        opponentMoves = gs.getValidMoves()
        if gs.staleMate:
            opponentMaxScore = DREW
        elif gs.checkMate:
            opponentMaxScore = -CHECKMATE
        else:
            opponentMaxScore = -CHECKMATE
            for opponentMove in opponentMoves:
                gs.makeMove(opponentMove)
                if gs.checkMate:
                    score = -turnMultiplier * CHECKMATE
                elif gs.staleMate:
                    score = DREW
                else:
                    score = -turnMultiplier * scoreMaterial(gs.board)
                if score > opponentMaxScore:
                    opponentMaxScore = score
                    # bestPlayerMove = playerMove
                gs.undoMove()

            if opponentMinMaxScore > opponentMaxScore:
                opponentMinMaxScore = opponentMaxScore
                bestPlayerMove = playerMove
        gs.undoMove()

    return bestPlayerMove


# helper method for first recursive
def findBestMove(gs, validMoves):
    global nextMove
    nextMove = None
    # findMoveNegaMax(gs, validMoves, DEPTH, 1 if gs.whiteToMove else -1)
    findMoveNegaMaxAlphaBeta(gs, validMoves, level, -CHECKMATE, CHECKMATE, 1 if gs.whiteToMove else -1)
    return nextMove


# min max alog
def findMoveMinMax(gs, validMoves, depth, whiteToMove):
    global nextMove
    if depth == 0:
        return scoreBoard(gs)

    random.shuffle(validMoves)
    if whiteToMove:
        maxScore = -CHECKMATE
        for move in validMoves:
            gs.makeMove(move)
            nextMoves = gs.getValidMoves()
            score = findMoveMinMax(gs, nextMoves, depth - 1, False)
            if score > maxScore:
                maxScore = score
                if depth == level:
                    nextMove = move
            gs.undoMove()
        return maxScore
    else:
        minScore = CHECKMATE
        for move in validMoves:
            gs.makeMove(move)
            nextMoves = gs.getValidMoves()
            score = findMoveMinMax(gs, nextMoves, depth - 1, True)
            if score < minScore:
                minScore = score
                if depth == level:
                    nextMove = move
            gs.undoMove()

        return minScore


# Nega min max
def findMoveNegaMax(gs, validMoves, depth, turnMultiplier):
    global nextMove
    if depth == 0:
        return turnMultiplier * scoreBoard(gs)

    maxScore = -CHECKMATE
    random.shuffle(validMoves)
    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        score = -findMoveNegaMax(gs, nextMoves, depth - 1, -turnMultiplier)
        if score > maxScore:
            maxScore = score
            if level == depth:
                nextMove = move
        gs.undoMove()
    return maxScore


# Nega min max with Alpha Beta
def findMoveNegaMaxAlphaBeta(gs, validMoves, depth,alpha, beta, turnMultiplier):
    global nextMove
    if depth == 0:
        return turnMultiplier * scoreBoard(gs)

    # move ordering - little more efficient
    maxScore = -CHECKMATE
    random.shuffle(validMoves)
    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        score = -findMoveNegaMaxAlphaBeta(gs, nextMoves, depth - 1,-beta, -alpha, -turnMultiplier)
        if score > maxScore:
            maxScore = score
            if level == depth:
                nextMove = move
        gs.undoMove()
        if maxScore > alpha:
            alpha = maxScore
        if alpha >= beta:
            break
    return maxScore


def scoreBoard(gs):
    if gs.checkMate:
        if gs.whiteToMove:
            return -CHECKMATE
        else:
            return CHECKMATE
    elif gs.staleMate:
        return DREW

    score = 0
    for row in gs.board:
        for square in row:
            if square[0] == 'w':
                score += pieceScore[square[1]]
            elif square[0] == 'b':
                score -= pieceScore[square[1]]
    return score


def scoreMaterial(board):
    pass
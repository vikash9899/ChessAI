import pygame as p
import ui, ai

p.init()
WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}
colors = [p.Color("white"), p.Color("dark green")]


def main():
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ui.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False  # flag when a move is made

    # print(gs.board)
    loadImages()  # only once , before the while loop
    drawBoard(screen)
    running = True
    sqSelected = ()  # empty no square selected
    playerClicks = []  # Keep track of player clicks
    playerOne = True
    playerTwo = False
    animate = False
    GameOver = False
    while running:
        humanTurn = (gs.whiteToMove and playerOne) or (not gs.whiteToMove and playerTwo)
        # mainSurface.fill((0, 0, 0))
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
                # mouse handler
            elif e.type == p.MOUSEBUTTONDOWN:
                if not GameOver:  # humanTurn:
                    location = p.mouse.get_pos()  # (x,y) location of the mouse
                    # print(location) # test which square is clicked
                    col = location[0] // SQ_SIZE
                    row = location[1] // SQ_SIZE
                    # print(f"row:{row}, col:{col}")
                    # sqSelected = (row, col)
                    if sqSelected == (row, col):  # user clicked the same square twice
                        sqSelected = ()
                        playerClicks = []  # clear player clicks
                    else:
                        sqSelected = (row, col)
                        playerClicks.append(sqSelected)  # append for both 1st and 2nd clicks
                    if len(playerClicks) == 2:  # after click

                        move = ui.Move(playerClicks[0], playerClicks[1], gs.board)
                        # for i in range(len(validMoves)):
                        #     if move == validMoves[i]:
                        #         # print(gs.board)
                        #         gs.makeMove(validMoves[i])
                        #         moveMade = True
                        #     sqSelected = ()  # reset user click
                        #     playerClicks = []
                        # if not moveMade:
                        #     playerClicks = [sqSelected]
                        if move in validMoves:
                            # print(gs.board)
                            gs.makeMove(move)
                            moveMade = True
                            animate = True
                            # GameOver = True
                        sqSelected = ()  # reset user click
                        playerClicks = []

            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:  # undo move
                    gs.undoMove()
                    moveMade = True
                    animate = False
                    GameOver = False
                if e.key == p.K_s:
                    gs = ui.GameState()
                    validMoves = gs.getValidMoves()
                    sqSelected = ()
                    playerClicks = []
                    moveMade = False
                    animate = False
                    GameOver = False


        # AI move maker
        if not GameOver and not humanTurn:
            AIMove = ai.findBestMove(gs, validMoves)
            if AIMove is None:
                AIMove = ai.findRandomMove(validMoves)
            gs.makeMove(AIMove)
            moveMade = True
            animate = True

        if moveMade:
            if animate:
                animateMove(gs.moveLog[-1], screen, gs.board, clock)
            validMoves = gs.getValidMoves()
            moveMade = False
            animate = False
            if gs.staleMate:
                GameOver = True
                # drawEndGameText(screen, "Stalemate")
            if gs.checkMate:
                GameOver = True
                # if gs.whiteToMove:
                #     drawEndGameText(screen, "Black wins by checkmate")
                # else:
                #     drawEndGameText(screen, "White wins by checkmate")

        drawGameState(screen, gs, validMoves, sqSelected)
        clock.tick(MAX_FPS)
        p.display.flip()


def highlightSquares(screen, gs, validMoves, sqSelected):
    if sqSelected != ():
        r, c = sqSelected
        if gs.board[r][c][0] == ('w' if gs.whiteToMove else 'b'):  # sqSelected is a piece which can be moved.
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100)
            s.fill(p.Color("red"))
            screen.blit(s, (c * SQ_SIZE, r * SQ_SIZE))
            # highlight moves from that square
            s.fill(p.Color('green'))
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s, (SQ_SIZE * move.endCol, SQ_SIZE * move.endRow))


def loadImages():
    pieces = ["bP", "bR", "bN", "bB", "bQ", "bK", "wP", "wR", "wN", "wB", "wQ", "wK"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))


def drawGameState(screen, gs, validMoves, sqSelected):
    drawBoard(screen)  # draw
    highlightSquares(screen, gs, validMoves, sqSelected)
    drawPieces(screen, gs.board)


def drawBoard(screen):
    colors = [p.Color("white"), p.Color("dark green")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r + c) % 2)]
            p.draw.rect(screen, color, p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def animateMove(move, screen, board, clock):
    """
    Animating a move
    """
    global colors
    d_row = move.endRow - move.startRow
    d_col = move.endCol - move.startCol
    frames_per_square = 10  # frames to move one square
    frame_count = (abs(d_row) + abs(d_col)) * frames_per_square
    for frame in range(frame_count + 1):
        row, col = (move.startRow + d_row * frame / frame_count, move.startCol + d_col * frame / frame_count)
        drawBoard(screen)
        drawPieces(screen, board)
        # erase the piece moved from its ending square
        color = colors[(move.endRow + move.endCol) % 2]
        end_square = p.Rect(move.endCol * SQ_SIZE, move.endRow * SQ_SIZE, SQ_SIZE, SQ_SIZE)
        p.draw.rect(screen, color, end_square)
        # draw captured piece onto rectangle
        if move.pieceCaptured != '--':
            screen.blit(IMAGES[move.pieceCaptured], end_square)
        # draw moving piece
        screen.blit(IMAGES[move.pieceMoved], p.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))
        p.display.flip()
        clock.tick(60)


# def drawEndGameText(screen, text):
#     font = p.font.SysFont("Liberation Serif", 32, True, False)
#     text_object = font.render(text, False, p.Color("gray"))
#     text_location = p.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH / 2 - text_object.get_width() / 2,
#                                                      HEIGHT / 2 - text_object.get_height() / 2)
#     screen.blit(text_object, text_location)
#     text_object = font.render(text, False, p.Color('black'))
#     screen.blit(text_object, text_location.move(2, 2))


if __name__ == "__main__":
    main()
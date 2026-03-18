import pygame

pygame.init()

WIDTH = 720
HEIGHT = 720
SQ_SIZE = WIDTH // 8

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess")

IMAGES = {}

selected_square = ()
player_clicks = []
valid_moves = []

# Load images
def load_images():
    pieces = ["wp","wr","wn","wb","wq","wk",
              "bp","br","bn","bb","bq","bk"]
    
    for piece in pieces:
        image = pygame.image.load(f"images/{piece}.png").convert_alpha()
        rect = image.get_bounding_rect()
        image = image.subsurface(rect)

        size = int(SQ_SIZE * 0.55)
        image = pygame.transform.smoothscale(image, (size, size))

        IMAGES[piece] = image


board = [
    ["br","bn","bb","bq","bk","bb","bn","br"],
    ["bp","bp","bp","bp","bp","bp","bp","bp"],
    ["--","--","--","--","--","--","--","--"],
    ["--","--","--","--","--","--","--","--"],
    ["--","--","--","--","--","--","--","--"],
    ["--","--","--","--","--","--","--","--"],
    ["wp","wp","wp","wp","wp","wp","wp","wp"],
    ["wr","wn","wb","wq","wk","wb","wn","wr"]
]

# Draw board
def draw_board():
    colors = [pygame.Color("#F0D9B5"), pygame.Color("#B58863")]

    for r in range(8):
        for c in range(8):
            color = colors[(r + c) % 2]
            pygame.draw.rect(screen, color, pygame.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

    # Selected square
    if selected_square != ():
        r, c = selected_square
        highlight = pygame.Surface((SQ_SIZE, SQ_SIZE))
        highlight.set_alpha(120)
        highlight.fill(pygame.Color("yellow"))
        screen.blit(highlight, (c * SQ_SIZE, r * SQ_SIZE))

    # Valid moves
    for move in valid_moves:
        r, c = move
        highlight = pygame.Surface((SQ_SIZE, SQ_SIZE))
        highlight.set_alpha(100)
        highlight.fill(pygame.Color("green"))
        screen.blit(highlight, (c * SQ_SIZE, r * SQ_SIZE))


# Draw pieces
def draw_pieces():
    for r in range(8):
        for c in range(8):
            piece = board[r][c]
            if piece != "--":
                img = IMAGES[piece]
                x = c * SQ_SIZE + (SQ_SIZE - img.get_width()) // 2
                y = r * SQ_SIZE + (SQ_SIZE - img.get_height()) // 2
                screen.blit(img, (x, y))


# logic
def is_valid_move(start, end):
    sr, sc = start
    er, ec = end
    piece = board[sr][sc]
    target = board[er][ec]

    if piece == "--":
        return False

    # ❌ Cannot capture same color
    if target != "--" and target[0] == piece[0]:
        return False

# ♙ WHITE PAWN
    if piece == "wp":
        if sc == ec and target == "--":
            if er == sr - 1:
                return True
            if sr == 6 and er == sr - 2:
                return True

        if abs(sc - ec) == 1 and er == sr - 1:
            if target.startswith("b"):
                return True

 # ♟ BLACK PAWN
    if piece == "bp":
        if sc == ec and target == "--":
            if er == sr + 1:
                return True
            if sr == 1 and er == sr + 2:
                return True

        if abs(sc - ec) == 1 and er == sr + 1:
            if target.startswith("w"):
                return True

# ♞ KNIGHT
    if piece[1] == "n":
        row_diff = abs(sr - er)
        col_diff = abs(sc - ec)

        if (row_diff == 2 and col_diff == 1) or (row_diff == 1 and col_diff == 2):
            return True
        
# ♜ ROOK 
    if piece[1] == "r":

        # Moving in same row
        if sr == er:
            step = 1 if ec > sc else -1
            for c in range(sc + step, ec, step):
                if board[sr][c] != "--":
                    return False
            return True

        # Moving in same column
        if sc == ec:
            step = 1 if er > sr else -1
            for r in range(sr + step, er, step):
                if board[r][sc] != "--":
                    return False
            return True

 # ♝ BISHOP
    if piece[1] == "b":

        if abs(sr - er) == abs(sc - ec):
            row_step = 1 if er > sr else -1
            col_step = 1 if ec > sc else -1

            r, c = sr + row_step, sc + col_step

            while r != er and c != ec:
                if board[r][c] != "--":
                    return False
                r += row_step
                c += col_step

            return True

 # 👑 QUEEN
    if piece[1] == "q":

        # Rook-like move
        if sr == er:
            step = 1 if ec > sc else -1
            for c in range(sc + step, ec, step):
                if board[sr][c] != "--":
                    return False
            return True

        if sc == ec:
            step = 1 if er > sr else -1
            for r in range(sr + step, er, step):
                if board[r][sc] != "--":
                    return False
            return True

        # Bishop-like move
        if abs(sr - er) == abs(sc - ec):
            row_step = 1 if er > sr else -1
            col_step = 1 if ec > sc else -1

            r, c = sr + row_step, sc + col_step

            while r != er and c != ec:
                if board[r][c] != "--":
                    return False
                r += row_step
                c += col_step

            return True
# 👑 KING
    if piece[1] == "k":
        if abs(sr - er) <= 1 and abs(sc - ec) <= 1:
            return True
    return False

def get_valid_moves(pos):
    moves = []
    for r in range(8):
        for c in range(8):
            if is_valid_move(pos, (r, c)):
                moves.append((r, c))
    return moves


def main():
    global selected_square, valid_moves, turn
    turn = "w"   # w = white, b = black

    load_images()
    running = True
    clock = pygame.time.Clock()

    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False

            elif e.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                col = mouse_pos[0] // SQ_SIZE
                row = mouse_pos[1] // SQ_SIZE

                # FIRST CLICK
                if selected_square == ():
                    if board[row][col] != "--" and board[row][col][0] == turn:
                        selected_square = (row, col)
                        valid_moves = get_valid_moves((row, col))

                # SECOND CLICK → MOVE
                else:
                    if (row, col) in valid_moves:
                        sr, sc = selected_square
                        piece = board[sr][sc]

                        board[sr][sc] = "--"
                        board[row][col] = piece

                        # 🔄 SWITCH TURN
                        if turn == "w":
                            turn = "b"
                        else:
                            turn = "w"
                    # Reset after second click
                    selected_square = ()
                    valid_moves = []

        draw_board()
        draw_pieces()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


main()

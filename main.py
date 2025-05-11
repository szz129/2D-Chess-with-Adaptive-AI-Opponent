import os
import pygame
import chess
import threading
import time
from chess_engine import get_best_move, choose_difficulty

# Constants
WIDTH, HEIGHT = 512, 512
SQ_SIZE = WIDTH // 8
FPS = 60
TIME_LIMIT = 3.0  # Time limit for AI move calculation in seconds

# Path to assets folder (make sure this is correct)
ASSET_DIR = r"C:\Users\Shanza Noor\Downloads\AI_Chess\AI_Chess\AI_CHESS Project\assets"

def load_images():
    pieces = ["P", "N", "B", "R", "Q", "K", "P2", "N2", "B2", "R2", "Q2", "K2"]
    images = {}
    for piece in pieces:
        img_path = os.path.join(ASSET_DIR, f"{piece}.png")
        if not os.path.exists(img_path):
            print(f"[ERROR] Missing image: {img_path}")
            continue
        try:
            image = pygame.image.load(img_path)
            image = pygame.transform.scale(image, (SQ_SIZE, SQ_SIZE))
            images[piece] = image
        except pygame.error as e:
            print(f"[ERROR] Failed to load image: {img_path} -> {e}")
    return images


def draw_board(screen, board_img):
    screen.blit(board_img, (0, 0))


def draw_pieces(screen, board, images, last_move):
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            col = chess.square_file(square)
            row = 7 - chess.square_rank(square)
            symbol = piece.symbol().upper()
            if not piece.color:
                symbol += "2"
            image = images.get(symbol)
            if image:
                x = col * SQ_SIZE
                y = row * SQ_SIZE
                screen.blit(image, (x, y))

    if last_move:
        start_square = last_move.from_square
        end_square = last_move.to_square
        pygame.draw.rect(screen, (0, 255, 0), (chess.square_file(start_square) * SQ_SIZE, (7 - chess.square_rank(start_square)) * SQ_SIZE, SQ_SIZE, SQ_SIZE), 5)
        pygame.draw.rect(screen, (0, 255, 0), (chess.square_file(end_square) * SQ_SIZE, (7 - chess.square_rank(end_square)) * SQ_SIZE, SQ_SIZE, SQ_SIZE), 5)


class ChessGame:
    def __init__(self):
        self.board = chess.Board()
        self.depth, self.randomness = 5, 0.0  # Hard mode settings
        self.last_move = None
        self.ai_thread = None
        self.ai_move = None
        self.ai_thinking = False

    def ai_move_calculation(self):
        self.ai_thinking = True
        start_time = time.time()
        self.ai_move = get_best_move(self.board, self.depth, self.randomness)
        elapsed = time.time() - start_time
        print(f"AI calculation time: {elapsed} seconds")
        self.ai_thinking = False

    def request_ai_move(self):
        if not self.ai_thinking:
            self.ai_thread = threading.Thread(target=self.ai_move_calculation)
            self.ai_thread.start()

    def handle_player_move(self, selected_square, target_square):
        move = chess.Move(selected_square, target_square)
        if move in self.board.legal_moves:
            self.board.push(move)
            self.last_move = move
            self.request_ai_move()


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Optimized Chess vs AI - Hard Mode")
    clock = pygame.time.Clock()

    board_img_path = os.path.join(ASSET_DIR, "board.png")
    if not os.path.exists(board_img_path):
        print(f"[ERROR] Board image not found: {board_img_path}")
        return

    board_img = pygame.image.load(board_img_path)
    board_img = pygame.transform.scale(board_img, (WIDTH, HEIGHT))
    images = load_images()
    game = ChessGame()
    selected_square = None
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN and not game.ai_thinking:
                x, y = pygame.mouse.get_pos()
                col = x // SQ_SIZE
                row = 7 - y // SQ_SIZE
                square = chess.square(col, row)
                if selected_square is None and game.board.piece_at(square) and game.board.piece_at(square).color == chess.WHITE:
                    selected_square = square
                elif selected_square is not None:
                    game.handle_player_move(selected_square, square)
                    selected_square = None

        if game.ai_move and not game.ai_thinking:
            game.board.push(game.ai_move)
            game.last_move = game.ai_move
            game.ai_move = None

        draw_board(screen, board_img)
        draw_pieces(screen, game.board, images, game.last_move)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()

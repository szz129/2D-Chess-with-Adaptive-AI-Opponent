import chess
import random

# Piece values for evaluation
piece_values = {
    chess.PAWN: 1,
    chess.KNIGHT: 3.2,
    chess.BISHOP: 3.33,
    chess.ROOK: 5,
    chess.QUEEN: 9,
    chess.KING: 0
}

# Center squares for evaluation
CENTER_SQUARES = [chess.D4, chess.E4, chess.D5, chess.E5]

# Piece-square tables for positional evaluation
piece_square_table = {
    chess.PAWN: [
        0, 0, 0, 0, 0, 0, 0, 0,
        5, 5, 5, 5, 5, 5, 5, 5,
        1, 1, 2, 3, 3, 2, 1, 1,
        0.5, 0.5, 1, 2.5, 2.5, 1, 0.5, 0.5,
        0, 0, 0, 2, 2, 0, 0, 0,
        0.5, -0.5, -1, 0, 0, -1, -0.5, 0.5,
        0.5, 1, 1, -2, -2, 1, 1, 0.5,
        0, 0, 0, 0, 0, 0, 0, 0
    ],
    chess.KNIGHT: [
        -5, -4, -3, -3, -3, -3, -4, -5,
        -4, -2, 0, 0, 0, 0, -2, -4,
        -3, 0, 1, 1.5, 1.5, 1, 0, -3,
        -3, 0.5, 1.5, 2, 2, 1.5, 0.5, -3,
        -3, 0, 1.5, 2, 2, 1.5, 0, -3,
        -3, 0.5, 1, 1.5, 1.5, 1, 0.5, -3,
        -4, -2, 0, 0.5, 0.5, 0, -2, -4,
        -5, -4, -3, -3, -3, -3, -4, -5
    ],
    chess.BISHOP: [
        -2, -1, -1, -1, -1, -1, -1, -2,
        -1, 0, 0, 0, 0, 0, 0, -1,
        -1, 0, 0.5, 1, 1, 0.5, 0, -1,
        -1, 0.5, 0.5, 1, 1, 0.5, 0.5, -1,
        -1, 0, 1, 1, 1, 1, 0, -1,
        -1, 1, 1, 1, 1, 1, 1, -1,
        -1, 0.5, 0, 0, 0, 0, 0.5, -1,
        -2, -1, -1, -1, -1, -1, -1, -2
    ],
    chess.ROOK: [
        0, 0, 0, 0, 0, 0, 0, 0,
        0.5, 1, 1, 1, 1, 1, 1, 0.5,
        -0.5, 0, 0, 0, 0, 0, 0, -0.5,
        -0.5, 0, 0, 0, 0, 0, 0, -0.5,
        -0.5, 0, 0, 0, 0, 0, 0, -0.5,
        -0.5, 0, 0, 0, 0, 0, 0, -0.5,
        -0.5, 0, 0, 0, 0, 0, 0, -0.5,
        0, 0, 0, 0.5, 0.5, 0, 0, 0
    ],
    chess.QUEEN: [
        -2, -1, -1, -0.5, -0.5, -1, -1, -2,
        -1, 0, 0, 0, 0, 0, 0, -1,
        -1, 0, 0.5, 0.5, 0.5, 0.5, 0, -1,
        -0.5, 0, 0.5, 0.5, 0.5, 0.5, 0, -0.5,
        0, 0, 0.5, 0.5, 0.5, 0.5, 0, -0.5,
        -1, 0, 0.5, 0.5, 0.5, 0.5, 0, -1,
        -1, 0, 0, 0, 0, 0, 0, -1,
        -2, -1, -1, -0.5, -0.5, -1, -1, -2
    ]
}

# Difficulty levels
def choose_difficulty():
    print("Select difficulty:")
    print("1. Easy")
    print("2. Medium")
    print("3. Hard")
    difficulty = int(input("Enter difficulty level (1-3): "))
    if difficulty == 1:
        return 2, 0.0  # Depth 2, randomness 0.0
    elif difficulty == 2:
        return 4, 0.2  # Depth 4, randomness 0.2
    else:
        return 5, 0.5  # Depth 5, randomness 0.5


# Evaluate board position
def evaluate_board(board):
    evaluation = 0
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            value = piece_values.get(piece.piece_type, 0)
            if piece.color:
                evaluation += value
            else:
                evaluation -= value
            evaluation += piece_square_table.get(piece.piece_type, [0] * 64)[square]
    return evaluation


def get_best_move(board, depth, randomness):
    legal_moves = list(board.legal_moves)
    best_move = None
    best_value = -float('inf')
    
    for move in legal_moves:
        board.push(move)
        value = -evaluate_board(board)  # Minimize the opponent's score
        if value > best_value:
            best_value = value
            best_move = move
        board.pop()
    
    return best_move

import chess

piece_square_table = {
    chess.PAWN: [0, 5, 1, 0.5, 0, 0.5, 0.5, 0] * 8,
    chess.KNIGHT: [-5, -4, -3, -3, -3, -3, -4, -5] * 8
}

def evaluate_board(board):
    material = {
        chess.PAWN: 1,
        chess.KNIGHT: 3,
        chess.BISHOP: 3,
        chess.ROOK: 5,
        chess.QUEEN: 9
    }
    score = 0
    for piece in material:
        score += len(board.pieces(piece, chess.WHITE)) * material[piece]
        score -= len(board.pieces(piece, chess.BLACK)) * material[piece]
    return score

def minimax(board, depth, alpha, beta, maximizing):
    if depth == 0 or board.is_game_over():
        return evaluate_board(board)
    if maximizing:
        max_eval = float("-inf")
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, alpha, beta, False)
            board.pop()
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float("inf")
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, alpha, beta, True)
            board.pop()
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

def get_best_move(board, depth):
    best_move = None
    best_eval = float("-inf")
    for move in board.legal_moves:
        board.push(move)
        eval = minimax(board, depth - 1, float("-inf"), float("inf"), False)
        board.pop()
        if eval > best_eval:
            best_eval = eval
            best_move = move
    return best_move

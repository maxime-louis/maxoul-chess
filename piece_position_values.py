import numpy as np
from beartype.typing import Dict
import chess


piece_raw_values = {'pawn': 100, 'knight': 300, 'bishop': 305, 'rook': 500, 'queen': 900}
piece_raw_values_typed = {
    chess.PAWN: 100,
    chess.KNIGHT: 300,
    chess.BISHOP: 305,
    chess.ROOK: 500,
    chess.QUEEN: 900,
    chess.KING: 0,
}


initial_non_pawn_material = 4 * piece_raw_values_typed[chess.KNIGHT] +\
                            4 * piece_raw_values_typed[chess.BISHOP] +\
                            4 * piece_raw_values_typed[chess.ROOK] +\
                            2 * piece_raw_values_typed[chess.QUEEN]

chess_board = np.array([np.array([0, 1, 2, 3, 4, 5, 6, 7]) + 8*i for i in range(8)])[::-1]

white_rook_values = np.array([
    [0, 0, 0, 20, 20, 20, 0, 0],  # 1 row from a to h
    [0, 0, 0, 0, 0, 0, 0, 0],  # 2nd row from a to h
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [22, 22, 22, 25, 25, 22, 25, 22],
    [0, 0, 0, 0, 0, 0, 0, 0]
])

white_knight_values = np.array([
    [-20, 0, -10, -10, -10, -10, 0, -20],  # 1 row from a to h
    [-10, -5, -5, -5, -5, -5, -5, -10],  # 2nd row from a to h
    [-10, -5, 15, 15, 15, 15, -5, -10],
    [-10, -5, 15, 15, 15, 15, -5, -10],
    [-10, -5, 15, 15, 15, 15, -5, -10],
    [-10, -5, 15, 15, 15, 15, -5, -10],
    [-10, -5, -5, -5, -5, -5, -5, -10],
    [-20, -10, -10, -10, -10, -10, -10, -20]
])

white_queen_values_beginning = np.array([
    [10, 10, 10, 20, 10, 10, 10, 10],  # 1 row from a to h
    [10, 10, 10, 10, 10, 10, 10, 10],  # 2nd row from a to h
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0]
])


white_queen_values_endgame = np.array([
    [-30, -20, -10, -10, -10, -10, -20, -30],  # 1 row from a to h
    [-20, -10, -5, -5, -5, -5, -10, -20],  # 2nd row from a to h
    [-10, -5, -5, -5, -5, -5, -5, -10],
    [-10, -5, 10, 20, 20, 10, -5, -10],
    [-10, -5, 10, 20, 20, 10, -5, -10],
    [-10, -5, 10, 10, 10, 10, -5, -10],
    [-10, -5, 10, 10, 10, 10, -5, -10],
    [-30, -20, -10, -10, -10, -10, -20, -30]
])

white_bishop_values_beginning = np.array([
    [-20, -10, -10, -10, -10, -10, -10, -20],  # 1 row from a to h
    [-10, 5, 5, 10, 10, 5, 5, -10],  # 2nd row from a to h
    [5, 5, 5, 10, 10, 5, 5, 5],
    [5, 5, 10, 25, 25, 10, 5, 5],
    [-10, 10, 10, 30, 30, 10, 10, -10],
    [-10, 0, 0, 5, 5, 0, 0, -10],
    [-15, 0, 0, 0, 0, 0, 0, -15],
    [-15, 0, 0, 0, 0, 0, 0, -15,]
])

white_bishop_values_endgame = np.array([
    [-30, -20, -10, -10, -10, -10, -20, -30],  # 1 row from a to h
    [-20, -10, -5, -5, -5, -5, -10, -20],  # 2nd row from a to h
    [-10, -5, -5, -5, -5, -5, -5, -10],
    [-10, -5, 10, 20, 20, 10, -5, -10],
    [-10, -5, 10, 20, 20, 10, -5, -10],
    [-10, -5, 10, 10, 10, 10, -5, -10],
    [-10, -5, 10, 10, 10, 10, -5, -10],
    [-30, -20, -10, -10, -10, -10, -20, -30]
])

white_pawn_values_beginning = np.array([
    [0,   0,   0,   0,   0,   0,   0,   0],  # 1 row from a to h
    [5,   5,   5, -20, -20,   5,   5,   5],  # 2nd row from a to h
    [5,   5,  10,  20,  20,   10,   5,   5],
    [5,   5,  15,  30,  30,  15,   5,   5],
    [20,  20,  20,  40,  40,  20,  20,  20],
    [0,  0,  0,  0,  0,  0,  0,  0],
    [0,  0,  0,  0,  0,  0,  0,  0],
    [0,   0,   0,   0,   0,   0,   0,   0]
])

white_pawn_values_endgame = np.array([
    [0,   0,   0,   0,   0,   0,   0,   0],  # 1 row from a to h
    [5,   5,   5, -20, -20,   5,   5,   5],  # 2nd row from a to h
    [5,   5,  10,  20,  20,   10,   5,   5],
    [10, 10,  15,  30,  30,  15, 10, 10],
    [20,  20,  20,  40,  40,  20,  20,  20],
    [50,  50,  50,  60,  60,  50,  50,  50],
    [70,  70,  70,  70,  80,  70,  70,  70],
    [0,   0,   0,   0,   0,   0,   0,   0]
])

white_king_values_beginning = np.array([
    [0,    0,    20,   -40,  -10,    -40,   20,    0],  # 1 row from a to h
    [0,    0,     0,   -40,  -40,    -40,    0,    0],  # 2nd row from a to h
    [0,    0,     0,     0,    0,    0,    0,    0],
    [0,    0,     0,    0,   0,    0,    0,    0],
    [0,    0,     0,    0,   0,    0,    0,    0],
    [0,    0,     0,     0,    0,    0,    0,    0,],
    [0,    0,     0,     0,    0,    0,    0,    0],
    [0,   0,   0,   0,   0,   0,   0,   0]
])

white_king_values_endgame = np.array([
    [-20, -10, -10, -10, -10, -10, -10, -20],  # 1 row from a to h
    [-10, -5, -5, -5, -5, -5, -5, -10],  # 2nd row from a to h
    [-10, -5, 15, 15, 15, 15, -5, -10],
    [-10, -5, 15, 20, 20, 15, -5, -10],
    [-10, -5, 15, 20, 20, 15, -5, -10],
    [-10, -5, 15, 15, 15, 15, -5, -10],
    [-10, -5, -5, -5, -5, -5, -5, -10],
    [-20, -10, -10, -10, -10, -10, -10, -20]
])


# to deliver mate !
king_edge_values = np.array([
    [-95,  -95,  -90,  -90,  -90,  -90,  -95,  -95],  # 1 row from a to h
    [-95,  -50,  -50,  -50,  -50,  -50,  -50,  -95],  # 2nd row from a to h
    [-90,  -50,  -20,  -20,  -20,  -20,  -50,  -90],
    [-90,  -50,  -20,    0,    0,  -20,  -50,  -90],
    [-90,  -50,  -20,    0,    0,  -20,  -50,  -90],
    [-90,  -50,  -20,  -20,  -20,  -20,  -50,  -90],
    [-95,  -50,  -50,  -50,  -50,  -50,  -50,  -95],
    [-95,  -95,  -90,  -90,  -90,  -90,  -95,  -95]
])

beginning_square_sets_white = {
    chess.PAWN: white_pawn_values_endgame,
    chess.KNIGHT: white_knight_values,
    chess.BISHOP: white_bishop_values_beginning,
    chess.ROOK:  white_rook_values,
    chess.QUEEN:  white_queen_values_beginning,
    chess.KING:  white_king_values_beginning,
}


endgame_square_sets_white = {
    chess.PAWN: white_pawn_values_beginning,
    chess.KNIGHT: white_knight_values,
    chess.BISHOP: white_bishop_values_endgame,
    chess.ROOK: white_rook_values,
    chess.QUEEN: white_queen_values_endgame,
    chess.KING: white_king_values_endgame,
}


beginning_square_sets_black = {key: val[::-1].flatten() for key, val in beginning_square_sets_white.items()}
beginning_square_sets_white = {key: val.flatten() for key, val in beginning_square_sets_white.items()}
endgame_square_sets_black = {key: val[::-1].flatten() for key, val in endgame_square_sets_white.items()}
endgame_square_sets_white = {key: val.flatten() for key, val in endgame_square_sets_white.items()}


def square_set_to_value(sq_set, game_phase: str, piece: chess.Piece, color):
    if game_phase == 'beginning':
        if color == chess.WHITE:
            pst = beginning_square_sets_white[piece]
        else:
            pst = beginning_square_sets_black[piece]
    elif game_phase == 'endgame':
        if color == chess.WHITE:
            pst = endgame_square_sets_white[piece]
        else:
            pst = endgame_square_sets_black[piece]
    else:
        raise ValueError(game_phase)

    return sum([pst[i] for i in sq_set])


if __name__ == '__main__':
    import matplotlib.pyplot as plt
    import seaborn as sns
    piece_list = [chess.PAWN, chess.KNIGHT, chess.BISHOP, chess.ROOK, chess.QUEEN, chess.KING]
    piece_list_str = ['PAWN', 'KNIGHT', 'BISHOP', 'ROOK', 'QUEEN', 'KING']

    color = chess.BLACK
    game_phase = 'beginning'
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))

    for ax, (piece_name, piece) in zip(axes.flatten(), zip(piece_list_str, piece_list)):
        key_values = np.zeros((8, 8))
        for i in range(len(chess_board)):
            for j in range(len(chess_board[i])):
                key_values[i, j] = square_set_to_value([chess_board[i, j]], game_phase, piece, color)

        sns.heatmap(key_values, annot=True, ax=ax)
        ax.set_title('Values for ' + piece_name)

    plt.tight_layout()
    plt.show()
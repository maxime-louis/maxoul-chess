from maxoul_chess.abstract_board import AbstractBoard
from maxoul_chess.python_chess_board import PythonChessBoard
import chess
from maxoul_chess.piece_position_values import square_set_to_value, piece_raw_values_typed, initial_non_pawn_material

from maxoul_chess.utils import LimitedHashTable

evaluation_cache = LimitedHashTable(max_size=1e8)


def evaluate(board: PythonChessBoard, z_hash: str, use_cache: bool = False):
    if use_cache:
        assert z_hash is not None
        out = evaluation_cache.get(z_hash)
        if out is not None:
            return out

    if board.is_checkmate():
        winner = board.winner()
        if winner == chess.WHITE:
            return 1000000
        else:
            return -1000000

    if board.is_stalemate() or board.is_insufficient_material() \
            or board.is_fifty_moves() or board.board.is_repetition():
        return 0

    material_evaluation = evaluate_material(board)

    # castle_evaluation = evaluate_castle(board)

    out = material_evaluation  # + castle_evaluation

    if use_cache:
        evaluation_cache.insert(z_hash, out)

    return out


# def evaluate_castle(board: AbstractBoard):
#     if isinstance(board, PythonChessBoard):
#         eval = 0
#         if board.board.has_castling_rights(chess.WHITE) or board.white_has_castled:
#             eval += 100
#         if board.board.has_castling_rights(chess.BLACK) or board.black_has_castled:
#             eval -= 100
#         return eval
#
#     raise ValueError


def evaluate_material(board: PythonChessBoard, verbose=False):
    assert isinstance(board, PythonChessBoard)
    pawn_raw_white, pawn_beg_white, pawn_end_white = piece_evaluation(board, chess.PAWN, chess.WHITE, verbose=verbose)
    pawn_raw_black, pawn_beg_black, pawn_end_black = piece_evaluation(board, chess.PAWN, chess.BLACK, verbose=verbose)

    knight_raw_white, knight_beg_white, knight_end_white = piece_evaluation(board, chess.KNIGHT, chess.WHITE, verbose=verbose)
    knight_raw_black, knight_beg_black, knight_end_black = piece_evaluation(board, chess.KNIGHT, chess.BLACK, verbose=verbose)

    bishop_raw_white, bishop_beg_white, bishop_end_white = piece_evaluation(board, chess.BISHOP, chess.WHITE, verbose=verbose)
    bishop_raw_black, bishop_beg_black, bishop_end_black = piece_evaluation(board, chess.BISHOP, chess.BLACK, verbose=verbose)

    rook_raw_white, rook_beg_white, rook_end_white = piece_evaluation(board, chess.ROOK, chess.WHITE, verbose=verbose)
    rook_raw_black, rook_beg_black, rook_end_black = piece_evaluation(board, chess.ROOK, chess.BLACK, verbose=verbose)

    queen_raw_white, queen_beg_white, queen_end_white = piece_evaluation(board, chess.QUEEN, chess.WHITE, verbose=verbose)
    queen_raw_black, queen_beg_black, queen_end_black = piece_evaluation(board, chess.QUEEN, chess.BLACK, verbose=verbose)

    _, king_beg_white, king_end_white = piece_evaluation(board, chess.KING, chess.WHITE, verbose=verbose)
    _, king_beg_black, king_end_black = piece_evaluation(board, chess.KING, chess.BLACK, verbose=verbose)

    total_non_pawn_material = knight_raw_white + knight_raw_black + \
                              bishop_raw_white + bishop_raw_black + \
                              rook_raw_white + rook_raw_black + \
                              queen_raw_white + queen_raw_black

    end_coeff = 1 - total_non_pawn_material / initial_non_pawn_material
    end_coeff = min(1, end_coeff)
    end_coeff = max(0, end_coeff)
    beg_coeff = 1 - end_coeff
    if verbose:
        print(f"Endgame coefficient: {end_coeff}")

    white_raw_eval = pawn_raw_white + knight_raw_white + bishop_raw_white + rook_raw_white + queen_raw_white
    black_raw_eval = pawn_raw_black + knight_raw_black + bishop_raw_black + rook_raw_black + queen_raw_black

    white_pst_eval = beg_coeff * pawn_beg_white + end_coeff * pawn_end_white + \
                     beg_coeff * knight_beg_white + end_coeff * knight_end_white + \
                     beg_coeff * bishop_beg_white + end_coeff * bishop_end_white + \
                     beg_coeff * rook_beg_white + end_coeff * rook_end_white + \
                     beg_coeff * queen_beg_white + end_coeff * queen_end_white + \
                     beg_coeff * king_beg_white + end_coeff * king_end_white

    black_pst_eval = beg_coeff * pawn_beg_black + end_coeff * pawn_end_black + \
                     beg_coeff * knight_beg_black + end_coeff * knight_end_black + \
                     beg_coeff * bishop_beg_black + end_coeff * bishop_end_black + \
                     beg_coeff * rook_beg_black + end_coeff * rook_end_black + \
                     beg_coeff * queen_beg_black + end_coeff * queen_end_black + \
                     beg_coeff * king_beg_black + end_coeff * king_end_black

    if verbose:
        print(f'Raw eval {white_raw_eval} vs {black_raw_eval}, pst eval {white_pst_eval} vs {black_pst_eval}')

    return white_raw_eval + white_pst_eval - black_raw_eval - black_pst_eval


def piece_evaluation(board, piece, color, verbose: bool = False):
    pieces = board.board.pieces(piece, color)
    raw_piece_evaluation = piece_raw_values_typed[piece] * len(pieces)
    pst_piece_evaluation_beginning = square_set_to_value(pieces, 'beginning', piece, color)
    pst_piece_evaluation_endgame = square_set_to_value(pieces, 'endgame', piece, color)
    if verbose:
        print(f"piece {piece}, color {color}, raw eval {raw_piece_evaluation} "
              f"beg eval {pst_piece_evaluation_beginning} end eval {pst_piece_evaluation_endgame}")
    return raw_piece_evaluation, pst_piece_evaluation_beginning, pst_piece_evaluation_endgame


if __name__ == '__main__':
    import time
    from chess.polyglot import zobrist_hash
    # from maxoul_chess.legal_moves_generation import order_moves
    #
    board = PythonChessBoard()
    # t0 = time.time()
    # for _ in range(10000):
    #     evaluate(board, z_hash=None, use_cache=False)
    # print(f"Evaluation takes {(time.time() - t0) / 10000}")

    # board = PythonChessBoard(fen='4k3/6p1/8/8/P2K4/8/6R1/8 w - - 0 1')
    # t0 = time.time()
    # for _ in range(10000):
    #     zobrist_hash(board.board)
    # print(f"Zobrist takes {(time.time() - t0) / 10000}")
    #
    # t0 = time.time()
    # for _ in range(10000):
    #     str(board.board)
    # print(f"fen takes {(time.time() - t0) / 10000}")
    #
    t0 = time.time()
    for _ in range(10000):
        board = PythonChessBoard()
        legal_moves = board.generate_legal_moves()
        # ordered_moves = order_moves(legal_moves, board)
    print(f"Move ordering and gen takes {(time.time() - t0) / 10000}")

    # board = PythonChessBoard(fen='8/8/8/8/8/8/5r2/8 w - - 0 1')
    # print(board.board)
    # from maxoul_chess.legal_moves_generation import quiescence_moves
    # print(quiescence_moves(board))

    # print(evaluate_material(board, verbose=True))

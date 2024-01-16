from beartype.typing import List
import numpy as np
import chess
from chess import Move
from maxoul_chess.piece_position_values import piece_raw_values_typed
from maxoul_chess.abstract_board import AbstractBoard
from maxoul_chess.evaluation import evaluate


def move_priority_bis(move: Move, board: AbstractBoard) -> float:
    board.push(move)
    priority = evaluate(board, z_hash=None, use_cache=False)
    board.pop()
    if board.board.turn == chess.BLACK:
        priority = -priority
    return priority


def get_quiescence_moves(board: AbstractBoard):
    # Firt case: we are not in check
    if not board.board.is_check():
        out = []
        priorities = []
        for move in board.generate_legal_moves():
            # if board.gives_check(move):  # Keeping checks:
            #     out.append(move)
            #     priorities.append(500)
            if move.promotion is not None and move.promotion == chess.QUEEN:  # Keeping queening
                out.append(move)
                priorities.append(400)
            elif board.is_capture(move):  # Capture of non-pawns
                origin_piece = board.piece_at(move.from_square).piece_type
                destination_piece = board.piece_at(move.to_square)
                origin_price = piece_raw_values_typed[origin_piece]

                if destination_piece is not None:  # because of en passant
                    destination_piece = destination_piece.piece_type
                    dest_price = piece_raw_values_typed[destination_piece]
                    if dest_price >= 300 and dest_price - origin_price >= -20:
                        out.append(move)
                        priorities.append(dest_price - origin_price)
        out_sorted = [out[i] for i in np.argsort(-1. * np.array(priorities))]
        return out_sorted
    else:
        # Sorted ways to avoid the check !
        return order_moves(board.generate_legal_moves(), board)


def move_priority(move: Move, board: AbstractBoard) -> int:
    origin_square = move.from_square
    origin_piece = board.piece_at(origin_square).piece_type
    destination_square = move.to_square

    out = 0
    # Promotions:
    prom = move.promotion
    if prom is not None:
        if prom == chess.QUEEN:
            out += 900
        elif prom == chess.ROOK:
            out += 500
        else:
            out += 30

    # Echecs:
    if board.gives_check(move):
        out += 300

    # Captures
    if board.is_capture(move):
        # In fact no we want the difference between piece captured and capturing piece !
        destination_piece = board.piece_at(destination_square)
        if destination_piece is not None:  # because of en passant
            destination_piece = destination_piece.piece_type
        else:
            destination_piece = chess.PAWN

        origin_price = piece_raw_values_typed[origin_piece]
        dest_price = piece_raw_values_typed[destination_piece]

        # We eat something more expensive than us ! smells good
        if origin_price < dest_price:
            out += dest_price - origin_price

        # We eat something as expensive as us, still a capture though
        elif origin_price == dest_price:
            out += 100

        # We eat something less expensive, unlikely to be a good move
        else:
            out += dest_price - origin_price

    # Mettre une pièce en prise d'un pion n'est pas bon (si ce n'est pas une capture!)
    elif origin_piece != chess.PAWN and origin_piece != chess.KING:
        dest_square_attackers = board.board.attackers(not board.board.turn, destination_square)
        for elt in dest_square_attackers:
            if board.board.piece_type_at(elt) == chess.PAWN:
                return -1000  # Not a good idea in general !

    return out


def move_priority_ter(move: Move, board: AbstractBoard) -> int:
    priority = 0

    origin_square = move.from_square
    origin_piece = board.piece_at(origin_square).piece_type
    destination_square = move.to_square
    if board.is_capture(move):
        destination_piece = board.piece_at(destination_square)
        if destination_piece is not None:  # because of en passant
            destination_piece = destination_piece.piece_type
        else:
            destination_piece = chess.PAWN

        origin_price = piece_raw_values_typed[origin_piece]
        dest_price = piece_raw_values_typed[destination_piece]
        priority += 10 * dest_price - origin_price

    if move.promotion is not None:
        priority += piece_raw_values_typed[move.promotion]

    if origin_piece != chess.PAWN and origin_piece != chess.KING:
        dest_square_attackers = board.board.attackers(not board.board.turn, destination_square)
        for elt in dest_square_attackers:
            if board.board.piece_type_at(elt) == chess.PAWN:
                priority -= piece_raw_values_typed[origin_piece]
                break

    return priority


selected_move_priority = move_priority_ter


def order_moves(moves: List[Move],
                board: AbstractBoard,
                candidate_best_move: Move = None) -> List[Move]:
    if candidate_best_move is not None:
        # If candidate_best_move is provided, put it at the beginning of the list
        moves.remove(candidate_best_move)
        sorted_moves = [candidate_best_move] + sorted(moves, key=lambda move: selected_move_priority(move, board), reverse=True)
    else:
        # If candidate_best_move is None, perform the regular sorting
        sorted_moves = sorted(moves, key=lambda move: selected_move_priority(move, board), reverse=True)

    return sorted_moves

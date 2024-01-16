"""
In this script, we implement the first version of evaluation and search !
"""
import time
from chess import Move
from maxoul_chess.abstract_board import AbstractBoard
from maxoul_chess.python_chess_board import PythonChessBoard
from maxoul_chess.evaluation import evaluate
from maxoul_chess.legal_moves_generation import order_moves, get_quiescence_moves
from maxoul_chess.utils import zobrist_hash, LimitedHashTable


def quiescence_search(board: AbstractBoard,
                      depth: int,
                      alpha: float,
                      beta: float,
                      maximizing_player: bool,
                      z_hash: str,
                      use_eval_cache: bool):
    """
    Performs a quiescence search on the given board state.
    """
    stand_pat = evaluate(board, z_hash=z_hash, use_cache=use_eval_cache)

    if depth == 0:
        return stand_pat

    if stand_pat == 0:  # There may be a draw here ! caution:
        if board.is_stalemate() or board.is_insufficient_material() \
                or board.is_fifty_moves() or board.board.is_repetition():
            return 0.

    moves = get_quiescence_moves(board)
    if len(moves) == 0:
        return stand_pat

    if maximizing_player:
        best_score = -float('inf')
        if stand_pat >= beta:
            return stand_pat
        if alpha < stand_pat:
            alpha = stand_pat

        for move in moves:
            board.push(move)
            score = quiescence_search(board=board,
                                      alpha=alpha,
                                      beta=beta,
                                      depth=depth - 1,
                                      maximizing_player=False,
                                      z_hash=z_hash,
                                      use_eval_cache=use_eval_cache)
            board.pop()
            best_score = max(best_score, score)
            if best_score >= beta:
                return best_score
            alpha = max(best_score, alpha)
        return best_score

    else:
        best_score = float('inf')
        if stand_pat <= alpha:
            return stand_pat
        if stand_pat < beta:
            beta = stand_pat

        for move in moves:
            board.push(move)
            score = quiescence_search(board=board,
                                      alpha=alpha,
                                      beta=beta,
                                      depth=depth - 1,
                                      maximizing_player=True,
                                      z_hash=z_hash,
                                      use_eval_cache=use_eval_cache)
            board.pop()
            best_score = min(best_score, score)
            if best_score <= alpha:
                return best_score
            beta = min(best_score, beta)
        return best_score


pv_cache = LimitedHashTable(max_size=1e7)
search_cache = LimitedHashTable(max_size=1e7)
n_calls = 0


def min_max_search(board: PythonChessBoard,
                   depth: int = 2,
                   maximizing_player: bool = True,
                   alpha: float = -float('inf'),
                   beta: float = float('inf'),
                   capture_max_depth: int = 4,
                   pruning: bool = True,
                   candidate_best_move: Move = None,
                   max_end_time: float = None,
                   use_search_cache: bool = False,
                   use_eval_cache: bool = False,
                   use_pv_cache: bool = False):
    """
    alpha: The best lower bound on the score for the maximizing player (White in chess).     beta is the worst possible score for black
    beta: Best upper bound on the score of black
    """
    global n_calls
    n_calls += 1

    z_hash = None

    if use_search_cache or use_eval_cache or use_pv_cache:
        z_hash = str(zobrist_hash(board.board))

    hash_key = None
    if use_search_cache:
        hash_key = z_hash + str(depth)
        out = search_cache.get(hash_key)
        if out is not None:
            return out

    if use_pv_cache and candidate_best_move is None:
        candidate_best_move = pv_cache.get(z_hash)  # only z_hash this time !

    if depth == 0:
        out = quiescence_search(board=board,
                                depth=capture_max_depth,
                                alpha=alpha,
                                beta=beta,
                                maximizing_player=maximizing_player,
                                z_hash=z_hash,
                                use_eval_cache=use_eval_cache)

        if use_search_cache:
            search_cache.insert(hash_key, (out, None))
        return out, None, False

    legal_moves = board.generate_legal_moves()
    ordered_moves = order_moves(legal_moves, board, candidate_best_move=candidate_best_move)

    search_cancelled = False

    if maximizing_player:
        best_evaluation = -float('inf')
        best_move = None

        for move in ordered_moves:
            if max_end_time is not None and time.time() > max_end_time:
                print('Stopping during current search, time is ellapsed')
                search_cancelled = True
                break  # Still wanna do the end routine !
            board.push(move)
            move_evaluation = min_max_search(board=board,
                                             depth=depth - 1,
                                             maximizing_player=False,
                                             alpha=alpha,
                                             beta=beta,
                                             pruning=pruning,
                                             capture_max_depth=capture_max_depth,
                                             use_search_cache=use_search_cache,
                                             use_eval_cache=use_eval_cache,
                                             use_pv_cache=use_pv_cache)[0]
            if move_evaluation > best_evaluation:
                best_evaluation = move_evaluation
                best_move = move
            alpha = max(alpha, best_evaluation)
            board.pop()
            if pruning:
                if beta <= alpha:
                    break
    else:
        best_evaluation = float('inf')
        best_move = None

        for move in ordered_moves:
            # Check time is not over:
            if max_end_time is not None and time.time() > max_end_time:
                print('Stopping during current search, time is ellapsed')
                search_cancelled = True
                break  # Still wanna do the end routine !

            board.push(move)
            move_evaluation = min_max_search(board=board,
                                             depth=depth - 1,
                                             maximizing_player=True,
                                             alpha=alpha,
                                             beta=beta,
                                             pruning=pruning,
                                             capture_max_depth=capture_max_depth,
                                             use_search_cache=use_search_cache,
                                             use_eval_cache=use_eval_cache,
                                             use_pv_cache=use_pv_cache)[0]
            if move_evaluation < best_evaluation:
                best_evaluation = move_evaluation
                best_move = move
            beta = min(beta, best_evaluation)
            board.pop()
            if pruning:
                if beta <= alpha:
                    break

    out = best_evaluation, best_move, search_cancelled

    if search_cancelled:
        return out

    # If there were no legal moves (checkmate or stalemate), we still need to evaluate the position
    if best_evaluation == float('inf') or best_evaluation == - float('inf'):
        out = evaluate(board=board,
                       z_hash=z_hash,
                       use_cache=use_eval_cache), None, True

    if use_search_cache:
        if not search_cancelled:
            search_cache.insert(hash_key, out)

    if use_pv_cache:
        pv_cache.insert(z_hash, out[1])

    return out

from maxoul_chess.python_chess_board import PythonChessBoard
from maxoul_chess.search import min_max_search
import chess


def play_one_full_game(max_ply=10, verbose=False):
    board = PythonChessBoard()

    while not board.is_game_over(claim_draw=True):
        eval, best_move = min_max_search(board,
                                         depth=4,
                                         maximizing_player=(board.turn == chess.WHITE),
                                         pruning=True,
                                         capture_max_depth=0
                                         )
        if verbose:
            print('best_move:', best_move, 'eval', eval, 'turn', board.turn == chess.WHITE)
        board.push(best_move)

        if max_ply is not None and board.get_ply() > max_ply:
            break


if __name__ == '__main__':
    play_one_full_game(10)

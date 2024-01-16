from maxoul_chess.search import min_max_search, pv_cache, search_cache
from maxoul_chess.python_chess_board import PythonChessBoard
from maxoul_chess.utils import LimitedHashTable
from maxoul_chess.evaluation import evaluation_cache, evaluate_material
from maxoul_chess.legal_moves_generation import get_quiescence_moves, order_moves, selected_move_priority
import chess
import time
import random
import numpy as np


# TODO: hash (for both stuff plz)
# TODO: ordering of moves in iterative deepening
# delta pruning, and improvements to quiescence


class MaxoulBot:
    def __init__(self,
                 max_depth: int = 5,
                 capture_max_depth: int = 0,
                 use_search_cache: bool = False,
                 use_eval_cache: bool = False,
                 use_pv_cache: bool = True,
                 pruning: bool = True):
        self.max_depth = max_depth
        self.capture_max_depth = capture_max_depth
        self.pruning = pruning
        self.current_cadence = 180
        self.use_search_cache = use_search_cache
        self.use_pv_cache = use_pv_cache
        self.use_eval_cache = use_eval_cache

    def time_allowance(self, board, time_limit):
        print(time_limit)
        ply = board.ply()
        increment = 0
        time_left = 180

        if time_limit is not None:
            if board.turn == chess.WHITE:
                if time_limit.white_clock is not None:
                    time_left = time_limit.white_clock
                if time_limit.white_inc is not None:
                    increment = time_limit.white_inc
            else:
                if time_limit.black_clock is not None:
                    time_left = time_limit.black_clock
                if time_limit.black_inc is not None:
                    increment = time_limit.black_inc

            # At first, we get the total time ! to calibrate all moves later on.
            # I did not found a better way than this syntax with lichess:
            if 2 <= ply <= 4:
                if time_limit.black_clock is not None:
                    self.current_cadence = time_limit.black_clock

        base_allowances = [4] * 20 + [6] * 20 + [11] * 20 + [14] * 20 + [11] * 20 + \
                          [7] * 20 + [4] * 2000

        allowed_time = base_allowances[ply] * (self.current_cadence / 180.) * 0.9

        # If there is less than 30 seconds, we cap thinking time at 5s:
        if time_left < 30:
            allowed_time = min(5, allowed_time)

        # If there is increment and we are low on time: allowed_time becomes increment
        if time_left < 10 and increment > 0:
            allowed_time = time_left / 10

        # If there is no increment and low on time: we use a fifth of left time
        elif time_left < 10 and increment == 0:
            allowed_time = time_left / 5

        allowed_time = min(allowed_time, 0.5 * time_left) + increment * 0.8
        print(f"Ply {ply} time left {time_left}"
              f" increment {increment} allowance {allowed_time:.2f}")

        return allowed_time

    def aspiration_window_size(self, depth):
        if depth == 1:
            return 400
        elif depth == 2:
            return 300
        elif depth == 3:
            return 200
        elif depth == 4:
            return 80
        elif depth == 5:
            return 60
        else:
            return 40

    def log_infos(self):
        if self.use_search_cache:
            print('Search cache stats:', search_cache.get_stats_str())
        if self.use_eval_cache:
            print('Eval cache stats:', evaluation_cache.get_stats_str())
        # print('Naive move priority order:', or) TODO
        if self.use_pv_cache:
            print('PV cache stats:', pv_cache.get_stats_str())

    def run_time_limited_search(self, alpha, beta, depth, best_move, best_eval, maxoul_board, end_time):
        search_t0 = time.time()

        new_eval, new_best_move, search_cancelled = min_max_search(board=maxoul_board,
                                                                   depth=depth,
                                                                   alpha=alpha,
                                                                   beta=beta,
                                                                   maximizing_player=(
                                                                           maxoul_board.board.turn == chess.WHITE),
                                                                   capture_max_depth=self.capture_max_depth,
                                                                   pruning=self.pruning,
                                                                   candidate_best_move=best_move,
                                                                   max_end_time=end_time,
                                                                   use_search_cache=self.use_search_cache,
                                                                   use_eval_cache=self.use_eval_cache,
                                                                   use_pv_cache=self.use_pv_cache
                                                                   )
        search_duration = time.time() - search_t0

        # Case 1 cancelled: we cancel everything anyway, and keep current best move
        if search_cancelled:
            # Only when the search could at least study the first move and we provided a candidate
            if new_best_move is not None and best_move is not None:
                return new_best_move, new_eval, search_duration
            else:
                return best_move, best_eval, search_duration

        return new_best_move, new_eval, search_duration

    def play_time_opt(self, board: chess.Board, time_limit):
        """
        :param board:
        :param allowed_time: in seconds
        :return:
        """
        allowed_time = self.time_allowance(board, time_limit)
        end_time = time.time() + allowed_time

        maxoul_board = PythonChessBoard(board=board)
        print('Quiescence moves', get_quiescence_moves(maxoul_board))

        best_move = None
        best_evaluation = None

        for depth in range(1, self.max_depth + 1):
            remaining_allowed_time = max(end_time - time.time(), 0)
            if remaining_allowed_time == 0:
                print('stopping, time ellapsed')
                break

            alpha = -float('inf')
            beta = float('inf')
            window_size = self.aspiration_window_size(depth)
            if best_evaluation is not None:
                alpha = best_evaluation - window_size
                beta = best_evaluation + window_size

            new_best_move, new_eval, search_duration = self.run_time_limited_search(alpha,
                                                                                    beta,
                                                                                    depth=depth,
                                                                                    best_move=best_move,
                                                                                    best_eval=best_evaluation,
                                                                                    maxoul_board=maxoul_board,
                                                                                    end_time=end_time)

            # Case 1: we are in the window: let's rolll
            if alpha <= new_eval <= beta:
                print(f'Aspiration bullseye! got {new_eval:.2f}, within {alpha:.2f} {beta:.2f}!')
                best_move = new_best_move
                best_evaluation = new_eval

            # Case 2: We missed the window: we launch again
            else:
                print(f'We missed: got {new_eval:.5f} not within {alpha:.5f} {beta:.5f}! launching again with infty')

                best_move, best_evaluation, search_duration = self.run_time_limited_search(alpha=-float('inf'),
                                                                                           beta=float('inf'),
                                                                                           depth=depth,
                                                                                           best_move=best_move,
                                                                                           best_eval=best_evaluation,
                                                                                           maxoul_board=maxoul_board,
                                                                                           end_time=end_time)

            remaining_allowed_time = max(end_time - time.time(), 0)

            print(f"Depth {depth} done, remaining time {remaining_allowed_time:.2f} "
                  f"current best move {best_move} and eval {best_evaluation:.2f}")

            if 2 * search_duration > remaining_allowed_time:
                print('Stopping, not enough left for next depth')
                break

        if best_move is None:
            best_move = random.choice(list(board.legal_moves))

        print('')
        print(f'Selected move {best_move} evaluation {best_evaluation:.2f}')
        self.log_infos()

        return best_move


bot = MaxoulBot(max_depth=10,
                capture_max_depth=4,
                pruning=True,
                use_search_cache=False,
                use_eval_cache=False,
                use_pv_cache=False)


def play(board: chess.Board,
         time_limit,
         ponder,
         draw_offered,
         root_moves):
    return bot.play_time_opt(board, time_limit=time_limit)


if __name__ == '__main__':
    from chess import Board

    def run_6_moves():
        board = Board(fen='rn1qk2r/pbpp1ppp/1p2pn2/8/1bPP4/2N2NP1/PPQ1PP1P/R1B1KB1R b KQkq - 2 6')
        for i in range(6):
            print(i)
            move = play(board, None, None, None, None)
            board.push(move)

    import cProfile

    profiler = cProfile.Profile()
    profiler.enable()

    # Call the function you want to profile
    run_6_moves()

    profiler.disable()
    profiler.dump_stats('profile_data.cprof')
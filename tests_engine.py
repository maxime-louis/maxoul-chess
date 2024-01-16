import chess
from maxoul_chess.search import min_max_search
from maxoul_chess.python_chess_board import PythonChessBoard

# Puzzle from lichess (thanks !)
# Black turn here
fen_1 = "1k2rQ2/1p2P3/1Ppq3p/p7/P7/6P1/5P2/5RK1 b - - 2 50"
best_move_1 = chess.Move.from_uci('e8f8')

fen_2 = "8/1p3p2/1Pkn1Q2/2r2P1P/8/5K2/8/8 b - - 0 63"
best_move_2 = chess.Move.from_uci('c5f5')

fen_3 = "8/8/3R4/1pk5/8/P2p3K/1P5P/8 b - - 2 50"
best_move_3 = chess.Move.from_uci('c5d6')

fen_4 = "r2qkb1r/pp3ppp/2n1bn2/1Bp1N3/4P3/2N5/PPPP2PP/R1BQ1RK1 b kq - 0 8"
best_move_4 = chess.Move.from_uci("d8d4")

# Hard one !
fen_5 = '8/5pp1/ppk1p1p1/4P3/3K2P1/1P6/1P3PP1/8 b - - 0 35'
best_move_5 = chess.Move.from_uci("c6b5")

fen_6 = "2k2r2/R7/3b4/1R6/n5N1/5PP1/P4PK1/3r4 b - - 2 45"


def get_best_move(fen, depth, pruning, capture_max_depth):
    board = PythonChessBoard(fen=fen)
    move = min_max_search(board,
                          depth=depth,
                          maximizing_player=(board.board.turn == chess.WHITE),
                          capture_max_depth=capture_max_depth,
                          pruning=pruning)[1]
    return move


def do_test_puzzle(fen, best_move, depth, pruning, capture_max_depth):
    engine_move = get_best_move(fen, depth, pruning, capture_max_depth)
    assert engine_move == best_move, f"{engine_move} vs {best_move}"


def test_puzzle_1():
    do_test_puzzle(fen_1, best_move_1, depth=2, pruning=True, capture_max_depth=0)
    # do_test_puzzle(fen_1, best_move_1, depth=2, pruning=False, capture_max_depth=0)
    # do_test_puzzle(fen_1, best_move_1, depth=1, pruning=True, capture_max_depth=0)
    # do_test_puzzle(fen_1, best_move_1, depth=1, pruning=True, capture_max_depth=1)
    # do_test_puzzle(fen_1, best_move_1, depth=4, pruning=True, capture_max_depth=1)
    # do_test_puzzle(fen_1, best_move_1, depth=2, pruning=True, capture_max_depth=5)
    # do_test_puzzle(fen_1, best_move_1, depth=5, pruning=True, capture_max_depth=3)
    # do_test_puzzle(fen_1, best_move_1, depth=6, pruning=True, capture_max_depth=3)


def test_puzzle_2():
    do_test_puzzle(fen_2, best_move_2, depth=2, pruning=True, capture_max_depth=2)
    do_test_puzzle(fen_2, best_move_2, depth=2, pruning=False, capture_max_depth=2)
    do_test_puzzle(fen_2, best_move_2, depth=2, pruning=True, capture_max_depth=1)
    do_test_puzzle(fen_2, best_move_2, depth=5, pruning=True, capture_max_depth=0)


def test_puzzle_3():
    do_test_puzzle(fen_3, best_move_3, depth=1, pruning=True, capture_max_depth=0)
    do_test_puzzle(fen_3, best_move_3, depth=2, pruning=True, capture_max_depth=2)
    do_test_puzzle(fen_3, best_move_3, depth=4, pruning=False, capture_max_depth=0)


def test_puzzle_4():
    do_test_puzzle(fen_4, best_move_4, depth=4, pruning=True, capture_max_depth=0)
    do_test_puzzle(fen_4, best_move_4, depth=4, pruning=True, capture_max_depth=0)


def test_puzzle_5():
    do_test_puzzle(fen_5, best_move_5, depth=7, pruning=True, capture_max_depth=0)


if __name__ == '__main__':
    #
    # # # for i in range(1, 7):•
    # board = PythonChessBoard(fen=fen_6)
    # depth = 4
    # print(get_best_move(board.board.fen(), depth, pruning=True, capture_max_depth=2))

    # for move_number in range(depth-1):
    #     best_move = get_best_move(board.board.fen(), depth-move_number, pruning=False, capture_max_depth=0)
    #     board.push(best_move)
    #     print(best_move, board)
    # board = PythonChessBoard(fen=fen_2)
    # out = min_max_search(board,
    #                      depth=4,
    #                      maximizing_player=(board.board.turn == chess.WHITE),
    #                      capture_max_depth=0,
    #                      alpha=1219,
    #                      beta=1223,
    #                      pruning=True)
    # print(out)
    # from maxoul_chess.search import n_calls
    #
    # print(n_calls)
    #
    # board = PythonChessBoard(fen=fen_2)
    # out = min_max_search(board,
    #                      depth=4,
    #                      maximizing_player=(board.board.turn == chess.WHITE),
    #                      capture_max_depth=0,
    #                      pruning=False)
    # print(out)
    # from maxoul_chess.search import n_calls
    #
    # print(n_calls)
    def run_6_moves():
        board = PythonChessBoard(fen='rn1qk2r/pbpp1ppp/1p2pn2/8/1bPP4/2N2NP1/PPQ1PP1P/R1B1KB1R b KQkq - 2 6')
        for i in range(6):
            print(i)
            eval, move, _ = min_max_search(board,
                                           depth=4,
                                           maximizing_player=(board.board.turn == chess.WHITE),
                                           capture_max_depth=5,
                                           pruning=True)
            board.push(move)

    import cProfile

    profiler = cProfile.Profile()
    profiler.enable()

    # Call the function you want to profile
    run_6_moves()

    profiler.disable()
    profiler.dump_stats('profile_data.cprof')


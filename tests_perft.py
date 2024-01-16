import numpy as np

from maxoul_chess.python_chess_board import PythonChessBoard
# from maxoul_chess.bitboard_chess_board import BitboardChessBoard


def perft(board, depth):
    if depth == 0:
        return 1
    count = 0
    moves = board.generate_legal_moves()
    for m in moves:
        board.push(m)
        count += perft(board, depth-1)
        board.pop()

    return count


def test_python_chess_board():
    b = PythonChessBoard()
    assert perft(b, 0) == 1
    assert perft(b, 1) == 20
    assert perft(b, 2) == 400
    assert perft(b, 3) == 8902
    assert perft(b, 4) == 197281


# def test_bitboard_chess_board():
#     b = BitboardChessBoard()
#     print(str(b.board))
#     assert perft(b, 0) == 1
#     assert perft(b, 1) == 20
#     assert perft(b, 2) == 400
#     assert perft(b, 3) == 8902
#     assert perft(b, 4) == 197281


if __name__ == '__main__':
    test_python_chess_board()
    # test_bitboard_chess_board()

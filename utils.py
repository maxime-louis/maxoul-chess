import collections
from collections import OrderedDict

import chess.pgn
import tempfile
from chess.polyglot import zobrist_hash
from chess import Board
import numpy as np

import pgn2gif
import os
import cProfile
import pstats
from lczero.backends import GameState


def board_to_lc0(fen, moves):
    # print('a')
    # print(fen, moves)
    # print('b')
    # print(GameState(fen, moves=moves).as_string())
    return GameState(fen, moves=moves)


def board_to_game(board):
    game = chess.pgn.Game()

    # Undo all moves.
    switchyard = collections.deque()
    while board.get_ply() > 0:
        switchyard.append(board.pop())

    new_board = Board()

    game.setup(new_board)
    node = game

    # Replay all moves.
    while switchyard:
        move = switchyard.pop()
        node = node.add_variation(move)
        board.push(move)

    game.headers["Result"] = new_board.result()
    return game


def save_game_to_gif(game, path):
    temp_pgn_path = tempfile.mktemp(suffix='.pgn')

    with open(temp_pgn_path, 'w') as f:
        f.write(str(game))

    creator = pgn2gif.PgnToGifCreator(reverse=False, duration=0.1, ws_color='white', bs_color='gray')
    creator.create_gif(temp_pgn_path, out_path=path)


def run_and_profile(func):
    cProfile.run(func.__name__ + "()", "profile_results")

    # Load the profiling results
    stats = pstats.Stats("profile_results")

    # Sort the statistics by cumulative time
    stats.sort_stats("cumulative")

    # Print the statistics in a more readable format
    stats.print_stats()
    os.system('/Users/maxime.louis/opt/miniconda3/envs/310python/bin/snakeviz '
              + str(os.path.join(os.getcwd(), 'profile_results')))


class LimitedHashTable:
    def __init__(self, max_size):
        self.max_size = max_size
        self.hash_table = OrderedDict()
        self.n_inserts = 0
        self.n_gets = 0

    def insert(self, key, value):
        if len(self.hash_table) >= self.max_size:
            # Pop the first item (oldest) if the size limit is reached
            self.hash_table.popitem(last=False)
        self.n_inserts += 1
        self.hash_table[key] = value

    def get(self, key):
        if key in self.hash_table:
            self.n_gets += 1
            # Move the accessed item to the end to maintain order
            value = self.hash_table.pop(key)
            self.hash_table[key] = value
            return value
        else:
            return None

    def get_stats_str(self):
        return f'N gets:{self.n_gets} N inserts: {self.n_inserts}'


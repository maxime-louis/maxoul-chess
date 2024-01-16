from beartype.typing import Union, List
from chess import Move, WHITE, BLACK, Square, Piece


class AbstractBoard:
    def generate_capture_moves(self) -> List[Move]:
        raise NotImplementedError

    def generate_legal_moves(self) -> List[Move]:
        raise NotImplementedError

    def push(self, move: Move) -> None:
        raise NotImplementedError

    def pop(self):
        raise NotImplementedError

    def hash(self):
        raise NotImplementedError

    def is_checkmate(self) -> bool:
        raise NotImplementedError

    def is_stalemate(self) -> bool:
        raise NotImplementedError

    def winner(self) -> bool:
        raise NotImplementedError

    def is_insufficient_material(self) -> bool:
        raise NotImplementedError

    def is_fifty_moves(self) -> bool:
        raise NotImplementedError

    def is_capture(self, move: Move) -> bool:
        raise NotImplementedError

    def gives_check(self, move: Move) -> bool:
        raise NotImplementedError

    def piece_at(self, square: Square) -> Piece:
        raise NotImplementedError

    def is_game_over(self, claim_draw: bool) -> bool:
        raise NotImplementedError

    def get_ply(self) -> int:
        return self.ply

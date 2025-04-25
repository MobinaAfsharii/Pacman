import heapq
import os
import random
import time
from typing import Any, TypeAlias

import numpy as np

Position: TypeAlias = tuple[int, int]
GameState: TypeAlias = dict[str, Any]
Path: TypeAlias = list[Position]

WALL = "o"
DOT = "."
EMPTY = " "
PACMAN = "P"
GHOST = "G"
POWER_PELLET = "*"

SCORE_DOT = 10
SCORE_MOVE = -1
SCORE_WIN = 1000.0
SCORE_LOSE = -1000.0
GHOST_DISTANCE_PENALTY = -2.0
GHOST_PROXIMITY_THRESHOLD = 1
GHOST_SEVERE_PENALTY = -200.0
DOT_PROXIMITY_BONUS_FACTOR = 5.0
DOT_REMAINING_PENALTY_FACTOR = 0.5


class Board:
    def __init__(self, layout: list[str]):
        if not layout:
            raise ValueError("Layout cannot be empty")

        first_row_len = len(layout[0])
        print(first_row_len)
        print([len(row) == first_row_len for row in layout])
        if not all(len(row) == first_row_len for row in layout):
            raise ValueError("All rows in the layout must have the same length.")


        self.layout = np.array([list(row) for row in layout], dtype=str)

        self.rows: int
        self.cols: int
        self.rows, self.cols = self.layout.shape
        self.dots_remaining: int = int(np.sum(self.layout == DOT))

    def __getitem__(self, pos: Position) -> str:
        r, c = pos
        if 0 <= r < self.rows and 0 <= c < self.cols:
            return str(self.layout[r, c])
        return WALL

    def __setitem__(self, pos: Position, value: str) -> None:
        r, c = pos
        if 0 <= r < self.rows and 0 <= c < self.cols:
            current_val = str(self.layout[r, c])
            if current_val == DOT and value != DOT:
                self.dots_remaining = max(0, self.dots_remaining - 1)
            self.layout[r, c] = value

    def is_wall(self, pos: Position) -> bool:
        return self[pos] == WALL

    def get_valid_moves(self, pos: Position) -> list[Position]:
        r, c = pos
        moves: list[Position] = []
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            new_pos: Position = (r + dr, c + dc)
            if not self.is_wall(new_pos):
                moves.append(new_pos)
        if not moves:
            if not self.is_wall(pos):
                moves.append(pos)

        return moves

    def draw(self, score: float = 0.0, message: str = "") -> None:
        _ = os.system("cls" if os.name == "nt" else "clear")
        for row in self.layout:
            print(" ".join(row))
        print(f"\nScore: {score:.0f}")
        if message:
            print(message)


class Pacman:
    def __init__(self, pos: Position):
        self.pos: Position = pos
        self.score: float = 0.0

    def move(self, new_pos: Position, board: Board) -> None:
        current_char: str = board[new_pos]
        if current_char == DOT:
            self.score += SCORE_DOT

        else:
            self.score += SCORE_MOVE

        board[self.pos] = EMPTY
        self.pos = new_pos
        board[self.pos] = PACMAN


class Ghost:
    def __init__(self, pos: Position, id_num: int):
        self.id: int = id_num
        self.start_pos: Position = pos
        self.pos: Position = pos
        self.previous_char: str = EMPTY

    def move(self, new_pos: Position, board: Board) -> None:
        board[self.pos] = self.previous_char
        self.previous_char = board[new_pos]
        if self.previous_char == PACMAN:
            self.previous_char = EMPTY
        self.pos = new_pos
        board[self.pos] = GHOST


def heuristic(a: Position, b: Position) -> float:
    (r1, c1) = a
    (r2, c2) = b
    return float(abs(r1 - r2) + abs(c1 - c2))


def a_star_search(board: Board, start: Position, goal: Position) -> Path | None:
    frontier: list[tuple[float, float, Position]] = [
        (0 + heuristic(start, goal), 0, start)
    ]
    came_from: dict[Position, Position | None] = {start: None}
    cost_so_far: dict[Position, float] = {start: 0}

    while frontier:
        _, current_g_score, current_pos = heapq.heappop(frontier)

        if current_pos == goal:
            path: Path = []
            temp: Position | None = current_pos
            while temp is not None:
                path.append(temp)
                temp = came_from[temp]
            return path[::-1]

        valid_moves = board.get_valid_moves(current_pos)
        valid_moves.sort(key=lambda p: heuristic(p, goal))

        for next_pos in valid_moves:
            new_cost: float = current_g_score + 1.0

            if next_pos not in cost_so_far or new_cost < cost_so_far[next_pos]:
                cost_so_far[next_pos] = new_cost
                priority: float = new_cost + heuristic(next_pos, goal)
                heapq.heappush(frontier, (priority, new_cost, next_pos))
                came_from[next_pos] = current_pos

    return None


def evaluate_state(
    board: Board,
    pacman_pos: Position,
    pacman_score: float,
    ghost_data: list[dict[str, Any]],
) -> float:
    ghost_positions = [g["pos"] for g in ghost_data]
    if pacman_pos in ghost_positions:
        return SCORE_LOSE

    if board.dots_remaining == 0:
        return SCORE_WIN

    score = pacman_score

    min_dist_to_ghost: float = float("inf")
    for ghost_pos in ghost_positions:
        dist = heuristic(pacman_pos, ghost_pos)
        min_dist_to_ghost = min(min_dist_to_ghost, dist)
        if dist <= GHOST_PROXIMITY_THRESHOLD:
            score += GHOST_SEVERE_PENALTY
        elif dist <= 3:
            score += GHOST_DISTANCE_PENALTY * (4.0 - dist)

    score -= board.dots_remaining * SCORE_DOT * DOT_REMAINING_PENALTY_FACTOR

    return score


def simulate_move(game_state: GameState, agent_index: int, move: Position) -> GameState:
    new_board_layout = np.copy(game_state["board"].layout)
    new_board = Board([])
    new_board.layout = new_board_layout
    new_board.rows, new_board.cols = new_board.layout.shape
    new_board.dots_remaining = game_state["board"].dots_remaining

    new_pacman_state = game_state["pacman"].copy()
    new_ghosts_state = [g.copy() for g in game_state["ghosts"]]
    new_score = game_state["score"]

    new_state: GameState = {
        "board": new_board,
        "pacman": new_pacman_state,
        "ghosts": new_ghosts_state,
        "score": new_score,
    }

    if agent_index == 0:
        pacman_info = new_state["pacman"]
        old_pos = pacman_info["pos"]
        new_pos = move

        char_at_new_pos = new_state["board"][new_pos]

        if char_at_new_pos == DOT:
            pacman_info["score"] += SCORE_DOT
            new_state["score"] += SCORE_DOT
            new_state["board"].dots_remaining = max(
                0, new_state["board"].dots_remaining - 1
            )
        else:
            pacman_info["score"] += SCORE_MOVE
            new_state["score"] += SCORE_MOVE

        new_state["board"][old_pos] = EMPTY
        new_state["board"][new_pos] = PACMAN
        pacman_info["pos"] = new_pos

    else:
        ghost_id_index = agent_index - 1
        ghost_info = new_state["ghosts"][ghost_id_index]
        old_pos = ghost_info["pos"]
        new_pos = move

        original_char_at_old_pos = ghost_info["previous_char"]
        new_state["board"][old_pos] = original_char_at_old_pos

        new_char_at_new_pos = new_state["board"][new_pos]
        ghost_info["previous_char"] = (
            EMPTY if new_char_at_new_pos == PACMAN else new_char_at_new_pos
        )

        new_state["board"][new_pos] = GHOST
        ghost_info["pos"] = new_pos

    return new_state


def minimax(
    game_state: GameState, depth: int, agent_index: int, alpha: float, beta: float
) -> float:
    num_agents: int = 1 + len(game_state["ghosts"])

    current_pacman_pos: Position = game_state["pacman"]["pos"]
    current_ghost_data: list[dict[str, Any]] = game_state["ghosts"]
    current_ghost_positions: list[Position] = [g["pos"] for g in current_ghost_data]

    if (
        current_pacman_pos in current_ghost_positions
        or game_state["board"].dots_remaining == 0
        or depth == 0
    ):
        return evaluate_state(
            game_state["board"],
            current_pacman_pos,
            game_state["pacman"]["score"],
            current_ghost_data,
        )

    next_agent_index: int = (agent_index + 1) % num_agents
    next_depth: int = depth - 1 if next_agent_index == 0 else depth

    possible_moves: list[Position] = []
    if agent_index == 0:
        possible_moves = game_state["board"].get_valid_moves(current_pacman_pos)
        safe_moves = [m for m in possible_moves if m not in current_ghost_positions]
        if not safe_moves:
            possible_moves = game_state["board"].get_valid_moves(current_pacman_pos)
        else:
            possible_moves = safe_moves
        if not possible_moves:
            possible_moves = [current_pacman_pos]

        best_val: float = -float("inf")
        for move in possible_moves:
            new_state = simulate_move(game_state, agent_index, move)
            val: float = minimax(new_state, next_depth, next_agent_index, alpha, beta)
            best_val = max(best_val, val)
            alpha = max(alpha, best_val)
            if beta <= alpha:
                break
        return best_val

    else:
        ghost_id_index: int = agent_index - 1
        current_ghost_pos: Position = current_ghost_positions[ghost_id_index]
        possible_moves = game_state["board"].get_valid_moves(current_ghost_pos)

        if not possible_moves:
            possible_moves = [current_ghost_pos]

        worst_val: float = float("inf")
        for move in possible_moves:
            new_state = simulate_move(game_state, agent_index, move)
            val = minimax(new_state, next_depth, next_agent_index, alpha, beta)
            worst_val = min(worst_val, val)
            beta = min(beta, worst_val)
            if beta <= alpha:
                break
        return worst_val


def get_best_pacman_action(game_state: GameState, depth: int) -> Position:
    pacman_pos: Position = game_state["pacman"]["pos"]
    possible_moves: list[Position] = game_state["board"].get_valid_moves(pacman_pos)
    ghost_positions: list[Position] = [g["pos"] for g in game_state["ghosts"]]
    safe_moves = [m for m in possible_moves if m not in ghost_positions]

    if not safe_moves:
        possible_moves = game_state["board"].get_valid_moves(pacman_pos)
        if not possible_moves:
            return pacman_pos
    else:
        possible_moves = safe_moves

    best_score: float = -float("inf")

    best_move: Position = possible_moves[0] if possible_moves else pacman_pos
    alpha: float = -float("inf")
    beta: float = float("inf")

    num_agents: int = 1 + len(game_state["ghosts"])
    next_agent_index: int = 1 % num_agents if num_agents > 1 else 0
    next_depth: int = depth

    for move in possible_moves:
        new_state = simulate_move(game_state, 0, move)
        score: float = minimax(new_state, next_depth, next_agent_index, alpha, beta)

        if score > best_score:
            best_score = score
            best_move = move
        alpha = max(alpha, best_score)

    return best_move


class PacmanGame:
    def __init__(
        self, layout_filename: str, num_ghosts: int = 2, pacman_ai_depth: int = 3
    ):
        self.layout_str: list[str] = self._load_layout(layout_filename)
        self.board: Board = Board(self.layout_str)

        pacman_starts: list[Position] = self._find_char(PACMAN)
        if not pacman_starts:
            raise ValueError("Layout must contain Pacman 'P'")
        self.pacman_start_pos: Position = pacman_starts[0]

        ghost_starts: list[Position] = self._find_char(GHOST)
        if not ghost_starts:
            empty_starts = self._find_char(EMPTY)
            if len(empty_starts) < num_ghosts:
                raise ValueError("Not enough empty spaces ' ' or 'G' for ghosts")

            indices = np.linspace(0, len(empty_starts) - 1, num_ghosts, dtype=int)
            ghost_starts = [empty_starts[i] for i in indices]

        self.pacman: Pacman = Pacman(self.pacman_start_pos)
        self.ghosts: list[Ghost] = []
        for i in range(num_ghosts):
            start_pos = ghost_starts[i % len(ghost_starts)]
            ghost = Ghost(start_pos, i)
            ghost.previous_char = self.board[start_pos]
            self.ghosts.append(ghost)

        self.board[self.pacman.pos] = PACMAN
        for ghost in self.ghosts:
            self.board[ghost.pos] = GHOST

        self.game_over: bool = False
        self.message: str = ""
        self.pacman_ai_depth: int = pacman_ai_depth

    def _load_layout(self, filename: str) -> list[str]:
        if not os.path.exists(filename):
            raise FileNotFoundError(f"Layout file not found: {filename}")
        with open(filename, "r") as f:
            return [line.strip() for line in f if line.strip()]

    def _find_char(self, char_to_find: str) -> list[Position]:
        positions: list[Position] = []
        for r, row in enumerate(self.layout_str):
            for c, cell in enumerate(row):
                if cell == char_to_find:
                    positions.append((r, c))
        return positions

    def _get_game_state(self) -> GameState:
        state: GameState = {
            "board": self.board,
            "pacman": {"pos": self.pacman.pos, "score": self.pacman.score},
            "ghosts": [
                {"pos": g.pos, "id": g.id, "previous_char": g.previous_char}
                for g in self.ghosts
            ],
            "score": self.pacman.score,
        }
        return state

    def run(self) -> None:
        turn: int = 0
        while not self.game_over:
            self.board.draw(self.pacman.score, self.message)
            self.message = ""
            turn += 1

            game_state = self._get_game_state()
            pacman_action = get_best_pacman_action(game_state, self.pacman_ai_depth)

            if pacman_action != self.pacman.pos:
                self.pacman.move(pacman_action, self.board)

            if self.pacman.pos in [g.pos for g in self.ghosts]:
                self.message = "Game Over! Pacman caught!"
                self.game_over = True
                self.board[self.pacman.pos] = "X"
                self.board.draw(self.pacman.score, self.message)
                break

            for ghost in self.ghosts:
                goal: Position = self.pacman.pos
                path: Path | None = a_star_search(self.board, ghost.pos, goal)

                ghost_action: Position = ghost.pos
                if path and len(path) > 1:
                    ghost_action = path[1]
                elif path and len(path) == 1:
                    ghost_action = path[0]
                else:
                    valid_moves = self.board.get_valid_moves(ghost.pos)
                    if valid_moves:
                        ghost_action = random.choice(
                            [m for m in valid_moves if m != ghost.pos] + [ghost.pos]
                        )

                if ghost_action != ghost.pos:
                    ghost.move(ghost_action, self.board)

                if ghost.pos == self.pacman.pos:
                    self.message = f"Game Over! Ghost {ghost.id} caught Pacman!"
                    self.game_over = True
                    self.board[ghost.pos] = "X"
                    break

            if self.game_over:
                self.board.draw(self.pacman.score, self.message)
                break

            if self.board.dots_remaining == 0:
                self.message = "You Win! All dots eaten!"
                self.game_over = True
                self.board.draw(self.pacman.score, self.message)
                break

            time.sleep(0.3)


if __name__ == "__main__":
    layout_content = """
oooooooooooooooooooo
oP.................o
o.ooooooooo.oooooo.o
o.o.......o..o.....o
o.o.ooooo.o.o.oooo.o
o......G...o..o.o..o
ooooo.o.ooo.oooo.o.o
oG....o............o
oooooo.oooooo.oooo.o
o..................o
oooooooooooooooooooo
"""
    layout_filename = "layout.txt"
    try:
        with open(layout_filename, "w") as f:
            f.write(layout_content.strip())

        game = PacmanGame(layout_filename, num_ghosts=2, pacman_ai_depth=4)
        game.run()

    except FileNotFoundError as e:
        print(e)
    except ValueError as e:
        print(e)
    finally:
        if os.path.exists(layout_filename):
            try:
                os.remove(layout_filename)
            except OSError as e:
                print(f"Error removing layout file: {e}")

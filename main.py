import copy
import math


class Game:
    def __init__(self):
        self.board = [['.' for j in range(8)] for i in range(8)]
        self.queen_x = 0
        self.queen_y = 0
        self.king_w_x = 0
        self.king_w_y = 0
        self.king_b_x = 0
        self.king_b_y = 0
        self.player = 'W'
        self.game_on = False
        self.history = []
        self.moves_since_capture_or_pawn_move = 0

    def start(self, queen_x, queen_y, king_w_x, king_w_y, king_b_x, king_b_y, player):
        if ((queen_x, queen_y) == (king_w_x, king_w_y) or (queen_x, queen_y) == (king_b_x, king_b_y)
                or (king_w_x, king_w_y) == (king_b_x, king_b_y)):
            print("Error: Initial piece positions cannot overlap.")
            return False

        if (0 <= queen_x < 8 and 0 <= queen_y < 8 and 0 <= king_w_x < 8 and 0 <= king_w_y < 8 and 0 <= king_b_x < 8
                and 0 <= king_b_y < 8):
            self.board = [['.' for j in range(8)] for i in range(8)]
            self.board[queen_y][queen_x] = 'Q'
            self.board[king_w_y][king_w_x] = 'K'
            self.board[king_b_y][king_b_x] = 'k'
            self.queen_x = queen_x
            self.queen_y = queen_y
            self.king_w_x = king_w_x
            self.king_w_y = king_w_y
            self.king_b_x = king_b_x
            self.king_b_y = king_b_y
            self.player = player
            self.game_on = True
            self.history = []
            self.moves_since_capture_or_pawn_move = 0
            return True
        return False

    def switch(self):
        if self.player == 'W':
            self.player = 'B'
        else:
            self.player = 'W'

    def draw(self):
        # 50-move rule
        if self.moves_since_capture_or_pawn_move >= 50:
            return True
        # Stalemate
        if self.player == 'B' and not self.is_check(self.king_b_x,
                                                    self.king_b_y) and not self.find_possible_king_b_moves():
            return True
        # Draw by Queen capture
        if self.queen_x == -1:
            return True
        return False

    def add_history(self):
        self.history.append(([[self.board[i][j] for j in range(8)] for i in range(8)], self.queen_x, self.queen_y,
                             self.king_w_x, self.king_w_y, self.king_b_x, self.king_b_y, self.player,
                             self.moves_since_capture_or_pawn_move))

    def undo(self):
        if self.history:
            (self.board, self.queen_x, self.queen_y, self.king_w_x, self.king_w_y, self.king_b_x, self.king_b_y,
             self.player, self.moves_since_capture_or_pawn_move) = self.history.pop()
            self.game_on = True
            return True
        return False

    def is_blocked(self, x1, y1, x2, y2):
        dx = x2 - x1
        dy = y2 - y1
        step_x = 0
        step_y = 0
        if dx != 0:
            step_x = int(dx / abs(dx))
        if dy != 0:
            step_y = int(dy / abs(dy))

        x, y = x1 + step_x, y1 + step_y
        while x != x2 or y != y2:
            if self.board[y][x] != '.':
                return True
            x += step_x
            y += step_y
        return False

    def is_check(self, x, y):
        # Check for queen attack on the given square, excluding the queen's position itself
        if self.queen_x == -1:
            return False

        if x == self.queen_x or y == self.queen_y or abs(x - self.queen_x) == abs(y - self.queen_y):
            if not self.is_blocked(self.queen_x, self.queen_y, x, y):
                return True
        return False

    def check_win(self):
        # Check for checkmate
        if self.is_check(self.king_b_x, self.king_b_y) and not self.find_possible_king_b_moves():
            return True
        return False

    def find_possible_queen_moves(self):
        moves = []
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        for dx, dy in directions:
            x, y = self.queen_x + dx, self.queen_y + dy
            while 0 <= x < 8 and 0 <= y < 8:
                if self.board[y][x] == '.':
                    moves.append((x, y))
                elif self.board[y][x] == 'k':
                    moves.append((x, y))
                    break
                else:
                    break
                x += dx
                y += dy
        return moves

    def find_possible_king_w_moves(self):
        moves = []
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                if dx == 0 and dy == 0:
                    continue
                x, y = self.king_w_x + dx, self.king_w_y + dy

                if 0 <= x < 8 and 0 <= y < 8:
                    if self.board[y][x] == 'Q':
                        continue
                    if abs(x - self.king_b_x) <= 1 and abs(y - self.king_b_y) <= 1:
                        continue
                    moves.append((x, y))
        return moves

    def find_possible_king_b_moves(self):
        moves = []
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                if dx == 0 and dy == 0:
                    continue
                x, y = self.king_b_x + dx, self.king_b_y + dy

                if 0 <= x < 8 and 0 <= y < 8:
                    if abs(x - self.king_w_x) <= 1 and abs(y - self.king_w_y) <= 1:
                        continue
                    if x == self.queen_x and y == self.queen_y:
                        moves.append((x, y))
                        continue
                    if self.board[y][x] == '.' and not self.is_check(x, y):
                        moves.append((x, y))
        return moves

    def move_queen(self, x, y):
        if self.player == 'W':
            if (x, y) in self.find_possible_queen_moves():
                self.add_history()
                self.board[self.queen_y][self.queen_x] = '.'
                self.queen_y = y
                self.queen_x = x
                self.board[y][x] = 'Q'
                self.moves_since_capture_or_pawn_move += 1
                return True
        return False

    def move_king_w(self, x, y):
        if self.player == 'W':
            if (x, y) in self.find_possible_king_w_moves():
                self.add_history()
                self.board[self.king_w_y][self.king_w_x] = '.'
                self.king_w_y = y
                self.king_w_x = x
                self.board[y][x] = 'K'
                self.moves_since_capture_or_pawn_move += 1
                return True
        return False

    def move_king_b(self, x, y):
        if self.player == 'B':
            if (x, y) in self.find_possible_king_b_moves():
                self.add_history()
                self.board[self.king_b_y][self.king_b_x] = '.'
                self.king_b_y = y
                self.king_b_x = x
                if self.queen_x == x and self.queen_y == y:
                    self.queen_x = -1
                    self.queen_y = -1
                self.board[y][x] = 'k'
                self.moves_since_capture_or_pawn_move += 1
                return True
        return False

    def evaluate_board(self):
        """Evaluates the board state from White's perspective."""
        if self.check_win():
            return 10000  # White wins (checkmate)
        if self.draw():
            return 0

        score = 0
        # Heuristic 1: Restrict the black king's movement. Fewer moves are better for White.
        score += (8 - len(self.find_possible_king_b_moves())) * 10
        # Heuristic 2: The white king should be close to the black king to help the queen.
        king_dist = abs(self.king_w_x - self.king_b_x) + abs(self.king_w_y - self.king_b_y)
        score -= king_dist * 5
        # Heuristic 3: It's good to force the black king to the edge of the board.
        dist_to_edge_x = min(self.king_b_x, 7 - self.king_b_x)
        dist_to_edge_y = min(self.king_b_y, 7 - self.king_b_y)
        score -= (dist_to_edge_x + dist_to_edge_y) * 10
        return score

    def get_all_moves(self):
        """Gets all possible moves for the current player."""
        moves = []
        if self.player == 'W':
            if self.queen_x != -1:
                for move in self.find_possible_queen_moves():
                    moves.append(('Q', move[0], move[1]))
            for move in self.find_possible_king_w_moves():
                moves.append(('K', move[0], move[1]))
        else:  # Player is 'B'
            for move in self.find_possible_king_b_moves():
                moves.append(('k', move[0], move[1]))
        return moves

    def apply_move(self, move_tuple):
        """Applies a move to the board without validation. Used for simulation."""
        piece, x, y = move_tuple
        if piece == 'Q':
            self.board[self.queen_y][self.queen_x] = '.'
            self.queen_x, self.queen_y = x, y
            self.board[y][x] = 'Q'
        elif piece == 'K':
            self.board[self.king_w_y][self.king_w_x] = '.'
            self.king_w_x, self.king_w_y = x, y
            self.board[y][x] = 'K'
        elif piece == 'k':
            self.board[self.king_b_y][self.king_b_x] = '.'
            self.king_b_x, self.king_b_y = x, y
            if self.queen_x == x and self.queen_y == y:  # Capture
                self.queen_x, self.queen_y = -1, -1
            self.board[y][x] = 'k'
        self.moves_since_capture_or_pawn_move += 1
        self.switch()

    def minimax(self, depth, alpha, beta, maximizing_player):
        """Minimax algorithm with alpha-beta pruning."""
        if depth == 0 or self.check_win() or self.draw():
            return self.evaluate_board()

        if maximizing_player:  # White's turn
            max_eval = -math.inf
            for move in self.get_all_moves():
                game_copy = copy.deepcopy(self)
                game_copy.apply_move(move)
                eval_score = game_copy.minimax(depth - 1, alpha, beta, False)
                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break
            return max_eval
        else:  # Black's turn
            min_eval = math.inf
            for move in self.get_all_moves():
                game_copy = copy.deepcopy(self)
                game_copy.apply_move(move)
                eval_score = game_copy.minimax(depth - 1, alpha, beta, True)
                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break
            return min_eval

    def find_best_move(self, depth):
        """Finds the best move for the current player using minimax."""
        best_move = None
        if self.player == 'W':  # Maximizer
            max_eval = -math.inf
            for move in self.get_all_moves():
                game_copy = copy.deepcopy(self)
                game_copy.apply_move(move)
                eval_score = game_copy.minimax(depth - 1, -math.inf, math.inf, False)
                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = move
        else:  # Minimizer
            min_eval = math.inf
            for move in self.get_all_moves():
                game_copy = copy.deepcopy(self)
                game_copy.apply_move(move)
                eval_score = game_copy.minimax(depth - 1, -math.inf, math.inf, True)
                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = move
        return best_move


def print_board(board):
    print("  a b c d e f g h")
    print("  ---------------")
    for i, row in enumerate(board):
        print(8 - i, end="|")
        for cell in row:
            print(cell, end=" ")
        print("", 8 - i)
    print("  ---------------")
    print("  a b c d e f g h")


def algebraic_to_coords(alg):
    if len(alg) != 2:
        return None, None
    x = ord(alg[0].lower()) - ord('a')
    y = 8 - int(alg[1])
    if 0 <= x < 8 and 0 <= y < 8:
        return x, y
    return None, None


def coords_to_algebraic(x, y):
    if 0 <= x < 8 and 0 <= y < 8:
        return chr(ord('a') + x) + str(8 - y)
    return ""


def main():
    game = Game()

    while True:
        if not game.game_on:
            print("\nWelcome to the Queen Endgame Trainer!")
            print("1. Start a new game")
            print("2. Quit")
            choice = input("Enter your choice: ")

            if choice == '1':
                print("Enter the initial positions for the pieces (e.g., a1):")
                queen_pos = input("White Queen (Q) position: ")
                king_w_pos = input("White King (K) position: ")
                king_b_pos = input("Black King (k) position: ")

                queen_x, queen_y = algebraic_to_coords(queen_pos)
                king_w_x, king_w_y = algebraic_to_coords(king_w_pos)
                king_b_x, king_b_y = algebraic_to_coords(king_b_pos)

                player = input("Who goes first? (W/B): ").upper()
                if player not in ['W', 'B']:
                    print("Invalid player. Defaulting to White (W).")
                    player = 'W'

                if queen_x is None or king_w_x is None or king_b_x is None:
                    print("Invalid initial position format. Please use algebraic notation (e.g., 'a1').")
                    continue

                if not game.start(queen_x, queen_y, king_w_x, king_w_y, king_b_x, king_b_y, player):
                    print("Invalid initial positions. Please try again.")
                else:
                    print("Game started!")
            elif choice == '2':
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")
        else:
            print_board(game.board)
            print(f"It's {game.player}'s turn.")

            if game.check_win():
                print(f"Checkmate! {'White' if game.player == 'B' else 'Black'} wins!")
                game.game_on = False
                continue

            if game.draw():
                print("Draw!")
                game.game_on = False
                continue

            print("1. Make a move")
            print("2. Undo last move")
            print("3. Start a new game")
            print("4. Get computer move")
            print("5. Quit")

            choice = input("Enter your choice: ")

            if choice == '1':
                move = input("Enter your move (e.g., Q:a1, K:b2, k:c3): ")
                try:
                    piece, coords = move.split(':')
                    x, y = algebraic_to_coords(coords)

                    if x is None or y is None:
                        print("Invalid coordinates.")
                        continue

                    moved = False
                    if piece.upper() == 'Q' and game.player == 'W':
                        moved = game.move_queen(x, y)
                    elif piece.upper() == 'K' and game.player == 'W':
                        moved = game.move_king_w(x, y)
                    elif piece.lower() == 'k' and game.player == 'B':
                        moved = game.move_king_b(x, y)
                    else:
                        print("Invalid piece or it's not your turn to move that piece.")
                        continue

                    if moved:
                        print("Move successful!")
                        game.switch()
                    else:
                        print("Invalid move. Please try again.")

                except ValueError:
                    print("Invalid move format. Please use 'Piece:coords' (e.g., Q:a1).")

            elif choice == '2':
                if game.undo():
                    print("Move undone.")
                else:
                    print("Cannot undo. No history available.")
            elif choice == '3':
                game.game_on = False
                print("Game reset. You can now start a new game.")
            elif choice == '4':
                try:
                    depth = int(input("Enter search depth (e.g., 2 or 3): "))
                    if depth < 1:
                        print("Depth must be at least 1.")
                        continue
                    print("Computer is thinking...")
                    best_move = game.find_best_move(depth)
                    if best_move:
                        piece, x, y = best_move
                        print(f"Computer moves {piece} to {coords_to_algebraic(x, y)}")
                        moved = False
                        if piece == 'Q':
                            moved = game.move_queen(x, y)
                        elif piece == 'K':
                            moved = game.move_king_w(x, y)
                        elif piece == 'k':
                            moved = game.move_king_b(x, y)

                        if moved:
                            game.switch()
                        else:
                            print("Error: The computer chose an invalid move.")
                    else:
                        print("The computer could not find a legal move.")
                except ValueError:
                    print("Invalid depth. Please enter a number.")
            elif choice == '5':
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()

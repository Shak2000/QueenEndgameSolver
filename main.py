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
                    # White king cannot move to a square occupied by a friendly piece (Q)
                    if self.board[y][x] == 'Q':
                        continue
                    # White king cannot move to a square adjacent to the black king
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
                    # Check if the square is not adjacent to the white king
                    if abs(x - self.king_w_x) <= 1 and abs(y - self.king_w_y) <= 1:
                        continue

                    # Check if the square is occupied by the queen (a legal capture)
                    if x == self.queen_x and y == self.queen_y:
                        moves.append((x, y))
                        continue

                    # Check if the empty square is not under attack by the queen
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

                # Check for capture
                if self.queen_x == x and self.queen_y == y:
                    self.queen_x = -1
                    self.queen_y = -1

                self.board[y][x] = 'k'
                self.moves_since_capture_or_pawn_move += 1
                return True
        return False


def print_board(board):
    print("  a b c d e f g h")
    print("  ---------------")
    for i, row in enumerate(board):
        print(8 - i, end="|")
        for cell in row:
            print(cell, end=" ")
        print(8 - i)
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


def main():
    game = Game()

    while True:
        if not game.game_on:
            print("\nWelcome to the Queen Endgame Solver!")
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
                print("Checkmate! White wins!")
                game.game_on = False
                continue

            if game.draw():
                print("Draw!")
                game.game_on = False
                continue

            print("1. Make a move")
            print("2. Undo last move")
            print("3. Start a new game")
            print("4. Quit")

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
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()

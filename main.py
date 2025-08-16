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

    def start(self, queen_x, queen_y, king_w_x, king_w_y, king_b_x, king_b_y, player):
        if (0 <= queen_x < 8 and 0 <= queen_y < 8 and 0 <= king_w_x < 8 and 0 <= king_w_y < 8 and 0 <= king_b_x < 8
                and 0 <= king_b_y < 8):
            self.board = [['.' for j in range(8)] for i in range(8)]
            self.board[queen_y][queen_x] = 'Q'
            self.board[king_w_y][king_w_x] = 'K'
            self.board[king_b_y][king_b_x] = 'K'
            self.queen_x = queen_x
            self.queen_y = queen_y
            self.king_w_x = king_w_x
            self.king_w_y = king_w_y
            self.king_b_x = king_b_x
            self.king_b_y = king_b_y
            self.player = player
            self.game_on = True
            self.history = []

    def switch(self):
        if self.player == 'W':
            self.player = 'B'
        else:
            self.player = 'W'

    def move_queen(self, x, y):
        if (self.player == 'W' and self.board[y][x] == '.' and 0 <= x < 8 and 0 <= y < 8
                and (x == self.queen_x or y == self.queen_y)):
            self.board[self.queen_y][self.queen_x] = '.'
            self.queen_y = y
            self.queen_x = x
            self.board[y][x] = 'Q'
            return True
        return False

    def move_king_w(self, x, y):
        if (self.player == 'W' and self.board[y][x] == '.' and 0 <= x < 8 and 0 <= y < 8 and abs(x - self.king_w_x) < 2
                and abs(y - self.king_w_y) < 2):
            self.board[self.king_w_y][self.king_w_x] = '.'
            self.king_w_y = y
            self.king_w_x = x
            self.board[y][x] = 'K'
            return True
        return False

    def move_king_b(self, x, y):
        if (self.player == 'B' and self.board[y][x] == '.' and 0 <= x < 8 and 0 <= y < 8 and abs(x - self.king_b_x) < 2
                and abs(y - self.king_b_y) < 2):
            self.board[self.king_b_y][self.king_b_x] = '.'
            self.king_b_y = y
            self.king_b_x = x
            self.board[y][x] = 'k'
            return True
        return False


def main():
    print("Welcome to the Queen Endgame Solver!")


if __name__ == "__main__":
    main()

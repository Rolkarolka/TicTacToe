import pygame as pg

class TicTacToe:
    def __init__(self, first_x=True):
        pg.init()
        pg.display.set_caption("TicTacToe")
        self.WIDTH = 600
        self.HEIGHT = self.WIDTH
        self.screen = pg.display.set_mode((self.WIDTH, self.HEIGHT))
        self.screen.fill((16, 16, 16))
        self.board_lines_colour = (240, 240, 240)
        self.board = [[None for i in range(3)] for i in range(3)]
        self.fields_start = [[(0, i), (self.WIDTH // 3, i), (self.WIDTH // 3 * 2, i)] for i in [0, self.HEIGHT // 3, self.HEIGHT // 3 * 2]]
        if first_x:
            self.player = 1
        else:
            self.player = 0
        self.run = True
        self.margin = int(self.WIDTH // 3 * 0.1)
        self.game()

    def draw_x(self, x, y):
        field_size = self.WIDTH // 3
        pg.draw.line(self.screen, (255, 120, 120), (x + self.margin, y + self.margin), (x + field_size - self.margin, y + field_size - self.margin), 5)
        pg.draw.line(self.screen, (255, 120, 120), (x + field_size - self.margin, y + self.margin), (x + self.margin, y + field_size - self.margin), 5)

    def draw_o(self, x, y):
        half_field_size = self.WIDTH // 6
        pg.draw.circle(self.screen, (135, 206, 250), [x + half_field_size, y + half_field_size], half_field_size - self.margin, 5)

    def draw_board(self):
        pg.draw.line(self.screen, self.board_lines_colour, (self.WIDTH // 3, 0), (self.WIDTH // 3, self.HEIGHT), 5)
        pg.draw.line(self.screen, self.board_lines_colour, (self.WIDTH // 3 * 2, 0), (self.WIDTH // 3 * 2, self.HEIGHT), 5)
        pg.draw.line(self.screen, self.board_lines_colour, (0, self.HEIGHT // 3), (self.WIDTH, self.HEIGHT // 3), 5)
        pg.draw.line(self.screen, self.board_lines_colour, (0, self.HEIGHT // 3 * 2), (self.WIDTH, self.HEIGHT // 3 * 2), 5)

    def draw_movements(self):
        for x_row in range(3):
            for y in range(3):
                if self.board[x_row][y] == 1:
                    coord = self.fields_start[x_row][y]
                    self.draw_x(coord[0], coord[1])
                elif self.board[x_row][y] == 0:
                    coord = self.fields_start[x_row][y]
                    self.draw_o(coord[0], coord[1])

    def find_fild(self, coord):
        if coord < self.WIDTH // 3:
            return 0
        elif coord < self.WIDTH // 3 * 2:
            return 1
        else:
            return 2

    def draw_horizontal_winning_line(self, x_row):
        y = self.fields_start[self.board.index(x_row)][0][1] + self.HEIGHT // 6
        self.draw_movements()
        pg.draw.line(self.screen, (255, 0, 0), (0, y), (self.WIDTH, y), 5)

    def draw_vertical_winning_line(self, i):
        x = self.fields_start[0][i][0] + self.WIDTH // 6
        self.draw_movements()
        pg.draw.line(self.screen, (255, 0, 0), (x, 0), (x, self.HEIGHT), 5)

    def check_winning(self):
        self.draw_movements()
        # form a horizontal line
        for x_row in self.board:
            if all([x is self.player for x in x_row]):
                self.draw_horizontal_winning_line(x_row)
                return self.player
        # form a vertical line
        for i in range(len(self.board[0])):
            if all([x[i] is self.player for x in self.board]):
                self.draw_vertical_winning_line(i)
                return self.player
        # form a diagonal line from the upper-left to the lower-right corner
        if all([self.board[i][i] is self.player for i in range(len(self.board))]):
            pg.draw.line(self.screen, (255, 0, 0), (0, 0), (self.WIDTH, self.HEIGHT), 10)
            return self.player
        # form a diagonal line from the lower-left to the upper-right corner
        if all([self.board[i][2 - i] is self.player for i in range(2, -1, -1)]):
            pg.draw.line(self.screen, (255, 0, 0), (0, self.HEIGHT), (self.WIDTH, 0), 10)
            return self.player
        # if draw
        if all([all([x[i] is not None for i in range(len(self.board))]) for x in self.board]):
            return -1
        return None

    def end_game(self, result):
        pg.time.delay(1000)
        pg.quit()

    def update_board(self, pos):
        y = self.find_fild(pos[1])
        x = self.find_fild(pos[0])
        if self.board[y][x] is None:
            self.board[y][x] = self.player
            result = self.check_winning()
            if result is not None:
                pg.display.update()
                self.end_game(result)
            self.player = int(not self.player)

    def game(self):
        while self.run:
            self.draw_board()
            pg.display.update()
            for event in pg.event.get():
                if event.type == pg.MOUSEBUTTONUP:
                    pos = pg.mouse.get_pos()
                    self.update_board(pos)
                if event.type == pg.QUIT:
                    self.run = False
        pg.quit()

tic = TicTacToe()

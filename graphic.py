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
        for x_row in range(3):
            for y in range(3):
                if self.board[x_row][y] == 1:
                    coord = self.fields_start[x_row][y]
                    self.draw_x(coord[0], coord[1])
                elif self.board[x_row][y] == 0:
                    coord = self.fields_start[x_row][y]
                    self.draw_o(coord[0], coord[1])
        pg.display.flip()
    
    def find_fild(self, coord):
        if coord < self.WIDTH // 3:
            return 0
        elif coord < self.WIDTH // 3 * 2:
            return 1
        else:
            return 2

    def check_winning(self):
        # form a horizontal line
        for x_row in self.board:
            if all([x is self.player for x in x_row]):
                return self.player
        # form a vertical line
        for i in range(len(self.board[0])):
            if all([x[i] is self.player for x in self.board]):
                return self.player
        # form a diagonal line from the upper-left to the lower-right corner
        if all([self.board[i][i] is self.player for i in range(len(self.board))]):
            return self.player
        # form a diagonal line from the lower-left to the upper-right corner
        if all([self.board[i][2 - i] is self.player for i in range(2, -1, -1)]):
            return self.player
        # if draw
        if all([all([x[i] is not None for i in range(len(self.board))]) for x in self.board]):
            return -1
        return None

    def update_board(self, pos):
        y = self.find_fild(pos[1])
        x = self.find_fild(pos[0])
        if self.board[y][x] is None:
            self.board[y][x] = self.player
            result = self.check_winning()
            if result is not None:
                return result
            self.player = int(not self.player)
        self.draw_board()
        return None

    def game(self):
        while self.run:
            self.draw_board()
            for event in pg.event.get():
                if event.type == pg.MOUSEBUTTONUP:
                    pos = pg.mouse.get_pos()
                    result = self.update_board(pos)
                    if result is not None:
                        self.run = False
                if event.type == pg.QUIT:
                    self.run = False
        pg.quit()
        return result

tic = TicTacToe()

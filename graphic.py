import pygame as pg

class Graphic:
    def __init__(self, screen, board):
        self.screen = screen
        self.WIDTH = screen.get_width()
        self.HEIGHT = screen.get_height()
        self.screen.fill((16, 16, 16))
        self.board_lines_colour = (240, 240, 240)
        self.board = board
        self.fields_start = [[(0, i), (self.WIDTH // 3, i), (self.WIDTH // 3 * 2, i)] for i in [0, self.HEIGHT // 3, self.HEIGHT // 3 * 2]]
        self.margin = int(self.WIDTH // 3 * 0.1)

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

    def display_string(self, string, pos):
        font = pg.font.SysFont('dejavuserif', 32)
        text = font.render(string, True, (255, 255, 255))
        self.screen.blit(text, pos)
    
    def draw_begin_screen(self):
        self.display_string("Do you want to start first?", (self.WIDTH // 4 + 20, self.HEIGHT // 8))
        self.display_string("Yes", (self.WIDTH // 4, self.HEIGHT // 2))
        self.display_string("No", (self.WIDTH // 4 * 3, self.HEIGHT // 2))
        pg.draw.line(self.screen, self.board_lines_colour, (self.WIDTH // 2, self.HEIGHT // 4), (self.WIDTH // 2, self.HEIGHT), 5)
        pg.display.update()

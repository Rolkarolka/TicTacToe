import pygame as pg
from copy import deepcopy
from numpy import random
class Node:
    # min player - o, max player - x
    def __init__(self, board, player):
        self.current_board = board
        self.config_matrix = [[3, 2, 3], [2, 4, 2], [3, 2, 3]]
        self.heuristic = self.calc_heuristic()
        self.children = []
        self.player = int(player)
        self.terminal = False
        if self.winning(int(not self.player)) is not None:
            self.terminal = True

    def calc_heuristic(self):
        result = 0
        for x in range(len(self.current_board)):
            for y in range(len(self.current_board[x])):
                if self.current_board[x][y] == 0:
                    result -= self.config_matrix[x][y]
                if self.current_board[x][y] == 1:
                    result += self.config_matrix[x][y]
        return result

    def set_children(self):
        for x in range(len(self.current_board)):
            for y in range(len(self.current_board[x])):
                if self.current_board[x][y] is None:
                    board = deepcopy(self.current_board)
                    board[x][y] = int(self.player)
                    self.children.append(Node(board, not self.player))
        if self.children == []:
            self.terminal = True

    def winning(self, player):
        # form a horizontal line
        for x_row in self.current_board:
            if all([x is player for x in x_row]):
                return player
        # form a vertical line
        for i in range(len(self.current_board[0])):
            if all([x[i] is player for x in self.current_board]):
                return player
        # form a diagonal line from the upper-left to the lower-right corner
        if all([self.current_board[i][i] is player for i in range(len(self.current_board))]):
            return player
        # form a diagonal line from the lower-left to the upper-right corner
        if all([self.current_board[i][2 - i] is player for i in range(2, -1, -1)]):
            return player
        # if draw
        if all([all([x[i] is not None for i in range(len(self.current_board))]) for x in self.current_board]):
            return -1
        return None

def minimax(node, depth, maximizingPlayer):
    node.set_children()
    if depth == 0 or node.terminal:
        return node.heuristic

    if maximizingPlayer:
        max_value = float('-inf')
        for child in node.children:
            value = minimax(child, depth - 1, False)
            max_value = max(max_value, value)
        return max_value
    else:
        min_value = float('inf')
        for child in node.children:
            value = minimax(child, depth - 1, True)
            min_value = min(min_value, value)
        return min_value

# ---------------------------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------------------------
class Graphic:
    def __init__(self):
        pg.init()
        pg.display.set_caption("TicTacToe")
        self.WIDTH = 600
        self.HEIGHT = self.WIDTH
        self.screen = pg.display.set_mode((self.WIDTH, self.HEIGHT))
        self.screen.fill((16, 16, 16))
        self.board_lines_colour = (240, 240, 240)
        self.board = [[None for i in range(3)] for i in range(3)]
        self.fields_start = [[(0, i), (self.WIDTH // 3, i), (self.WIDTH // 3 * 2, i)] for i in [0, self.HEIGHT // 3, self.HEIGHT // 3 * 2]]
        self.player = 1     # x = 1,  o = 0
        self.run = True
        self.result = None
        self.whoiswho = {}
        self.margin = int(self.WIDTH // 3 * 0.1)
        self.begin_screen()
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

    def check_conditions(self):
        self.draw_movements()
        # form a horizontal line
        for x_row in self.board:
            if all([x is self.player for x in x_row]):
                y = self.fields_start[self.board.index(x_row)][0][1] + self.HEIGHT // 6
                self.result = self.player
                return [(0, y), (self.WIDTH, y)]
        # form a vertical line
        for i in range(len(self.board[0])):
            if all([x[i] is self.player for x in self.board]):
                x = self.fields_start[0][i][0] + self.WIDTH // 6
                self.result = self.player
                return [(x, 0), (x, self.HEIGHT)]
        # form a diagonal line from the upper-left to the lower-right corner
        if all([self.board[i][i] is self.player for i in range(len(self.board))]):
            self.result = self.player
            return [(0, 0), (self.WIDTH, self.HEIGHT)]
        # form a diagonal line from the lower-left to the upper-right corner
        if all([self.board[i][2 - i] is self.player for i in range(2, -1, -1)]):
            self.result = self.player
            return [(0, self.HEIGHT), (self.WIDTH, 0)]
        # if draw
        if all([all([x[i] is not None for i in range(len(self.board))]) for x in self.board]):
            self.result = 'Tie'
        return []

    def end_game(self):
        pg.time.delay(1000)
        pg.quit()

    def display_string(self, string, pos):
        font = pg.font.SysFont('dejavuserif', 32)
        text = font.render(string, True, (255, 255, 255))
        self.screen.blit(text, pos)
    
    def begin_screen(self):
        self.display_string("Do you want to start first?", (self.WIDTH // 4 + 20, self.HEIGHT // 8))
        self.display_string("Yes", (self.WIDTH // 4, self.HEIGHT // 2))
        self.display_string("No", (self.WIDTH // 4 * 3, self.HEIGHT // 2))
        pg.draw.line(self.screen, self.board_lines_colour, (self.WIDTH // 2, self.HEIGHT // 4), (self.WIDTH // 2, self.HEIGHT), 5)
        pg.display.update()
        while self.run:
            for event in pg.event.get():
                if event.type == pg.MOUSEBUTTONUP:
                    pos = pg.mouse.get_pos()
                    if pos[0] < self.WIDTH // 2:
                        self.whoiswho = {1: 'H', 0: 'AI'}
                    else:
                        self.whoiswho = {1: 'AI', 0: 'H'}
                    return
                if event.type == pg.QUIT:
                    self.run = False
        pg.quit()

    def choose_next_AI_step(self, current_heurisitic, function, node):
        children = []
        terminal = []
        for child in node.children:
            if child.terminal is True:
                terminal.append(child)
            if function(child.heuristic, current_heurisitic):
                current_heurisitic = child.heuristic
                children.clear()
                children.append(child)
            elif child.heuristic == current_heurisitic:
                children.append(child)
        if len(terminal) > 0:
            child = random.choice(terminal)
        else:
            child = random.choice(children)
        return child

    def update_board(self, pos):
            y = self.find_fild(pos[1])
            x = self.find_fild(pos[0])
            if self.board[y][x] is None:
                self.board[y][x] = self.player
                coords = self.check_conditions()
                self.player = int(not self.player)
            return coords

    def game(self):
        self.screen.fill((16, 16, 16))
        self.draw_board()
        pg.display.update()
        while self.run:
            for event in pg.event.get():

                if self.whoiswho[self.player] == 'H' and event.type == pg.MOUSEBUTTONUP:
                    pos = pg.mouse.get_pos()
                    coords = self.update_board(pos)

                elif self.whoiswho[self.player] == 'AI':
                    node = Node(self.board, self.player)
                    minimax(node, 4, True)
                    if self.player == 0:
                        child = self.choose_next_AI_step(float("inf"), lambda x, y: x < y, node)
                    elif self.player == 1:
                        child = self.choose_next_AI_step(float("-inf"), lambda x, y: x > y, node)
                    self.board = child.current_board
                    coords = self.check_conditions()
                    self.player = int(not self.player)

                if self.result is not None:
                    if coords != []:
                        pg.draw.line(self.screen, (255, 0, 0), coords[0], coords[1], 10)
                    pg.display.update()
                    self.end_game()

                if event.type == pg.QUIT:
                    self.run = False
                self.draw_movements()
                pg.display.update()
        pg.quit()

tic = Graphic()



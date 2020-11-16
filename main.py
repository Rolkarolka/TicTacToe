
from numpy import random
import pygame as pg
from graphic import Graphic
from node import Node, minimax

class TicTacToe(Graphic):
    def __init__(self):
        pg.init()
        pg.display.set_caption("TicTacToe")
        self.WIDTH = 600
        self.HEIGHT = self.WIDTH
        self.screen = pg.display.set_mode((self.WIDTH, self.HEIGHT))
        self.board = [[None for i in range(3)] for i in range(3)]
        Graphic.__init__(self, self.screen, self.board)
        self.player = 1     # x = 1,  o = 0
        self.run = True
        self.result = None
        self.whoiswho = {}
        self.begin_screen()
        self.game()

    def begin_screen(self):
        self.draw_begin_screen()
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

    def find_fild(self, coord):     # find index in Graphic.fields_start based on mouse position
        if coord < self.WIDTH // 3:
            return 0
        elif coord < self.WIDTH // 3 * 2:
            return 1
        else:
            return 2

    def update_board(self, pos):    # update board after player movement
        y = self.find_fild(pos[1])
        x = self.find_fild(pos[0])
        coords = None
        if self.board[y][x] is None:
            self.board[y][x] = self.player
            coords, player = self.check_conditions(int(self.player), self.board)
            self.result = player
            self.player = int(not self.player)
        return coords

    def check_conditions(self, player, board):
        # form a horizontal line
        for x_row in board:
            if all([x is player for x in x_row]):
                y = self.fields_start[board.index(x_row)][0][1] + self.HEIGHT // 6
                return [(0, y), (self.WIDTH, y)], player
        # form a vertical line
        for i in range(len(board[0])):
            if all([x[i] is player for x in board]):
                x = self.fields_start[0][i][0] + self.WIDTH // 6
                return [(x, 0), (x, self.HEIGHT)], player
        # form a diagonal line from the upper-left to the lower-right corner
        if all([board[i][i] is player for i in range(len(board))]):
            return [(0, 0), (self.WIDTH, self.HEIGHT)], player
        # form a diagonal line from the lower-left to the upper-right corner
        if all([board[i][2 - i] is player for i in range(2, -1, -1)]):
            return [(0, self.HEIGHT), (self.WIDTH, 0)], player
        # if draw
        if all([all([x[i] is not None for i in range(len(board))]) for x in board]):
            return [], 'Tie'
        return [], None

    def choose_next_AI_step(self, optimal_move, node):  # choose best movement for AI
        children = []
        terminal = []
        for child in node.children:
            if child.terminal is True:
                terminal.append(child)
            if child.heuristic == optimal_move:
                children.append(child)
        if len(terminal) > 0:
            child = random.choice(terminal)
        else:
            child = random.choice(children)
        return child

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
                    node = Node(self.board, self.player, self.check_conditions)
                    next_move = minimax(node, 4, True)
                    child = self.choose_next_AI_step(next_move, node)
                    self.board = child.current_board
                    coords, player = self.check_conditions(int(self.player), self.board)
                    self.result = player
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
    
    def end_game(self):
        self.draw_movements()
        pg.display.update()
        pg.time.delay(3000)
        pg.quit()

tic = TicTacToe()
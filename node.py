from copy import deepcopy

class Node:
    # min player - o, max player - x
    def __init__(self, board, player, function, terminal=False):
        self.current_board = board
        self.config_matrix = [[3, 2, 3], [2, 4, 2], [3, 2, 3]]
        self.heuristic = None
        self.children = []
        self.player = int(player)
        self.terminal = terminal
        self.function = function
        self.set_children()

    def calc_heuristic(self):   # calculate heuristic based on current board
        result = 0
        if self.terminal is True:
            if int(not self.player) == 0:
                result = -100
            elif int(not self.player) == 1:
                result = 100
        for x in range(len(self.current_board)):
            for y in range(len(self.current_board[x])):
                if self.current_board[x][y] == 0:
                    result -= self.config_matrix[x][y]
                if self.current_board[x][y] == 1:
                    result += self.config_matrix[x][y]
        return result

    def set_children(self):     # set children for current node
        if not self.terminal:
            for x in range(len(self.current_board)):
                for y in range(len(self.current_board[x])):
                    if self.current_board[x][y] is None:
                        board = deepcopy(self.current_board)
                        board[x][y] = int(self.player)
                        terminal = False
                        coords, result = self.function(int(self.player), board)
                        if result is not None and result != 'Tie':
                            terminal = True
                        self.children.append(Node(board, int(not self.player), self.function, terminal))


def minimax(node, depth, maximizingPlayer):     # create game tree
    if depth == 0 or node.terminal:
        node.heuristic = node.calc_heuristic()
        return node.heuristic 

    if maximizingPlayer:
        max_value = float('-inf')
        for child in node.children:
            value = minimax(child, depth - 1, False)
            max_value = max(max_value, value)
        node.heuristic = max_value
        return max_value
    else:
        min_value = float('inf')
        for child in node.children:
            value = minimax(child, depth - 1, True)
            min_value = min(min_value, value)
        node.heuristic = min_value
        return min_value

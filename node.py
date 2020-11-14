from copy import deepcopy

class Node:
    # min player - o, max player - x
    def __init__(self, board, player, function):
        self.current_board = board
        self.config_matrix = [[3, 2, 3], [2, 4, 2], [3, 2, 3]]
        self.heuristic = self.calc_heuristic()
        self.children = []
        self.player = int(player)
        self.terminal = False
        self.function = function
        coords, result = function(int(not self.player), self.current_board) 
        if result is not None:
            self.terminal = True

    def calc_heuristic(self):   # calculate heuristic based on current board
        result = 0
        for x in range(len(self.current_board)):
            for y in range(len(self.current_board[x])):
                if self.current_board[x][y] == 0:
                    result -= self.config_matrix[x][y]
                if self.current_board[x][y] == 1:
                    result += self.config_matrix[x][y]
        return result

    def set_children(self):     # set children for current node
        for x in range(len(self.current_board)):
            for y in range(len(self.current_board[x])):
                if self.current_board[x][y] is None:
                    board = deepcopy(self.current_board)
                    board[x][y] = int(self.player)
                    self.children.append(Node(board, int(not self.player), self.function))
        if self.children == []:
            self.terminal = True


def minimax(node, depth, maximizingPlayer):     # create game tree
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

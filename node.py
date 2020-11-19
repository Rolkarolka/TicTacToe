from copy import deepcopy

class Node:
    # min player - o, max player - x
    def __init__(self, board, player, function, win=False):
        self.current_board = board
        self.player = int(player)
        self.win = win
        self.function = function
        self.config_matrix = [[3, 2, 3], [2, 4, 2], [3, 2, 3]]
        self.children = []
        self.set_children()
        self.heuristic = self.calc_heuristic()

    def calc_heuristic(self):   # calculate heuristic based on current board
        result = 0
        if self.win:
            if self.player:
                result = -25
            else:
                result = 25
        else:
            for x in range(len(self.current_board)):
                for y in range(len(self.current_board[x])):
                    if self.current_board[x][y] == 0:
                        result -= self.config_matrix[x][y]
                    if self.current_board[x][y] == 1:
                        result += self.config_matrix[x][y]
        return result

    def set_children(self):     # set children for current node
        if not self.win:
            for x in range(len(self.current_board)):
                for y in range(len(self.current_board[x])):
                    if self.current_board[x][y] is None:
                        win = False
                        board = deepcopy(self.current_board)
                        board[x][y] = int(self.player)
                        coords, result = self.function(int(self.player), board) 
                        if result is not None:
                            if result == 'Tie':
                                win = None
                            else:
                                win = True
                            
                        self.children.append(Node(board, int(not self.player), self.function, win))

def minimax(node, depth, maximizingPlayer):     # create game tree
    if depth == 0 or node.win:
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

from random import choice
from copy import deepcopy, copy
from node import Node
from time import process_time, time
from math import sqrt
from sys import maxsize
import numpy
from collections import deque

USER = 'user'
PROGRAM = 'program'

RANDOM = 'random'
MINIMAX = 'minimax'
MCTS = 'mcts'

WIN = 1
LOSS = -1

INF = maxsize


class User(object) :
    def __init__(self, colour, row, column, max_row, max_column, mode):
        self.row = row
        self.column = column
        self.colour = colour

        self.mode = mode

        self.direction = ''

        self.max_row = max_row - 1
        self.max_column = max_column - 1
    
    def manhattan_distance(self, r1, c1, r2, c2):
        return abs(r1 - r2) + abs(c1 - c2)
    
    def get_possible_moves(self, grid, player = None):
        if player == None:
            player = self
        possible_moves = []
        # left
        if not player.check_crash(grid, player.row, player.column - 1):
            possible_moves.append({'row': player.row, 'column': player.column - 1, 'direction': 'left'})
        # right 
        if not player.check_crash(grid, player.row, player.column + 1):
            possible_moves.append({'row': player.row, 'column': player.column + 1, 'direction': 'right'})
        # up
        if not player.check_crash(grid, player.row + 1, player.column):
            possible_moves.append({'row': player.row + 1, 'column': player.column, 'direction': 'up'})
        # down
        if not player.check_crash(grid, player.row - 1, player.column):
            possible_moves.append({'row': player.row - 1, 'column': player.column, 'direction': 'down'})

        return possible_moves
    
    def get_all_moves(self, player):
        possible_moves = []
        # left
        if player.column - 1 > 0 and player.column - 1 < player.max_column:
            possible_moves.append({'row': player.row, 'column': player.column - 1, 'direction': 'left'})
        # right
        if player.column + 1 > 0 and player.column + 1 < player.max_column:
            possible_moves.append({'row': player.row, 'column': player.column + 1, 'direction': 'right'})
        # up
        if player.row + 1 > 0 and player.row + 1 < player.max_row:
            possible_moves.append({'row': player.row + 1, 'column': player.column, 'direction': 'up'})
        # down
        if player.row - 1 > 0 and player.row - 1 < player.max_row:
            possible_moves.append({'row': player.row - 1, 'column': player.column, 'direction': 'down'})

        return possible_moves

    def valid_direction(self, direction):
        if self.direction == 'left' and direction == 'right':
            return False
        if self.direction == 'right' and direction == 'left':
            return False
        if self.direction == 'up' and direction == 'down':
            return False
        if self.direction == 'down' and direction == 'up':
            return False
        return True

    def check_crash(self, grid, row, column):
        return self.row <= 0 or self.column <= 0 or self.row >= self.max_row or self.column >= self.max_column or grid[row][column] != 0

    def random(self, grid):
        moves = self.get_possible_moves(grid, self)
        if (len(moves) != 0):
            self.direction = choice(moves)["direction"]
    
    def dijkstra(self, grid, agent):
        # copy agent row and cloumn values
        hr = agent.row
        hc = agent.column
        # create array to store distances
        distances = numpy.zeros((agent.max_row + 1, agent.max_column + 1))
        # fill all elements with INF (sys.inf)
        distances[:] = INF
        # create array to keep track of visited cells
        visited = numpy.zeros((agent.max_row + 1, agent.max_column + 1))
        # set distance to head as 0
        distances[hr, hc] = 0
        # make head visited
        visited[hr, hc] = 1
        # get all valid neighbours
        neighbours = agent.get_possible_moves(grid, agent)
        for n in neighbours:
            # make distance to neighbour 1
            distances[n["row"], n["column"]] = 1
            # create Deque with neighbours
        q = deque(agent.get_possible_moves(grid, agent))
        while len(q) != 0:
            # get leftmot value
            val = q.popleft()
            current_row = val["row"]
            current_column = val["column"]
            agent.row = current_row
            agent.column = current_column
            # increment distance
            ndist = distances[current_row, current_column] + 1
            # get all valid neighbours
            for n in agent.get_possible_moves(grid, agent):
                neighbour_row = n["row"]
                neighbour_column = n["column"]
                if grid[neighbour_row][neighbour_column] != 0:
                    continue
                # check if distance is greater than distance to parent
                if ndist < distances[neighbour_row, neighbour_column]:
                    distances[neighbour_row, neighbour_column] = ndist
                # append cell to Deque if not visited and set visted to 1
                if visited[neighbour_row, neighbour_column] == 0:
                    q.append(n)
                    visited[neighbour_row, neighbour_column] = 1
        agent.row = hr
        agent.column = hc
        return distances
    
    def voronoi(self, player, enemy, grid):
        # start = time()
        player_cells = 0
        enemy_cells = 0
        # get cost to move to each cell in grid (uses Dijkstra's algorithm)
        player_heuristic_values = self.dijkstra(grid, player)
        enemy_heuristic_values = self.dijkstra(grid, enemy)
        for row in range(1, self.max_row):
            for column in range(1, self.max_column):
                player_heuristic = player_heuristic_values[row, column]
                enemy_heuristic = enemy_heuristic_values[row, column]
                # check if cell is equidistant to player and enemy
                if player_heuristic < 10e5 and player_heuristic == enemy_heuristic:
                    continue
                # check if cell is closer to player
                elif player_heuristic < enemy_heuristic:
                    player_cells += 1
                # or enemy
                elif enemy_heuristic < player_heuristic:
                    enemy_cells +=1
        # print(time() - start)
        return (player_cells - enemy_cells) / (self.max_row * self.max_column)

    def minimax(self, enemy, grid, max_depth):
        best_score = LOSS
        best_move = self.direction
        depth = 0

        for move in self.get_possible_moves(grid, self):
            # if self.valid_direction(move["direction"]) and not self.check_crash(grid, move["row"], move["column"]):
            if self.valid_direction(move["direction"]):
                # copy values of Grid and player
                temp_direction = self.direction
                temp_row = self.row
                temp_column = self.column
                # change values
                grid[move["row"]][move["column"]] = self.colour
                self.direction = move["direction"]
                self.row = move["row"]
                self.column = move["column"]
                # call maxmin to get score
                score = self.maxmin(self, enemy, grid, depth, max_depth, best_score, WIN, False)
                # revert changes
                grid[move["row"]][move["column"]] = 0
                self.row = temp_row
                self.column = temp_column
                self.direction = temp_direction
                # check if score is better than best score and change best_score
                if score > best_score:
                    best_score = score
                    best_move = move["direction"]
                if best_score >= WIN: break
        
        self.direction = best_move

    def maxmin(self, player, enemy, grid, depth, max_depth, alpha, beta, maxing):
        # check if max depth is reached
        if depth == max_depth:
            return self.voronoi(player, enemy, grid)

        if maxing:
            # go through all possible moves
            for move in player.get_possible_moves(grid, player):
                if player.valid_direction(move["direction"]):
                    # copy values of Grid and players 
                    temp_row = player.row
                    temp_column = player.column
                    temp_direction = player.direction
                    # change values
                    grid[move["row"]][move["column"]] = player.colour
                    player.direction = move["direction"]
                    player.row = move["row"]
                    player.column = move["column"]
                    # get max value of best_score and result from maxmin
                    temp_score = player.maxmin(player, enemy, grid, depth, max_depth, alpha, beta, False)
                    # revert changes
                    grid[move["row"]][move["column"]] = 0
                    player.row = temp_row
                    player.column = temp_column
                    player.direction = temp_direction
                    # check if aplha is greater than temp score
                    if alpha >= temp_score: break
                    alpha = max(alpha, temp_score)
            return alpha
        else:
            # go through all possible moves
            for move in enemy.get_possible_moves(grid, enemy):
                if enemy.valid_direction(move["direction"]): 
                    # copy values of Grid and players
                    temp_direction = enemy.direction
                    temp_row = enemy.row
                    temp_column = enemy.column
                    # change values
                    grid[move["row"]][move["column"]] = enemy.colour
                    enemy.direction = move["direction"]
                    enemy.row = move["row"]
                    enemy.column = move["column"]
                    # get min value of best_score and result from maxmin
                    temp_score = enemy.maxmin(player, enemy, grid, depth + 1, max_depth, alpha, beta, True)
                    # revert changes
                    grid[move["row"]][move["column"]] = 0
                    enemy.row = temp_row
                    enemy.column = temp_column
                    enemy.direction = temp_direction
                    # check if beta is less than temp_score
                    if beta <= temp_score: break
                    beta = min(beta, temp_score)
            return beta

    def monte_carlo_tree_search(self, grid, enemy, time_limit):
        start = time()
        root_node = Node((self.row, self.column, self.direction), None)
        while time() - start <= time_limit:
            cloned_grid = deepcopy(grid)
            cloned_player = deepcopy(self)
            cloned_enemy = deepcopy(enemy)
            node = cloned_player.select(cloned_grid, root_node, cloned_player)
            outcome = cloned_player.roll_out(cloned_grid, cloned_player, cloned_enemy, time_limit)
            cloned_player.back_propogate(node, outcome)

        if len(root_node.children.values()) != 0:
            max_value = max(root_node.children.values(), key=lambda n: n.n).n
            max_nodes = [n for n in root_node.children.values() if n.n == max_value]
            best_child = choice(max_nodes)

            best_move = best_child.cell[2]
            self.direction = best_move

    def select(self, grid, node, current_player):
        while len(node.children) != 0:
            max_uct = max(node.children.values(), key=lambda n: n.calculate_value(sqrt(20))).calculate_value(sqrt(20))

            max_nodes = [n for n in node.children.values() if n.calculate_value(sqrt(20)) == max_uct]

            node = choice(max_nodes)

            if not current_player.check_crash(grid, node.cell[0], node.cell[1]):
                grid[node.cell[0]][node.cell[1]] = current_player.colour
                current_player.row = node.cell[0]
                current_player.column = node.cell[1]

                if node.n == 0:
                    return node
                
        if self.expand(node, grid, current_player):
            node = choice(list(node.children.values()))
            grid[node.cell[0]][node.cell[1]] = current_player.colour
            current_player.row = node.cell[0]
            current_player.column = node.cell[1]
        
        return node
        
    def expand(self, parent, grid, current_player):
        if len(current_player.get_possible_moves(grid, current_player)) != 0:
            cells = [Node((move["row"], move["column"], move["direction"]), parent) for move in current_player.get_possible_moves(grid, current_player)]
            parent.add_children(cells)
            return True
        return False

    def roll_out(self, grid, player, enemy, time_limit):
        game_over = False
        outcome = 0
        turn = PROGRAM

        start = time()
        while not game_over and (time() - start <= time_limit):
            if (turn == PROGRAM):
                if len(player.get_all_moves(player)) > 0:
                    move = choice(player.get_all_moves(player))
                    if not player.check_crash(grid, move["row"], move["column"]):
                        player.row = move["row"]
                        player.column = move["column"]
                        grid[move["row"]][move["column"]] = player.colour
                        turn = USER
                    else:
                        game_over = True
                        outcome = -1
                else:
                    game_over = True
                    outcome = -1
            else:
                if len(enemy.get_all_moves(enemy)) > 0:
                    move = choice(enemy.get_all_moves(enemy))
                    if not enemy.check_crash(grid, move["row"], move["column"]):
                        enemy.row = move["row"]
                        enemy.column = move["column"]
                        grid[move["row"]][move["column"]] = enemy.colour
                        turn = PROGRAM
                    else:
                        game_over = True
                        outcome = 1
                else:
                    game_over = True
                    outcome = 1
        return outcome
    
    def back_propogate(self, node, outcome):
        while node is not None:
            node.n += 1
            node.q += outcome
            node = node.parent

    def update(self, enemy, grid, direction):
        if self.mode == 'user':
            if direction != '' or direction != self.direction:
                if self.valid_direction(direction):
                    self.direction = direction
        elif self.mode == 'random':
            self.random(grid)
        elif self.mode == MINIMAX:
            # start = time()
            self.minimax(enemy, grid, 2)
            # print(str(time() - start) + ",")
        elif self.mode == MCTS:
            # start = time()
            self.monte_carlo_tree_search(grid, enemy, 0.5)
            # print(str(time() - start) + ",")


        crash = False
        
        if self.direction != '':
            if self.direction == 'left':
                if not self.check_crash(grid, self.row, self.column - 1):
                    self.column -= 1
                else:
                    crash = True
            if self.direction == 'right':
                if not self.check_crash(grid, self.row, self.column + 1):
                    self.column += 1
                else:
                    crash = True
            if self.direction == 'down':
                if not self.check_crash(grid, self.row - 1, self.column):
                    self.row -= 1
                else:
                    crash = True
            if self.direction == 'up':
                if not self.check_crash(grid, self.row + 1, self.column):
                    self.row += 1
                else:
                    crash = True
        # set user's current location in grid to user's colour
        grid[self.row][self.column] = self.colour
        return crash

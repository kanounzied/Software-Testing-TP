from node import Node
import numpy as np
import math


def get_value_coordinates_in_goal(value: int, size: int):
    matrix = np.array(range(size * size)).reshape(size, size)
    for i in range(size):
        for j in range(size):
            if matrix[i][j] == value:
                return i, j


class TreeSearch:
    open = np.array([])
    closed = {}
    goal_dict = {}
    algorithms_result = {
        "bfs": 0,
        "dfs": 0,
        "iterative-dfs": 0,
        "a-etoile": 0
    }

    def __init__(self, size: int):
        for i in range(size * size):
            self.goal_dict[i] = get_value_coordinates_in_goal(i, size)

    def bfs_search(self, node: Node):
        self.closed = {}
        self.closed[node.board.state.state_matrix_id_gen()] = "root"
        self.open = np.array([
            {
                "parent": "tree",
                "node": node
            }
        ])
        while not self.open[0]["node"].board.state.isFinal:
            print("queue length: ", len(self.open))  # nodes queue
            head = self.open[0]["node"]
            print("board: ")
            head.board.afficher_pieces()
            # if head.board.state.isFinal:
            #     break
            direction_states = self.remove_redondant_nodes(head)  # children array
            self.open = np.delete(self.open, 0)
            self.open = np.append(self.open, direction_states)
        print("taquin solved: ")
        # self.open[0]["node"].board.afficher_pieces()
        solution_path_length = self.find_solution_path(algo="bfs")
        return solution_path_length

    def dfs_search(self, node: Node):
        self.closed = {}
        # ========  5edmet zied

        self.closed[node.board.state.state_matrix_id_gen()] = "root"
        self.open = np.array([
            {
                "parent": "tree",
                "node": node
            }
        ])
        while not self.open[0]["node"].board.state.isFinal:
            print("queue length: ", len(self.open))  # nodes queue
            head = self.open[0]["node"]
            print("board: ")
            head.board.afficher_pieces()
            # if head.board.state.isFinal:
            #     break
            direction_states = self.remove_redondant_nodes(head)
            self.open = np.delete(self.open, 0)
            self.open = np.append(direction_states, self.open)
        print("taquin solved: ")
        solution_path_length = self.find_solution_path(algo="dfs")
        return solution_path_length


    def dfs_iterative_search(self, node: Node):
        self.closed = {}
        level = 0
        self.closed[node.board.state.state_matrix_id_gen()] = "root"
        self.open = np.array([{
            "level": level,
            "node": node,
            "parent": "root"
        }])
        index = 0
        while not self.open[index]["node"].board.state.isFinal:
            print("============== level: ", level, " =================")
            index = 0
            children = self.get_leveled_children(self.open[index])
            self.open = np.append(children, self.open)

            while self.open[-1]["node"] != self.open[index]["node"]:  # index != len(self.open)
                self.open[index]["node"].board.afficher_pieces()
                head = self.open[index]
                if head["node"].board.state.isFinal:
                    break
                if head["level"] < level:
                    children = self.get_leveled_children(head)
                    self.open = np.delete(self.open, index)
                    self.open = np.insert(self.open, index, children)
                else:
                    index += 1
            print("break in while!!!!")
            level += 1
        solution_path_length = self.find_solution_path(index, algo="iterative-dfs")
        return solution_path_length

    def remove_redondant_nodes(self, head: Node):
        nodes = [head.left, head.right, head.up, head.down]
        final_list = []
        for node in nodes:
            if self.closed.get(node.board.state.state_matrix_id_gen()) is None:
                node.cost += 1 + head.cost
                final_list.append(
                    {
                        "parent": head.board.state.state_matrix_id_gen(),
                        "node": node
                    }
                )
                self.closed[node.board.state.state_matrix_id_gen()] = head.board.state.state_matrix_id_gen()
        return final_list

    # this function is for iterative dfs
    def get_leveled_children(self, head):
        nodes = [head["node"].left, head["node"].right, head["node"].up, head["node"].down]
        final_list = []
        for node in nodes:
            if self.closed.get(node.board.state.state_matrix_id_gen()) is None:
                final_list.append(
                    {
                        "parent": head["node"].board.state.state_matrix_id_gen(),
                        "level": head["level"] + 1,
                        "node": node
                    }
                )
                self.closed[node.board.state.state_matrix_id_gen()] = head["node"].board.state.state_matrix_id_gen()
        return final_list

    # this is an old version of remove redondant nodes
    def remove_redondant_nodes_safe_copy(self, head: Node):
        nodes = [head.left, head.right, head.up, head.down]
        final_list = []
        for i in nodes:
            if self.closed.get(i.board.state.state_matrix_id_gen()) is None:
                final_list.append(i)
                self.closed[i.board.state.state_matrix_id_gen()] = True
        return final_list

    def find_solution_path(self, index=0, parent_id="", solution_node=None, algo=""):
        # parent id
        if parent_id == "":
            parent = self.open[index]["parent"]
        else:
            parent = parent_id

        # put solution node in solution array
        if solution_node is None:
            solution_node = self.open[index]["node"]
        solution_path = np.array([solution_node.board.state.state_matrix_id_gen()])
        while parent != "root":
            solution_path = np.append(parent, solution_path)
            parent = self.closed[parent]

        # solution_path = np.append(parent, solution_path)
        print("solution found in ", len(solution_path), " steps!")
        self.algorithms_result[algo] = len(solution_path)
        for sol in solution_path:
            self.string_to_matrix(sol)

        return len(solution_path)

    def string_to_matrix(self, s):
        size = int(math.sqrt(len(s)))
        matrix = np.empty((size, size), dtype=str)
        for i in range(len(s)):
            if s[i] != '0':
                matrix[i // size][i % size] = s[i]
            else:
                matrix[i // size][i % size] = ' '

        s = [[str(e) for e in row] for row in matrix]
        lens = [max(map(len, col)) for col in zip(*s)]
        fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
        table = [fmt.format(*row) for row in s]
        print('--------')
        print('\n'.join(table))

    # we suppose all costs are = 1 so f(n) = h(n)
    def a_etoile(self, node: Node, heuristique):
        self.closed = {}
        self.closed = {node.board.state.state_matrix_id_gen(): "root"}
        indice_min = heuristique(node.board.get_matrix_numbers())
        node.cost = 1
        self.open = {
            indice_min: np.array([
                {
                    "parent": "tree",
                    "node": node
                }
            ])
        }
        while not self.open[indice_min][0]["node"].board.state.isFinal:
            head = self.open[indice_min][0]["node"]
            # print("board: ")
            # head.board.afficher_pieces()
            if head.board.state.isFinal:
                break
            direction_states = self.remove_redondant_nodes(head)

            if len(self.open[indice_min]) == 1:
                self.open.pop(indice_min)
            else:
                self.open[indice_min] = np.delete(self.open[indice_min], 0)

            for child in direction_states:
                indice_child = heuristique(child["node"].board.get_matrix_numbers()) + child["node"].cost
                if indice_child not in self.open:
                    self.open[indice_child] = np.array([])
                self.open[indice_child] = \
                    np.append(
                        self.open[indice_child],
                        child,
                    )
                if indice_child < indice_min:
                    indice_min = indice_child
            while indice_min not in self.open:
                indice_min += 1
                # print(indice_min)
            # print("taquin solved: ")
        solution_path_length = self.find_solution_path(
            parent_id=self.open[indice_min][0]["parent"],
            solution_node=self.open[indice_min][0]["node"],
            algo="a-etoile"
        )
        return solution_path_length

    def heuristique_mahattan(self, matrix):
        sum = 0
        size = int(len(matrix))
        for i in range(size):
            for j in range(size):
                sum += abs(self.goal_dict[matrix[i][j]][0] - i) + abs(self.goal_dict[matrix[i][j]][1] - j)
        return sum

    def missplaced_pieces_heuristic(self, matrix):
        sum = 0
        size = int(len(matrix))
        for i in range(size):
            for j in range(size):
                piece = matrix[i][j]
                # compare x coordinates and y coordinates
                if self.goal_dict.get(piece)[0] != i or self.goal_dict.get(piece)[1] != j:
                    sum += 1
        return sum
import pandas as pd
import matplotlib.pyplot as plt

from tree_search import TreeSearch
from board import Board
from node import Node


def plot_a_star_heuristics_results(manhattan_results, miss_placed_pieces_results):
    comp_list = [[manhattan_results[i], miss_placed_pieces_results[i]] for i in range(len(manhattan_results))]
    comp_df = pd.DataFrame(comp_list, columns=['mahattan_heuristic', 'miss_placed_pieces_heuristic'])
    comp_df['number_of_essay'] = comp_df.index

    fig, ax = plt.subplots(figsize=[9, 7])
    ax.plot(comp_df['number_of_essay'], comp_df['mahattan_heuristic'], label="Mahattan Heuristic",
            marker='o', linewidth=2
            )
    ax.plot(comp_df['number_of_essay'], comp_df['miss_placed_pieces_heuristic'], label="Miss Placed Pieces Heuristic",
            marker='o', linewidth=2
            )
    ax.set_xlabel('Number Of Visited Nodes')
    ax.set_ylabel('Number of Moves')
    plt.title('Comparison Between Manhattan and Miss Placed Pieces Heuristics')
    plt.legend()
    plt.savefig('./heuristics_comp.png')
    plt.show()


def compare_a_star_heuristics(n):
    tree_search = TreeSearch(int(n))
    SEED_NUMBER = 10
    manhattan_results = []
    miss_placed_pieces_results = []
    for i in range(SEED_NUMBER):
        board = Board(int(n))
        node = Node(board)
        manhattan_results.append(tree_search.a_etoile(node, tree_search.heuristique_mahattan))
        miss_placed_pieces_results.append(tree_search.a_etoile(node, tree_search.missplaced_pieces_heuristic))
    print(manhattan_results)
    plot_a_star_heuristics_results(manhattan_results, miss_placed_pieces_results)


def compare_all_algorithms(n):
    fig, ax = plt.subplots(figsize=[9, 7])
    board = Board(int(n))
    node = Node(board)
    tree_search = TreeSearch(int(n))
    algorithms = ['Iterative DFS', 'BFS', 'A* (Miss placed)', 'A* (Manhattan)']
    results = []
    # results.append(tree_search.dfs_search(node))
    results.append(tree_search.dfs_iterative_search(node))
    results.append(tree_search.bfs_search(node))
    results.append(tree_search.a_etoile(node, tree_search.missplaced_pieces_heuristic))
    results.append(tree_search.a_etoile(node, tree_search.heuristique_mahattan))
    ax.bar(algorithms, results)
    ax.set_xlabel('Algorithms')
    ax.set_ylabel('Number of Steps')
    plt.title('Comparison Between Different Search Algorithms')
    plt.legend()
    plt.savefig('./all_algos_comp2.png')
    plt.show()

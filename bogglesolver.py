# Boggle solver takes in list of 16 words and outputs all the 4+ letter words that can be made
from time import time
from typing import Dict, List


letters = ["S", "A", "N", "B", "E", "I", "W", "A", "N", "K", "O", "R", "T", "N", "H", "D"]


class Graph:
    """Stripped back version of a mathematical graph."""

    def __init__(self, data: Dict[int, List[int]]):
        self.graph = data

    @classmethod
    def create_blank(cls, width: int = 4, height: int = 4):
        return cls({n: cls.get_adjacent_nodes(n, width, height) for n in range(width * height)})

    @staticmethod
    def get_adjacent_nodes(node: int, width: int, height: int):
        x = node % width
        y = node // height
        adjacent = []
        for i in (-1, 0, 1):
            for j in (-1, 0, 1):
                if i != 0 or j != 0:
                    if x + i in range(width) and y + j in range(height):
                        adjacent.append(x + i + width * (y + j))
        return adjacent

    def remove_node(self, node: int):
        new_graph = dict(self.graph)
        for other_node in new_graph[node]:
            new_adjacent = self.graph[other_node][:]
            try:
                new_adjacent.remove(node)
            except ValueError:
                ...
            new_graph[other_node] = new_adjacent
        new_graph[node] = []
        return new_graph

    def __str__(self):
        return "\n".join([(k, v) for k, v in self.graph.items()])


class BoggleSolver:
    with open("words.txt") as file:
        DICTIONARY = file.read().splitlines()

    def __init__(self, letters):
        self.letters_lookup = {i: letters[i] for i in range(16)}
        self.words = set()
        self.subgraphs = []

    def find_words(self, graph=None, path=None, current_node=None):
        if current_node is None:
            for node in range(16):
                self.find_words(self.create_blank_graph(), [node], node)
        else:
            if self.check_path_valid(path):
                for new_node in graph[current_node]:
                    self.find_words(
                        self.remove_node(graph, current_node),
                        path + [new_node],
                        new_node,
                    )

    def check_path_valid(self, path):
        word = "".join(self.letters_lookup[letter] for letter in path)
        if word in self.DICTIONARY:
            if word not in self.words:
                print(word)
            self.words.add(word)

        if any(word in w for w in self.DICTIONARY):
            return True
        return False


if __name__ == "__main__":
    g = Graph.create_blank()
    g.remove_node(3)
    print(g)
    # bs = BoggleSolver(letters)
    # time_start = time()
    # bs.find_words()
    # print(bs.words)
    # print(f"Took {time()-time_start} seconds to execute")

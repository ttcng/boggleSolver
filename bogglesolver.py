# Boggle solver takes in list of 16 words and outputs all the 4+ letter words that can be made

from __future__ import annotations

from time import time
from typing import Dict, List, Optional


letters = ["S", "A", "N", "B", "E", "I", "W", "A", "N", "K", "O", "R", "T", "N", "H", "D"]
letters2 = ["C", "O", "M", "P", "M", "T", "R", "A", "E", "N", "T", "A", "E", "S", "I", "L"]
letters3 = [l for l in "URSNLHAKMSBONRET"]
letters4 = ['Y', 'U', 'D', 'K', 'E', 'O', 'Y', 'E', 'T', 'N', 'S', 'G', 'I', 'A', 'O', 'H']

class Graph:
    """Stripped back version of a mathematical graph."""

    def __init__(self, data: Dict[int, List[int]]):
        """Creates instance of Graph class"""
        self.graph = data

    @classmethod
    def create_blank(cls, width: int = 4, height: int = 4):
        """Creates blank graph with width x height nodes in a grid shape"""
        return cls({n: cls.get_adjacent_nodes(n, width, height) for n in range(width * height)})

    @staticmethod
    def get_adjacent_nodes(node: int, width: int, height: int) -> List[int]:
        """Gets all adjacent nodes of one particular node on the grid graph"""
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
        """Returns a new instance of the class with"""
        new_graph = dict(self.graph)
        for other_node in new_graph[node]:
            new_adjacent = self.graph[other_node][:]
            try:
                new_adjacent.remove(node)
            except ValueError:
                ...
            new_graph[other_node] = new_adjacent
        new_graph[node] = []
        return Graph(new_graph)

    def get(self, node: int):
        """Gets a particular node of the graph"""
        return self.graph.get(node)

    def __str__(self):
        """Displays graph nicely"""
        return "\n".join([str((k, v)) for k, v in self.graph.items()])


class BoggleSolver:
    """Boggle solver takes a list of letters and returns a list of all valid 4+ letter words"""

    # Loads list of all valid words from file
    with open("words.txt") as file:
        DICTIONARY = set(file.read().splitlines())

    # Loads lists of all potential word beginnings of length n from file
    BEGINNING = {}
    for i in range(1, 16):
        with open(f"beginning{i}.txt") as file:
            BEGINNING[i] = set(file.read().splitlines())

    def __init__(self, letters):
        """Create instance of BoggleSolver"""
        self.letters_lookup = {i: letters[i] for i in range(16)}
        self.words = set()

    def find_words(self, graph: Optional[Graph] = None, path=None):
        """
        Recursive function finds all potential paths through the graph. Arguments:
        graph: the graph to find paths through
        path: the current path that has been found
        """
        if graph is None:
            for node in range(16):
                self.find_words(Graph.create_blank(), [node])
        else:
            if self.check_path_valid(path):
                for new_node in graph.get(path[-1]):
                    self.find_words(graph.remove_node(path[-1]), path + [new_node])

    def check_path_valid(self, path):
        """
        Checks that a current path is either a valid word or is the start of a valid word.
        """
        word = "".join(self.letters_lookup[letter] for letter in path)
        if word in self.DICTIONARY:
            self.words.add(word)
        if len(word) >= 14:
            print(word)
        if len(word) <= 15:
            return word in self.BEGINNING[len(word)]


if __name__ == "__main__":
    bs = BoggleSolver(letters4)
    time_start = time()
    bs.find_words()
    print(bs.words)
    print(f"Took {time()-time_start} seconds to execute")

# 65.57435822486877
# 65.62787389755249
# 60.21643900871277
# 6.654704809188843
# 0.009509801864624

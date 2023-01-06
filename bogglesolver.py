# Boggle solver takes in list of 16 words and outputs all the 4+ letter words that can be made
from typing import Dict


letters = [
    'S', 'A', 'N', 'B', 
    'E', 'I', 'W', 'A', 
    'N', 'K', 'O', 'R', 
    'T', 'N', 'H', 'D'
]


class BoggleSolver:
    with open("words.txt") as file:
        DICTIONARY = file.read().splitlines()

    def __init__(self, letters):
        self.letters_lookup = {i: letters[i] for i in range(16)}
        self.words = set()
        self.subgraphs = []
    

    @staticmethod
    def create_blank_graph() -> Dict[str, list]:
        return {node: BoggleSolver.get_adjacent_nodes(node) for node in range(16)}
    
    @staticmethod
    def get_adjacent_nodes(node: int):
        x = node % 4
        y = node // 4
        adjacent = []
        for i in (-1,0,1):
            for j in (-1,0,1):
                if (i!=0 or j!=0):
                    if x+i in range(4) and y+j in range(4):
                        adjacent.append(x+i+4*(y+j))
        return adjacent

    
    @staticmethod
    def remove_node(graph: Dict[str, list], node: int):
        new_graph = dict(graph)
        new_graph[node] = []
        for other_node in BoggleSolver.get_adjacent_nodes(node):
            new_adjacent = graph[other_node][:]
            try:
                new_adjacent.remove(node)
            except ValueError:
                ...
            new_graph[other_node] = new_adjacent
        return new_graph
    

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
    bs = BoggleSolver(letters)
    bs.find_words()
    print(bs.words)
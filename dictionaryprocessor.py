"""
Takes a raw text file and performs some processing to make it faster to search through
"""


def prune_invalid_length_words():
    with open("words.txt", "r") as file:
        words = file.read().splitlines()
        newwords = []
        for word in words:
            if len(word) in range(4, 17):
                newwords.append(word)
    with open("words.txt", "w") as file:
        file.write("\n".join(newwords))


def get_n_letter_starts(words, n):
    starts = set()
    for word in words:
        if len(word) > n:
            starts.add(word[:n])
    return list(starts)

def generate_beginning_files():
    with open("words.txt", "r") as file:
        words = file.read().splitlines()
        for n in range(1, 16):
            with open(f"beginning{n}.txt", "w") as new_file:
                new_file.write("\n".join(get_n_letter_starts(words, n)))


if __name__ == "__main__":
    
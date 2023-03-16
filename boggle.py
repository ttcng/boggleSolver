import random as r
from tkinter import *
import tkinter.ttk as ttk
from threading import Timer

DICE = [
    "EIOSST",
    "HIMNQU",
    "CIMOTU",
    "AFFKPS",
    "ACHOPS",
    "DEILRX",
    "ELRTTY",
    "AAAEGN",
    "DELRVY",
    "HLNNRZ",
    "EEINSU",
    "ABBJOO",
    "EHRTVW",
    "AOOTTW",
    "DISTTY",
    "EEGHNW",
]



def generateLetters():
    letters = []

    for die in DICE:
        letter = die[r.randint(0, 5)]
        letters.append(letter)

    r.shuffle(letters)
    print(letters)
    return letters


def encodeLetters(letters):
    encoded = ""
    for letter in letters:
        number = str(ord(letter))
        encoded = encoded + number
    return str(hex(int(encoded))[2:])


def decodeLetters(coded):
    letters = []
    dex = str(int(coded, 16))
    print(dex)
    for i in range(0, 32, 2):
        letter = str(chr(int(dex[i : i + 2])))
        letters.append(letter)
    return letters


def drawBoard(boggleBoard, letters, width, height):
    board_coords, border_size, die_width, padding, font_size, tile_border = get_dimensions(width, height)
    boggleBoard.create_rectangle(board_coords, fill = "#FF6600", width=0)
    index = 0
    for x in range(board_coords[0][0] + border_size, board_coords[1][0] - border_size, die_width + padding):
        for y in range(board_coords[0][1] + border_size, board_coords[1][1] - border_size, die_width + padding):
            boggleBoard.create_rectangle(
                x, y, x + die_width, y + die_width, fill="white", width=tile_border, outline="#883300"
            )
            if letters[index] == "Q":
                boggleBoard.create_text(
                    x + (die_width / 2),
                    y + (die_width / 2) - 5,
                    text="Qu",
                    font=("Bahnschrift", font_size-5),
                )
            else:
                boggleBoard.create_text(
                    x + (die_width / 2),
                    y + (die_width / 2) - 5,
                    text=letters[index],
                    font=("Bahnschrift", font_size),
                )

            index += 1


def get_dimensions(width, height):
    window_size = min(width, height)
    board_coords = (
        (int(width // 2 - window_size // 2 + window_size * (20/800)), int(height // 2 - window_size // 2 + window_size * (20/800))),
        (int(width // 2 + window_size // 2 - window_size * (20/800)), int(height // 2 + window_size // 2 - window_size * (20/800))),
    )
    board_size = window_size - window_size * 2 * (20/800)
    border_size = int(board_size * (75 / 800))
    die_width = int(board_size * (125 / 800))
    padding = int(board_size * (50 / 800))
    font_size = int(board_size * (70 / 800))
    tile_border = int(board_size * (3.5 / 800))
    return board_coords, border_size, die_width, padding, font_size, tile_border


def cover(boggleBoard):
    print("here")
    board_coords, border_size, die_width, padding, font_size, tile_border = get_dimensions(window.winfo_width(), window.winfo_height())
    c = boggleBoard.create_rectangle(board_coords, fill="#BBBBBB", tags="rem")
    t = boggleBoard.create_text(
        window.winfo_width()//2, window.winfo_height()//2, tags="rem", text="Click to reveal", font=("Bahnschrift", font_size)
    )
    boggleBoard.tag_bind("rem", "<ButtonPress-1>", lambda x: boggleBoard.delete("rem"))
    boggleBoard.pack(fill="both", expand=True)


def alarm(boggleBoard):
    board_coords, border_size, die_width, padding, font_size, tile_border = get_dimensions(window.winfo_width(), window.winfo_height())
    a = boggleBoard.create_text(
        min(window.winfo_width(), window.winfo_height()), min(window.winfo_width(), window.winfo_height()) * 9 / 10, text="30 seconds left!", font=("Bahnschrift", font_size//2), fill="white"
    )
    window.after(5000, lambda: boggleBoard.delete(a))


def resize_start_window(event, title, firstTime):
    if firstTime:
        window.after(10, lambda: resize_start_window(event, title, False))
    elif event.width == window.winfo_width() and event.height == window.winfo_height():
        title.config(font=("Berlin Sans FB Demi", (event.width + event.height) // 15))


def resize_board(event, board, letters, firstTime):
    if firstTime:
        window.after(10, lambda: resize_board(event, board, letters, False))
    elif event.width == window.winfo_width() and event.height == window.winfo_height():
        board.delete("all")
        drawBoard(board, letters, event.width, event.height)


def clear():
    list = window.pack_slaves()
    for l in list:
        l.destroy()


def playGame():
    window.title("Boggle Board")
    window.configure(bg="#FF6600")

    clear()

    if seed.get() == "":
        letters = generateLetters()
    else:
        letters = decodeLetters(seed.get())

    boggleBoard = Canvas(
        window,
        bg="light blue",
        width=700,
        height=700
    )
    boggleBoard.pack(fill="both", expand=True)

    window.bind("<Configure>", lambda x: resize_board(x, boggleBoard, letters, True))

    window.after(180 * 1000, lambda: cover(boggleBoard))

    window.after(150 * 1000, lambda: alarm(boggleBoard))

        


# Welcome
window = Tk()
window.title("Boggle")
window.minsize(500, 500)
window.configure(bg="Light blue")

title = Label(window, text="Boggle", font=("Berlin Sans FB Demi", 100), bg="Light blue")
title.pack(side="top", expand=True, fill="both", pady=(90, 10))

# To resize Boggle title
window.bind("<Configure>", lambda x: resize_start_window(x, title, True))


letterInput = Frame(window, bg="Light blue")
letterInput.pack(side="top", expand=True, fill="both", pady=60)

seed = StringVar()  # Text entry
ttk.Style().configure("pad.TEntry", padding="10 1 1 1")
entry = ttk.Entry(
    letterInput, width=30, font=("Bahnschrift 30"), textvariable=seed, style="pad.TEntry"
)
entry.pack(side="left", expand=True, fill="both", pady=0, padx=(50, 10))
entry.focus_set()


generator = Button(
    letterInput,
    command=lambda: seed.set(encodeLetters(generateLetters())),
    text="Generate",
    font=("Bahnschrift 25"),
)
generator.pack(side="right", expand=True, fill="both", pady=0, padx=(10, 50))


start = Button(window, text="START", font=("Bahnschrift 60"), command=playGame)
start.pack(side="top", expand=True, fill="both", pady=(0, 60), padx=(250, 250))

window.mainloop()


# print("bean awesome")

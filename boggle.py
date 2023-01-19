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


def drawBoard(window_size):
    print("resizing")
    boggleBoard.delete("all")
    border_size, die_width, padding, font_size = get_dimensions(window_size)
    index = 0
    for x in range(border_size, window_size-border_size, die_width + padding):
        for y in range(border_size, window_size-border_size, die_width + padding):
            boggleBoard.create_rectangle(
                x, y, x + die_width, y + die_width, fill="white", width=3.5, outline="#883300"
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


def get_dimensions(window_size):
    border_size = int(window_size * (75 / 800))
    die_width = int(window_size * (125 / 800))
    padding = int(window_size * (50 / 800))
    font_size = int(window_size * (55 / 800))
    return border_size, die_width, padding, font_size


def cover(board):
    c = board.create_rectangle(0, 0, 850, 850, fill="#BBBBBB", tags="rem")
    t = board.create_text(
        850 / 2, 850 / 2, tags="rem", text="Click to reveal", font=("Bahnschrift", 75)
    )
    board.tag_bind("rem", "<ButtonPress-1>", lambda x: board.delete("rem"))
    board.pack(expand=True)


def alarm(board):
    a = board.create_text(
        900 / 2, 80, text="30 seconds left!", font=("Bahnschrift", 150 - 80), fill="white"
    )
    root.after(5000, lambda: board.delete(a))


# def resize_start_window(event, title, firstTime):
#     if firstTime:
#         startWindow.after(10, lambda: resize_start_window(event, title, False))
#     elif event.width == startWindow.winfo_width() and event.height == startWindow.winfo_height():
#         title.config(font=("Berlin Sans FB Demi", (event.width + event.height) // 15))


def resize_board(event, board, firstTime):
    if firstTime:
        root.after(10, lambda: resize_board(event, board, False))
    elif event.width == root.winfo_width() and event.height == root.winfo_height():
        drawBoard(min(event.width, event.height))
        


# # Welcome
# startWindow = Tk()
# startWindow.title("Boggle")
# startWindow.minsize(500, 500)
# startWindow.configure(bg="Light blue")

# title = Label(startWindow, text="Boggle", font=("Berlin Sans FB Demi", 100), bg="Light blue")
# title.pack(side="top", expand=True, fill="both", pady=(90, 10))

# # To resize Boggle title
# startWindow.bind("<Configure>", lambda x: resize_start_window(x, title, True))


# letterInput = Frame(startWindow, bg="Light blue")
# letterInput.pack(side="top", expand=True, fill="both", pady=60)

# seed = StringVar()  # Text entry
# ttk.Style().configure("pad.TEntry", padding="10 1 1 1")
# entry = ttk.Entry(
#     letterInput, width=30, font=("Bahnschrift 30"), textvariable=seed, style="pad.TEntry"
# )
# entry.pack(side="left", expand=True, fill="both", pady=0, padx=(50, 10))
# entry.focus_set()


# generator = Button(
#     letterInput,
#     command=lambda: seed.set(encodeLetters(generateLetters())),
#     text="Generate",
#     font=("Bahnschrift 25"),
# )
# generator.pack(side="right", expand=True, fill="both", pady=0, padx=(10, 50))


# start = Button(
#     startWindow, text="START", font=("Bahnschrift 60"), command=lambda: startWindow.destroy()
# )  # GUI destroys
# start.pack(side="top", expand=True, fill="both", pady=(0, 60), padx=(250, 250))

# startWindow.mainloop()


# GUI
root = Tk()
root.title("Boggle Board")
root.configure(bg="#FF6600")


# if seed.get() == "":
letters = generateLetters()
# else:
#     letters = decodeLetters(seed.get())

boggleBoard = Canvas(
    root,
    height=800,
    width=800,
    bg="#FF6600",
    highlightbackground="light blue",
    highlightthickness=50,
)
boggleBoard.pack(expand=True)

drawBoard(800)

root.bind("<Configure>", lambda x: resize_board(x, boggleBoard, True))

# t = Timer(180.0, lambda: cover(boggleBoard))
# t.start()

# a = Timer(150.0, lambda: alarm(boggleBoard))
# a.start()

root.mainloop()

# print("bean awesome")

import random as r
from tkinter import *
import tkinter.ttk as ttk
from threading import Timer
from bogglesolver import *

global DICE
DICE =['EIOSST', 'HIMNQU', 'CIMOTU', 'AFFKPS',
       'ACHOPS', 'DEILRX', 'ELRTTY', 'AAAEGN',
       'DELRVY', 'HLNNRZ', 'EEINSU', 'ABBJOO',
       'EHRTVW', 'AOOTTW', 'DISTTY', 'EEGHNW']


def generateLetters():
    letters = []

    for die in DICE:
        letter = die[r.randint(0,5)]
        letters.append(letter)

    r.shuffle(letters)
    print(letters)
    return letters

def encodeLetters(letters):
    encoded = ""
    for letter in letters:
        number = str(ord(letter))
        encoded = encoded + number
    return(str(hex(int(encoded))[2:]))

def decodeLetters(coded):
    letters = []
    dex = str(int(coded, 16))
    print(dex)
    for i in range(0,32,2):
        letter = str(chr(int(dex[i:i+2])))
        letters.append(letter)
    return letters


def cover(board):
    c = board.create_rectangle(0,0,850,850,fill="#BBBBBB", tags="rem")
    t = board.create_text(850/2,850/2, tags="rem",
                          text="Click to reveal", font = ("Bahnschrift", die_width - 50))
    board.tag_bind("rem", '<ButtonPress-1>', lambda x: board.delete("rem"))
    board.pack(expand=True)

def alarm(board):
    a = board.create_text(900/2,80, text="30 seconds left!",
                          font = ("Bahnschrift", die_width - 80),
                          fill="white")
    root.after(5000, lambda: board.delete(a))


def resize(event, title, firstTime):
    if firstTime:
        startWindow.after(10, lambda: resize(event, title, False))
    elif event.width == startWindow.winfo_width() and event.height == startWindow.winfo_height():    
        title.config(font=("Berlin Sans FB Demi", (event.width+event.height)//15))

    #solutionBoard.create_text(10, 10, text=bs.words, font=("Bahnschrift"))


def boggleSolverFxn(letters):
    bs = BoggleSolver(letters)
    time_start = time()
    bs.find_words()
    print(bs.words)
    answers = list(bs.words)
    answers.sort()

    print(f"Took {time() - time_start} seconds to execute")

    return answers


def openNewWindow():
    newWindow = Toplevel(root)
    newWindow.title("Boggle Solutions")
    newWindow.configure(bg="light blue")
    newWindow.geometry("600x400")


    newWindow.grid_columnconfigure(0, weight=1)
    newWindow.grid_rowconfigure(0, weight=1)

    bs = boggleSolverFxn(letters)
    numberofWords = len(bs)

    text = Text(newWindow, height=20, bg="light blue", font=("Bahnschrift", 25))
    text.grid(row=0, column=0, sticky=NS)

    scrollbar = Scrollbar(newWindow, orient='vertical', command=text.yview)
    scrollbar.grid(row=0, column=2, sticky=NS)

    text['yscrollcommand'] = scrollbar.set

    for i in range(1, len(bs)):
        position = f'{i}.0'
        text.insert(position, f'{bs[i]}\n');

    text1 = Text(newWindow, height=20, bg="light blue", font=("Bahnschrift", 25))
    text1.grid(row=0, column=1, sticky=NS)
    text1.insert('1.0', "Wahey")


# Code starts here again

#Welcome
startWindow = Tk()
startWindow.title("Boggle")
startWindow.minsize(500,500)
startWindow.configure(bg="Light blue")

#To resize Boggle title
startWindow.bind("<Configure>", lambda x:resize(x, title, True))

title = Label(startWindow, text="Boggle", font=("Berlin Sans FB Demi",100), bg="Light blue")
title.pack(side = "top", expand = True, fill = "both", pady=(90,10))


letterInput = Frame(startWindow, bg="Light blue")
letterInput.pack(side = "top", expand = True, fill = "both", pady=60)

seed = StringVar() #Text entry
ttk.Style().configure('pad.TEntry', padding='10 1 1 1')
entry = ttk.Entry(letterInput, width=30, font=("Bahnschrift 30"),
              textvariable = seed, style='pad.TEntry')
entry.pack(side="left", expand = True, fill = "both", pady=0, padx=(50,10))
entry.focus_set()


generator = Button(letterInput, command = lambda: seed.set(encodeLetters(generateLetters())),
                   text="Generate", font=("Bahnschrift 25"))
generator.pack(side="right", expand = True, fill = "both", pady=0, padx=(10,50))


start = Button(startWindow, text="START", font=("Bahnschrift 60"),
               command = lambda: startWindow.destroy()) #GUI destroys
start.pack(side="top", expand = True, fill = "both", pady=(0,60), padx=(250,250))


startWindow.mainloop()


#GUI
root = Tk()
root.title("Boggle Board")
root.configure(bg="#FF6600")

if seed.get() == "":
    letters = generateLetters()
else:
    letters = decodeLetters(seed.get())

boggleBoard = Canvas(root, height=800, width=800, bg="#FF6600",
                     highlightbackground="light blue", highlightthickness=50)
boggleBoard.pack(expand=True)

border = 75+50
padding = 50
die_width = 125

index = 0
for x in range(border, 700, die_width + padding):
    for y in range(border, 700, die_width + padding):
        boggleBoard.create_rectangle(x,y,x+die_width,y+die_width, fill="white", width=3.5,
                                     outline = "#883300")
        if letters[index] == "Q":
            boggleBoard.create_text(x + (die_width/2),y + (die_width/2)-5, text="Qu",
                                font = ("Bahnschrift", die_width - 55))
        else:
            boggleBoard.create_text(x + (die_width/2),y + (die_width/2)-5, text=letters[index],
                                font = ("Bahnschrift", die_width - 50))
        
        index += 1

solutionsButton = Button(boggleBoard, text="View the possibilities!", command=openNewWindow,
                  font=("Bahnschrift 25"), width=20, height=1)
solutionsButton.place(x=260, y=50)

t = Timer(180.0, lambda: cover(boggleBoard))
t.start()


a = Timer(150.0, lambda: alarm(boggleBoard))
a.start()


root.mainloop()

#print("bean awesome")

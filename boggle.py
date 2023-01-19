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
    answers = list(bs.words)
    answers.sort()
    print(answers)

    print(f"Took {time() - time_start} seconds to execute")

    return answers


def openNewWindow():

    newWindow = Toplevel(root)
    newWindow.title("Boggle Solutions")
    newWindow.configure(bg="light blue")
    newWindow.geometry("600x400")

    # creating main containers
    top_Frame = Frame(newWindow, bg='red', width=400, height=200)
    bottom_Frame = Frame(newWindow, bg='yellow', width=400, height=200)

    # layout of containers
    newWindow.grid_columnconfigure(0, weight=1)
    newWindow.grid_rowconfigure(1, weight=1)

    top_Frame.grid(row=0, sticky="ew")
    bottom_Frame.grid(row=1, sticky="nsew")

    # widgets for bottom frame

    bs = boggleSolverFxn(letters)
    number_of_words = len(bs)

    text = Text(bottom_Frame, height=20,
                bg='light blue', font=("Bahnschrift", 25))

    scrollbar = Scrollbar(bottom_Frame, orient='vertical', command=text.yview)
    text['yscroll'] = scrollbar.set

    scrollbar.pack(side="right", fill="y")
    text.pack(side="left", fill="both", expand=True)

    for i in range(0, len(bs)):
        position = f'{i+1}.0'
        text.insert(position, f'{bs[i]}\n')



'''
    menu = Frame(newWindow, bg='gold')
    menu.pack(expand=True)
    menu_label = Label(menu, text="Top label", bg="red")
    menu_label.grid(row=0, column=0)
    menu_label2 = Label(menu, text="ha Jonny")
    menu_label2.grid(row=0, column=1)
    
    container = Frame(newWindow)
    container.pack(expand=True, fill="both")

    canvas = Canvas(container)
    canvas.grid(row=1, column=0)
    canvas.columnconfigure(0,weight=3)
    scrollbarTest = Scrollbar(container, orient="vertical", command=canvas.yview)
    scrollableFrame = Frame(canvas)

    # Whenever contents of scrollable frame change, need to tell canvas how
    # large frame is going to be, so knows how much can scroll
    # <Configure> triggers whenever scrollableFrame changes size

    # Modifying canvas' scrollregion to have size of all canvas:
    # bbox: 4-value tuple describing two corner positions of a rectangle (scroll region)
    scrollableFrame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    # Drawing scrollable frame inside the canvas
    canvas.create_window((0, 0), window=scrollableFrame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbarTest.set)

    for i in range(0, len(bs)):
        Label(scrollableFrame, text=f'{bs[i]}\n').pack()

    container.pack()
    canvas.pack(side="left", fill="both", expand=True)
    scrollbarTest.pack(side="right", fill="y")
'''






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

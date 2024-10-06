import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import threading
import random
import time
import winsound

window = tk.Tk()
window.geometry("700x700")

#Matriisit
pool = np.zeros(shape=(20,60))
ernestiOja = np.ones(shape=(100,1))
kernestiOja = np.ones(shape=(100,1))
monkeys = []

#Functions here
def createMonkey(amount):
    for i in range(amount):
        monkey = {
            "x": random.randint(210,490),
            "y": random.randint(500,590),
            "status": "free",
            "label": tk.Label(window, padx=0, pady=0, borderwidth=0, bg="brown")
        }
        monkeys.append(monkey)
        monkey["label"].place(x=monkey["x"], y=monkey["y"], height=3, width = 3)

def getMonkeyE(x, y):
    for monkey in monkeys:
        if monkey["status"] == "free":
            monkey["status"] = "busy"
            move(monkey, x, y, "ernesti")
            break

def getMonkeyEHandle():
    threading.Thread(target=getMonkeyE, args=(332, 399)).start()

def getNewMonkeyE():
    if any(1 in row for row in ernestiOja) == False: #Katsoo onko ojassa yhtään ykkösiä jälellä
        print("Kaikki kaivettu")
        return
    y = random.randint(100,399)
    index = (y - 100) // 3
    if ernestiOja[index][0] == 1:
        getMonkeyE(332, y)
    else:
        getNewMonkeyE()

def getNewMonkeyEHandle():
    threading.Thread(target=getNewMonkeyE).start()

def getMonkeyK(x, y):
    for monkey in monkeys:
        if monkey["status"] == "free":
            monkey["status"] = "busy"
            move(monkey,x,y, "kernesti")
            break

def getMonkeyKHandle():
    threading.Thread(target=getMonkeyK, args=(372, 399)).start()
    
def getNewMonkeyK():
    if any(1 in row for row in kernestiOja) == False:
        print("Kaikki kaivettu")
        return
    y = random.randint(100,399)
    index = (y - 100) // 3
    if kernestiOja[index][0] == 1:
        getMonkeyK(372, y)
    else:
        getNewMonkeyK()

def getNewMonkeyKHandle():
    threading.Thread(target=getNewMonkeyK).start()

def move(thing, x, y, person):
    if thing["x"] != x or thing["y"] != y:
        if thing["x"] < x:
            thing["x"] += 1
        elif thing["x"] > x:
            thing["x"] -= 1
        if thing["y"] < y:
            thing["y"] += 1
        elif thing["y"] > y:
            thing["y"] -= 1
        thing["label"].place(x=thing["x"], y=thing["y"])
        window.after(5, lambda: move(thing, x, y, person))
    elif person == "ernesti":
        threading.Thread(target=digE, args=(thing,)).start()
    elif person == "kernesti":
        threading.Thread(target=digK, args=(thing,)).start()

def digE(monkey):
    diggingTime = 1
    while monkey["y"] > 99:
        time.sleep(diggingTime)
        if monkey["label"].winfo_exists() == False:
            break
        index = (monkey["y"] - 100) // 3
        ernestiOja[index][0] -= 1
        print(ernestiOja[index][0])
        caxE.set_data(ernestiOja)
        canvasE.draw()
        winsound.Beep(500,100)
        diggingTime *= 2
        monkey["y"] -= 3
        monkey["label"].place(x=monkey["x"], y=monkey["y"])
    monkey["label"].destroy()

def digK(monkey):
    diggingTime = 1
    while monkey["y"] > 99:
        time.sleep(diggingTime)
        if monkey["label"].winfo_exists() == False:
            break
        index = (monkey["y"] - 100) // 3
        kernestiOja[index][0] -= 1
        print(ernestiOja[index][0])
        caxK.set_data(kernestiOja)
        canvasK.draw()
        winsound.Beep(500,100)
        diggingTime *= 2
        monkey["y"] -= 3
        monkey["label"].place(x=monkey["x"], y=monkey["y"])
    monkey["label"].destroy()

def fillOjat():
    global monkeys
    busyMonkeys = [monkey for monkey in monkeys if monkey["status"] == "busy"] #Katotaan kaikki apinat jotka on töissä ja poistetaan ne
    for monkey in busyMonkeys:
        monkey["label"].destroy()
    monkeys = [monkey for monkey in monkeys if monkey["status"] != "busy"]

    for i in range(len(ernestiOja)): #Käydään läpi matriisi ja täytetään kaikki ykkösillä
        ernestiOja[i][0] = 1
        kernestiOja[i][0] = 1

    caxE.set_data(ernestiOja)
    caxK.set_data(kernestiOja)
    canvasE.draw()
    canvasK.draw()

def get10MonkeysE():
    y = random.randint(100, 399)
    getMonkeyE(332,y)
    for i in range(10):
        getMonkeyE(332, 399-i*30)
        time.sleep(1)

def get10MonkeysEHandle():
    threading.Thread(target=get10MonkeysE).start()

def get10MonkeysK():
    y = random.randint(100, 399)
    getMonkeyE(372,y)
    for i in range(10):
        getMonkeyK(372, 399-i*30)
        time.sleep(1)

def get10MonkeysKHandle():
    threading.Thread(target=get10MonkeysK).start()

#Saaren canvas
canvas = tk.Canvas(window, width=700, height=700, bg="lightblue")
canvas.create_rectangle(100,100,600,650, fill="yellow", outline="yellow")
canvas.create_rectangle(200,500,500,600, fill="green", outline="green")
canvas.place(x=0, y=0)

#Allas matriisi
figP = Figure(figsize=(180,60), dpi=1)
axP = figP.add_subplot(111)
caxPool = axP.matshow(pool, cmap='viridis', vmin=-3, vmax=1)
axP.set_xticks([])
axP.set_yticks([])
figP.subplots_adjust(left=0, right=1, top=1, bottom=0)
canvasP = FigureCanvasTkAgg(figP,master=window)
canvasP.draw()
canvasP.get_tk_widget().place(x=260, y=400)

#Ernesti oja matriisi
figE = Figure(figsize=(3,300), dpi=1)
axE = figE.add_subplot(111)
caxE = axE.matshow(ernestiOja, cmap='viridis', vmin=-3, vmax=1)
axE.set_xticks([])
axE.set_yticks([])
figE.subplots_adjust(left=0, right=1, top=1, bottom=0)
canvasE = FigureCanvasTkAgg(figE,master=window)
canvasE.draw()
canvasE.get_tk_widget().place(x=330, y=100)

#Kernesti oja matriisi
figK = Figure(figsize=(3,300), dpi=1)
axK = figK.add_subplot(111)
caxK = axK.matshow(kernestiOja, cmap='viridis', vmin=-3, vmax=1)
axK.set_xticks([])
axK.set_yticks([])
figK.subplots_adjust(left=0, right=1, top=1, bottom=0)
canvasK = FigureCanvasTkAgg(figK,master=window)
canvasK.draw()
canvasK.get_tk_widget().place(x=370, y=100)

#Napit
btnGetFirstMonkeyE = tk.Button(window, text="Hae eka apina E", command=getMonkeyEHandle)
btnGetFirstMonkeyE.place(x=0, y=0)
btnGetFirstMonkeyK = tk.Button(window, text="Hae eka apina K", command=getMonkeyKHandle)
btnGetFirstMonkeyK.place(x=100, y=0)
btnGetNewMonkeyE = tk.Button(window, text="Hae uus apina E", command=getNewMonkeyEHandle)
btnGetNewMonkeyE.place(x=200, y=0)
btnGetNewMonkeyK = tk.Button(window, text="Hae uus apina K", command=getNewMonkeyKHandle)
btnGetNewMonkeyK.place(x=300, y=0)
btnFillOjat = tk.Button(window, text="Täytä ojat", command=fillOjat)
btnFillOjat.place(x=400, y=0)
btnGet10MonkeysE = tk.Button(window, text="Hae 10 apinaa E", command=get10MonkeysEHandle)
btnGet10MonkeysE.place(x=470, y=0)
btnGet10MonkeysK = tk.Button(window, text="Hae 10 apinaa K", command=get10MonkeysKHandle)
btnGet10MonkeysK.place(x=570, y=0)

createMonkey(50)

window.mainloop()
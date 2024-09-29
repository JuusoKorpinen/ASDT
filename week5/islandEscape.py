import threading
import tkinter as tk
import random
import winsound
import time

message = ["apua", "jumissa", "autio", "saari", "länsi", "yksi", "kaksi", "kolme", "neljä", "viisi", "kuusi", "seitsemän", "kahdeksan"] #Couldn't come up with more words so added numbers

ernesti = {
    "monkeysSent": 0,
    "monkeysArrived": 0
}

kernesti = {
    "monkeysSent": 0,
    "monkeysArrived": 0
}


#Functions here
def sendMonkeyE():
    monkey = tk.Label(window, text='M')
    monkey.place(x=400, y=200)
    word = random.choice(message)
    ernesti["monkeysSent"] += 1
    updateStats()
    threading.Thread(target=moveMonkey, args=(monkey,"ernesti", word)).start()

def send10MonkeysE():
    for i in range(10):
        window.after(1000*i, sendMonkeyE)

def sendMonkeyK():
    monkey = tk.Label(window, text='M')
    monkey.place(x=400, y=600)
    word = random.choice(message)
    kernesti["monkeysSent"] += 1
    updateStats()
    threading.Thread(target=moveMonkey, args=(monkey,"kernesti", word)).start()

def send10MonkeysK():
    for i in range(10):
        window.after(1000*i, sendMonkeyK)

def moveMonkey(monkey, sender, word):
    window.update()
    monkeyX = monkey.winfo_x()
    monkeyY = monkey.winfo_y()
        
    while monkeyX != 1100:
        lantti = random.random()
        if lantti > 0.993:
            monkey.destroy()
            playSound("shark")
            break
        else:
            monkeyX+=7
            monkey.place(x=monkeyX, y=monkeyY)
            playSound("swim")
        time.sleep(0.1)
    if monkeyX >= 1100:
        goal(monkey, sender, word)

def goal(monkey, sender, word):
    monkeyX = monkey.winfo_x()
    if monkeyX >= 1100:
        if sender == "ernesti":
            wordListE.insert(tk.END, word)
            ernesti["monkeysArrived"] += 1
            updateStats()
        elif sender == "kernesti":
            wordListK.insert(tk.END, word)
            kernesti["monkeysArrived"] += 1
            updateStats()
        monkey.destroy()
        playSound("goal")

def playSound(sound):
    if sound == "goal":
        winsound.Beep(1000,400)
    elif sound == "swim":
        winsound.Beep(300,200)
    elif sound == "shark":
        winsound.Beep(600,300)

def updateStats():
    lblErnestiStats.config(text=f"Apinoita lähetetty: {ernesti['monkeysSent']} | Apinoita perillä: {ernesti['monkeysArrived']}")
    lblKernestiStats.config(text=f"Apinoita lähetetty: {kernesti['monkeysSent']} | Apinoita perillä: {kernesti['monkeysArrived']}")

boatSent = False

def pohteri():
    global boatSent
    while True:
        uniqueWords = set(wordListE.get(0, tk.END))
        if len(uniqueWords) > 10:
            if boatSent == False:
                sendBoat("ernersti")
                boatSent = True
            break

def eteteri():
    global boatSent
    while True:
        uniqueWords = set(wordListK.get(0, tk.END))
        if len(uniqueWords) > 10:
            if boatSent == False:
                sendBoat("kernesti")
                boatSent = True
            break
        
def sendBoat(winner):
    boat = tk.Label(window, text='B')
    if winner == "ernersti":
        boat.place(x=1100, y=200)
        threading.Thread(target=moveBoat, args=(boat,"ernesti")).start()
    elif winner == "kernesti":
        boat.place(x=1100, y=600)
        threading.Thread(target=moveBoat, args=(boat,"kernesti")).start()

def moveBoat(boat, winner):
    window.update()
    boatX = boat.winfo_x()
    boatY = boat.winfo_y()

    while boatX != 400:
        boatX-=7
        boat.place(x=boatX, y=boatY)
        playSound("swim")
        time.sleep(0.1)

    if boatX == 400:
        goalBoat(winner)

def goalBoat(winner):
    if winner == "ernesti":
        lblText.config(text="Hahaa Kernesti! Minun apinat oli parempia!")
    elif winner == "kernesti":
        lblText.config(text="Voitto on minun Ernesti!")
    makeSoup()

def makeSoup():
    time.sleep(5)
    monkeysE = ernesti["monkeysArrived"]
    monkeysK = kernesti["monkeysArrived"]
    if monkeysE < monkeysK:
        lblText.config(text=f"Kernesti syötti enemmän. Hän syötti {monkeysK * 4} henkeä")
    elif monkeysE > monkeysK:
        lblText.config(text=f"Ernesti syötti enemmän. Hän syötti {monkeysE * 4} henkeä")

    pepperE = monkeysE * 2
    pepperK = monkeysK * 2
    time.sleep(5)
    lblText.config(text=f"Juhlissa kului yhteensä {pepperE + pepperK} tl mustapippuria")



window = tk.Tk()
window.geometry("1500x800")
canvas = tk.Canvas(window, width=1980, height=1080, bg="lightblue")
canvas.create_rectangle(100,100,400,700, fill="yellow")
canvas.create_rectangle(1100,100,1400,700, fill="grey")


#Buttons and stuff
btnSendMonkeyE = tk.Button(window, text="Ernesti", command=sendMonkeyE)
btnSendMonkeyE.place(x=0, y=0)
btnSendMonkeyK = tk.Button(window, text="Kernesti", command=sendMonkeyK)
btnSendMonkeyK.place(x=80, y=0)
btnSend10MonkeysE = tk.Button(window, text="10 Ernesti", command=send10MonkeysE)
btnSend10MonkeysE.place(x=170, y=0)
btnSend10MonkeysK = tk.Button(window, text="10 Kernesti", command=send10MonkeysK)
btnSend10MonkeysK.place(x=270, y=0)

lblErnestiStats = tk.Label(window, text=f"Apinoita lähetetty: {ernesti['monkeysSent']} | Apinoita perillä: {ernesti['monkeysArrived']}", bg="yellow")
lblErnestiStats.place(x=101, y=101)
lblKernestiStats = tk.Label(window, text=f"Apinoita lähetetty: {ernesti['monkeysSent']} | Apinoita perillä: {ernesti['monkeysArrived']}", bg="yellow")
lblKernestiStats.place(x=101, y=500)
lblText = tk.Label(window, bg="lightblue")
lblText.place(x=600, y=0)

wordListE = tk.Listbox(window,height=18, width=20)
wordListE.place(x=1275, y=101)
wordListK = tk.Listbox(window,height=18, width=20)
wordListK.place(x=1275, y=405)

threading.Thread(target=pohteri).start()
threading.Thread(target=eteteri).start()

canvas.pack()
window.mainloop()
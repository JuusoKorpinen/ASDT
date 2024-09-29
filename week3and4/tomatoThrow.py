import threading
import random
import tkinter as tk
from PIL import Image, ImageTk
import winsound
import time

kernestiInfo = {
    "x": random.randint(0,100),
    "y": random.randint(400,600),
    "score": 0
}

ernestiInfo = {
   "x": 0,
    "y": 0,
    "score": 0
}

def placeKernesti():
    x = kernestiInfo["x"]
    y = kernestiInfo["y"]
    kernesti.place(x=x, y=y)

def placeErnesti():
    ernestiInfo["x"] = random.randint(1200, 1300)
    ernestiInfo["y"] = random.randint(400, 600)
    ernesti.place(x=ernestiInfo["x"], y=ernestiInfo["y"])

def throwTomatoK():
    tomato = tk.Label(window, image=tomatoImage)
    tomato.place(x=kernestiInfo["x"], y=kernestiInfo["y"])
    if kernestiInfo["score"] - ernestiInfo["score"] >=2:
        threading.Thread(target=moveTomato, args=(tomato, kernestiInfo["x"], kernestiInfo["y"], ernestiInfo["x"], ernestiInfo["y"], "kernesti", True)).start()
    else:
        threading.Thread(target=moveTomato, args=(tomato, kernestiInfo["x"], kernestiInfo["y"], 650, 200, "kernesti", False)).start()

def throwTomatoE():
    tomato = tk.Label(window, image=tomatoImage)
    tomato.place(x=ernestiInfo["x"], y=ernestiInfo["y"])
    if ernestiInfo["score"] - kernestiInfo["score"] >=2:
        threading.Thread(target=moveTomato, args=(tomato, ernestiInfo["x"], ernestiInfo["y"], kernestiInfo["x"], kernestiInfo["y"], "ernesti", True)).start()
    else:
        threading.Thread(target=moveTomato, args=(tomato, ernestiInfo["x"], ernestiInfo["y"], 650, 200, "ernesti", False)).start()

def moveTomato(tomato, throwerX, throwerY, targetX, targetY, thrower, isWinThrow):
    tomatoX = throwerX
    tomatoY = throwerY

    targetX += 50 #add a little extra so it seems to hit the center
    targetY += 25

    while tomatoX != targetX or tomatoY != targetY:
        if tomatoX < targetX:
            tomatoX += 1
        elif tomatoX > targetX:
            tomatoX -= 1

        if tomatoY < targetY:
            tomatoY += 1
        elif tomatoY > targetY:
            tomatoY -= 1

        tomato.place(x=tomatoX, y=tomatoY)
        time.sleep(0.0001) #a little delay to make it move smoother
    time.sleep(0.1)
    checkHit(tomato, thrower, targetX, targetY, isWinThrow)

def checkHit(tomato, thrower, targetX, targetY, isWinThrow):
    tomatoX = tomato.winfo_x()
    tomatoY = tomato.winfo_y()
    
    if targetX == tomatoX and targetY == tomatoY:
        lantti = random.randint(1,10)
        if lantti < 7:
            if thrower == "kernesti":
                if isWinThrow == True:
                    scoreboard.config(text="Kernesti wins")
                    window.after(1000, resetScore)
                else:
                    kernestiInfo["score"] += 1
                    updateScore()

            if thrower == "ernesti":
                if isWinThrow == True:
                    scoreboard.config(text="Ernesti wins")
                    window.after(1000, resetScore)
                else:
                    ernestiInfo["score"] += 1
                    updateScore()

            print("hit")
            tomato.config(image=splatImage)
            threading.Thread(target=playSound("hit")).start()
            window.after(200, tomato.destroy())
        else:
            print("miss")
            threading.Thread(target=playSound("miss")).start()
            window.after(10, tomato.destroy()) 

def updateScore():
    scoreboard.config(text=f"Kernesti score: {kernestiInfo['score']} Ernesti score: {ernestiInfo['score']}")

def resetScore():
    kernestiInfo["score"]= 0
    ernestiInfo["score"] = 0
    updateScore()

def playSound(sound):
    if sound == "hit":
        winsound.Beep(600, 200)
    if sound == "miss":
        winsound.Beep(200, 200)
   
window = tk.Tk()
window.geometry("1920x1080")

#Images
kernestiImage = Image.open("images/kerne.png")
kernestiImage = kernestiImage.resize((200, 200), resample=Image.BILINEAR)
kernestiImage = ImageTk.PhotoImage(kernestiImage)

ernestiImage = Image.open("images/erne.png")
ernestiImage = ernestiImage.resize((200, 200), resample=Image.BILINEAR)
ernestiImage = ImageTk.PhotoImage(ernestiImage)

targetImage = Image.open("images/maalitaulu.png")
targetImage = targetImage.resize((200, 200), resample=Image.BILINEAR)
targetImage = ImageTk.PhotoImage(targetImage)

tomatoImage = Image.open("images/tomaatti.png")
tomatoImage = tomatoImage.resize((100, 100), resample=Image.BILINEAR)
tomatoImage = ImageTk.PhotoImage(tomatoImage)

splatImage = Image.open("images/splat.png")
splatImage = splatImage.resize((100, 100), resample=Image.BILINEAR)
splatImage = ImageTk.PhotoImage(splatImage)


#Labels and stuff
kernesti = tk.Label(window, image=kernestiImage)

ernesti = tk.Label(window, image=ernestiImage)

target = tk.Label(window, image=targetImage)
target.place(x=650, y=200)

scoreboard = tk.Label(window, text="Kernesti Hits: 0 | Ernesti Hits: 0")
scoreboard.pack()

btnPlaceErnerti = tk.Button(window, text="Place Ernesti", command=placeErnesti)
btnPlaceErnerti.pack()

btnThrowTomatoK = tk.Button(window, text="Throw Tomato K", command=throwTomatoK)
btnThrowTomatoK.pack()

btnThrowTomatoE = tk.Button(window, text="Throw Tomato E", command=throwTomatoE)
btnThrowTomatoE.pack()

btnReset = tk.Button(window, text="Reset score", command=resetScore)
btnReset.pack()

placeKernesti()

window.mainloop()
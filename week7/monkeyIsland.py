import tkinter as tk
import random
import winsound
import threading
import time

#Ikkunan määrittely
window = tk.Tk()
window.geometry("1000x1000")
canvas = tk.Canvas(window, width=1000, height=1000, bg="lightblue")
canvas.place(x=0, y=0)

islands = [] #Tänne kaikki saaret
islandId = 0

#Functiot tänne
def volcanoEruption():
    global islandId
    startX = random.randint(10,750)
    startY = random.randint(10,750)
    endX = startX + random.randint(150,200) 
    endY = startY + random.randint(150,200)

    if checkIslandCollision(startX ,startY, endX, endY) == True:
        volcanoEruption()
    else:
        islandId += 1
        travelingKnowledge = False
        if islandId == 1: #Jos on eka saari niin annetaan sille tietoisuus matkailusta
            travelingKnowledge = True
        island = {
            "id": islandId,
            "startX": startX,
            "startY": startY,
            "endX": endX,
            "endY": endY,
            "travelingKnowledge": travelingKnowledge,
            "monkeys": [],
            "laiturit": []
        }
        islands.append(island)
        winsound.Beep(400,200)
        island["islandRectangle"] = canvas.create_rectangle(island["startX"], island["startY"], island["endX"], island["endY"], fill="yellow", outline="yellow")
        island["infoText"] = canvas.create_text(island["startX"]+70, island["startY"]+30, text=f"S{island['id']} Apinoiden määrä: {len(island['monkeys'])}")
        createMonkeys(10, island)
        addLaiturit(island)

def checkIslandCollision(startX ,startY, endX, endY): #Kattoo onko toinen saari eessä
    if canvas.find_overlapping(startX - 30, startY - 30, endX + 30, endY + 30):
        return True
    else:
        return False

def createMonkeys(amount, island): #Tekee saarelle x määrä apinoit
    for i in range(amount):
        monkey = {
            "island": island,
            "x": random.randint(island["startX"], island["endX"]),
            "y": random.randint(island["startY"], island["endY"]),
            "label": tk.Label(window, padx=0, pady=0, borderwidth=0, bg="brown"),
            "swimming": False
        }
        island["monkeys"].append(monkey)
        monkey["label"].place(x=monkey["x"], y=monkey["y"], height=3, width = 3)
    updateInfo(island)

def addLaiturit(island):
    if island["travelingKnowledge"] and not island["laiturit"]: #Tarkastaa onko tietoisuus matkailusta ja laitureita ei ole vielä
        island["laiturit"] = []
        island["laiturit"].append(canvas.create_rectangle(island["startX"] + (island["endX"] - island["startX"]) / 2 - 2, island["startY"], island["startX"] + (island["endX"] - island["startX"]) / 2 + 2, island["startY"] - 10, fill="black")) #Ylös
        island["laiturit"].append(canvas.create_rectangle(island["startX"] + (island["endX"] - island["startX"]) / 2 - 2, island["endY"], island["startX"] + (island["endX"] - island["startX"]) / 2 + 2, island["endY"] + 10, fill="black")) #Alas
        island["laiturit"].append(canvas.create_rectangle(island["startX"], island["startY"] + (island["endY"] - island["startY"]) / 2 - 2, island["startX"] - 10, island["startY"] + (island["endY"] - island["startY"]) / 2 + 2, fill="black")) #Vasen
        island["laiturit"].append(canvas.create_rectangle(island["endX"], island["startY"] + (island["endY"] - island["startY"]) / 2 - 2, island["endX"] + 10, island["startY"] + (island["endY"] - island["startY"]) / 2 + 2, fill="black")) #Oikee
        
def deleteIslands():
    global islandId
    for island in islands:
        canvas.delete(island["islandRectangle"])
        canvas.delete(island["infoText"])
        for laituri in island["laiturit"]:
            canvas.delete(laituri)
        for monkey in island["monkeys"]:
            monkey["label"].destroy()
    islands.clear()
    islandId = 0

def sendMonkey(island): #Asettaa apinan randomisti jollekin laiturille ja lähettää sen uimaan
        if island["travelingKnowledge"] and island["monkeys"]:
            for monkey in island["monkeys"]:
                if monkey["swimming"] == False:
                    monkey["swimming"] = True
                    direction = random.choice(["up", "down", "left", "right"])
                    if direction == "up":
                        monkey["x"] = island["startX"] + (island["endX"] - island["startX"]) / 2
                        monkey["y"] = island["startY"] - 11
                    elif direction == "down":
                        monkey["x"] = island["startX"] + (island["endX"] - island["startX"]) / 2
                        monkey["y"] = island["endY"] + 11
                    elif direction == "left":
                        monkey["x"] = island["startX"] - 11
                        monkey["y"] = island["startY"] + (island["endY"] - island["startY"]) / 2
                    elif direction == "right":
                        monkey["x"] = island["endX"] + 11
                        monkey["y"] = island["startY"] + (island["endY"] - island["startY"]) / 2
                    monkey["label"].place(x=monkey["x"], y=monkey["y"])
                    island["monkeys"].remove(monkey)
                    updateInfo(island)
                    threading.Thread(target=swim, args=(monkey, direction)).start()
                    break
                
def swim(monkey, direction):
    while not canvas.find_overlapping(monkey["x"],monkey["y"],monkey["x"],monkey["y"]): #Uidaan niin kauan kunnes tulee jotain vastaan
        if random.random() < 0.01: #Prosentin mahdollisuus tulla syödyksi
            print("Hai soi apinan")
            winsound.Beep(500, 500)
            monkey["label"].destroy()
            break
        if direction == "up":
            monkey["y"] -= 5
        elif direction == "down":
            monkey["y"] += 5
        elif direction == "right":
            monkey["x"] += 5
        elif direction == "left":
            monkey["x"] -= 5
        monkey["label"].place(x=monkey["x"], y=monkey["y"])
        winsound.Beep(200, 50)
        time.sleep(1)

    for item in canvas.find_overlapping(monkey["x"],monkey["y"],monkey["x"] + 10,monkey["y"] + 10): #Katotaan mihin se apina törmäs
        for island in islands:
            if item == island["islandRectangle"]:
                monkey["swimming"] = False
                monkey["island"] = island
                monkey["x"] = random.randint(island["startX"], island["endX"])
                monkey["y"] = random.randint(island["startY"], island["endY"])
                monkey["label"].place(x=monkey["x"], y=monkey["y"])
                island["monkeys"].append(monkey)
                island["travelingKnowledge"] = True
                updateInfo(island)
                addLaiturit(island)
                return
      
def islandObserver(): #Tarkkailee jokaista saarta
    while True:
        for island in islands:
            sendMonkey(island)
            for monkey in island["monkeys"]:
                if random.random() < 0.01: #Yhen prosentin mahdollisuus kuolla nauruun
                    print("Apina kuoli nauruun")
                    winsound.Beep(1000, 500)
                    monkey["label"].destroy()
                    island["monkeys"].remove(monkey)
                    updateInfo(island)
                else: #Jos ei kuole nauruun niin muuten vaan ääntelee
                    winsound.Beep(random.randint(400,2000), 50)
        time.sleep(10)

def islandObserverHandle():
    threading.Thread(target=islandObserver, daemon=True).start()

def updateInfo(island): #Päivittää saaren info tekstin
    canvas.itemconfig(island["infoText"], text=f"S{island['id']} Apinoiden määrä: {len(island['monkeys'])}")

#Napit ja muut
btnVolcano = tk.Button(window, text="Tulivuorenpurkaus", command=volcanoEruption)
btnVolcano.place(x=0, y=0)
btnDeleteIslands = tk.Button(window, text="Poista saaret", command=deleteIslands)
btnDeleteIslands.place(x=120, y=0)
btnSendMonkey = tk.Button(window, text="Lähetä apina", command=lambda: sendMonkey(islands[0])) #Nappi testaukseen joka lähettää ekalta saarelta apinan
btnSendMonkey.place(x=220, y=0)

islandObserverHandle()

window.mainloop()

import numpy as np
import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation

jungle = [[0 for i in range(100)] for i in range(100)]

Ernesti = {
    'position': (random.randint(0, 99), random.randint(0, 99))
}

Kernesti = {
    'position': (random.randint(0, 99), random.randint(0, 99))
}

Lions = []

def addLion():
    lion = {
        'position': (random.randint(0, 99), random.randint(0, 99))
        }
    Lions.append(lion)

addLion()
#addLion()
#addLion()

def move(character):
    x, y = character['position']
    direction = random.choice(['up', 'down', 'left', 'right'])
    if direction == 'up' and x > 0:
        x -= 1
    elif direction == 'down' and x < 99:
        x += 1
    elif direction == 'left' and y > 0:
        y -= 1
    elif direction == 'right' and y < 99:
        y += 1
    character['position'] = (x, y)

def moveLion(lion, preys):
    lionX, lionY = lion['position']
    prey = min(preys, key=lambda t: abs(t[0] - lionX) + abs(t[1] - lionY))
    preyX, preyY = prey

    if lionX < preyX and lionX < 99:
        lionX += 1
    elif lionX > preyX and lionX > 0:
        lionX -= 1
    if lionY < preyY and lionY < 99:
        lionY += 1
    elif lionY > preyY and lionY > 0:
        lionY -= 1
    lion['position'] = (lionX, lionY)


def update(frame):
    jungle = [[0 for i in range(100)] for i in range(100)]
    move(Ernesti)
    move(Kernesti)
    for lion in Lions:
        moveLion(lion, [Ernesti['position'], Kernesti['position']])
    jungle[Ernesti['position'][0]][Ernesti['position'][1]] = 3
    jungle[Kernesti['position'][0]][Kernesti['position'][1]] = 3
    for lion in Lions:
        jungle[lion['position'][0]][lion['position'][1]] = 1
    plt.clf()
    plt.imshow(jungle, cmap='Greens_r', interpolation='none')

    if Ernesti['position'] == Kernesti['position']:
        plt.title('Vau, onpa mukava nähdä taas!')
        ani.event_source.stop()

    for lion in Lions:
        if Ernesti['position'] == lion['position'] or Kernesti['position'] == lion['position']:
            plt.title('Slups, olipa hyvä ohjelmoija!')
            ani.event_source.stop()

fig = plt.figure()
ani = animation.FuncAnimation(fig, update, frames=100, interval = 100)
plt.show()
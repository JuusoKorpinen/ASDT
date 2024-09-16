import tkinter as tk
import pyaudio
import winsound
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time
import random


records = {
    1912: {'time': 10.6, 'athlete': 'Donald Lippincott'},
    1921: {'time': 10.4, 'athlete': 'Charlie Paddock'},
    1930: {'time': 10.3, 'athlete': 'Percy Williams'},
    1936: {'time': 10.2, 'athlete': 'Jesse Owens'},
    1956: {'time': 10.1, 'athlete': 'Willie Williams'},
    1960: {'time': 10.0, 'athlete': 'Armin Hary'},
    1968: {'time': 9.95, 'athlete': 'Jim Hines'},
    1983: {'time': 9.93, 'athlete': 'Calvin Smith'},
    1988: {'time': 9.92, 'athlete': 'Carl Lewis'},
    1991: {'time': 9.86, 'athlete': 'Carl Lewis'},
    1994: {'time': 9.85, 'athlete': 'Leroy Burrell'},
    1996: {'time': 9.84, 'athlete': 'Donovan Bailey'},
    1999: {'time': 9.79, 'athlete': 'Maurice Greene'},
    2002: {'time': 9.78, 'athlete': 'Tim Montgomery'},
    2005: {'time': 9.77, 'athlete': 'Asafa Powell'},
    2007: {'time': 9.74, 'athlete': 'Asafa Powell'},
    2008: {'time': 9.69, 'athlete': 'Usain Bolt'},
    2009: {'time': 9.58, 'athlete': 'Usain Bolt'}
}

lions = {
    'lion1': {'time': 7.20},
    'lion2': {'time': 7.35},
    'lion3': {'time': 7.40},
    'lion4': {'time': 7.58},
    'lion5': {'time': 7.24},
    'lion6': {'time': 7.70},
    'lion7': {'time': 7.80},
    'lion8': {'time': 7.93},
    'lion9': {'time': 8.10},
    'lion10': {'time': 8.50}
}

#window
window = tk.Tk()
window.geometry('600x600')

#global variables
ernestiX = 10
kernestiX = 10
ernestiStartTime = None
kernestiStartTime = None
ernestiFinishTime = None
kernestiFinishTime = None
ernestiTime = random.uniform(15.5,18.2)
kernestiTime = random.uniform(24.4,27.6)
distance = 100

#functions
def reset():
    global ernestiX, kernestiX, ernestiTime, kernestiTime, ernestiStartTime, kernestiStartTime, ernestiFinishTime, kernestiFinishTime
    ernestiX = 10
    kernestiX = 10
    ernesti.place(x=kernestiX, y=500)
    kernesti.place(x=kernestiX, y=520)
    ernestiTime = random.uniform(15.5,18.2)
    kernestiTime = random.uniform(24.4,27.6)
    ernestiStartTime = None
    kernestiStartTime = None
    ernestiFinishTime = None
    kernestiFinishTime = None
    ernestiTimer.config(text='0.00')
    kernestiTimer.config(text='0.00')


def ernestiRun():
    global ernestiX, ernestiStartTime, ernestiFinishTime
    if ernestiStartTime is None:
        ernestiStartTime = time.time()
    if ernestiX < distance:
        ernestiX += 1
        ernesti.place(x=ernestiX, y=500)
        delay = int(ernestiTime / distance * 1000)
        window.after(delay, ernestiRun)
    else:
        ernestiFinishTime = time.time() - ernestiStartTime
        ernestiTimer.config(text=f'{ernestiFinishTime:.2f}')

def kernestiRun():
    global kernestiX, kernestiStartTime, kernestiFinishTime
    if kernestiStartTime is None:
        kernestiStartTime = time.time()
    if kernestiX < distance:
        kernestiX += 1
        kernesti.place(x=kernestiX, y=520)
        delay = int(kernestiTime / distance * 1000)
        window.after(delay, kernestiRun)
    else:
        kernestiFinishTime = time.time() - kernestiStartTime
        kernestiTimer.config(text=f'{kernestiFinishTime:.2f}')

def bothRun(i):
    global ernestiFinishTime, kernestiFinishTime
    if i == 0:
        raceStatus.config(text='Ready...')
        winsound.Beep(540, 400)
    elif i == 1:
        raceStatus.config(text='Set...')
        winsound.Beep(540, 400)
    elif i == 2:
        raceStatus.config(text='Go!')
        winsound.Beep(740, 800)
    if i < 2:
        window.after(1000, bothRun, i + 1)
    else:
        ernestiRun()
        kernestiRun()

    if ernestiFinishTime is not None and kernestiFinishTime is not None:
        if ernestiFinishTime < kernestiFinishTime:
            raceStatus.config(text='Ernesti wins!')
        elif kernestiFinishTime < ernestiFinishTime:
            raceStatus.config(text='Kernesti wins!')
        else:
            raceStatus.config(text='It\'s a tie!')

#parts
ernesti = tk.Label(window, text='E')
ernesti.place(x=ernestiX, y=500)

kernesti = tk.Label(window, text='K')
kernesti.place(x=kernestiX, y=520)

raceStatus = tk.Label(window, text='Waiting to start...')
raceStatus.place(x=10, y=480)

ernestiTimer = tk.Label(window, text='0.00')
ernestiTimer.place(x=300, y=500)

kernestiTimer = tk.Label(window, text='0.00')
kernestiTimer.place(x=300, y=520)

btnErnestiStart = tk.Button(window, text='Ernesti start', command=ernestiRun)
btnErnestiStart.place(x=10, y=10)

btKernerstiStart = tk.Button(window, text='Kernesti start', command=kernestiRun)
btKernerstiStart.place(x=100, y=10)

btnBothStart = tk.Button(window, text='Both start', command=lambda: bothRun(i=0))
btnBothStart.place(x=190, y=10)

btnReset = tk.Button(window, text='Reset', command=reset)
btnReset.place(x=280, y=10)

canvas = tk.Canvas(window, width=50, height=40)
canvas.place(x=110, y=500)

#plot
fig = Figure(figsize=(5,4), dpi = 100)
ax = fig.add_subplot(111)
ax.set_xlabel('Year')
ax.set_ylabel('Time (s)')
years = list(records.keys())
times = [records[year]['time'] for year in years]
ax.plot(years, times, 'b-o')  

canvas = FigureCanvasTkAgg(fig, master=window)
canvas.draw()
canvas.get_tk_widget().place(x=10, y=60)


window.mainloop()


import tkinter as tk
from tkinter import ttk
import sys
import time

# --- Zvuk: različiti tonovi za prvi i ostale udarce ---
if sys.platform.startswith("win"):
    import winsound
    def play_click():
        if current_beat[0] == 1:
            winsound.Beep(800, 100)  # viši ton za prvi udarac
        else:
            winsound.Beep(200, 100)   # niži ton za ostale
else:
    def play_click():
        root.bell()  # jednostavan signal na Linux/macOS

# --- Funkcije metronoma i štoperice ---
def metronome_tick():
    if running[0]:
        play_click()

        # Vizualni puls prema taktu
        color = "red" if current_beat[0] == 1 else "yellow"
        canvas.itemconfig(circle, fill=color)
        root.after(100, lambda: canvas.itemconfig(circle, fill="white"))

        # Pulsirajući efekt kruga
        pulse_effect()

        # Sljedeći takt
        current_beat[0] += 1
        if current_beat[0] > beats_per_measure[0]:
            current_beat[0] = 1

        # Ažuriraj štopericu
        elapsed = time.time() - start_time[0] + paused_time[0]
        minutes = int(elapsed // 60)
        seconds = int(elapsed % 60)
        stopwatch_label.config(text=f"Vrijeme: {minutes:02d}:{seconds:02d}")

        root.after(interval_ms[0], metronome_tick)

def start_metronome():
    if running[0]:
        return

    try:
        beats_per_measure[0] = int(takt_var.get())
    except ValueError:
        beats_per_measure[0] = 2

    try:
        bpm = int(bpm_var.get())
    except ValueError:
        bpm = 160

    interval_ms[0] = int(60000 / bpm)

    running[0] = True
    current_beat[0] = 1
    start_time[0] = time.time()
    metronome_tick()

def stop_metronome():
    if running[0]:
        running[0] = False
        paused_time[0] += time.time() - start_time[0]

def reset_metronome():
    running[0] = False
    paused_time[0] = 0
    stopwatch_label.config(text="Vrijeme: 00:00")
    current_beat[0] = 1
    canvas.itemconfig(circle, fill="white")

# --- Efekt pulsa kruga ---
def pulse_effect():
    def animate(size):
        canvas.coords(circle, 50 - size/2, 50 - size/2, 50 + size/2, 50 + size/2)
    for s in [80, 85, 90, 85, 80]:
        root.after(int((s-80)*2), lambda sz=s: animate(sz))

# --- Slajder funkcije ---
def update_bpm(val):
    bpm_var.set(str(int(float(val))))
    if running[0]:
        bpm = int(float(val))
        interval_ms[0] = int(60000 / bpm)

def update_takt(val):
    takt_var.set(str(int(float(val))))
    if running[0]:
        beats_per_measure[0] = int(float(val))

# --- GUI ---
root = tk.Tk()
root.title("Metronom s automatskim ritmom")

running = [False]
current_beat = [1]
beats_per_measure = [2]
interval_ms = [375]  # 160 BPM
start_time = [0.0]
paused_time = [0.0]

bpm_var = tk.StringVar(value="160")
takt_var = tk.StringVar(value="2")

# Glavni frame
main_frame = ttk.Frame(root)
main_frame.pack(padx=10, pady=10)

# --- Lijeva kolona: Slajderi i unosi ---
col1 = ttk.Frame(main_frame)
col1.grid(row=0, column=0, padx=10)

inputs_frame = ttk.Frame(col1)
inputs_frame.pack()

bpm_slider = ttk.Scale(inputs_frame, from_=40, to=240, orient="vertical", command=update_bpm)
bpm_slider.set(160)
bpm_slider.grid(row=0, column=0, padx=5)

entries_frame = ttk.Frame(inputs_frame)
entries_frame.grid(row=0, column=1, padx=5)

ttk.Label(entries_frame, text="BPM:").pack(pady=5)
ttk.Entry(entries_frame, textvariable=bpm_var, width=10).pack(pady=5)
ttk.Label(entries_frame, text="Takt:").pack(pady=5)
ttk.Entry(entries_frame, textvariable=takt_var, width=10).pack(pady=5)

takt_slider = ttk.Scale(inputs_frame, from_=1, to=12, orient="vertical", command=update_takt)
takt_slider.set(2)
takt_slider.grid(row=0, column=2, padx=5)

# --- Srednja kolona: Gumbi i štoperica ---
col2 = ttk.Frame(main_frame)
col2.grid(row=0, column=1, padx=10)

# Stilovi gumba
style = ttk.Style()
style.configure("Clicked.TButton", background="#ffcc00")

def flash_button(button):
    original_style = button.cget("style")
    button.config(style="Clicked.TButton")
    root.after(150, lambda: button.config(style=original_style))

start_button = ttk.Button(col2, text="Start", command=start_metronome)
stop_button = ttk.Button(col2, text="Stop / Pauza", command=stop_metronome)
reset_button = ttk.Button(col2, text="Reset", command=reset_metronome)

start_button.pack(pady=5)
stop_button.pack(pady=5)
reset_button.pack(pady=5)

stopwatch_label = ttk.Label(col2, text="Vrijeme: 00:00")
stopwatch_label.pack(pady=5)

# --- Desna kolona: Vizualni krug ---
col3 = ttk.Frame(main_frame)
col3.grid(row=0, column=2, padx=10)

canvas = tk.Canvas(col3, width=100, height=100)
canvas.pack(pady=10)
circle = canvas.create_oval(10, 10, 90, 90, fill="white", outline="black", width=2)

# --- Tipkovni prečaci ---
def toggle_metronome(event=None):
    if running[0]:
        stop_metronome()
        flash_button(stop_button)
    else:
        start_metronome()
        flash_button(start_button)

def reset_shortcut(event=None):
    reset_metronome()
    flash_button(reset_button)

def increase_bpm(event=None):
    bpm = int(bpm_var.get() or 120)
    bpm = min(bpm + 5, 300)
    bpm_var.set(str(bpm))
    bpm_slider.set(bpm)
    update_bpm(bpm)

def decrease_bpm(event=None):
    bpm = int(bpm_var.get() or 120)
    bpm = max(bpm - 5, 30)
    bpm_var.set(str(bpm))
    bpm_slider.set(bpm)
    update_bpm(bpm)

def increase_takt(event=None):
    takt = int(takt_var.get() or 4)
    takt = min(takt + 1, 12)
    takt_var.set(str(takt))
    takt_slider.set(takt)
    update_takt(takt)

def decrease_takt(event=None):
    takt = int(takt_var.get() or 4)
    takt = max(takt - 1, 1)
    takt_var.set(str(takt))
    takt_slider.set(takt)
    update_takt(takt)

root.bind("<space>", toggle_metronome)
root.bind("<r>", reset_shortcut)
root.bind("<Up>", increase_bpm)
root.bind("<Down>", decrease_bpm)
root.bind("<Right>", increase_takt)
root.bind("<Left>", decrease_takt)

# Info o prečacima
ttk.Label(root, text="Prečaci: [Space]=Start/Stop, [R]=Reset, ↑↓=BPM, ←→=Takt").pack(pady=5)

# --- Pokretanje ---
root.mainloop()

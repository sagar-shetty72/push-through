import tkinter as tk
import csv
import datetime
import os
import sys

APP_SUPPORT_DIR = os.path.expanduser("~/Library/Application Support/PushThrough")
os.makedirs(APP_SUPPORT_DIR, exist_ok=True)

SESSION_FILE = os.path.join(APP_SUPPORT_DIR, "session.csv")
RECORDS_FILE = os.path.join(APP_SUPPORT_DIR, "records.csv")

# Try to load existing session
if os.path.exists(SESSION_FILE):
    with open(SESSION_FILE, 'r') as f:
        reader = csv.reader(f)
        row = next(reader)
        session = {
            "start_time": datetime.datetime.fromisoformat(row[0]),
            "count": int(row[1])
        }
else:
    session = {
        "start_time": datetime.datetime.now(),
        "count": 0
    }
    with open(SESSION_FILE, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([session["start_time"].isoformat(), session["count"]])

# Tkinter window setup
window = tk.Tk()
window.title("PushThrough")
window.geometry("360x400")
window.configure(bg='#f0f0e0')
window.resizable(False, False)

count = tk.IntVar(window, value=session["count"])

# Write session to permanent log
def write_session(end_time):
    write_header = not os.path.exists(RECORDS_FILE)
    with open(RECORDS_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        if write_header:
            writer.writerow(["Start Time","End Time","Clicks"])
        writer.writerow([session["start_time"].isoformat(), end_time.isoformat(), count.get()])

# Save session without deleting
def pause_window():
    with open(SESSION_FILE, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([session["start_time"].isoformat(), count.get()])
    window.destroy()

# Exit and cleanup session
def exit_window():
    end_time = datetime.datetime.now()
    write_session(end_time)
    if os.path.exists(SESSION_FILE):
        os.remove(SESSION_FILE)
    window.destroy()

# Green screen display
screen = tk.Label(
    window,
    text="Session Active",
    font=("Courier", 14),
    bg="#003300",
    fg="#00FF00",
    width=32,
    height=2,
    relief="sunken",
    bd=2
)
screen.pack(pady=(20, 10))

# Button click logic
def on_click():
    current = count.get() + 1
    count.set(current)
    counter.config(text=f"Applied: {current}")
    with open(SESSION_FILE, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([session["start_time"].isoformat(), current])

# Glowing green button
counter = tk.Button(
    window,
    text=f"Applied: {count.get()}",
    command=on_click,
    font=("Courier", 20, "bold"),
    bg="#00FF00",
    activebackground="#00cc00",
    fg="black",
    relief="raised",
    bd=6,
    padx=20,
    pady=10
)
counter.pack(pady=(10, 20))

# Bezel frame for power and pause buttons
bezel = tk.Frame(window, bg="#d0d0c0", height=40)
bezel.pack(fill='x', side='bottom')

# Power button (Exit and wipe session)
power_btn = tk.Label(
    bezel,
    text="⏻",
    font=("Courier", 14, "bold"),
    fg="white",
    bg="red",
    width=2,
    height=1,
    relief="raised",
    bd=2
)
power_btn.place(relx=0.75, rely=0.5, anchor='center')
power_btn.bind("<Button-1>", lambda e: exit_window())

# Pause button (Save session and exit)
pause_btn = tk.Label(
    bezel,
    text="||",
    font=("Courier", 14, "bold"),
    fg="white",
    bg="gray",
    width=2,
    height=1,
    relief="raised",
    bd=2
)
pause_btn.place(relx=0.25, rely=0.5, anchor='center')
pause_btn.bind("<Button-1>", lambda e: pause_window())

window.protocol("WM_DELETE_WINDOW", exit_window)  # Ensures window closes correctly

window.mainloop()
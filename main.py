import tkinter as tk
from tkinter import ttk
import sqlite3
from datetime import datetime
import threading
import time
from Event import Event  # Make sure the Event class is properly defined in the Event module

# Basic structure for storing notes
notes = {}

def init_db():
    conn = sqlite3.connect('Event.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS notes (
            date TEXT PRIMARY KEY,
            title TEXT,
            description TEXT
        )
    ''')
    conn.commit()
    conn.close()

def load_notes_from_db():
    conn = sqlite3.connect('Event.db')
    cursor = conn.cursor()
    cursor.execute('SELECT date, title, description FROM notes')
    for row in cursor.fetchall():
        notes[row[0]] = {'title': row[1], 'description': row[2]}
        deadline = datetime.strptime(row[0], '%Y-%m-%d')
        event = Event(deadline, row[1], row[2])
        threading.Thread(target=monitor_event, args=(event,)).start()
    conn.close()

def monitor_event(event):
    while True:
        if event.check_deadline():
            break
        time.sleep(60)

def save_note_to_db():
    conn = sqlite3.connect('Event.db')
    cursor = conn.cursor()
    cursor.execute('REPLACE INTO notes (date, title, description) VALUES (?, ?, ?)',
                   (selected_date.get(), title.get(), description.get('1.0', tk.END).strip()))
    conn.commit()
    conn.close()

def save_note():
    notes[selected_date.get()] = {
        'title': title.get(),
        'description': description.get('1.0', tk.END).strip()
    }
    save_note_to_db()
    display_events(selected_date.get())

def display_events(date):
    events = notes.get(date, {})
    output_text = f"Title: {events.get('title', 'No events')}\nDescription: {events.get('description', '')}"
    event_display.config(state='normal')
    event_display.delete('1.0', tk.END)
    event_display.insert(tk.END, output_text)
    event_display.config(state='disabled')

# Create the main window
root = tk.Tk()
root.title("Event Calendar")

# Add a frame for the calendar
calendar_frame = ttk.Frame(root)
calendar_frame.grid(row=0, column=0, padx=10, pady=10)

# Create a StringVar to hold the selected date
selected_date = tk.StringVar()

# Function to create a calendar button
def create_calendar_button(frame, text, command):
    button = ttk.Button(frame, text=text, command=lambda: [command(), update_button_color(button)])
    return button

def update_button_color(button):
    # Reset all buttons to default color
    for child in calendar_frame.winfo_children():
        child.configure(style='TButton')
    # Change color of the selected button
    button.configure(style='Selected.TButton')

# Style for selected button
style = ttk.Style(root)
style.configure('Selected.TButton', background='lightblue')

# Add buttons for each day
buttons = []
for day in range(1, 31):
    def command_factory(d=day):
        return lambda: selected_date.set(f"{datetime.now().year}-{datetime.now().month}-{d:02d}")

    btn = create_calendar_button(calendar_frame, text=str(day), command=command_factory(day))
    btn.grid(row=(day - 1) // 7, column=(day - 1) % 7, sticky='ew')
    buttons.append(btn)

# Entry for title
title_label = ttk.Label(root, text="Enter Title Here")
title_label.grid(row=1, column=0, padx=10)
title = ttk.Entry(root)
title.grid(row=2, column=0, padx=10)

# Text box for description
description_label = ttk.Label(root, text="Enter Description Here")
description_label.grid(row=3, column=0, padx=10)
description = tk.Text(root, height=10, width=50)
description.grid(row=4, column=0, padx=10)

# Button to save notes
save_button = ttk.Button(root, text="Save", command=save_note)
save_button.grid(row=5, column=0, padx=10, pady=10)

# Text box to display events
event_display = tk.Text(root, height=10, width=50, state='disabled')
event_display.grid(row=6, column=0, padx=10, pady=10)

# Initialize the database and load notes when the application starts
init_db()
load_notes_from_db()

# Start the Tkinter loop
root.mainloop()

import tkinter as tk
from tkinter import messagebox
import json
import os
import re
import time
from datetime import datetime


def save_reminders():
    with open("reminders.json", "w") as file:
        json.dump(reminders, file)

def load_reminders():
    if os.path.exists("reminders.json"):
        with open("reminders.json", "r") as file:
            return json.load(file)
    return []


def is_valid_time_format(time_str):
    return re.match(r"^([01]\d|2[0-3]):[0-5]\d$", time_str)


def add_reminder():
    med = med_entry.get().strip()
    time = time_entry.get().strip()

    if not med or not time:
        messagebox.showwarning("Missing Info", "Enter both Medicine Name and Time.")
        return
    
    if not is_valid_time_format(time):
        messagebox.showerror("Invalid Time Format", "Use 24-hour format like 08:00 or 18:30.")
        return

    reminder_text = f"💊 {med} at 🕒 {time}"
    reminders.append(reminder_text)
    reminder_list.insert(tk.END, reminder_text)

    save_reminders()
    med_entry.delete(0, tk.END)
    time_entry.delete(0, tk.END)

def delete_reminder():
    selected = reminder_list.curselection()
    if not selected:
        messagebox.showwarning("Select Reminder", "Choose a reminder to delete.")
        return

    index = selected[0]
    reminder_list.delete(index)
    del reminders[index]
    save_reminders()


already_alerted = set()

def check_reminders():
    current_time = datetime.now().strftime("%H:%M")
    
    for reminder in reminders:
        # Extract time and med name from saved reminder
        if "at 🕒 " in reminder:
            parts = reminder.split("at 🕒 ")
            if len(parts) == 2:
                med_name = parts[0].replace("💊", "").strip()
                rem_time = parts[1].strip()

                if current_time == rem_time and reminder not in already_alerted:
                    messagebox.showinfo("⏰ Time for Medicine!", f"Take: {med_name}")
                    already_alerted.add(reminder)

    # Call this function again after 60 seconds
    root.after(60000, check_reminders)


root = tk.Tk()
root.title("💊 Medicine Reminder")
root.geometry("420x500")
root.configure(bg="#f0f4f7")

font_title = ("Helvetica", 20, "bold")
font_label = ("Segoe UI", 12)
font_entry = ("Segoe UI", 11)
font_list = ("Consolas", 11)

entry_style = {"font": font_entry, "bg": "#ffffff", "bd": 2, "relief": "groove"}
button_style = {"font": ("Segoe UI", 11, "bold"), "bd": 0, "padx": 10, "pady": 6, "activebackground": "#005f73"}

reminders = load_reminders()

tk.Label(root, text="Medicine Reminder App", font=font_title, bg="#f0f4f7", fg="#0a9396").pack(pady=15)

tk.Label(root, text="Medicine Name:", font=font_label, bg="#f0f4f7").pack()
med_entry = tk.Entry(root, **entry_style)
med_entry.pack(pady=5)

tk.Label(root, text="Reminder Time (HH:MM - 24hr):", font=font_label, bg="#f0f4f7").pack()
time_entry = tk.Entry(root, **entry_style)
time_entry.pack(pady=5)

tk.Button(root, text="➕ Add Reminder", command=add_reminder, bg="#94d2bd", fg="black", **button_style).pack(pady=10)
tk.Button(root, text="🗑️ Delete Reminder", command=delete_reminder, bg="#ee6c4d", fg="white", **button_style).pack(pady=2)

tk.Label(root, text="Your Reminders:", font=font_label, bg="#f0f4f7").pack(pady=10)
reminder_list = tk.Listbox(root, font=font_list, width=40, height=10, bd=2, relief="sunken", selectbackground="#94d2bd")
reminder_list.pack()

# Load saved reminders
for reminder in reminders:
    reminder_list.insert(tk.END, reminder)

check_reminders()

root.mainloop()

Added main application script


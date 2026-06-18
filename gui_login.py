import tkinter as tk
from tkinter import messagebox
import gui_dashboard

from database import get_connection


def check_login(username, password):
    conn = get_connection()
    cursor = conn.cursor()

    # Check password as plain text for user login
    cursor.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, password)
    )

    user = cursor.fetchone()
    conn.close()

    return user



def login():
    username = entry_user.get().strip()
    password = entry_pass.get().strip()

    user = check_login(username, password)

    if user:
        root.destroy()
        gui_dashboard.open_dashboard(username)
    else:
        messagebox.showerror("Login failed", "Invalid credentials")



def on_enter(e):
    e.widget['background'] = '#5a4fcf'


def on_leave(e):
    e.widget['background'] = '#6c5ce7'


# -------- WINDOW --------
root = tk.Tk()
root.title("Wordlist Generator - Login")
root.geometry("450x550")
root.resizable(False, False)
root.configure(bg="#1a1a2e")

# -------- HEADER FRAME --------
header_frame = tk.Frame(root, bg="#16213e", height=120)
header_frame.pack(fill="x")
header_frame.pack_propagate(False)

# Icon/Logo placeholder
icon_label = tk.Label(
    header_frame,
    text="🔐",
    font=("Arial", 40),
    bg="#16213e",
    fg="#6c5ce7"
)
icon_label.pack(pady=(20, 5))

title_label = tk.Label(
    header_frame,
    text="WORDLIST GENERATOR",
    font=("Arial", 16, "bold"),
    bg="#16213e",
    fg="#ffffff"
)
title_label.pack()

# -------- MAIN FRAME --------
main_frame = tk.Frame(root, bg="#1a1a2e")
main_frame.pack(expand=True, fill="both", padx=40, pady=30)

# Subtitle
subtitle = tk.Label(
    main_frame,
    text="Secure Access Portal",
    font=("Arial", 10),
    bg="#1a1a2e",
    fg="#a29bfe"
)
subtitle.pack(pady=(0, 30))

# -------- USERNAME FIELD --------
username_label = tk.Label(
    main_frame,
    text="Username",
    font=("Arial", 10, "bold"),
    bg="#1a1a2e",
    fg="#dfe6e9"
)
username_label.pack(anchor="w", pady=(0, 5))

username_frame = tk.Frame(main_frame, bg="#2d3436", highlightbackground="#6c5ce7", highlightthickness=2)
username_frame.pack(fill="x", pady=(0, 20))

entry_user = tk.Entry(
    username_frame,
    font=("Arial", 11),
    bg="#2d3436",
    fg="#ffffff",
    relief="flat",
    insertbackground="#6c5ce7",
    bd=0
)
entry_user.pack(padx=10, pady=8, fill="x")

# -------- PASSWORD FIELD --------
password_label = tk.Label(
    main_frame,
    text="Password",
    font=("Arial", 10, "bold"),
    bg="#1a1a2e",
    fg="#dfe6e9"
)
password_label.pack(anchor="w", pady=(0, 5))

password_frame = tk.Frame(main_frame, bg="#2d3436", highlightbackground="#6c5ce7", highlightthickness=2)
password_frame.pack(fill="x", pady=(0, 30))

entry_pass = tk.Entry(
    password_frame,
    font=("Arial", 11),
    bg="#2d3436",
    fg="#ffffff",
    relief="flat",
    show="●",
    insertbackground="#6c5ce7",
    bd=0
)
entry_pass.pack(padx=10, pady=8, fill="x")

# -------- LOGIN BUTTON --------
login_btn = tk.Button(
    main_frame,
    text="LOGIN",
    font=("Arial", 12, "bold"),
    bg="#6c5ce7",
    fg="#ffffff",
    activebackground="#5a4fcf",
    activeforeground="#ffffff",
    relief="flat",
    cursor="hand2",
    command=login,
    height=2
)
login_btn.pack(fill="x", pady=(10, 10))
login_btn.bind("<Enter>", on_enter)
login_btn.bind("<Leave>", on_leave)

# -------- FOOTER --------
footer = tk.Label(
    main_frame,
    text="Authorized Personnel Only",
    font=("Arial", 8),
    bg="#1a1a2e",
    fg="#636e72"
)
footer.pack(side="bottom", pady=(20, 0))

# Bind Enter key to login
entry_pass.bind("<Return>", lambda e: login())

root.mainloop()
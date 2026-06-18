import tkinter as tk
from tkinter import messagebox, scrolledtext
from generator import generate_wordlist_from_params
from utils import save_to_file
from database import save_wordlist, get_user_wordlists, get_wordlist_passwords, delete_wordlist, hash_password
import re


def open_dashboard(username):
    window = tk.Tk()
    window.title("Wordlist Generator - Dashboard")
    window.geometry("900x750")
    window.configure(bg="#0a0e27")
    window.resizable(True, True)
    
    # -------- HEADER --------
    header_frame = tk.Frame(window, bg="#2563eb", height=70)
    header_frame.pack(fill="x")
    header_frame.pack_propagate(False)

    header_left = tk.Frame(header_frame, bg="#2563eb")
    header_left.pack(side="left", padx=25, pady=20)

    welcome_label = tk.Label(
        header_left,
        text=f"👤 Welcome, {username}",
        font=("Arial", 15, "bold"),
        bg="#2563eb",
        fg="#ffffff"
    )
    welcome_label.pack(side="left")

    # History button
    history_btn = tk.Button(
        header_frame,
        text="📚 View History",
        font=("Arial", 10, "bold"),
        bg="#10b981",
        fg="#ffffff",
        relief="flat",
        cursor="hand2",
        command=lambda: show_history(username)
    )
    history_btn.pack(side="right", padx=25, pady=20)

    # Detect hash button
    detect_btn = tk.Button(
        header_frame,
        text="🔍 Detect Hash",
        font=("Arial", 10, "bold"),
        bg="#f59e0b",
        fg="#ffffff",
        relief="flat",
        cursor="hand2",
        command=lambda: open_detect_window()
    )
    detect_btn.pack(side="right", padx=10, pady=20)

    # -------- SCROLLABLE MAIN AREA --------
    canvas = tk.Canvas(window, bg="#0a0e27", highlightthickness=0)
    scrollbar = tk.Scrollbar(window, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="#0a0e27")

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True, padx=20)
    scrollbar.pack(side="right", fill="y")

    # -------- INPUT SECTION --------
    input_frame = tk.Frame(scrollable_frame, bg="#1e293b", highlightbackground="#3b82f6", highlightthickness=2)
    input_frame.pack(fill="x", pady=(15, 10), padx=5)

    input_inner = tk.Frame(input_frame, bg="#1e293b")
    input_inner.pack(padx=20, pady=15)

    section_title = tk.Label(
        input_inner,
        text="⚙️ Configuration",
        font=("Arial", 13, "bold"),
        bg="#1e293b",
        fg="#60a5fa"
    )
    section_title.pack(anchor="w", pady=(0, 12))

    # Keywords
    tk.Label(
        input_inner,
        text="Keywords (space separated)",
        font=("Arial", 10, "bold"),
        bg="#1e293b",
        fg="#e2e8f0"
    ).pack(anchor="w", pady=(0, 5))

    keywords_entry = tk.Entry(
        input_inner,
        font=("Arial", 10),
        bg="#334155",
        fg="#ffffff",
        relief="flat",
        insertbackground="#3b82f6",
        width=85
    )
    keywords_entry.pack(fill="x", pady=(0, 10), ipady=6)

    # Birthdate
    tk.Label(
        input_inner,
        text="Birthdate (YYYYMMDD)",
        font=("Arial", 10, "bold"),
        bg="#1e293b",
        fg="#e2e8f0"
    ).pack(anchor="w", pady=(0, 5))

    date_entry = tk.Entry(
        input_inner,
        font=("Arial", 10),
        bg="#334155",
        fg="#ffffff",
        relief="flat",
        insertbackground="#3b82f6",
        width=30
    )
    date_entry.pack(anchor="w", pady=(0, 10), ipady=6)

    # Min/Max Length
    length_frame = tk.Frame(input_inner, bg="#1e293b")
    length_frame.pack(anchor="w", fill="x")

    tk.Label(
        length_frame,
        text="Min Length",
        font=("Arial", 10, "bold"),
        bg="#1e293b",
        fg="#e2e8f0"
    ).pack(side="left", padx=(0, 10))

    min_entry = tk.Entry(
        length_frame,
        font=("Arial", 10),
        bg="#334155",
        fg="#ffffff",
        relief="flat",
        insertbackground="#3b82f6",
        width=10
    )
    min_entry.insert(0, "4")
    min_entry.pack(side="left", ipady=6, padx=(0, 25))

    tk.Label(
        length_frame,
        text="Max Length",
        font=("Arial", 10, "bold"),
        bg="#1e293b",
        fg="#e2e8f0"
    ).pack(side="left", padx=(0, 10))

    max_entry = tk.Entry(
        length_frame,
        font=("Arial", 10),
        bg="#334155",
        fg="#ffffff",
        relief="flat",
        insertbackground="#3b82f6",
        width=10
    )
    max_entry.insert(0, "12")
    max_entry.pack(side="left", ipady=6)

    # Hash algorithm selection
    hash_frame = tk.Frame(input_inner, bg="#1e293b")
    hash_frame.pack(anchor="w", pady=(10, 0))

    tk.Label(
        hash_frame,
        text="Hash Algorithm:",
        font=("Arial", 10, "bold"),
        bg="#1e293b",
        fg="#e2e8f0"
    ).pack(side="left", padx=(0, 10))

    hash_var = tk.StringVar(value="SHA256")
    tk.Radiobutton(hash_frame, text="MD5", variable=hash_var, value="MD5", bg="#1e293b", fg="#e2e8f0", selectcolor="#0a0e27").pack(side="left", padx=5)
    tk.Radiobutton(hash_frame, text="SHA256", variable=hash_var, value="SHA256", bg="#1e293b", fg="#e2e8f0", selectcolor="#0a0e27").pack(side="left", padx=5)
    tk.Radiobutton(hash_frame, text="SHA512", variable=hash_var, value="SHA512", bg="#1e293b", fg="#e2e8f0", selectcolor="#0a0e27").pack(side="left", padx=5)

    # -------- BUTTONS (RIGHT AFTER CONFIG) --------
    button_frame = tk.Frame(scrollable_frame, bg="#0a0e27")
    button_frame.pack(fill="x", pady=15, padx=5)

    def on_btn_enter(e):
        e.widget['background'] = '#1d4ed8'

    def on_btn_leave(e):
        e.widget['background'] = '#3b82f6'

    def on_export_enter(e):
        e.widget['background'] = '#047857'

    def on_export_leave(e):
        e.widget['background'] = '#10b981'

    def generate():
        keywords = keywords_entry.get().split()
        date = date_entry.get() or None

        try:
            min_len = int(min_entry.get())
            max_len = int(max_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Min and Max length must be numbers")
            return

        status_label.config(text="⏳ Generating wordlist...", fg="#fbbf24")
        window.update()

        passwords = generate_wordlist_from_params(
            keywords=keywords,
            date=date,
            min_len=min_len,
            max_len=max_len
        )

        # Show plaintext and hashed passwords in the interface according to selected algorithm
        selected_algo = hash_var.get()
        try:
            plaintext_box.delete("1.0", tk.END)
            hashed_box.delete("1.0", tk.END)
        except NameError:
            # UI not yet created or missing; fall back to single output_box
            pass

        for pwd in passwords:
            try:
                plaintext_box.insert(tk.END, pwd + "\n")
                hashed_box.insert(tk.END, hash_password(pwd, selected_algo) + "\n")
            except NameError:
                # fallback
                output_box.insert(tk.END, hash_password(pwd, selected_algo) + "\n")

        # Save to database
        try:
            # Save plaintext passwords; database will store hashed values using selected algorithm
            wordlist_id = save_wordlist(username, keywords, date, min_len, max_len, passwords, selected_algo)
            status_label.config(
                text=f"✅ {len(passwords)} passwords generated & saved to database (ID: {wordlist_id})", 
                fg="#22c55e"
            )
            messagebox.showinfo("Success", f"{len(passwords)} passwords generated and saved to database!")
        except Exception as e:
            status_label.config(text=f"⚠️ Generated but failed to save: {str(e)}", fg="#ef4444")
            messagebox.showwarning("Warning", f"Passwords generated but not saved to database:\n{str(e)}")

    def export():
        text = output_box.get("1.0", tk.END).strip()
        if not text:
            messagebox.showwarning("Empty", "No passwords to export")
            return

        passwords = text.split("\n")
        saved = save_to_file(passwords, "wordlist")
        if saved:
            status_label.config(text=f"💾 Wordlist saved to {saved}", fg="#60a5fa")
            messagebox.showinfo("Saved", f"Wordlist saved to {saved}")
        else:
            status_label.config(text="⚠️ Failed to save wordlist", fg="#ef4444")
            messagebox.showwarning("Error", "Failed to save wordlist to disk")

    def open_detect_window():
        dwin = tk.Toplevel(window)
        dwin.title("Detect Hash Algorithm")
        dwin.geometry("450x180")
        dwin.configure(bg="#0a0e27")

        tk.Label(
            dwin,
            text="Enter hashed password to detect algorithm:",
            font=("Arial", 11, "bold"),
            bg="#0a0e27",
            fg="#60a5fa"
        ).pack(pady=(12, 6))

        entry = tk.Entry(dwin, font=("Consolas", 12), width=60, bg="#0f172a", fg="#ffffff", insertbackground="#60a5fa")
        entry.pack(pady=(0, 10), padx=12)

        result_label = tk.Label(dwin, text="", font=("Arial", 11), bg="#0a0e27", fg="#94a3b8")
        result_label.pack(pady=(6, 0))

        def detect():
            h = entry.get().strip()
            if not h:
                messagebox.showwarning("Empty", "Please paste a hashed value")
                return
            # must be hex
            if not re.fullmatch(r"[0-9a-fA-F]+", h):
                result_label.config(text="Not a valid hex hash (contains invalid chars)", fg="#ef4444")
                return
            L = len(h)
            if L == 32:
                alg = "MD5"
            elif L == 64:
                alg = "SHA256"
            elif L == 128:
                alg = "SHA512"
            else:
                alg = "Unknown"
            result_label.config(text=f"Detected: {alg}", fg="#22c55e" if alg != "Unknown" else "#ef4444")

        tk.Button(dwin, text="Detect", command=detect, bg="#3b82f6", fg="#ffffff", font=("Arial", 10, "bold"), relief="flat").pack(pady=(6, 8))

    def show_history(user):
        """Show wordlist history window"""
        history_window = tk.Toplevel(window)
        history_window.title("Wordlist History")
        history_window.geometry("700x500")
        history_window.configure(bg="#0a0e27")

        tk.Label(
            history_window,
            text=f"📚 Wordlist History - {user}",
            font=("Arial", 14, "bold"),
            bg="#0a0e27",
            fg="#60a5fa"
        ).pack(pady=15)

        # Listbox with scrollbar
        list_frame = tk.Frame(history_window, bg="#1e293b")
        list_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        list_scrollbar = tk.Scrollbar(list_frame)
        list_scrollbar.pack(side="right", fill="y")

        history_list = tk.Listbox(
            list_frame,
            font=("Consolas", 10),
            bg="#334155",
            fg="#ffffff",
            selectbackground="#3b82f6",
            yscrollcommand=list_scrollbar.set,
            height=15
        )
        history_list.pack(side="left", fill="both", expand=True)
        list_scrollbar.config(command=history_list.yview)

        # Load wordlists
        wordlists = get_user_wordlists(user)
        for wl in wordlists:
            # wl: id, keywords, birthdate, password_count, created_at, hash_algorithm
            wl_id, keywords, birthdate, count, created, algo = wl
            display_text = f"ID:{wl_id} | {created} | {count} passwords | Algo: {algo} | Keywords: {keywords}"
            history_list.insert(tk.END, display_text)

        def view_selected():
            selection = history_list.curselection()
            if not selection:
                messagebox.showwarning("No Selection", "Please select a wordlist")
                return
            
            wl_id = wordlists[selection[0]][0]
            password_hashes = get_wordlist_passwords(wl_id)
            
            # Show in new window
            view_window = tk.Toplevel(history_window)
            view_window.title(f"Wordlist #{wl_id} - HASHED")
            view_window.geometry("650x450")
            view_window.configure(bg="#0a0e27")
            
            tk.Label(
                view_window,
                text="🔒 Passwords are stored HASHED for security",
                font=("Arial", 11, "bold"),
                bg="#0a0e27",
                fg="#fbbf24"
            ).pack(pady=10)
            
            text_box = scrolledtext.ScrolledText(
                view_window,
                font=("Consolas", 8),
                bg="#0f172a",
                fg="#fbbf24"
            )
            text_box.pack(fill="both", expand=True, padx=10, pady=(0, 10))
            
            for pwd_hash in password_hashes:
                text_box.insert(tk.END, pwd_hash + "\n")

        def delete_selected():
            selection = history_list.curselection()
            if not selection:
                messagebox.showwarning("No Selection", "Please select a wordlist")
                return
            
            wl_id = wordlists[selection[0]][0]
            if messagebox.askyesno("Confirm Delete", f"Delete wordlist #{wl_id}?"):
                delete_wordlist(wl_id)
                history_window.destroy()
                show_history(user)

        # Buttons
        btn_frame = tk.Frame(history_window, bg="#0a0e27")
        btn_frame.pack(pady=(0, 20))

        tk.Button(
            btn_frame,
            text="👁️ View",
            font=("Arial", 10, "bold"),
            bg="#3b82f6",
            fg="#ffffff",
            command=view_selected,
            width=15
        ).pack(side="left", padx=5)

        tk.Button(
            btn_frame,
            text="🗑️ Delete",
            font=("Arial", 10, "bold"),
            bg="#ef4444",
            fg="#ffffff",
            command=delete_selected,
            width=15
        ).pack(side="left", padx=5)

    generate_btn = tk.Button(
        button_frame,
        text="🚀 GENERATE WORDLIST",
        font=("Arial", 12, "bold"),
        bg="#3b82f6",
        fg="#ffffff",
        activebackground="#1d4ed8",
        activeforeground="#ffffff",
        relief="flat",
        cursor="hand2",
        command=generate,
        height=2,
        bd=0
    )
    generate_btn.pack(side="left", fill="x", expand=True, padx=(0, 8))
    generate_btn.bind("<Enter>", on_btn_enter)
    generate_btn.bind("<Leave>", on_btn_leave)

    export_plain_btn = tk.Button(
        button_frame,
        text="💾 EXPORT PLAINTEXT",
        font=("Arial", 12, "bold"),
        bg="#10b981",
        fg="#ffffff",
        activebackground="#047857",
        activeforeground="#ffffff",
        relief="flat",
        cursor="hand2",
        command=export,
        height=2,
        bd=0
    )
    export_plain_btn.pack(side="left", fill="x", expand=True, padx=(0,8))
    export_plain_btn.bind("<Enter>", on_export_enter)
    export_plain_btn.bind("<Leave>", on_export_leave)

    def export_hashed():
        # Export hashed column
        try:
            text = hashed_box.get("1.0", tk.END).strip()
        except NameError:
            # fall back to output_box if present
            text = output_box.get("1.0", tk.END).strip()
        if not text:
            messagebox.showwarning("Empty", "No hashed passwords to export")
            return
        items = text.split("\n")
        saved = save_to_file(items, "wordlist_hashed")
        if saved:
            status_label.config(text=f"💾 Hashed wordlist saved to {saved}", fg="#60a5fa")
            messagebox.showinfo("Saved", f"Hashed wordlist saved to {saved}")
        else:
            status_label.config(text="⚠️ Failed to save hashed wordlist", fg="#ef4444")
            messagebox.showwarning("Error", "Failed to save hashed wordlist to disk")

    export_hashed_btn = tk.Button(
        button_frame,
        text="🔐 EXPORT HASHED",
        font=("Arial", 12, "bold"),
        bg="#f97316",
        fg="#ffffff",
        activebackground="#ea580c",
        activeforeground="#ffffff",
        relief="flat",
        cursor="hand2",
        command=export_hashed,
        height=2,
        bd=0
    )
    export_hashed_btn.pack(side="left", fill="x", expand=True)
    export_hashed_btn.bind("<Enter>", lambda e: e.widget.config(background="#ea580c"))
    export_hashed_btn.bind("<Leave>", lambda e: e.widget.config(background="#f97316"))

    # -------- OUTPUT SECTION --------
    output_frame = tk.Frame(scrollable_frame, bg="#1e293b", highlightbackground="#3b82f6", highlightthickness=2)
    output_frame.pack(fill="both", expand=True, pady=(10, 20), padx=5)

    output_label = tk.Label(
        output_frame,
        text="📋 Generated Wordlist (Plaintext | Hashed)",
        font=("Arial", 13, "bold"),
        bg="#1e293b",
        fg="#60a5fa"
    )
    output_label.pack(anchor="w", padx=20, pady=(12, 8))

    # Two-column output: left=plaintext, right=hashed
    cols_frame = tk.Frame(output_frame, bg="#1e293b")
    cols_frame.pack(padx=20, pady=(0, 10), fill="both", expand=True)

    left_frame = tk.Frame(cols_frame, bg="#1e293b")
    left_frame.pack(side="left", fill="both", expand=True, padx=(0, 8))

    tk.Label(left_frame, text="Plaintext", font=("Arial", 10, "bold"), bg="#1e293b", fg="#60a5fa").pack(anchor="w")
    plaintext_box = scrolledtext.ScrolledText(
        left_frame,
        font=("Consolas", 9),
        bg="#0f172a",
        fg="#22c55e",
        relief="flat",
        insertbackground="#3b82f6",
        wrap="none",
        height=12
    )
    plaintext_box.pack(fill="both", expand=True)

    right_frame = tk.Frame(cols_frame, bg="#1e293b")
    right_frame.pack(side="left", fill="both", expand=True, padx=(8, 0))

    tk.Label(right_frame, text="Hashed", font=("Arial", 10, "bold"), bg="#1e293b", fg="#60a5fa").pack(anchor="w")
    hashed_box = scrolledtext.ScrolledText(
        right_frame,
        font=("Consolas", 9),
        bg="#0f172a",
        fg="#fbbf24",
        relief="flat",
        insertbackground="#3b82f6",
        wrap="none",
        height=12
    )
    hashed_box.pack(fill="both", expand=True)

    # Status label
    status_label = tk.Label(
        output_frame,
        text="Ready to generate...",
        font=("Arial", 9),
        bg="#1e293b",
        fg="#94a3b8"
    )
    status_label.pack(anchor="w", padx=20, pady=(0, 12))

    # Enable mousewheel scrolling
    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    canvas.bind_all("<MouseWheel>", _on_mousewheel)

    window.mainloop()
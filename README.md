# 🔐 Custom Password Wordlist Generator

> A Python-based security auditing tool that generates targeted, personalized wordlists for ethical penetration testing and password auditing purposes.

---

## 📌 Context

This project was developed as part of the **Cybersecurity and Information Systems** curriculum at **TEK-UP Engineering School** (Academic Year 2025/2026).

**Authors:** Ameni Fayech · Ranim Naat

---

## 🎯 Problem Statement

Generic wordlists like `rockyou.txt` are widely used in security audits, but they fail to account for personal or contextual information specific to a target system or user. This tool addresses that gap by generating **custom, targeted wordlists** based on real-world social engineering factors.

---

## ✨ Features

- 🔑 **Targeted generation** — create wordlists from names, birthdates, and custom keywords
- 🔄 **Mutation rules** — capitalization, character substitution (e.g. `a → @`), number and symbol appending
- 🔐 **Multiple hash algorithms** — MD5, SHA256, SHA512
- 📤 **Export options** — plaintext `.txt` or hashed wordlist
- 📜 **Generation history** — all sessions saved with timestamps in SQLite
- 🔍 **Hash detector** — identify the algorithm used to hash any given string
- 🖥️ **GUI interface** — built with Tkinter for ease of use
- ⚡ **Performance optimized** — controlled memory usage with `itertools`

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.x |
| GUI | Tkinter |
| Database | SQLite |
| Core Logic | `itertools`, `argparse`, `hashlib` |
| Modeling | UML (Draw.io) |
| Version Control | Git / GitHub |

---

## 🏗️ Architecture

The project follows a **layered architecture**:

- **GUI Layer** — `LoginGUI`, `DashboardGUI`
- **Business Logic** — `AuthManager`, `WordlistGenerator`, `HashingService`
- **Persistence Layer** — `DatabaseManager` (SQLite)
- **Export** — `FileExporter` (plaintext / hashed `.txt`)

Full UML diagrams (Use Case, Class, Sequence, Deployment, Component) are available in the project report.

---

## 🚀 Getting Started

### Prerequisites
```bash
Python 3.x
```
All libraries used (`tkinter`, `sqlite3`, `hashlib`, `itertools`) are built into Python — **no external dependencies needed**.

### Run the app
```bash
git clone https://github.com/amenifayech2/wordlist-generator.git
cd wordlist-generator
python wordlist_gui.py
```

### Default credentials (first run)
```
Username: admin
Password: admin123
```

---

## 📁 Project Structure

```
wordlist-generator/
│
├── wordlist_gui.py        # Main application entry point
├── auth.py                # Authentication manager
├── database.py            # SQLite database handler
├── generator.py           # Core wordlist generation logic
├── config.json            # Mutation rules configuration
│
├── screenshots/           # UI screenshots
│   ├── login.png
│   ├── dashboard.png
│   ├── history.png
│   └── detect_hash.png
│
└── report/
    └── RAPPORT_PYTHON.pdf # Full project report
```

---

## 📄 Report

The full technical report is available in (Project's report/.pdf).

It includes: project framework, requirements specification, UML diagrams (use case, class, sequence, deployment, component), work environment, and interface demonstrations.

---

## ⚠️ Disclaimer

This tool is developed **strictly for educational and ethical security auditing purposes**.  
It must only be used in **controlled environments** with explicit authorization.  
The authors take no responsibility for any misuse of this tool.

---

## 📜 License

MIT License — © 2025 Ameni Fayech & Ranim Naat  
You are free to use, modify, and distribute this project with attribution.


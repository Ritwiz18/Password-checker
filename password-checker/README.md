# 🔐 Password Strength Analyzer

A professional Python desktop application that analyzes password security in real-time.

## ✨ Features

| Feature | Description |
|---------|-------------|
| **Real-time Analysis** | Instant feedback as you type |
| **Entropy Calculation** | Shannon entropy in bits (L × log₂(N)) |
| **Strength Meter** | Animated visual progress bar |
| **Smart Suggestions** | Actionable tips to improve your password |
| **Checklist** | 7-point validation checklist |
| **Crack Time Estimate** | Brute-force time estimation |
| **Password Generator** | One-click strong password generation |
| **Copy to Clipboard** | Quick copy with visual feedback |
| **Dark Mode UI** | Modern, premium dark theme |

## 🚀 How to Run

```bash
cd password-checker
python main.py
```

No external dependencies — uses only Python standard library (`tkinter`, `re`, `math`, `string`, `random`).

## 📐 Entropy Formula

```
Entropy = L × log₂(N)
```

- **L** = Password length
- **N** = Character pool size (26 lowercase + 26 uppercase + 10 digits + 32 symbols)

## 🎯 Scoring System (7 Points)

1. ✅ At least 8 characters
2. ✅ 12+ characters (recommended)
3. ✅ Contains uppercase (A-Z)
4. ✅ Contains lowercase (a-z)
5. ✅ Contains numbers (0-9)
6. ✅ Contains special characters
7. ✅ Not a commonly used password

## 📁 Project Structure

```
password-checker/
├── main.py            # Main application (GUI + logic)
├── requirements.txt   # Dependencies (none needed)
└── README.md          # This file
```

## 🖼️ Tech Stack

- **Language:** Python 3
- **GUI:** Tkinter (built-in)
- **Validation:** Regular Expressions
- **Math:** Shannon Entropy

## 📝 Resume Description

> **Password Strength Analyzer** — Developed a Python-based GUI application to analyze password security. Implemented Shannon entropy calculation and a password recommendation system with real-time feedback. Built with Tkinter featuring a modern dark-mode interface, animated strength meter, and one-click strong password generator.

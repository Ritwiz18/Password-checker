"""
Password Strength Analyzer
===========================
A clean, simple GUI application using Tkinter.
Features: strength scoring, entropy calculation, suggestions, and password generator.
"""

import tkinter as tk
from tkinter import messagebox
import re
import math
import string
import random


# ─────────────────────────────────────────────
# Password Analysis Logic
# ─────────────────────────────────────────────
def calculate_entropy(password):
    """Entropy = L × log2(N) where L=length, N=character pool size."""
    if not password:
        return 0.0
    pool = 0
    if any(c.islower() for c in password):
        pool += 26
    if any(c.isupper() for c in password):
        pool += 26
    if any(c.isdigit() for c in password):
        pool += 10
    if any(c in string.punctuation for c in password):
        pool += 32
    if pool == 0:
        return 0.0
    return len(password) * math.log2(pool)


def analyze_password(password):
    """Analyze password and return score, label, suggestions, entropy."""
    if not password:
        return 0, "—", [], 0.0, {}

    suggestions = []
    checks = {}
    score = 0

    # Length
    checks["8+ characters"] = len(password) >= 8
    checks["12+ characters"] = len(password) >= 12
    if len(password) >= 8:
        score += 1
    else:
        suggestions.append("• Use at least 8 characters")
    if len(password) >= 12:
        score += 1
    elif len(password) >= 8:
        suggestions.append("• Try 12+ characters for better security")

    # Character types
    checks["Uppercase (A-Z)"] = bool(re.search(r"[A-Z]", password))
    checks["Lowercase (a-z)"] = bool(re.search(r"[a-z]", password))
    checks["Numbers (0-9)"] = bool(re.search(r"[0-9]", password))
    checks["Symbols (!@#$%)"] = bool(re.search(r"[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>/?~`]", password))

    if checks["Uppercase (A-Z)"]:
        score += 1
    else:
        suggestions.append("• Add uppercase letters (A-Z)")
    if checks["Lowercase (a-z)"]:
        score += 1
    else:
        suggestions.append("• Add lowercase letters (a-z)")
    if checks["Numbers (0-9)"]:
        score += 1
    else:
        suggestions.append("• Add numbers (0-9)")
    if checks["Symbols (!@#$%)"]:
        score += 1
    else:
        suggestions.append("• Add special characters (!@#$%^&*)")

    # Common password check
    common = {"password", "123456", "12345678", "qwerty", "abc123",
              "letmein", "admin", "welcome", "monkey", "dragon",
              "master", "login", "password1", "password123", "iloveyou"}
    checks["Not common"] = password.lower() not in common
    if checks["Not common"]:
        score += 1
    else:
        suggestions.insert(0, "⚠ This is a commonly used password!")

    # Entropy
    entropy = calculate_entropy(password)

    # Label
    if password.lower() in common:
        label = "Very Weak"
    elif score <= 2:
        label = "Weak"
    elif score <= 4:
        label = "Fair"
    elif score <= 5:
        label = "Good"
    else:
        label = "Strong"

    return score, label, suggestions, entropy, checks


def generate_password(length=16):
    """Generate a strong random password."""
    chars = [
        random.choice(string.ascii_uppercase),
        random.choice(string.ascii_lowercase),
        random.choice(string.digits),
        random.choice("!@#$%^&*()_+-="),
    ]
    pool = string.ascii_letters + string.digits + "!@#$%^&*()_+-="
    chars += [random.choice(pool) for _ in range(length - 4)]
    random.shuffle(chars)
    return "".join(chars)


# ─────────────────────────────────────────────
# GUI Application
# ─────────────────────────────────────────────
class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Password Strength Checker")
        self.root.configure(bg="#1a1a2e")
        self.root.resizable(False, False)

        # Center on screen
        w, h = 460, 560
        x = (self.root.winfo_screenwidth() - w) // 2
        y = (self.root.winfo_screenheight() - h) // 2
        self.root.geometry(f"{w}x{h}+{x}+{y}")

        self.showing_pw = False
        self._build()

    def _build(self):
        bg = "#1a1a2e"
        fg_main = "#e0e0e0"
        fg_dim = "#888aaa"
        accent = "#00d4aa"
        pad = 24

        # ── Title ──
        tk.Label(
            self.root, text="🔐 Password Strength Checker",
            font=("Segoe UI", 16, "bold"), bg=bg, fg=fg_main
        ).pack(pady=(pad, 4))

        tk.Label(
            self.root, text="Check strength, entropy & get suggestions",
            font=("Segoe UI", 10), bg=bg, fg=fg_dim
        ).pack()

        # ── Input Frame ──
        input_frame = tk.Frame(self.root, bg=bg)
        input_frame.pack(padx=pad, pady=(18, 0), fill="x")

        tk.Label(input_frame, text="Enter Password:", font=("Segoe UI", 10),
                 bg=bg, fg=fg_dim).pack(anchor="w")

        entry_row = tk.Frame(input_frame, bg=bg)
        entry_row.pack(fill="x", pady=(4, 0))

        self.entry = tk.Entry(entry_row, font=("Consolas", 12), show="●", width=28,
                              bg="#16213e", fg=fg_main, insertbackground=accent,
                              relief="flat")
        self.entry.pack(side="left", fill="x", expand=True, ipady=4)
        self.entry.bind("<KeyRelease>", self._update)

        self.eye_btn = tk.Button(entry_row, text="👁", font=("Segoe UI", 11),
                                  relief="flat", bg="#16213e", fg=fg_dim,
                                  cursor="hand2", command=self._toggle_show)
        self.eye_btn.pack(side="left", padx=(4, 0))

        # ── Strength Bar ──
        bar_frame = tk.Frame(self.root, bg=bg)
        bar_frame.pack(padx=pad, pady=(12, 0), fill="x")

        self.bar_canvas = tk.Canvas(bar_frame, height=12, bg="#2a2a4a",
                                     highlightthickness=0)
        self.bar_canvas.pack(fill="x")

        # ── Strength & Entropy Row ──
        info_frame = tk.Frame(self.root, bg=bg)
        info_frame.pack(padx=pad, pady=(8, 0), fill="x")

        self.strength_lbl = tk.Label(info_frame, text="Strength: —",
                                      font=("Segoe UI", 11, "bold"), bg=bg, fg=fg_dim)
        self.strength_lbl.pack(side="left")

        self.entropy_lbl = tk.Label(info_frame, text="Entropy: 0.00 bits",
                                     font=("Segoe UI", 10), bg=bg, fg=fg_dim)
        self.entropy_lbl.pack(side="right")

        # ── Score ──
        self.score_lbl = tk.Label(self.root, text="Score: 0 / 7",
                                   font=("Segoe UI", 10), bg=bg, fg=fg_dim)
        self.score_lbl.pack(padx=pad, anchor="w", pady=(4, 0))

        # ── Checklist ──
        tk.Label(self.root, text="Checks:", font=("Segoe UI", 10, "bold"),
                 bg=bg, fg=fg_main).pack(padx=pad, anchor="w", pady=(14, 4))

        self.checks_frame = tk.Frame(self.root, bg=bg)
        self.checks_frame.pack(padx=pad + 8, fill="x")

        self.check_labels = {}
        for name in ["8+ characters", "12+ characters", "Uppercase (A-Z)",
                      "Lowercase (a-z)", "Numbers (0-9)", "Symbols (!@#$%)", "Not common"]:
            lbl = tk.Label(self.checks_frame, text=f"  ○  {name}",
                           font=("Segoe UI", 9), bg=bg, fg=fg_dim, anchor="w")
            lbl.pack(fill="x", pady=1)
            self.check_labels[name] = lbl

        # ── Suggestions ──
        tk.Label(self.root, text="Suggestions:", font=("Segoe UI", 10, "bold"),
                 bg=bg, fg=fg_main).pack(padx=pad, anchor="w", pady=(14, 4))

        self.suggestions_lbl = tk.Label(
            self.root, text="Type a password to begin.",
            font=("Segoe UI", 9), bg=bg, fg=fg_dim,
            anchor="w", justify="left", wraplength=400
        )
        self.suggestions_lbl.pack(padx=pad + 8, fill="x")

        # ── Buttons ──
        btn_frame = tk.Frame(self.root, bg=bg)
        btn_frame.pack(padx=pad, pady=(18, 0), fill="x")

        tk.Button(
            btn_frame, text="⚡ Generate Password", font=("Segoe UI", 10, "bold"),
            bg="#00d4aa", fg="#1a1a2e", activebackground="#00b894",
            relief="flat", cursor="hand2", padx=12, pady=6,
            command=self._gen
        ).pack(side="left", fill="x", expand=True, padx=(0, 4))

        tk.Button(
            btn_frame, text="📋 Copy", font=("Segoe UI", 10, "bold"),
            bg="#2a2a4a", fg=fg_main, activebackground="#3a3a5a",
            relief="flat", cursor="hand2", padx=12, pady=6,
            command=self._copy
        ).pack(side="right")

    # ── Update on keystroke ──
    def _update(self, event=None):
        pw = self.entry.get()
        score, label, suggestions, entropy, checks = analyze_password(pw)

        # Colors for strength levels
        colors = {
            "—": "#555", "Very Weak": "#ff4757", "Weak": "#ff4757",
            "Fair": "#ffa502", "Good": "#2ed573", "Strong": "#00d4aa"
        }
        color = colors.get(label, "#aaa")

        # Update bar
        self.bar_canvas.delete("all")
        if pw:
            fill_w = (score / 7) * self.bar_canvas.winfo_width()
            self.bar_canvas.create_rectangle(0, 0, fill_w, 12, fill=color, outline="")

        # Update labels
        self.strength_lbl.config(text=f"Strength: {label}", fg=color)
        self.entropy_lbl.config(text=f"Entropy: {entropy:.2f} bits")
        self.score_lbl.config(text=f"Score: {score} / 7")

        # Update checklist
        for name, lbl in self.check_labels.items():
            if name in checks and checks[name]:
                lbl.config(text=f"  ✓  {name}", fg="#2ed573")
            else:
                lbl.config(text=f"  ✗  {name}", fg="#444466")

        # Update suggestions
        if not pw:
            self.suggestions_lbl.config(text="Type a password to begin.", fg="#888aaa")
        elif suggestions:
            self.suggestions_lbl.config(text="\n".join(suggestions), fg="#ffa502")
        else:
            self.suggestions_lbl.config(text="✅ Your password is strong!", fg="#00d4aa")

    def _toggle_show(self):
        self.showing_pw = not self.showing_pw
        self.entry.config(show="" if self.showing_pw else "●")
        self.eye_btn.config(text="🔒" if self.showing_pw else "👁")

    def _gen(self):
        pw = generate_password(16)
        self.entry.delete(0, tk.END)
        self.entry.insert(0, pw)
        self.showing_pw = True
        self.entry.config(show="")
        self.eye_btn.config(text="🔒")
        self._update()

    def _copy(self):
        pw = self.entry.get()
        if pw:
            self.root.clipboard_clear()
            self.root.clipboard_append(pw)
            messagebox.showinfo("Copied", "Password copied to clipboard!")

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    App().run()

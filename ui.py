import tkinter as tk
from tkinter import messagebox
import time

from data import generate_paragraph
from logic import calculate_wpm_accuracy, highlight_errors
from storage import save_result, get_leaderboard, export_pdf
from utils import plot_progress

class TypingSpeedApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Typing Speed Test")
        self.master.geometry("900x650")
        self.master.configure(bg="#f0f4f8")
        self.theme = "light"
        self.reset_data()
        self.show_start_screen()

    def reset_data(self):
        self.start_time = None
        self.typed = False
        self.progress = []
        self.countdown_seconds = 60
        self.elapsed_seconds = 0
        self.username = tk.StringVar()
        self.difficulty = tk.StringVar(value="Easy")

    # ─── Welcome Screen ───────────────────────────────────────────────────────
    def show_start_screen(self):
        for widget in self.master.winfo_children():
            widget.destroy()

        tk.Label(self.master, text="Welcome to Typing Speed Test", font=("Arial", 20, "bold"), bg="#f0f4f8").pack(pady=20)

        tk.Label(self.master, text="Enter Your Name:", font=("Arial", 12), bg="#f0f4f8").pack(pady=(10, 2))
        tk.Entry(self.master, textvariable=self.username, font=("Arial", 12)).pack(pady=(0, 10))

        tk.Label(self.master, text="Select Difficulty:", font=("Arial", 12), bg="#f0f4f8").pack(pady=(10, 2))
        mode_menu = tk.OptionMenu(self.master, self.difficulty, "Easy", "Medium", "Hard")
        mode_menu.config(font=("Arial", 11))
        mode_menu.pack(pady=(0, 20))

        tk.Button(self.master, text="Start Typing", font=("Arial", 13), bg="#4caf50", fg="white", width=15, command=self.start_typing_test).pack()

    # ─── Typing Screen ───────────────────────────────────────────────────────
    def start_typing_test(self):
        if not self.username.get().strip():
            messagebox.showerror("Missing Info", "Please enter your name.")
            return

        self.current_text = generate_paragraph(self.difficulty.get())
        self.build_typing_screen()

    def build_typing_screen(self):
        for widget in self.master.winfo_children():
            widget.destroy()

        self.typed = False
        self.start_time = None

        tk.Label(self.master, text=f"Typing Test - {self.difficulty.get()} Mode", font=("Arial", 18, "bold"), bg="#f0f4f8").pack(pady=10)
        tk.Label(self.master, text=f"Name: {self.username.get()}", font=("Arial", 12), bg="#f0f4f8").pack()

        self.timer_label = tk.Label(self.master, text="Time left: 60", font=("Arial", 12), bg="#f0f4f8")
        self.timer_label.pack(pady=5)

        self.text_label = tk.Label(self.master, text=self.current_text, wraplength=800, font=("Consolas", 14), bg="#ffffff", fg="#333", relief="groove", bd=2)
        self.text_label.pack(pady=10, padx=10, fill="x")

        self.entry = tk.Text(self.master, height=6, width=100, font=("Consolas", 14), bg="#eef2fa", fg="#222", bd=2, relief="sunken")
        self.entry.pack(pady=10, padx=10)
        self.entry.bind("<KeyRelease>", self.on_type)

        self.live_wpm = tk.Label(self.master, text="WPM: 0", font=("Arial", 12, "bold"), bg="#f0f4f8")
        self.live_wpm.pack()
        self.live_acc = tk.Label(self.master, text="Accuracy: 100%", font=("Arial", 12, "bold"), bg="#f0f4f8")
        self.live_acc.pack()

        self.elapsed_label = tk.Label(self.master, text="Elapsed Time: 0s", font=("Arial", 12), bg="#f0f4f8")
        self.elapsed_label.pack()
        self.word_count_label = tk.Label(self.master, text="Words Typed: 0", font=("Arial", 12), bg="#f0f4f8")
        self.word_count_label.pack()
        
        btn_frame = tk.Frame(self.master, bg="#f0f4f8")
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Submit", command=self.submit_test, font=("Arial", 11)).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Reset", command=self.reset_test, font=("Arial", 11)).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Progress Chart", command=lambda: plot_progress(self.progress), font=("Arial", 11)).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Leaderboard", command=self.show_leaderboard, font=("Arial", 11)).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Export PDF", command=self.export_pdf_report, font=("Arial", 11)).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Main Menu", command=self.show_start_screen, font=("Arial", 11)).pack(side=tk.LEFT, padx=5)

        self.result_label = tk.Label(self.master, text="", font=("Arial", 13, "bold"), bg="#f0f4f8", fg="#444")
        self.result_label.pack(pady=10)

    # ─── Typing Logic ───────────────────────────────────────────────────────
    def on_type(self, event):
        if not self.typed:
            self.start_time = time.time()
            self.typed = True
            self.countdown(self.countdown_seconds)
            self.update_elapsed_timer()

        typed_text = self.entry.get("1.0", tk.END).strip()
        highlight_errors(self.entry, typed_text, self.current_text)
        self.update_live_stats(typed_text)

    def update_live_stats(self, typed_text):
        if not self.start_time:
            return
        wpm, acc = calculate_wpm_accuracy(self.start_time, typed_text, self.current_text)
        self.live_wpm.config(text=f"WPM: {wpm}")
        self.live_acc.config(text=f"Accuracy: {acc}%")
        word_count = len(typed_text.strip().split())
        self.word_count_label.config(text=f"Words Typed: {word_count}")

    def countdown(self, seconds):
        if seconds > 0:
            self.timer_label.config(text=f"Time left: {seconds}")
            self.master.after(1000, lambda: self.countdown(seconds - 1))
        else:
            self.submit_test()

    def update_elapsed_timer(self):
        if self.typed:
           self.elapsed_seconds += 1
           self.elapsed_label.config(text=f"Elapsed Time: {self.elapsed_seconds}s")
           self.master.after(1000, self.update_elapsed_timer)

    def submit_test(self):
        if not self.start_time:
            messagebox.showinfo("Error", "Please start typing first.")
            return

        typed_text = self.entry.get("1.0", tk.END).strip()
        wpm, acc = calculate_wpm_accuracy(self.start_time, typed_text, self.current_text)
        name = self.username.get() or "Anonymous"
        save_result(name, wpm, acc)

        self.progress.append((wpm, acc))
        self.result_label.config(text=f"Final Speed: {wpm} WPM | Accuracy: {acc}%")

    def reset_test(self):
        self.start_typing_test()

    def show_leaderboard(self):
        top = get_leaderboard()
        if top is None:
            messagebox.showerror("Error", "No leaderboard data available.")
            return
        msg = "\n".join(f"{row['Name']} - {row['WPM']} WPM" for _, row in top.iterrows())
        messagebox.showinfo("Top 5 Leaderboard", msg)

    def export_pdf_report(self):
        if not self.progress:
            messagebox.showinfo("Info", "Please complete a test first.")
            return
        name = self.username.get() or "Anonymous"
        last_wpm, last_acc = self.progress[-1]
        export_pdf(name, last_wpm, last_acc)
        messagebox.showinfo("PDF Saved", "Report saved as 'typing_report.pdf'")

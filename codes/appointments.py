import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime
import os
from language import LanguageManager


def pet_id_exists_in_db(pet_id):
    with sqlite3.connect(os.path.join('db', 'clinic.db')) as conn:
        cur = conn.cursor()
        cur.execute("SELECT 1 FROM Pets WHERE pet_id = ?", (pet_id,))
        return cur.fetchone() is not None


class AppointmentFrame(tk.Frame):

    def __init__(self, parent, controller, role=None):
        super().__init__(parent)
        self.controller = controller
        self.role = role
        self.selected_app_id = None
        self.clinic_db = os.path.join('db', 'clinic.db')

        self.title = tk.Label(self, font=("Arial", 18, "bold"))
        self.title.pack(pady=10)

        form = tk.Frame(self)
        form.pack(pady=5)

        keys = ["pet_id", "date", "time", "description"]
        self.labels = {}
        self.entries = {}

        for i, key in enumerate(keys):
            lbl = tk.Label(form)
            lbl.grid(row=i, column=0, padx=10, pady=4, sticky="w")

            entry = tk.Entry(form, width=30)
            entry.grid(row=i, column=1)

            self.labels[key] = lbl
            self.entries[key] = entry

        btns = tk.Frame(self)
        btns.pack(pady=5)

        self.add_btn = tk.Button(btns, width=10, command=self.add)
        self.update_btn = tk.Button(btns, width=10, command=self.update)
        self.delete_btn = tk.Button(btns, width=10, command=self.delete)

        self.add_btn.grid(row=0, column=0, padx=5)
        self.update_btn.grid(row=0, column=1, padx=5)
        self.delete_btn.grid(row=0, column=2, padx=5)

        search_frame = tk.Frame(self)
        search_frame.pack(pady=5)

        self.search_label = tk.Label(search_frame)
        self.search_label.grid(row=0, column=0)

        self.search_entry = tk.Entry(search_frame, width=25)
        self.search_entry.grid(row=0, column=1, padx=5)

        self.search_btn = tk.Button(search_frame, command=self.search)
        self.today_btn = tk.Button(search_frame, command=self.show_today)

        self.search_btn.grid(row=0, column=2)
        self.today_btn.grid(row=0, column=3)

        self.listbox = tk.Listbox(self, width=100)
        self.listbox.pack(pady=10)
        self.listbox.bind("<<ListboxSelect>>", self.select)

        self.back_btn = tk.Button(self, command=lambda: controller.show_frame("DashboardFrame"))
        self.back_btn.pack(pady=10)

        self.init_db()
        self.load()

        if self.role: self.apply_role(self.role)

        self.update_texts()


    def apply_role(self, role):
        self.role = role
        if role == "veterinarian":
            self.add_btn.config(state="disabled")
            self.update_btn.config(state="disabled")
            self.delete_btn.config(state="disabled")
        else:
            self.add_btn.config(state="normal")
            self.update_btn.config(state="normal")
            self.delete_btn.config(state="normal")

    
    def init_db(self):
        with sqlite3.connect(self.clinic_db) as conn:
            cur = conn.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS Appointments (
                    app_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    pet_id INTEGER NOT NULL,
                    date TEXT NOT NULL,
                    time TEXT NOT NULL,
                    description TEXT,
                    status TEXT DEFAULT 'Scheduled'
                )
            """)

    
    def clear_form(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)
        self.selected_app_id = None

    def has_conflict(self, pet_id, date, time):
        with sqlite3.connect(self.clinic_db) as conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT 1 FROM Appointments
                WHERE pet_id=? AND date=? AND time=? AND status='Scheduled'
            """, (pet_id, date, time))
            return cur.fetchone() is not None

    
    def add(self):
        t = self.controller.language.translate

        pet_id = self.entries["pet_id"].get()
        date = self.entries["date"].get()
        time = self.entries["time"].get()
        desc = self.entries["description"].get()

        if not pet_id.isdigit():
            messagebox.showerror(t("error"), t("pet_id_numeric")); return

        if not pet_id_exists_in_db(int(pet_id)):
            messagebox.showerror(t("error"), t("pet_not_found")); return

        try:
            if datetime.strptime(date, "%Y-%m-%d").date() < datetime.today().date():
                messagebox.showerror(t("error"), t("past_date_not_allowed")); return
            datetime.strptime(time, "%H:%M")
        except ValueError:
            messagebox.showerror(t("error"), t("invalid_date_time")); return

        if self.has_conflict(pet_id, date, time):
            messagebox.showerror(t("error"), t("appointment_conflict")); return

        with sqlite3.connect(self.clinic_db) as conn:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO Appointments (pet_id, date, time, description)
                VALUES (?, ?, ?, ?)
            """, (pet_id, date, time, desc))

        self.load()
        self.clear_form()


    def load(self):
        self.listbox.delete(0, tk.END)
        with sqlite3.connect(self.clinic_db) as conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT * FROM Appointments
                WHERE status='Scheduled'
                ORDER BY date, time
            """)
            for row in cur.fetchall():
                self.listbox.insert(tk.END, f"#{row[0]} | Pet {row[1]} | {row[2]} {row[3]} | {row[4]}")


    def select(self, event):
        try:
            index = self.listbox.curselection()[0]
            text = self.listbox.get(index)
            app_id = int(text.split("|")[0].replace("#", "").strip())

            with sqlite3.connect(self.clinic_db) as conn:
                cur = conn.cursor()
                cur.execute("SELECT * FROM Appointments WHERE app_id=?", (app_id,))
                row = cur.fetchone()

            self.selected_app_id = row[0]
            self.entries["pet_id"].delete(0, tk.END)
            self.entries["pet_id"].insert(0, row[1])
            self.entries["date"].delete(0, tk.END)
            self.entries["date"].insert(0, row[2])
            self.entries["time"].delete(0, tk.END)
            self.entries["time"].insert(0, row[3])
            self.entries["description"].delete(0, tk.END)
            self.entries["description"].insert(0, row[4])
        except IndexError:
            pass


    def update(self):
        if not self.selected_app_id: return

        with sqlite3.connect(self.clinic_db) as conn:
            cur = conn.cursor()
            cur.execute("""
                UPDATE Appointments
                SET date=?, time=?, description=?
                WHERE app_id=?
            """, (
                self.entries["date"].get(),
                self.entries["time"].get(),
                self.entries["description"].get(),
                self.selected_app_id
            ))

        self.load()
        self.clear_form()


    def delete(self):
        t = self.controller.language.translate

        if not self.selected_app_id: return

        if not messagebox.askyesno(t("delete"), t("confirm_cancel_appointment")): return

        with sqlite3.connect(self.clinic_db) as conn:
            cur = conn.cursor()
            cur.execute("""
                UPDATE Appointments
                SET status='Cancelled'
                WHERE app_id=?
            """, (self.selected_app_id,))

        self.load()
        self.clear_form()

    
    def search(self):
        keyword = self.search_entry.get()
        self.listbox.delete(0, tk.END)

        with sqlite3.connect(self.clinic_db) as conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT * FROM Appointments
                WHERE status='Scheduled'
                AND (pet_id LIKE ? OR date LIKE ?)
                ORDER BY date, time
            """, (f"%{keyword}%", f"%{keyword}%"))

            for row in cur.fetchall():
                self.listbox.insert(
                    tk.END,
                    f"#{row[0]} | Pet {row[1]} | {row[2]} {row[3]} | {row[4]}"
                )


    def show_today(self):
        today = datetime.today().strftime("%Y-%m-%d")
        self.search_entry.delete(0, tk.END)
        self.search_entry.insert(0, today)
        self.search()

    
    def update_texts(self):
        t = self.controller.language.translate

        self.title.config(text=t("appointment_title"))
        self.labels["pet_id"].config(text=t("pet_id"))
        self.labels["date"].config(text=t("date"))
        self.labels["time"].config(text=t("time"))
        self.labels["description"].config(text=t("description"))
        self.search_label.config(text=t("search_label"))
        self.add_btn.config(text=t("add"))
        self.update_btn.config(text=t("update"))
        self.delete_btn.config(text=t("delete"))
        self.search_btn.config(text=t("search"))
        self.today_btn.config(text=t("today"))
        self.back_btn.config(text=t("back_to_main_menu"))

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


class MedicalHistoryFrame(tk.Frame):

    def __init__(self, parent, controller, role=None):
        super().__init__(parent)
        self.controller = controller
        self.role = role
        self.selected_id = None

        self.title = tk.Label(self, font=("Arial", 18, "bold"))
        self.title.pack(pady=15)

        form = tk.Frame(self)
        form.pack()

        keys = ["pet_id", "visit_date", "treatment", "vaccination", "notes"]
        self.entries = {}
        self.labels = {}

        for i, key in enumerate(keys):
            lbl = tk.Label(form)
            lbl.grid(row=i, column=0, sticky="w")

            ent = tk.Entry(form, width=40)
            ent.grid(row=i, column=1)

            self.entries[key] = ent
            self.labels[key] = lbl

        btns = tk.Frame(self)
        btns.pack(pady=10)

        self.add_btn = tk.Button(btns, command=self.add)
        self.update_btn = tk.Button(btns, command=self.update)
        self.delete_btn = tk.Button(btns, command=self.delete)

        self.add_btn.grid(row=0, column=0, padx=5)
        self.update_btn.grid(row=0, column=1, padx=5)
        self.delete_btn.grid(row=0, column=2, padx=5)

        self.listbox = tk.Listbox(self, width=100)
        self.listbox.pack(pady=10)
        self.listbox.bind("<<ListboxSelect>>", self.select)

        self.back_btn = tk.Button(self, command=lambda: controller.show_frame("DashboardFrame"))
        self.back_btn.pack(pady=15)

        self.init_db()
        self.load()

        if self.role: self.apply_role(self.role)

        self.update_texts()

   
    def apply_role(self, role):
        self.role = role
        if role == "veterinarian":
            self.add_btn.config(state="normal")
            self.update_btn.config(state="normal")
            self.delete_btn.config(state="normal")
        else:
            self.add_btn.config(state="disabled")
            self.update_btn.config(state="disabled")
            self.delete_btn.config(state="disabled")

   
    def init_db(self):
        with sqlite3.connect(os.path.join('db', 'clinic.db')) as conn:
            cur = conn.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS MedicalHistory (
                    record_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    pet_id INTEGER NOT NULL,
                    visit_date TEXT NOT NULL,
                    treatment TEXT,
                    vaccination TEXT,
                    notes TEXT
                )
            """)


    def add(self):
        t = self.controller.language.translate

        pet_id = self.entries["pet_id"].get()
        visit_date = self.entries["visit_date"].get()

        if not pet_id.isdigit():
            messagebox.showerror(t("error"), t("pet_id_numeric"))
            return

        if not pet_id_exists_in_db(int(pet_id)):
            messagebox.showerror(t("error"), t("pet_not_found"))
            return

        try:
            visit_dt = datetime.strptime(visit_date, "%Y-%m-%d").date()
            if visit_dt > datetime.today().date():
                messagebox.showerror(t("error"), t("future_date_not_allowed")); return
        except ValueError:
            messagebox.showerror(t("error"), t("invalid_date_format")); return


        with sqlite3.connect(os.path.join('db', 'clinic.db')) as conn:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO MedicalHistory
                (pet_id, visit_date, treatment, vaccination, notes)
                VALUES (?, ?, ?, ?, ?)
            """, (
                pet_id,
                visit_date,
                self.entries["treatment"].get(),
                self.entries["vaccination"].get(),
                self.entries["notes"].get()
            ))

        self.load()
        self.clear_form()


    def load(self):
        self.listbox.delete(0, tk.END)
        with sqlite3.connect(os.path.join('db', 'clinic.db')) as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM MedicalHistory ORDER BY visit_date DESC")
            for row in cur.fetchall():
                self.listbox.insert(tk.END, row)


    def select(self, event):
        try:
            row = self.listbox.get(self.listbox.curselection())
            self.selected_id = row[0]

            self.entries["pet_id"].delete(0, tk.END)
            self.entries["pet_id"].insert(0, row[1])

            self.entries["visit_date"].delete(0, tk.END)
            self.entries["visit_date"].insert(0, row[2])

            self.entries["treatment"].delete(0, tk.END)
            self.entries["treatment"].insert(0, row[3])

            self.entries["vaccination"].delete(0, tk.END)
            self.entries["vaccination"].insert(0, row[4])

            self.entries["notes"].delete(0, tk.END)
            self.entries["notes"].insert(0, row[5])
        except IndexError:
            pass


    def update(self):
        if not self.selected_id: return

        with sqlite3.connect(os.path.join('db', 'clinic.db')) as conn:
            cur = conn.cursor()
            cur.execute("""
                UPDATE MedicalHistory
                SET visit_date=?, treatment=?, vaccination=?, notes=?
                WHERE record_id=?
            """, (
                self.entries["visit_date"].get(),
                self.entries["treatment"].get(),
                self.entries["vaccination"].get(),
                self.entries["notes"].get(),
                self.selected_id
            ))

        self.load()
        self.clear_form()


    def delete(self):
        t = self.controller.language.translate

        if not self.selected_id: return

        if not messagebox.askyesno(t("delete"), t("confirm_delete_history")): return

        with sqlite3.connect(os.path.join('db', 'clinic.db')) as conn:
            cur = conn.cursor()
            cur.execute("DELETE FROM MedicalHistory WHERE record_id=?", (self.selected_id,))

        self.load()
        self.clear_form()


    def clear_form(self):
        for ent in self.entries.values():
            ent.delete(0, tk.END)
        self.selected_id = None


    def update_texts(self):
        t = self.controller.language.translate

        self.title.config(text=t("history_title"))
        self.labels["pet_id"].config(text=t("pet_id"))
        self.labels["visit_date"].config(text=t("visit_date"))
        self.labels["treatment"].config(text=t("treatment"))
        self.labels["vaccination"].config(text=t("vaccination"))
        self.labels["notes"].config(text=t("notes"))

        self.add_btn.config(text=t("add"))
        self.update_btn.config(text=t("update"))
        self.delete_btn.config(text=t("delete"))
        self.back_btn.config(text=t("back"))

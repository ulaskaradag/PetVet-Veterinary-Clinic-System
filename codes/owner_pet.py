import tkinter as tk
from tkinter import messagebox
import sqlite3
import random
import re
import os
import pandas as pd
from language import LanguageManager


def connect_db():
    conn = sqlite3.connect(os.path.join("db", "clinic.db"))
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Owners (
        owner_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        phone TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Pets (
        pet_id INTEGER PRIMARY KEY,
        owner_id INTEGER,
        species TEXT NOT NULL,
        breed TEXT NOT NULL,
        age INTEGER,
        FOREIGN KEY(owner_id) REFERENCES Owners(owner_id)
    )
    """)

    conn.commit()
    conn.close()


def is_valid_phone(phone):
    return bool(re.fullmatch(r"0\d{10}", phone))


def generate_unique_pet_id(cursor):
    while True:
        pet_id = random.randint(10**6, 10**7 - 1)
        cursor.execute("SELECT 1 FROM Pets WHERE pet_id = ?", (pet_id,))
        if cursor.fetchone() is None: return pet_id


def export_to_excel(controller):
    t = controller.language.translate

    conn = sqlite3.connect(os.path.join("db", "clinic.db"))
    query = """
    SELECT
        Pets.pet_id AS "Pet ID",
        Owners.name AS "Owner Name",
        Owners.phone AS "Phone Number",
        Pets.species AS "Species",
        Pets.breed AS "Breed",
        Pets.age AS "Age"
    FROM Pets
    JOIN Owners ON Pets.owner_id = Owners.owner_id
    """

    df = pd.read_sql_query(query, conn)
    conn.close()

    if df.empty:
        messagebox.showwarning(
            t("export"),
            t("no_data_export")
        )
        return

    df.to_excel(os.path.join("excel_files", "pet_and_owner_list.xlsx"), index=False)


class OwnerPetFrame(tk.Frame):
    
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        connect_db()

        self.title = tk.Label(self, font=("Arial", 18, "bold"))
        self.title.pack(pady=15)

        form = tk.Frame(self)
        form.pack()

        self.entries = {}
        self.labels = {}

        fields = ["owner_name", "owner_phone", "pet_species", "pet_breed", "pet_age"]

        for i, key in enumerate(fields):
            lbl = tk.Label(form)
            lbl.grid(row=i, column=0, sticky="w")

            entry = tk.Entry(form)
            entry.grid(row=i, column=1)

            self.labels[key] = lbl
            self.entries[key] = entry

        self.save_btn = tk.Button(self, command=self.save_data)
        self.save_btn.pack(pady=5)

        self.export_btn = tk.Button(self, command=lambda: export_to_excel(self.controller))
        self.export_btn.pack(pady=5)

        self.back_btn = tk.Button(self, command=lambda: controller.show_frame("DashboardFrame"))
        self.back_btn.pack(pady=5)

        self.update_texts()

    def save_data(self):
        t = self.controller.language.translate

        name = self.entries["owner_name"].get()
        phone = self.entries["owner_phone"].get()
        species = self.entries["pet_species"].get()
        breed = self.entries["pet_breed"].get()
        age = self.entries["pet_age"].get()

        if not all([name, phone, species, breed, age]):
            messagebox.showwarning(t("warning"), t("all_fields_required")); return

        if not is_valid_phone(phone):
            messagebox.showwarning(t("warning"), t("invalid_phone")); return

        try:
            age = int(age)
        except ValueError:
            messagebox.showwarning(t("warning"), t("invalid_pet_age")); return

        conn = sqlite3.connect(os.path.join("db", "clinic.db"))
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO Owners (name, phone) VALUES (?, ?)", (name, phone))
        owner_id = cursor.lastrowid

        pet_id = generate_unique_pet_id(cursor)

        cursor.execute("""
            INSERT INTO Pets (pet_id, owner_id, species, breed, age)
            VALUES (?, ?, ?, ?, ?) """, (pet_id, owner_id, species, breed, age))

        conn.commit()
        conn.close()

        messagebox.showinfo(t("success"), t("register_success_pet").format(pet_id=pet_id))

        for entry in self.entries.values():
            entry.delete(0, tk.END)

        export_to_excel(self.controller)

    def update_texts(self):
        t = self.controller.language.translate

        self.title.config(text=t("owner_pet_reg_title"))

        for key, lbl in self.labels.items():
            lbl.config(text=t(key))

        self.save_btn.config(text=t("save"))
        self.export_btn.config(text=t("export"))
        self.back_btn.config(text=t("back"))
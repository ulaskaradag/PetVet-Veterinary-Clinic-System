import tkinter as tk
from tkinter import messagebox
import sqlite3
import os
import matplotlib.pyplot as plt
from language import LanguageManager


class ReportsFrame(tk.Frame):
    
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.report_title = tk.Label(self,font=("Arial", 18, "bold"))
        self.report_title.pack(pady=20)

        self.show_btn = tk.Button(self,width=35,command=self.show_chart)
        self.show_btn.pack(pady=10)

        self.back_btn = tk.Button(self, command=lambda: controller.show_frame("DashboardFrame"))
        self.back_btn.pack(pady=20)

        self.update_texts()

    def show_chart(self):
        t = self.controller.language.translate

        conn = sqlite3.connect(os.path.join("db", "clinic.db"))
        cur = conn.cursor()
        cur.execute("SELECT species, COUNT(*) FROM Pets GROUP BY species")
        data = cur.fetchall()
        conn.close()

        if not data:
            messagebox.showwarning(t("no_data_title"), t("no_data_message"))
            return

        labels = [row[0] for row in data]
        sizes = [row[1] for row in data]

        plt.figure()
        plt.pie(sizes, labels=labels, autopct="%1.1f%%")
        plt.title(t("species_distribution_title"))
        plt.show()

    def update_texts(self):
        t = self.controller.language.translate

        self.report_title.config(text=t("reports_title"))
        self.show_btn.config(text=t("show"))
        self.back_btn.config(text=t("back"))

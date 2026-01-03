import tkinter as tk
from language import LanguageManager


class DashboardFrame(tk.Frame):

    def __init__(self, parent, controller): 
        super().__init__(parent)
        self.controller = controller

        self.main_title = tk.Label(self, text="Main Menu", font=("Arial", 18, "bold"))
        self.main_title.pack(pady=20)

        self.owner_pet_reg_btn = tk.Button(self, text="Owner & Pet Registration", width=30, command=lambda: controller.show_frame("OwnerPetFrame"))
        self.owner_pet_reg_btn.pack(pady=5)

        self.appointment_btn = tk.Button(self, text="Appointment Management", width=30, command=lambda: controller.show_frame("AppointmentFrame"))
        self.appointment_btn.pack(pady=5)

        self.history_btn = tk.Button(self, text="Medical History", width=30, command=lambda: controller.show_frame("MedicalHistoryFrame"))
        self.history_btn.pack(pady=5)

        self.reports_btn = tk.Button(self, text="Reports & Statistics", width=30, command=lambda: controller.show_frame("ReportsFrame"))
        self.reports_btn.pack(pady=5)

        self.logout_btn = tk.Button(self, text="Logout", width=30, command=self.controller.logout)
        self.logout_btn.pack(pady=20)


    def tkraise(self):
        super().tkraise()

        role = self.controller.current_role
        self.reports_btn.config(state="disabled") if role == "secretary" else self.reports_btn.config(state="normal")


    def update_texts(self):
        t = self.controller.language.translate

        self.main_title.config(text=t("main_title"))
        self.owner_pet_reg_btn.config(text=t("owner_pet_reg_title"))
        self.appointment_btn.config(text=t("appointment_title"))
        self.history_btn.config(text=t("history_title"))
        self.reports_btn.config(text=t("reports_title"))
        self.logout_btn.config(text=t("logout"))

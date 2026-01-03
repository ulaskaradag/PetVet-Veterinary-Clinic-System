import tkinter as tk
from tkinter import messagebox
from language import LanguageManager
from login_window import LoginFrame, RegisterFrame, init_db
from dashboard import DashboardFrame
from owner_pet import OwnerPetFrame
from appointments import AppointmentFrame
from medical_history import MedicalHistoryFrame
from reports import ReportsFrame
import sys


class ClinicApp(tk.Tk):
    
    def __init__(self):
        super().__init__()

        self.language = LanguageManager()

        self.current_user_id = None
        self.current_user_name = None
        self.current_role = None

        self.title("PetVet Clinic Management System")
        self.geometry("900x900") if sys.platform == "darwin" else self.geometry("600x600")
        self.resizable(False, False)

        top_bar = tk.Frame(self)
        top_bar.pack(fill="x")

        self.user_info_label = tk.Label(top_bar, text="", font=("Arial", 12, "italic"), fg="gray")
        self.user_info_label.pack(side="left", padx=10)

        lang_combo = self.language.create_language_combobox(top_bar)
        lang_combo.pack(side="right", padx=10, pady=5)

        init_db()

        container = tk.Frame(self)
        container.pack(fill="both", expand=True)

        self.frames = {}

        for F in (
            LoginFrame,
            RegisterFrame,
            DashboardFrame,
            OwnerPetFrame,
            AppointmentFrame,
            MedicalHistoryFrame,
            ReportsFrame
        ):
            frame = F(container, self)
            self.frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.language.register_callback(self.refresh_ui)
        self.show_frame("LoginFrame")

    
    def show_frame(self, frame_name):
        frame = self.frames[frame_name]
        frame.tkraise()
        self.update_user_info_label()

    
    def update_user_info_label(self):
        if self.current_user_name and self.current_role:
            t = self.language.translate

            self.user_info_label.config(text=f"{self.current_user_name} ({t(self.current_role)})")
        else:
            self.user_info_label.config(text="")

    
    def refresh_ui(self):
        for frame in self.frames.values():
            if hasattr(frame, "update_texts"): frame.update_texts()
        self.update_user_info_label()

    
    def logout(self):
        t = self.language.translate

        self.current_user_id = None
        self.current_user_name = None
        self.current_role = None

        self.show_frame("LoginFrame")
        messagebox.showinfo(t("success"), t("logout_success"))


if __name__ == "__main__":
    app = ClinicApp()
    app.mainloop()

from tkinter import ttk

class LanguageManager:

    def __init__(self):
        self.current_language = "en"
        self._callbacks = []

        self.languages = {
            "en": {
                #login window texts
                "login": "Login",
                "register": "Register",
                "user_id": "User ID",
                "password": "Password",
                "success": "Success",
                "login_success_vet": "Successfully logined as veterinarian",
                "login_success_sec": "Successfully logined as secretary",
                "error": "Error",
                "warning": "Warning",
                "invalid_credentials": "Invalid credentials",
                "user_id_required": "User ID is required",
                "user_not_found": "User ID not found",
                "back": "Back",
                "change_password": "Change Password",
                "password_length_invalid" : "Password must contain at least 6 and at most 20 characters",
                "confirm_reset": "Are you sure you want to reset your account and register again?",
                "reset_success": "Your account has been reset. Please register again.",
                "reset_failed": "Account reset failed. Please try again.",
                "register_success": "Registration completed successfully.",
                "register_failed": "Registration failed. Please check your information and try again.",
                #main menu window texts
                "main_title": "Main Menu",
                "owner_pet_reg_title": "Owner & Pet Registration",
                "appointment_title": "Appointment Manager",
                "history_title": "Medical History",
                "reports_title": "Reports & Statistics",
                "logout": "Logout",
                #owner & pet registration menu window texts
                "owner_name": "Owner Name",
                "owner_phone": "Owner Phone (Start with 0)",
                "pet_species": "Pet Species",
                "pet_breed": "Pet Breed",
                "pet_age": "Pet Age",
                "save": "Save",
                "export": "Export to Excel",
                "all_fields_required": "All fields are required.",
                "invalid_phone": "Phone number must start with 0 and be exactly 11 digits.",
                "invalid_pet_age": "Pet age must be a number.",
                "register_success_pet": "Successfully registered.\nPet ID is {pet_id}",
                "no_data_export": "No data available to export.",
                #appointment window texts
                "pet_id": "Pet ID",
                "date": "Date (YYYY-MM-DD)",
                "time": "Time (HH:MM)",
                "description": "Description",
                "search_label": "Search (Pet ID / Date):",
                "add": "Add",
                "update": "Update",
                "delete": "Delete",
                "search": "Search",
                "today": "Today",
                "back_to_main_menu": "Back to Main Menu",
                "pet_id_numeric": "Pet ID must be numeric.",
                "pet_not_found": "Pet ID cannot be found.",
                "past_date_not_allowed": "Past date is not allowed.",
                "invalid_date_time": "Invalid date or time format.",
                "appointment_conflict": "Appointment conflict detected.",
                "confirm_cancel_appointment": "Are you sure you want to cancel this appointment?",
                #medical history window texts(medical_history.py)
                "visit_date": "Visit Date",
                "treatment": "Treatment",
                "vaccination": "Vaccination",
                "notes": "Notes",
                "pet_id_numeric": "Pet ID must be numeric.",
                "pet_not_found": "Pet ID cannot be found.",
                "future_date_not_allowed": "Future dates are not allowed.",
                "invalid_date_format": "Invalid date format (YYYY-MM-DD).",
                "confirm_delete_history": "Are you sure you want to delete this medical record?",
                #report window texts(report.py)
                "show": "Show Species Distribution Chart",
                "species_distribution_title": "Species Distribution Chart",
                "no_data_title": "No Data",
                "no_data_message": "No records found",
                #main.py texts
                "veterinarian": "Veterinarian",
                "secretary": "Secretary",
                "logout_success": "Successfully logged out."

            },
            "tr": {
                #login window texts(login_window.py)
                "login": "Giriş",
                "register": "Kayıt Ol",
                "user_id": "Kullanıcı ID",
                "password": "Şifre",
                "full_name": "Ad Soyad",
                "success": "Başarılı",
                "login_success_vet": "Veteriner olarak giriş başarılı",
                "login_success_sec": "Sekreter olarak giriş başarılı",
                "login_success": "Giriş başarılı",
                "error": "Hata",
                "warning": "Uyarı",
                "invalid_credentials": "Hatalı bilgiler",
                "user_id_required": "Kullanıcı ID Gerekli",
                "user_not_found": "Kullanıcı ID bulunamadı",
                "back": "Geri",
                "change_password": "Şifre Değiştir",
                "password_length_invalid" : "Şifre en az 6 ve en fazla 20 karakter içermelidir.",
                "confirm_reset": "Hesabınızı sıfırlayıp tekrar kayıt olmak istediğinize emin misiniz?",
                "reset_success": "Hesabınız sıfırlandı. Lütfen tekrar kayıt olun.",
                "reset_failed": "Hesap sıfırlama başarısız oldu. Lütfen tekrar deneyin.",
                "register_success": "Kayıt işlemi başarıyla tamamlandı.",
                "register_failed": "Kayıt işlemi başarısız oldu. Bilgilerinizi kontrol edip tekrar deneyin.",
                #main menu window texts(dashboard.py)
                "main_title": "Ana Menu",
                "owner_pet_reg_title": "Hayvan ve Sahip Kayıt",
                "appointment_title": "Randevu Yöneticisi",
                "history_title": "Medikal Geçmiş",
                "reports_title": "Raporlar ve İstatistikler",
                "logout": "Çıkış",
                #owner & pet registration menu window texts(owner_pet.py)
                "owner_name": "Sahip Ad",
                "owner_phone": "Sahip Telefon (0 ile başlayan)",
                "pet_species": "Hayvanın türü",
                "pet_breed": "Hayvanın cinsi",
                "pet_age": "Hayvanın yaşı",
                "save": "Kaydet",
                "export": "Excel'e aktar",
                "all_fields_required": "Tüm alanların doldurulması zorunludur.",
                "invalid_phone": "Telefon numarası 0 ile başlamalı ve 11 haneli olmalıdır.",
                "invalid_pet_age": "Hayvan yaşı sayısal olmalıdır.",
                "register_success_pet": "Kayıt başarıyla tamamlandı.\nPet ID: {pet_id}",
                "no_data_export": "Dışa aktarılacak veri bulunamadı.",
                #appointment window texts(appointment.py)
                "pet_id": "Hayvan ID",
                "date": "Tarih (YYYY-AA-GG)",
                "time": "Saat (SS:DD)",
                "description": "Açıklama",
                "search_label": "Ara (Hasta ID / Tarih):",
                "add": "Ekle",
                "update": "Güncelle",
                "delete": "Sil",
                "search": "Ara",
                "today": "Bugün",
                "back_to_main_menu": "Ana Menüye Dön",
                "pet_id_numeric": "Pet ID sayısal olmalıdır.",
                "pet_not_found": "Pet ID bulunamadı.",
                "past_date_not_allowed": "Geçmiş tarih seçilemez.",
                "invalid_date_time": "Tarih veya saat formatı hatalı.",
                "appointment_conflict": "Randevu çakışması tespit edildi.",
                "confirm_cancel_appointment": "Bu randevuyu iptal etmek istediğinize emin misiniz?",
                #medical history window texts(medical_history.py)
                "visit_date": "Ziyaret Tarihi",
                "treatment": "Tedavi",
                "vaccination": "Aşılama",
                "notes": "Notlar",
                "pet_id_numeric": "Pet ID sayısal olmalıdır.",
                "pet_not_found": "Pet ID bulunamadı.",
                "future_date_not_allowed": "Gelecek tarih girilemez.",
                "invalid_date_format": "Tarih formatı hatalı (YYYY-AA-GG).",
                "confirm_delete_history": "Bu tıbbi kaydı silmek istediğinize emin misiniz?",
                #report window texts(reports.py)
                "show": "Tür Dağılım Tablosunu Göster",
                "species_distribution_title": "Tür Dağılım Tablosu",
                "no_data_title": "Veri Yok",
                "no_data_message": "Kayıt bulunamadı",
                #main.py texts
                "veterinarian": "Veteriner",
                "secretary": "Sekreter",
                "logout_success": "Başarıyla çıkış yapıldı."
            }
        }

    
    def set_language(self, lang_code):
        if lang_code in self.languages: self.current_language = lang_code; self._notify()


    def translate(self, key):
        return self.languages[self.current_language].get(key, key)
    

    def register_callback(self, callback):
        if callback not in self._callbacks: self._callbacks.append(callback)
            

    def _notify(self):
        for cb in self._callbacks: cb()


    def create_language_combobox(self, parent):
        combo = ttk.Combobox(parent, values=["EN", "TR"], state="readonly", width=5)

        combo.set("EN" if self.current_language == "en" else "TR")

        def on_change(event=None):
            lang = "en" if combo.get() == "EN" else "tr"
            self.set_language(lang)

        combo.bind("<<ComboboxSelected>>", on_change)
        return combo

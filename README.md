## 🐾 **PetVet Clinic Management System**

The PetVet Clinic Management System is a desktop-based application developed using Python, Tkinter, and SQLite.
The system is designed to support daily operations of a veterinary clinic, including user authentication, pet and owner management, appointment scheduling, medical history tracking, and species distribution report generation.

The system implements role-based access control with two predefined roles: Veterinarian and Secretary. User identities and roles are preloaded from an Excel file to ensure controlled access.

## ✨ **Key Features**:

    - 🔐 Secure login and registration with password validation
  
    - 🐕 Owner and pet registration with unique Pet ID generation
  
    - 📅 Appointment management with pet existence validation
  
    - 🩺 Medical history tracking for registered pets
  
    - 📊 Excel import (users) and export (pet data)
  
    - 🌐 English and Turkish language support
  
    - 🖥 Cross-platform graphical user interface

## 🏗 **Architecture Overview**:

    - 🧩 Modular Tkinter-based window structure
    
    - 🗄 SQLite database with normalized tables
    
    - 🔄 Centralized navigation and session management
    
    - 🔍 Clear separation of UI, logic, and data layers

## ⚙️ Prerequisites:

    - 🐍 Python 3.9 or later
    
    - Install the required libraries using pip with the following command: pip install pandas matplotlib openpyxl

    - tkinter and sqlite3 libraries are included with standard python installations so any additional installation is not needed.

## 🚀 **Running the Application**:

    1) 📁 Ensure worker_list.xlsx is located in the excel_files/ directory.

    2) ▶️ Run the application with the following command: python main.py

## ✅ **Conclusion**:

This project demonstrates a well-structured desktop application with role-based access control, reliable data validation, and cross-platform compatibility, suitable for practical use.
    

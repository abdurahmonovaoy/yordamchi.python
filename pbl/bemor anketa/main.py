import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from sklearn import tree
from tkcalendar import DateEntry
import sqlite3
import csv

# Create or connect to the database
conn = sqlite3.connect('hospital.db')
cursor = conn.cursor()

# Create tables
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS patients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        familya TEXT NOT NULL,
        ismi TEXT NOT NULL,
        telefon TEXT,
        tugilgan_kuni TEXT,
        pasport TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS anketa (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_bemor INTEGER,
        kelgan_sana TEXT,
        tolov TEXT,
        eslatma TEXT,
        FOREIGN KEY (id_bemor) REFERENCES patients(id)
    )
''')
conn.commit()

# Function to center the window on the screen
def center_window(win, width=600, height=400):
    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    win.geometry(f'{width}x{height}+{x}+{y}')

# Register screen
def register_screen():
    register_win = tk.Toplevel(root)
    register_win.title("Register")
    register_win.configure(bg='#f0f0f0')
    center_window(register_win, 400, 300)

    frame = ttk.Frame(register_win, padding="20")
    frame.pack(expand=True)

    ttk.Label(frame, text="Username:", background='#f0f0f0', font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
    ttk.Label(frame, text="Password:", background='#f0f0f0', font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)

    username_entry = ttk.Entry(frame, font=("Arial", 12))
    password_entry = ttk.Entry(frame, show='*', font=("Arial", 12))

    username_entry.grid(row=0, column=1, padx=10, pady=10)
    password_entry.grid(row=1, column=1, padx=10, pady=10)

    def register_user():
        username = username_entry.get()
        password = password_entry.get()
        try:
            cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
            conn.commit()
            messagebox.showinfo("Success", "User registered successfully")
            register_win.destroy()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username already exists")

    ttk.Button(frame, text="Register", command=register_user, style="TButton").grid(row=2, columnspan=2, pady=20)

# Login screen
def login_screen():
    login_win = tk.Toplevel(root)
    login_win.title("Login")
    login_win.configure(bg='#f0f0f0')
    center_window(login_win, 400, 300)

    frame = ttk.Frame(login_win, padding="20")
    frame.pack(expand=True)

    ttk.Label(frame, text="Username:", background='#f0f0f0', font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
    ttk.Label(frame, text="Password:", background='#f0f0f0', font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)

    username_entry = ttk.Entry(frame, font=("Arial", 12))
    password_entry = ttk.Entry(frame, show='*', font=("Arial", 12))

    username_entry.grid(row=0, column=1, padx=10, pady=10)
    password_entry.grid(row=1, column=1, padx=10, pady=10)

    def login_user():
        username = username_entry.get()
        password = password_entry.get()
        cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
        user = cursor.fetchone()
        if user:
            messagebox.showinfo("Success", "Login successful")
            login_win.destroy()
            patient_information_screen()
        else:
            messagebox.showerror("Error", "Invalid credentials")

    ttk.Button(frame, text="Login", command=login_user, style="TButton").grid(row=2, columnspan=2, pady=20)

# Patient information screen
def patient_information_screen():
    patient_win = tk.Toplevel(root)
    patient_win.title("Bemor ma'lumotlari")
    center_window(patient_win, 800, 600)

    # Patient form
    form_frame = ttk.Frame(patient_win, padding="10")
    form_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    ttk.Label(form_frame, text="Familiya:", font=("Arial", 12)).grid(row=0, column=0, padx=5, pady=5)
    ttk.Label(form_frame, text="Ismi:", font=("Arial", 12)).grid(row=1, column=0, padx=5, pady=5)
    ttk.Label(form_frame, text="Telefon raqam:", font=("Arial", 12)).grid(row=2, column=0, padx=5, pady=5)
    ttk.Label(form_frame, text="Tug'ilgan kuni:", font=("Arial", 12)).grid(row=3, column=0, padx=5, pady=5)
    ttk.Label(form_frame, text="Pasport seriyasi:", font=("Arial", 12)).grid(row=4, column=0, padx=5, pady=5)

    familya_entry = ttk.Entry(form_frame, font=("Arial", 12))
    ismi_entry = ttk.Entry(form_frame, font=("Arial", 12))
    telefon_entry = ttk.Entry(form_frame, font=("Arial", 12))
    tugilgan_kuni_entry = DateEntry(form_frame, font=("Arial", 12), date_pattern='yyyy-mm-dd')
    pasport_entry = ttk.Entry(form_frame, font=("Arial", 12))

    familya_entry.grid(row=0, column=1, padx=5, pady=5)
    ismi_entry.grid(row=1, column=1, padx=5, pady=5)
    telefon_entry.grid(row=2, column=1, padx=5, pady=5)
    tugilgan_kuni_entry.grid(row=3, column=1, padx=5, pady=5)
    pasport_entry.grid(row=4, column=1, padx=5, pady=5)

    def add_patient():
        patient = (
            familya_entry.get(),
            ismi_entry.get(),
            telefon_entry.get(),
            tugilgan_kuni_entry.get(),
            pasport_entry.get()
        )
        cursor.execute('''
            INSERT INTO patients (familya, ismi, telefon, tugilgan_kuni, pasport) 
            VALUES (?, ?, ?, ?, ?)
        ''', patient)
        conn.commit()
        update_patient_list()

    def update_patient_list():
        for row in tree.get_children():
            tree.delete(row)
        cursor.execute('SELECT * FROM patients')
        for row in cursor.fetchall():
            tree.insert("", "end", values=row)

    def delete_patient():
        selected_item = tree.selection()
        if selected_item:
            item = tree.item(selected_item)
            patient_id = item["values"][0]
            cursor.execute('DELETE FROM patients WHERE id = ?', (patient_id,))
            conn.commit()
            update_patient_list()
        else:
            messagebox.showerror("Error", "No patient selected")

    def export_to_text_file():
        with open('bemorlar.txt', 'w') as file:
            writer = csv.writer(file, delimiter='\t')
            writer.writerow(["ID", "Familiya", "Ismi", "Pasport seriyasi", "Telefon raqam", "Tug'ilgan kuni"])
            cursor.execute('SELECT * FROM patients')
            for row in cursor.fetchall():
                writer.writerow(row)
        messagebox.showinfo("Success", "Data exported to bemorlar.txt")

    def navigate_to_anketa():
        selected_item = tree.selection()
        if selected_item:
            item = tree.item(selected_item)
            patient_id = item["values"][0]
            patient_win.withdraw()
            open_anketa_window(patient_id)
        else:
            messagebox.showerror("Error", "No patient selected")

    button_frame = ttk.Frame(patient_win, padding="10")
    button_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    ttk.Button(button_frame, text="Ma'lumot qo'shish", command=add_patient, style="TButton").grid(row=0, column=0, padx=5, pady=5)
    ttk.Button(button_frame, text="O'chirish", command=delete_patient, style="TButton").grid(row=0, column=1, padx=5, pady=5)
    ttk.Button(button_frame, text="Export to Text File", command=export_to_text_file, style="TButton").grid(row=0, column=2, padx=5, pady=5)
    ttk.Button(button_frame, text="Anketaga o'tish", command=navigate_to_anketa, style="TButton").grid(row=0, column=3, padx=5, pady=5)

    # Patient list
    columns = ("ID", "Familiya", "Ismi", "Pasport seriyasi", "Telefon raqam", "Tug'ilgan kuni")
    tree = ttk.Treeview(patient_win, columns=columns, show='headings')
    for col in columns:
        tree.heading(col, text=col)
    tree.grid(row=2, column=0, columnspan=4, padx=10, pady=10, sticky=(tk.W, tk.E, tk.N, tk.S))

    update_patient_list()
    
    

# Anketa window
def open_anketa_window(patient_id):
    anketa_win = tk.Toplevel(root)
    anketa_win.title("Anketa ma'lumotlari")
    center_window(anketa_win, 800, 600)

    # Anketa form
    form_frame = ttk.Frame(anketa_win, padding="10")
    form_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    ttk.Label(form_frame, text="Kelgan sana:", font=("Arial", 12)).grid(row=0, column=0, padx=5, pady=5)
    ttk.Label(form_frame, text="To'lov:", font=("Arial", 12)).grid(row=1, column=0, padx=5, pady=5)
    ttk.Label(form_frame, text="Eslatma:", font=("Arial", 12)).grid(row=2, column=0, padx=5, pady=5)

    kelgan_sana_entry = DateEntry(form_frame, font=("Arial", 12), date_pattern='yyyy-mm-dd')
    tolov_entry = ttk.Entry(form_frame, font=("Arial", 12))
    eslatma_entry = ttk.Entry(form_frame, font=("Arial", 12))

    kelgan_sana_entry.grid(row=0, column=1, padx=5, pady=5)
    tolov_entry.grid(row=1, column=1, padx=5, pady=5)
    eslatma_entry.grid(row=2, column=1, padx=5, pady=5)

    def add_anketa():
        anketa = (
            patient_id,
            kelgan_sana_entry.get(),
            tolov_entry.get(),
            eslatma_entry.get()
        )
        cursor.execute('''
            INSERT INTO anketa (id_bemor, kelgan_sana, tolov, eslatma) 
            VALUES (?, ?, ?, ?)
        ''', anketa)
        conn.commit()
        update_anketa_list()

    def update_anketa_list():
        for row in tree.get_children():
            tree.delete(row)
        cursor.execute('SELECT * FROM anketa WHERE id_bemor = ?', (patient_id,))
        for row in cursor.fetchall():
            tree.insert("", "end", values=row)

    def delete_anketa():
        selected_item = tree.selection()
        if selected_item:
            item = tree.item(selected_item)
            anketa_id = item["values"][0]
            cursor.execute('DELETE FROM anketa WHERE id = ?', (anketa_id,))
            conn.commit()
            update_anketa_list()
        else:
            messagebox.showerror("Error", "No anketa selected")

    def back_to_previous_page():
        anketa_win.destroy()





    button_frame = ttk.Frame(anketa_win, padding="10")
    button_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    ttk.Button(button_frame, text="Ma'lumot qo'shish", command=add_anketa, style="TButton").grid(row=0, column=0, padx=5, pady=5)
    ttk.Button(button_frame, text="O'chirish", command=delete_anketa, style="TButton").grid(row=0, column=1, padx=5, pady=5)
    ttk.Button(button_frame, text="Back to Previous Page", command=back_to_previous_page, style="TButton").grid(row=0, column=3, padx=5, pady=5)
    

    # Anketa list
    columns = ("ID", "Kelgan sana", "To'lov", "Eslatma")
    tree = ttk.Treeview(anketa_win, columns=columns, show='headings')
    for col in columns:
        tree.heading(col, text=col)
    tree.grid(row=2, column=0, columnspan=4, padx=10, pady=10, sticky=(tk.W, tk.E, tk.N, tk.S))

    update_anketa_list()

# Main application
root = tk.Tk()
root.title("Main Screen")
root.configure(bg='#f0f0f0')

main_frame = ttk.Frame(root, padding="20")
main_frame.pack(expand=True)

ttk.Label(main_frame, text="Bemorlarni boshqarish tizimiga xush kelibsiz", background='#f0f0f0', font=("Arial", 16)).grid(row=0, columnspan=2, pady=20)
ttk.Button(main_frame, text="Register", command=register_screen, style="TButton").grid(row=1, column=0, padx=10, pady=10)
ttk.Button(main_frame, text="Login", command=login_screen, style="TButton").grid(row=1, column=1, padx=10, pady=10)

center_window(root, 600, 400)
root.mainloop()
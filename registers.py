import sqlite3
import tkinter as tk
from tkinter import messagebox

conn = sqlite3.connect("project.db")
cursor = conn.cursor()

cursor.execute("""
    Create table if not exists users (
        id integer Primary key autoincrement,
        name text,
        age integer,
        email text,
        password text    
    )           
    """)
conn.commit()

root = tk.Tk()
root.geometry("400x500")
root.title("Registration Page")

name_var = tk.StringVar()
age_var = tk.StringVar()
email_var = tk.StringVar()
password_var = tk.StringVar()

def register():
    name = name_var.get()
    age = age_var.get()
    email = email_var.get()
    password = password_var.get()
    if name== "" or age == "" or email== "" or password =="":
        messagebox.showerror("Validation", "Cannot be empty")
        return
    try: 
        age = int(age)
    except ValueError:
        messagebox.showerror("Error", "age cannot be String")
        return
    else:
        cursor.execute(
            "Insert into users (name, age, email, password) values(?,?,?,?)",
            [name,age, email, password ])
        conn.commit()
        messagebox.showinfo("Congratulation", "Registered Successful")
        
    name_var.set("")
    email_var.set("")
    password_var.set("")
    age_var.set("")

nameLabel = tk.Label(root, text="name", font=("Arial", 12, "bold"))
nameLabel.pack()
nameEntry = tk.Entry(root, textvariable=name_var, font=("Arial", 12, "bold"))
nameEntry.pack()
ageLabel = tk.Label(root, text="age", font=("Arial", 12, "bold"))
ageLabel.pack()
ageEntry = tk.Entry(root, textvariable=age_var, font=("Arial", 12, "bold"))
ageEntry.pack()
emailLabel = tk.Label(root, text="email", font=("Arial", 12, "bold"))
emailLabel.pack()
emailEntry = tk.Entry(root, textvariable=email_var, font=("Arial", 12, "bold"))
emailEntry.pack()
passwordLabel = tk.Label(root, text="password", font=("Arial", 12, "bold"))
passwordLabel.pack()
passwordEntry = tk.Entry(root, textvariable=password_var, font=("Arial", 12, "bold"))
passwordEntry.pack()


btn = tk.Button(root, text="submit", command= register).pack()
root.mainloop()
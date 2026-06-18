import sqlite3
import tkinter as tk
from tkinter import messagebox, filedialog
import shutil
import os
from tkinter import ttk

conn = sqlite3.connect("project.db")
cursor = conn.cursor()

cursor.execute("""
    Create table if not exists users (
        id integer Primary key autoincrement,
        name text,
        age integer,
        email text,
        password text, 
        image text    
    )           
    """)
conn.commit()

root = tk.Tk()
root.geometry("400x500")
root.title("Registration Page")

image_path = None
edit_id = None
register_frame = tk.Frame(root)
name_var = tk.StringVar()
age_var = tk.StringVar()
email_var = tk.StringVar()
password_var = tk.StringVar()

def upload_image():
    file_path = filedialog.askopenfilename(
        filetypes=[("image files", "*.png *.jpg")]
    )
    if file_path:
        filename = os.path.basename(file_path)
        if not os.path.exists("images"):
            os.makedirs("images")
        new_path = f"images/{filename}"
        shutil.copy(file_path, new_path)
        return new_path
        
def select_image():
    global image_path
    image_path = upload_image()
    if image_path:
        img_label.config(text="image added")

def edit_user():
    
    global edit_id, image_path
    
    selected = tree.focus()
    if not selected:
        messagebox.showwarning("Error", "Not selected")
        return
    print(selected)
    data = tree.item(selected, "values")
    user_id = data[0]
    
    cursor.execute (
        "select * from users where id = ?" ,
        [user_id]  
    )
    user = cursor.fetchone()
    print(user)
    if user:
        edit_id = user[0]
        name_var.set(user[1])
        age_var.set(user[2])
        email_var.set(user[3])
        password_var.set(user[4])
        image_path = user[5]
        
        user_frame.pack_forget()
        register_frame.pack()
        

def delete_user():
    
    global edit_id, image_path
    
    selected = tree.focus()
    if not selected:
        messagebox.showwarning("Error", "Not selected")
        return
  
    data = tree.item(selected, "values")
    user_id = data[0]
    
    cursor.execute (
        "delete from users where id = ?" ,
        [user_id]  
    )
    conn.commit()
    messagebox.showinfo("Inof", "Deleted")
    user_show()
    
def register():
    global image_path
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
    if edit_id:
        cursor.execute(
            "update users set name =?, age =?, email=?, password = ?, image = ? where id = ?",
             [name,age, email, password, image_path , edit_id]
        )
        conn.commit()
    else:
        cursor.execute(
            "Insert into users (name, age, email, password, image) values(?,?,?,?,?)",
            [name,age, email, password, image_path ])
        conn.commit()
        messagebox.showinfo("Congratulation", "Registered Successful")
        
    name_var.set("")
    email_var.set("")
    password_var.set("")
    age_var.set("")
    
# def user_show():
#     register_frame.pack_forget()
#     user_frame.pack()
#     listbox.delete(0, tk.END)
    
#     cursor.execute(
#         "Select * from users"
#     )
#     users = cursor.fetchall()
#     if len(users) == 0 :
#         listbox.insert(
#             tk.END, "No data"
#         )
#     else:
#         for user in users:
#             listbox.insert(
#                 tk.END, 
#                 f"{user[0]} {user[3]}"
#             )
                 
   
def user_show():
    register_frame.pack_forget()
    user_frame.pack()
    
    for item in tree.get_children():
        tree.delete(item)
    
    cursor.execute(
        "Select * from users"
    )
    users = cursor.fetchall()
    if len(users) == 0 :
        messagebox.showinfo("Info", "No entries")
    else:
        for user in users:
            tree.insert(
                "",
                tk.END, 
                values=(user[0], user[1],user[2], user[3] )
            )
                 

nameLabel = tk.Label(register_frame, text="name", font=("Arial", 12, "bold"))
nameLabel.pack()
nameEntry = tk.Entry(register_frame, textvariable=name_var, font=("Arial", 12, "bold"))
nameEntry.pack()
ageLabel = tk.Label(register_frame, text="age", font=("Arial", 12, "bold"))
ageLabel.pack()
ageEntry = tk.Entry(register_frame, textvariable=age_var, font=("Arial", 12, "bold"))
ageEntry.pack()
emailLabel = tk.Label(register_frame, text="email", font=("Arial", 12, "bold"))
emailLabel.pack()
emailEntry = tk.Entry(register_frame, textvariable=email_var, font=("Arial", 12, "bold"))
emailEntry.pack()
passwordLabel = tk.Label(register_frame, text="password", font=("Arial", 12, "bold"))
passwordLabel.pack()
passwordEntry = tk.Entry(register_frame, textvariable=password_var, font=("Arial", 12, "bold"))
passwordEntry.pack()
button1 = tk.Button(register_frame, text= "upload" ,command=select_image)
button1.pack()
img_label = tk.Label(register_frame, text="image")
img_label.pack()


btn = tk.Button(register_frame, text="submit", command= register).pack()
btn1 = tk.Button(register_frame, text="view", command= user_show).pack()

def back():
    user_frame.pack_forget()
    register_frame.pack()
    
user_frame = tk.Frame(root)
btn2 = tk.Button(user_frame,text= "back" ,command=back)
btn2.pack()
btn3 = tk.Button(user_frame, text="edit", command= edit_user)
btn3.pack()
btn4 = tk.Button(user_frame, text="delete", command= delete_user)
btn4.pack()

# listbox = tk.Listbox(user_frame, width="65")
# listbox.pack()

tree = ttk.Treeview(
    user_frame,
    columns= ("ID", "Name", "Age" , "Email"),
    show ="headings"
)
tree.heading("ID", text="ID")
tree.heading("Name", text="Name")
tree.heading("Age", text="Age")
tree.heading("Email", text="Email")
tree.pack()
register_frame.pack()
root.mainloop()
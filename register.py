import tkinter as tk

root = tk.Tk()
root.geometry("400x500")
root.title("My firts project")

label = tk.Label(root, text = "name" )
label.pack()

name = tk.StringVar()
t1 = tk.Entry(root, textvariable= name,width= 45)
t1.pack()

root.mainloop()
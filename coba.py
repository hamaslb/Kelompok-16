import tkinter as tk

root = tk.Tk()

label = tk.Label(root, text="Label")
label.place(x=50, y=50)

entry = tk.Entry(root)
entry.place(x=150, y=50)

button = tk.Button(root, text="Submit")
button.place(x=100, y=100)

root.mainloop()


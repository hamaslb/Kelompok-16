import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

def verify_login():
    username = entry_username.get()
    password = entry_password.get()

    valid_username = "user"
    valid_password = "password"

    if username == valid_username and password == valid_password:
        messagebox.showinfo("Login Successful", "Welcome!")
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")

root = tk.Tk()
root.title("Login Page")
root.geometry("400x300")

bg_image = Image.open("LOGO BIS WKWK.jpg")
bg_photo = ImageTk.PhotoImage(bg_image)

bg_label = tk.Label(root, image=bg_photo)
bg_label.place(relwidth=1, relheight=1)

frame = tk.Frame(root, bg="white", bd=5)
frame.place(relx=0.5, rely=0.5, anchor="center")

label_username = tk.Label(frame, text="Username")
label_username.grid(row=0, column=0, padx=10, pady=5)
entry_username = tk.Entry(frame)
entry_username.grid(row=0, column=1, padx=10, pady=5)

label_password = tk.Label(frame, text="Password")
label_password.grid(row=1, column=0, padx=10, pady=5)
entry_password = tk.Entry(frame, show="*")
entry_password.grid(row=1, column=1, padx=10, pady=5)

button_login = tk.Button(frame, text="Login", command=verify_login)
button_login.grid(row=2, columnspan=2, pady=20)

root.mainloop()
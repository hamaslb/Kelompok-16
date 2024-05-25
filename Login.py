import csv
import random
from email.message import EmailMessage
import smtplib
from tkinter import *
from tkinter import messagebox


def create_user_table():
    with open('user_data.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['name', 'username', 'email', 'phone', 'password', 'nik'])


def send_otp():
    global otp
    otp = "".join([str(random.randint(0, 9)) for i in range(6)])
    print(f"Generated OTP: {otp}")

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()

    from_mail = 'mhmmd.rayhan1104@gmail.com'
    app_password = 'mkyh haip obvy idtg'  

    try:
        server.login(from_mail, app_password)
        to_mail = entry_email.get()

        msg = EmailMessage()
        msg['Subject'] = "OTP Verification Amour Biz"
        msg['From'] = from_mail
        msg['To'] = to_mail
        msg.set_content(f"Dear user,\n\nThank you for registering with Amour Biz. To verify your registration information and protect your account security, we need you to complete email verification with the verification code.\n\nPlease use the following verification code to complete the registration process:\n\nVerification Code: {otp}\n\nPlease enter this code on the registration page to complete the verification.\n\nIf you did not initiate this registration, please ignore this email.")
        server.send_message(msg)
        messagebox.showinfo("Email Sent", "OTP has been sent to your email.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to send email: {e}")
    finally:
        server.quit()


def verify_otp():
    entered_otp = entry_otp.get()
    if entered_otp == otp:
        messagebox.showinfo("Success", "OTP verified successfully!")
        save_user_data()
    else:
        messagebox.showerror("Error", "Invalid OTP. Please try again.")


def save_user_data():
    name = entry_name.get()
    username = entry_username.get()
    email = entry_email.get()
    phone = entry_phone.get()
    password = entry_password.get()
    nik = entry_nik.get()

    with open('user_data.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([name, username, email, phone, password, nik])
    messagebox.showinfo("Success", "Account created successfully!")


def login():
    username = entry_login_username.get()
    password = entry_login_password.get()
    
    with open('user_data.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)  
        for row in reader:
            if row[1] == username and row[4] == password:
                messagebox.showinfo("Success", "Login successful!")
                return
    messagebox.showerror("Error", "Invalid username or password.")

def show_login_frame():
    register_frame.pack_forget()
    login_frame.pack()

def show_register_frame():
    login_frame.pack_forget()
    register_frame.pack()

root = Tk()
root.title("User Registration and Login")
root.geometry("400x600")

create_user_table()

login_frame = Frame(root)
Label(login_frame, text="Login", font=("Arial", 16)).pack(pady=10)

Label(login_frame, text="Username:", font=("Arial", 12)).pack(pady=5)
entry_login_username = Entry(login_frame, font=("Arial", 12))
entry_login_username.pack(pady=5)

Label(login_frame, text="Password:", font=("Arial", 12)).pack(pady=5)
entry_login_password = Entry(login_frame, font=("Arial", 12), show="*")
entry_login_password.pack(pady=5)

Button(login_frame, text="Login", font=("Arial", 12), command=login).pack(pady=10)
Button(login_frame, text="Register", font=("Arial", 12), command=show_register_frame).pack(pady=10)

login_frame.pack()

register_frame = Frame(root)

Label(register_frame, text="Name:", font=("Arial", 12)).pack(pady=5)
entry_name = Entry(register_frame, font=("Arial", 12))
entry_name.pack(pady=5)

Label(register_frame, text="Username:", font=("Arial", 12)).pack(pady=5)
entry_username = Entry(register_frame, font=("Arial", 12))
entry_username.pack(pady=5)

Label(register_frame, text="Email:", font=("Arial", 12)).pack(pady=5)
entry_email = Entry(register_frame, font=("Arial", 12))
entry_email.pack(pady=5)

Label(register_frame, text="Phone:", font=("Arial", 12)).pack(pady=5)
entry_phone = Entry(register_frame, font=("Arial", 12))
entry_phone.pack(pady=5)

Label(register_frame, text="Password:", font=("Arial", 12)).pack(pady=5)
entry_password = Entry(register_frame, font=("Arial", 12), show="*")
entry_password.pack(pady=5)

Label(register_frame, text="NIK:", font=("Arial", 12)).pack(pady=5)
entry_nik = Entry(register_frame, font=("Arial", 12))
entry_nik.pack(pady=5)

Button(register_frame, text="Send OTP", font=("Arial", 12), command=send_otp).pack(pady=10)

Label(register_frame, text="Enter OTP:", font=("Arial", 12)).pack(pady=5)
entry_otp = Entry(register_frame, font=("Arial", 12))
entry_otp.pack(pady=5)

Button(register_frame, text="Verify OTP", font=("Arial", 12), command=verify_otp).pack(pady=10)
Button(register_frame, text="Back to Login", font=("Arial", 12), command=show_login_frame).pack(pady=10)

root.mainloop()

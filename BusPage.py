import csv
import random
from email.message import EmailMessage
import smtplib
from tkinter import *
from tkinter import messagebox, ttk
import customtkinter as ctk


selected_bus = None
buses_info = []


def create_user_table():
    with open('Kelompok-16/user_data.csv', 'a', newline='') as file:
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
        show_city_selection() 
    else:
        messagebox.showerror("Error", "Invalid OTP. Please try again.")


def save_user_data():
    name = entry_name.get()
    username = entry_username.get()
    email = entry_email.get()
    phone = entry_phone.get()
    password = entry_password.get()
    nik = entry_nik.get()

    with open('kelompok-16/user_data.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([name, username, email, phone, password, nik])
    messagebox.showinfo("Success", "Account created successfully!")


def login():
    username = entry_login_username.get()
    password = entry_login_password.get()
    
    with open('kelompok-16/user_data.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            if row[1] == username and row[4] == password:
                messagebox.showinfo("Success", "Login successful!")
                show_city_selection()  
                return
    messagebox.showerror("Error", "Invalid username or password.")

def hide_all_frames():
    login_frame.pack_forget()
    register_frame.pack_forget()
    city_selection_frame.pack_forget()
    bus_selection_frame.pack_forget()
    seat_selection_frame.pack_forget()


def show_login_frame():
    hide_all_frames()
    login_frame.pack()


def show_register_frame():
    hide_all_frames()
    register_frame.pack()


def show_city_selection():
    hide_all_frames()
    city_selection_frame.pack() 


def show_bus_selection_page(buses_info):
    hide_all_frames()
    bus_selection_frame.pack()  

    for widget in bus_selection_frame.winfo_children():
        widget.destroy()

    ctk.CTkLabel(bus_selection_frame, text="Bus", font=("Arial", 12)).grid(row=0, column=0, padx=5, pady=5)
    ctk.CTkLabel(bus_selection_frame, text="Price", font=("Arial", 12)).grid(row=0, column=1, padx=5, pady=5)
    ctk.CTkLabel(bus_selection_frame, text="Departure Time", font=("Arial", 12)).grid(row=0, column=2, padx=5, pady=5)
    ctk.CTkLabel(bus_selection_frame, text="Select", font=("Arial", 12)).grid(row=0, column=3, padx=5, pady=5)

    for i, bus in enumerate(buses_info, start=1):
        ctk.CTkLabel(bus_selection_frame, text=bus[3], font=("Arial", 10)).grid(row=i, column=0, padx=5, pady=5)
        ctk.CTkLabel(bus_selection_frame, text=bus[4], font=("Arial", 10)).grid(row=i, column=1, padx=5, pady=5)
        ctk.CTkLabel(bus_selection_frame, text=bus[2], font=("Arial", 10)).grid(row=i, column=2, padx=5, pady=5)
        ctk.CTkButton(bus_selection_frame, text="Select", font=("Arial", 10), 
               command=lambda bus=bus: show_seat_selection(bus, buses_info)).grid(row=i, column=3, padx=5, pady=5)

    ctk.CTkButton(bus_selection_frame, text="Back", font=("Arial", 12), 
           command=show_city_selection).grid(row=i+1, column=2, pady=10)


def show_seat_selection(bus, buses_info_local):
    global selected_bus, buses_info
    selected_bus = bus
    buses_info = buses_info_local

    hide_all_frames()
    seat_selection_frame.pack()

    
    for widget in seat_selection_frame.winfo_children():
        widget.destroy()

    ctk.CTkLabel(seat_selection_frame, text=f"Select Seats for {bus[0]} to {bus[1]}", font=("Arial", 12)).grid(row=0, column=0, columnspan=4, padx=5, pady=5)

    
    seats = []
    for i in range(4):
        row = []
        for j in range(4):
            seat_button = Button(seat_selection_frame, text=f"{chr(65+i)}{j+1}", font=("Arial", 10))
            seat_button.config(command=lambda b=seat_button: toggle_seat(b))
            seat_button.grid(row=i+1, column=j, padx=5, pady=5)
            row.append(seat_button)
        seats.append(row)

    ctk.CTkButton(seat_selection_frame, text="Confirm", font=("Arial", 12), command=lambda: confirm_seat_selection(bus, seats)).grid(row=5, column=1, columnspan=2, pady=10)
    ctk.CTkButton(seat_selection_frame, text="Back", font=("Arial", 12), command=lambda: show_bus_selection_page(buses_info)).grid(row=6, column=1, columnspan=2, pady=10)
    


def toggle_seat(button):
    if button.config('relief')[-1] == 'sunken':
        button.config(relief="raised", bg="SystemButtonFace")
    else:
        button.config(relief="sunken", bg="lightgreen")


def confirm_seat_selection(bus, seats):
    selected_seats = []
    for row in seats:
        for seat in row:
            if seat.config('relief')[-1] == 'sunken':
                selected_seats.append(seat.cget('text'))
    
    if selected_seats:
        messagebox.showinfo("Success", f"Seats selected: {', '.join(selected_seats)}")
        show_payment_page() 
    else:
        messagebox.showerror("Error", "No seats selected. Please select at least one seat.")


def get_cities():
    cities = []
    with open('Kelompok-16\cities_and_buses.csv', 'r', newline='') as file:
        reader = csv.reader(file)
        next(reader)  
        for row in reader:
            if len(row) == 0:  
                break
            cities.append(row[0])
    return cities

def show_selection():
    origin_city = origin_combobox.get()
    destination_city = destination_combobox.get()
    departure_date = f"{int(day_combobox.get()):02d}-{int(month_combobox.get()):02d}-{year_combobox.get()}"

    selected_classes = []
    if gold_var.get():
        selected_classes.append("Gold")
    if silver_var.get():
        selected_classes.append("Silver")
    if bronze_var.get():
        selected_classes.append("Bronze")

    print(f"Origin: {origin_city}, Destination: {destination_city}, Date: {departure_date}, Classes: {selected_classes}")

    if not origin_city or not destination_city or not departure_date or not selected_classes:
        messagebox.showerror("Error", "Please make sure all fields are selected.")
        return

    buses_info = []
    with open('Kelompok-16\cities_and_buses.csv', 'r') as file:
        reader = csv.reader(file)
        city_section = True
        for row in reader:
            if city_section:
                if len(row) == 0:
                    city_section = False
                continue

            if not city_section and len(row) > 1:
                print(f"Checking row: {row}")  
                if (row[0] == origin_city and row[1] == destination_city 
                        and row[2].startswith(departure_date) and row[3] in selected_classes):
                    buses_info.append(row)

    if buses_info:
        print(f"Buses found: {buses_info}")  
        show_bus_selection_page(buses_info)
    else:
        print("No buses found")  
        messagebox.showinfo("No Buses", "No buses found for the selected route and date.")



def close_bus_selection():
    hide_all_frames()


def insert_cities_and_buses():
    cities = [
        "Jakarta", "Bogor", "Depok", "Tangerang", "Bandung",
    ]
    buses = [
        ("Jakarta", "Bogor", "01-06-2023 08:00", "Gold", 150000),
        ("Jakarta", "Depok", "01-06-2023 12:00", "Silver", 100000),
        ("Jakarta", "Tangerang", "01-06-2023 18:00", "Bronze", 80000),
        ("Jakarta", "Bandung", "02-06-2023 09:00", "Gold", 120000),
        ("Tangerang", "Bogor", "02-06-2023 13:00", "Silver", 90000),
        ("Tangerang", "Depok", "02-06-2023 17:00", "Bronze", 70000),
    ]
    with open('Kelompok-16\cities_and_buses.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["city"])
        for city in cities:
            writer.writerow([city])
        writer.writerow([]) 
        writer.writerow(["origin_city", "destination_city", "departure_datetime", "bus_class", "price"]) 
        for bus in buses:
            writer.writerow(bus)



def show_payment_page():
    hide_all_frames()
    payment_frame.pack()

    ctk.CTkLabel(payment_frame, text="Select Payment Method", font=("Arial", 16)).pack(pady=10)

    payment_methods = [
        ("Bank BCA Virtual Account", "BCA"),
        ("Bank Mandiri Virtual Account", "Mandiri"),
        ("Bank BNI Virtual Account", "BNI"),
        ("Dana E-Wallet", "Dana"),
        ("OVO E-Wallet", "OVO"),
        ("GoPay E-Wallet", "GoPay"),
        ("ShopeePay E-Wallet", "ShopeePay")
    ]

    selected_payment_method = StringVar()
    selected_payment_method.set(payment_methods[0][1])

    for text, method in payment_methods:
        ctk.CTkRadioButton(payment_frame, text=text, variable=selected_payment_method, value=method, font=("Arial", 12)).pack(anchor='w', pady=5)

    ctk.CTkButton(payment_frame, text="Confirm Payment", font=("Arial", 12), command=lambda: confirm_payment(selected_payment_method.get())).pack(pady=20)
    ctk.CTkButton(payment_frame, text="Back", font=("Arial", 12), command=lambda: show_seat_selection(selected_bus, buses_info)).pack()

def confirm_payment(method):
    messagebox.showinfo("Payment Success", f"Payment through {method} was successful!")
    show_city_selection()

def hide_all_frames():
    for frame in [login_frame, register_frame, city_selection_frame, bus_selection_frame, seat_selection_frame, payment_frame]:
        frame.pack_forget()


root = ctk.CTk()
root.title("Amour Biz")
root.geometry("500x500")

create_user_table()



login_frame = ctk.CTkFrame(root)

ctk.CTkLabel(login_frame, text="Username", font=("Arial", 12)).grid(row=0, column=0, padx=5, pady=5)
entry_login_username = ctk.CTkEntry(login_frame)
entry_login_username.grid(row=0, column=1, padx=5, pady=5)

ctk.CTkLabel(login_frame, text="Password", font=("Arial", 12)).grid(row=1, column=0, padx=5, pady=5)
entry_login_password = ctk.CTkEntry(login_frame, show='*')
entry_login_password.grid(row=1, column=1, padx=5, pady=5)

ctk.CTkButton(login_frame, text="Login", font=("Arial", 12), command=login).grid(row=2, column=0, columnspan=2, pady=10)
ctk.CTkButton(login_frame, text="Go to Register", font=("Arial", 12), command=show_register_frame).grid(row=3, column=0, columnspan=2, pady=10)


register_frame = ctk.CTkFrame(root)

ctk.CTkLabel(register_frame, text="Name", font=("Arial", 12)).grid(row=0, column=0, padx=5, pady=5)
entry_name = ctk.CTkEntry(register_frame)
entry_name.grid(row=0, column=1, padx=5, pady=5)

ctk.CTkLabel(register_frame, text="Username", font=("Arial", 12)).grid(row=1, column=0, padx=5, pady=5)
entry_username = ctk.CTkEntry(register_frame)
entry_username.grid(row=1, column=1, padx=5, pady=5)

ctk.CTkLabel(register_frame, text="Email", font=("Arial", 12)).grid(row=2, column=0, padx=5, pady=5)
entry_email = ctk.CTkEntry(register_frame)
entry_email.grid(row=2, column=1, padx=5, pady=5)

ctk.CTkLabel(register_frame, text="Phone", font=("Arial", 12)).grid(row=3, column=0, padx=5, pady=5)
entry_phone = ctk.CTkEntry(register_frame)
entry_phone.grid(row=3, column=1, padx=5, pady=5)

ctk.CTkLabel(register_frame, text="Password", font=("Arial", 12)).grid(row=4, column=0, padx=5, pady=5)
entry_password = ctk.CTkEntry(register_frame, show='*')
entry_password.grid(row=4, column=1, padx=5, pady=5)

ctk.CTkLabel(register_frame, text="NIK", font=("Arial", 12)).grid(row=5, column=0, padx=5, pady=5)
entry_nik = ctk.CTkEntry(register_frame)
entry_nik.grid(row=5, column=1, padx=5, pady=5)

ctk.CTkButton(register_frame, text="Register", font=("Arial", 12), command=send_otp).grid(row=6, column=0, columnspan=2, pady=10)

ctk.CTkLabel(register_frame, text="OTP", font=("Arial", 12)).grid(row=7, column=0, padx=5, pady=5)
entry_otp = ctk.CTkEntry(register_frame)
entry_otp.grid(row=7, column=1, padx=5, pady=5)

ctk.CTkButton(register_frame, text="Verify OTP", font=("Arial", 12), command=verify_otp).grid(row=8, column=0, columnspan=2, pady=10)

ctk.CTkButton(register_frame, text="Go to Login", font=("Arial", 12), command=show_login_frame).grid(row=9, column=0, columnspan=2, pady=10)

register_frame.pack()


city_selection_frame = ctk.CTkFrame(root)

ctk.CTkLabel(city_selection_frame, text="Select Origin City:", font=("Arial", 12)).pack(pady=10)
origin_combobox = ttk.Combobox(city_selection_frame, values=get_cities(), font=("Arial", 12))
origin_combobox.pack(pady=5)

ctk.CTkLabel(city_selection_frame, text="Select Destination City:", font=("Arial", 12)).pack(pady=10)
destination_combobox = ttk.Combobox(city_selection_frame, values=get_cities(), font=("Arial", 12))
destination_combobox.pack(pady=5)

ctk.CTkLabel(city_selection_frame, text="Select Departure Date:", font=("Arial", 12)).pack(pady=10)

date_frame = ctk.CTkFrame(city_selection_frame)
date_frame.pack(pady=5)

days = list(range(1, 32))
months = list(range(1, 13))
years = list(range(2023, 2025))

day_combobox = ttk.Combobox(date_frame, values=days, width=5, font=("Arial", 12))
day_combobox.grid(row=0, column=0, padx=5)
month_combobox = ttk.Combobox(date_frame, values=months, width=5, font=("Arial", 12))
month_combobox.grid(row=0, column=1, padx=5)
year_combobox = ttk.Combobox(date_frame, values=years, width=7, font=("Arial", 12))
year_combobox.grid(row=0, column=2, padx=5)

ctk.CTkLabel(city_selection_frame, text="Select Bus Classes:", font=("Arial", 12)).pack(pady=10)

class_frame = ctk.CTkFrame(city_selection_frame)
class_frame.pack(pady=5)

gold_var = BooleanVar()
silver_var = BooleanVar()
bronze_var = BooleanVar()

gold_check = Checkbutton(class_frame, text="Gold", variable=gold_var, font=("Arial", 12))
gold_check.grid(row=0, column=0, padx=5)

silver_check = Checkbutton(class_frame, text="Silver", variable=silver_var, font=("Arial", 12))
silver_check.grid(row=0, column=1, padx=5)

bronze_check = Checkbutton(class_frame, text="Bronze", variable=bronze_var, font=("Arial", 12))
bronze_check.grid(row=0, column=2, padx=5)

ctk.CTkButton(city_selection_frame, text="Show Selection", font=("Arial", 12), command=show_selection).pack(pady=20)


bus_selection_frame = ctk.CTkFrame(root)

ctk.CTkButton(bus_selection_frame, text="Close", font=("Arial", 12), command=close_bus_selection).grid(row=0, column=3, padx=5, pady=5)


seat_selection_frame = ctk.CTkFrame(root)


payment_frame = ctk.CTkFrame(root)


show_login_frame()

root.mainloop()
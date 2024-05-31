import csv
import random
from email.message import EmailMessage
import smtplib
from tkinter import *
from tkinter import messagebox, ttk
import customtkinter as ctk
import string
from PIL import Image, ImageTk
import tkinter as tk

selected_bus = None
buses_info = []
selected_seat = []
payment_method = ""
otp = ""
booking_code = None
selected_date = ""
selected_classes = []
booked_seats = set()


def reset_selected_seat():
    global selected_seat
    selected_seat = []

def format_rupiah(amount):
    amount_str = str(amount)
    rupiah = ""
    while amount_str:
        if len(amount_str) > 3:
            rupiah = "." + amount_str[-3:] + rupiah
            amount_str = amount_str[:-3]
        else:
            rupiah = amount_str + rupiah
            amount_str = ""
    return "Rp " + rupiah


def create_user_table():
    with open('Kelompok-16/user_data.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['name', 'username', 'email', 'phone', 'password', 'nik'])

def save_user_data():
    name = entry_name.get()
    username = entry_username.get()
    email = entry_email.get()
    phone = entry_phone.get()
    password = entry_password.get()
    nik = entry_nik.get()

    with open('Kelompok-16/user_data.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([name, username, email, phone, password, nik])
    
    messagebox.showinfo("Success", "Registration Successful. Please Log in again to continue.")
    show_login_frame()

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

def register_user():
    phone = entry_phone.get()
    nik = entry_nik.get()
    
    if not phone.isdigit():
        error_var_phone.set("Phone harus angka")
        return
    else:
        error_var_phone.set("")
    
    if not nik.isdigit():
        error_var_nik.set("NIK harus angka")
        return
    else:
        error_var_nik.set("")
    
    send_otp()
    

def verify_otp():
    entered_otp = entry_otp.get()
    if entered_otp == otp:
        messagebox.showinfo("Success", "OTP verified successfully!")
        save_user_data()
        show_login_frame()
    else:
        messagebox.showerror("Error", "Invalid OTP. Please try again.")

def login():
    global username
    username = entry_login_username.get()
    password = entry_login_password.get()
    
    with open('Kelompok-16/user_data.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)  
        for row in reader:
            if row[1] == username and row[4] == password:
                messagebox.showinfo("Success", "Login successful!")
                show_menu_frame()  
                return
    messagebox.showerror("Error", "Invalid username or password.")

def hide_all_frames():
    login_frame.place_forget()
    register_frame.place_forget()
    city_selection_frame.place_forget()
    bus_selection_frame.place_forget()
    seat_selection_frame.place_forget()
    payment_frame.place_forget()
    confirmation_frame.place_forget()
    payment_confirmation_frame.place_forget()
    menu_frame.place_forget()


def show_login_frame():
    hide_all_frames()
    login_frame.place(x=485,y=235)


def show_register_frame():
    hide_all_frames()
    register_frame.place(x=485,y=220)

def show_menu_frame() :
    hide_all_frames()

    for widget in menu_frame.winfo_children():
        widget.destroy()

    menu_frame.place(x=480,y=230)
    
    welcome_message = f"Welcome Back, {username}!"
    ctk.CTkLabel(menu_frame, text=welcome_message, font=("Prata", 50,), text_color="black", fg_color="#ebac4e").place(relx=0.5,rely=0.2,anchor="center")


    ctk.CTkButton(menu_frame, text="Pesan Tiket Baru", font=("Arial", 12), command=show_city_selection).place(relx=0.5,rely=0.5, anchor="center")
    ctk.CTkButton(menu_frame, text="Pembatalan Tiket", font=("Arial", 12), command=show_cancel_seat_page).place(relx=0.5,rely=0.6, anchor="center")


def show_city_selection():
    hide_all_frames()
    city_selection_frame.place(x=480,y=230)


def show_bus_selection_page(buses_info, selected_classes):
    hide_all_frames()

    for widget in bus_selection_frame.winfo_children():
        widget.destroy()

    bus_selection_frame.place(x=480, y=230)

    bus_image_path = "Kelompok-16/BG PEMILIHAN BIS.png"

    bus_image = Image.open(bus_image_path)
    resized_bus_image = bus_image.resize((960, 560), Image.LANCZOS)
    photo = ImageTk.PhotoImage(resized_bus_image)

    bus_image_label = tk.Label(bus_selection_frame, image=photo, bg='#CDCDCD')
    bus_image_label.image = photo
    bus_image_label.place(x=0, y=0)
    

    header_frame = ctk.CTkFrame(bus_selection_frame, width=601, height=220, fg_color="#ebac4e")
    header_frame.place(x=85, y=50)

    ctk.CTkLabel(header_frame, text="Tipe", font=("Arial", 14), text_color="black").place(x=15, y=5)
    ctk.CTkLabel(header_frame, text="Harga", font=("Arial", 14), text_color="black").place(x=115, y=5)
    ctk.CTkLabel(header_frame, text="Jam Keberangkatan", font=("Arial", 14), text_color="black").place(x=207, y=5)
    ctk.CTkLabel(header_frame, text="Estimasi Tiba", font=("Arial", 14), text_color="black").place(x=350, y=5)
    ctk.CTkLabel(header_frame, text="", font=("Arial", 12), text_color="white").place(x=405, y=5)

    arrow3_image = Image.open("Kelompok-16/BG ARROW.png")  # Ganti dengan path gambar tanda panah
    arrow3_image = arrow3_image.resize((30, 30), Image.Resampling.LANCZOS)

    # Mengonversi gambar ke format yang digunakan oleh CTkImage
    arrow3_ctk_image = ctk.CTkImage(light_image=arrow3_image, size=(30, 30))

    # Membuat tombol dengan gambar tanda panah
    arrow3_button = ctk.CTkButton(bus_selection_frame, image=arrow3_ctk_image, text="Pilih Tiket", fg_color="#CDCDCD", text_color="black", command=show_city_selection)
    arrow3_button.place(x=0, y=5)

    for i, bus in enumerate(buses_info, start=1):
        y_position = 30 + i * 30  

        row_frame = ctk.CTkFrame(bus_selection_frame, width=590, height=40, fg_color="#ebac4e", corner_radius=0)
        row_frame.place(x=95, y=y_position + 50)

        ctk.CTkLabel(row_frame, text=bus[4], font=("Arial", 12), text_color="black").place(x=5, y=5)
        price_in_rupiah = format_rupiah(int(bus[5]))
        ctk.CTkLabel(row_frame, text=price_in_rupiah, font=("Arial", 12), text_color="black").place(x=105, y=5)
        ctk.CTkLabel(row_frame, text=bus[2], font=("Arial", 12), text_color="black").place(x=205, y=5)
        ctk.CTkLabel(row_frame, text=bus[3], font=("Arial", 12), text_color="black").place(x=350, y=5)
        ctk.CTkButton(row_frame, text="Pilih", font=("Arial", 12), command=lambda bus=bus: show_seat_selection(bus, username, selected_date, origin_city, destination_city, buses_info, [bus[4]])).place(x=435, y=2)


def load_selected_seats(departure_date, origin_city, destination_city, selected_classes):
    global booked_seats
    booked_seats.clear()
    try:
        with open('Kelompok-16/selected_seats.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row and row[1] == departure_date and row[2] == origin_city and row[3] == destination_city and row[5] in selected_classes:
                    booked_seats.add(row[4])
    except FileNotFoundError:
        pass
    except Exception as e:
        print(f"Error loading selected seats: {e}")
    return booked_seats


def save_booking_data(selected_seat, username, departure_date, origin_city, destination_city, selected_class, booking_codes):
    try:
        with open('Kelompok-16/selected_seats.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            for seat, code in zip(selected_seat, booking_codes):
                writer.writerow([username, departure_date, origin_city, destination_city, seat, selected_class, code])
    except Exception as e:
        print(f"Error saving booking data: {e}")


def toggle_seat(button, seat_number):
    global selected_seat, booked_seats

    if seat_number in booked_seats:
        messagebox.showerror("Error", f"Seat {seat_number} is already booked. Please choose another seat.")
        return

    if button.config('relief')[-1] == 'sunken':
        button.config(relief="raised", bg="SystemButtonFace")
        selected_seat.remove(seat_number)
    else:
        button.config(relief="sunken", bg="lightgreen")
        selected_seat.append(seat_number)


def show_seat_selection(bus, username, selected_date, origin_city, destination_city, buses_info, selected_classes):
    global selected_bus, booked_seats, selected_seat
    selected_bus = bus
    selected_seat = []

    hide_all_frames()
    seat_selection_frame.place(x=480, y=230)

    for widget in seat_selection_frame.winfo_children():
        widget.destroy()


    seat_image_path = "Kelompok-16/BG PEMILIHAN KURSI.png"

    seat_image = Image.open(seat_image_path)
    resized_seat_image = seat_image.resize((960, 560), Image.LANCZOS)
    photo = ImageTk.PhotoImage(resized_seat_image)

    seat_image_label = tk.Label(seat_selection_frame, image=photo, bg='#CDCDCD')
    seat_image_label.image = photo
    seat_image_label.place(x=0, y=0)

    arrow2_image = Image.open("Kelompok-16/BG ARROW.png")  # Ganti dengan path gambar tanda panah
    arrow2_image = arrow2_image.resize((30, 30), Image.Resampling.LANCZOS)

    # Mengonversi gambar ke format yang digunakan oleh CTkImage
    arrow2_ctk_image = ctk.CTkImage(light_image=arrow2_image, size=(30, 30))

    # Membuat tombol dengan gambar tanda panah
    arrow2_button = ctk.CTkButton(seat_selection_frame, image=arrow2_ctk_image, text="Pilih Bis", fg_color="#CDCDCD", text_color="black", command=lambda: show_bus_selection_page(buses_info, selected_classes))
    arrow2_button.place(x=0, y=5)
    
    ctk.CTkLabel(seat_selection_frame, text=f"Pilih Kursi dari {bus[0]} ke {bus[1]} (Tipe {bus[4]})", text_color="black",font=("Prata", 14)).place(relx=0.3,rely=0.155)

    seat_count = {"Gold": 4, "Silver": 8, "Bronze": 16}
    total_seats = seat_count[bus[4]]

    seats = []
    x_start = 355
    y_start = 230
    seat_width = 50
    seat_height = 30
    seat_gap = 10
    middle_gap = seat_gap * 6

    booked_seats = load_selected_seats(selected_date, origin_city, destination_city, bus[4])

    for i in range(total_seats // 4):
        for j in range(4):
            seat_number = f"{i + 1}{chr(65 + j)}"
            seat_state = 'normal'
            seat_bg_color = "SystemButtonFace"
            if seat_number in selected_seat or seat_number in booked_seats:
                seat_state = 'disabled'
                seat_bg_color = 'red'
            seat_button = tk.Button(seat_selection_frame, text=seat_number, font=("Arial", 10), state=seat_state, bg=seat_bg_color)
            seat_button.config(command=lambda b=seat_button, sn=seat_number: toggle_seat(b, sn))
            # Penempatan kursi dengan jarak di tengah
            if j < 2:
                x_position = x_start + j * (seat_width + seat_gap)
            else:
                x_position = x_start + j * (seat_width + seat_gap) + middle_gap

            seat_button.place(x=x_position, y=y_start + i * (seat_height + seat_gap))
            seats.append(seat_button)

    ctk.CTkButton(seat_selection_frame,text="Simpan", font=("Arial", 12), bg_color="#ebac4e",command=lambda: confirm_seat_selection(bus, seats, selected_classes)).place(relx=0.5,rely=0.75, anchor="center")


def confirm_seat_selection(bus_info, seats, selected_classes):
    global selected_seat, username, selected_date, origin_city, destination_city
    selected_seat = [seat.cget('text') for seat in seats if seat.config('relief')[-1] == 'sunken']

    if selected_seat:
        print(f"Selected seats: {selected_seat}")
        booked_seats.update(selected_seat)
        messagebox.showinfo("Success", f"Seats selected: {', '.join(selected_seat)}")
        show_payment_page()
    else:
        messagebox.showerror("Error", "No seats selected. Please select at least one seat.")


def get_cities():
    cities = []
    with open('Kelompok-16/cities_and_buses.csv', 'r', newline='') as file:
        reader = csv.reader(file)
        next(reader)  
        for row in reader:
            if len(row) == 0:  
                break
            cities.append(row[0])
    return cities

def show_selection():
    global selected_date
    global origin_city
    global destination_city
    global selected_classes
    
    selected_date = f"{int(day_combobox.get()):02d}-{int(month_combobox.get()):02d}-{year_combobox.get()}"
    origin_city = origin_combobox.get()
    destination_city = destination_combobox.get()

    selected_classes = []  
    if gold_var.get():
        selected_classes.append("Gold")
    if silver_var.get():
        selected_classes.append("Silver")
    if bronze_var.get():
        selected_classes.append("Bronze")

    print(f"Origin: {origin_city}, Destination: {destination_city}, Date: {selected_date}, Classes: {selected_classes}")

    if not origin_city or not destination_city or not selected_date or not selected_classes:
        messagebox.showerror("Error", "Please make sure all fields are selected.")
        return

    buses_info = []
    with open('Kelompok-16/cities_and_buses.csv', 'r') as file:
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
                        and row[2].startswith(selected_date) and row[4] in selected_classes):
                    buses_info.append(row)

    if buses_info:
        show_bus_selection_page(buses_info, selected_classes)
    else:
        messagebox.showerror("Error", "No buses found for the selected criteria.")


def close_bus_selection():
    hide_all_frames()


def get_virtual_account(payment_method):
    virtual_accounts = {
        "BCA": "1234567890",
        "Mandiri": "9876543210",
        "BNI": "5678901234",
        "Dana": "081234567890",
        "OVO": "081098765432",
        "GoPay": "089876543210",
        "ShopeePay": "081234567890"
    }
    return virtual_accounts.get(payment_method, "N/A")

def show_payment_page():
    hide_all_frames()
    payment_frame.place(x=480,y=230)

    pay_image_path = "Kelompok-16/BG PEMILIHAN BAYAR.png"

    pay_image = Image.open(pay_image_path)
    resized_pay_image = pay_image.resize((960, 560), Image.LANCZOS)
    photo = ImageTk.PhotoImage(resized_pay_image)

    pay_image_label = tk.Label(payment_frame, image=photo, bg='#CDCDCD')
    pay_image_label.image = photo
    pay_image_label.place(x=0, y=0)

    ctk.CTkLabel(payment_frame, text="Pilih Cara Pembayaran", text_color="black", font=("Prata", 16)).place(relx=0.5, rely=0.092 , anchor='n')

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

    y_offset = 0.25
    for text, method in payment_methods:
        ctk.CTkRadioButton(payment_frame, text=text, bg_color= '#ebac43',variable=selected_payment_method, value=method,text_color="black", font=("Arial", 12)).place(relx=0.4, rely=y_offset, anchor='w')
        y_offset += 0.07

    ctk.CTkButton(payment_frame, text="Konfirmasi", font=("Arial", 12), bg_color="#ebac4e", command=lambda: confirm_payment(selected_payment_method)).place(relx=0.5, rely=0.8, anchor='center')
    
    arrow4_image = Image.open("Kelompok-16/BG ARROW.png")  # Ganti dengan path gambar tanda panah
    arrow4_image = arrow4_image.resize((30, 30), Image.Resampling.LANCZOS)

    # Mengonversi gambar ke format yang digunakan oleh CTkImage
    arrow4_ctk_image = ctk.CTkImage(light_image=arrow4_image, size=(30, 30))

    # Membuat tombol dengan gambar tanda panah
    arrow4_button = ctk.CTkButton(payment_frame, image=arrow4_ctk_image, text="Pilih Kursi", fg_color="#CDCDCD", text_color="black", command=lambda: show_seat_selection(selected_bus, username, selected_date, origin_city, destination_city, buses_info, [selected_bus[4]]))
    arrow4_button.place(x=0, y=5)

def confirm_payment(selected_payment_method):
    global payment_method, booking_code, selected_seat, username, selected_date, origin_city, destination_city, selected_bus
    payment_method = selected_payment_method.get()
    virtual_account = get_virtual_account(payment_method)
    booking_codes = generate_booking_code(len(selected_seat))
    booking_code = booking_codes  # Store the list of booking codes
    messagebox.showinfo("Payment Success", f"Payment through {payment_method} was successful!\nVirtual Account: {virtual_account}")
    show_confirmation_page()


def generate_booking_code(seat_count):
    try:
        with open('Kelompok-16/booking_codes.csv', 'r') as file:
            lines = file.readlines()
            if lines:
                last_booking_code = lines[-1].strip()
                last_number = int(last_booking_code[1:])
            else:
                last_number = 0
    except (FileNotFoundError, IndexError, ValueError):
        last_number = 0 

    booking_codes = []
    for i in range(seat_count):
        new_number = last_number + 1 + i
        new_booking_code = f'B{new_number:04}'
        booking_codes.append(new_booking_code)

    # Save the new booking codes to the file
    try:
        with open('Kelompok-16/booking_codes.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            for code in booking_codes:
                writer.writerow([code])
    except Exception as e:
        print(f"Error saving booking codes: {e}")

    return booking_codes


def show_confirmation_page():
    global booking_code
    hide_all_frames()
    confirmation_frame.place(x=485, y=230)

    for widget in confirmation_frame.winfo_children():
        widget.destroy()

    confirm_image_path = "Kelompok-16/BG KONFIRMASI.png"

    confirm_image = Image.open(confirm_image_path)
    resized_confirm_image = confirm_image.resize((960, 560), Image.LANCZOS)
    photo = ImageTk.PhotoImage(resized_confirm_image)

    confirm_image_label = tk.Label(confirmation_frame, image=photo, bg='#CDCDCD')
    confirm_image_label.image = photo
    confirm_image_label.place(x=0, y=0)

    ctk.CTkLabel(confirmation_frame, text="Konfirmasi Pemesanan",text_color="black", font=("Prata", 17)).place(relx=0.5, rely=0.11, anchor='n')

    virtual_account = get_virtual_account(payment_method)

    booking_details = f"""
    Kode Pemesanan\t\t: {', '.join(booking_code)}
    Dari\t\t\t: {selected_bus[0]}
    Tujuan\t\t\t: {selected_bus[1]}
    Tanggal dan Waktu\t: {selected_bus[2]}
    Estimasi Tiba\t\t: {selected_bus[3]}
    Kursi\t\t\t: {', '.join(selected_seat)}
    Tipe\t\t\t: {selected_bus[4]}
    Metode Pembayaran\t: {payment_method}
    Kode Pembayaran\t: {virtual_account}
    """

    try:
        price_per_seat = int(selected_bus[5])
        total_price = len(selected_seat) * price_per_seat
        price_per_seat_formatted = format_rupiah(price_per_seat)
        total_price_formatted = format_rupiah(total_price)
        booking_details += f"\nHarga per Kursi\t\t: {price_per_seat_formatted}"
        booking_details += f"\nJumlah yang harus dibayar\t: {total_price_formatted}"
    except ValueError:
        booking_details += "\nPrice per Seat\t: Error retrieving price"
        booking_details += "\nTotal Price\t: Error retrieving price"

    ctk.CTkLabel(confirmation_frame, text=booking_details, font=("Prata", 13), text_color="black",bg_color="#ebac4e", justify=LEFT).place(relx=0.5, rely=0.45, anchor='center')

    ctk.CTkButton(confirmation_frame, text="Bayar", font=("Arial", 12),bg_color="#ebac4e", command=show_payment_confirmation_page).place(relx=0.5, rely=0.8, anchor='center')

    arrow5_image = Image.open("Kelompok-16/BG ARROW.png")  # Ganti dengan path gambar tanda panah
    arrow5_image = arrow5_image.resize((30, 30), Image.Resampling.LANCZOS)

    # Mengonversi gambar ke format yang digunakan oleh CTkImage
    arrow5_ctk_image = ctk.CTkImage(light_image=arrow5_image, size=(30, 30))

    # Membuat tombol dengan gambar tanda panah
    arrow5_button = ctk.CTkButton(confirmation_frame, image=arrow5_ctk_image, text="Pilih Pembayaran", fg_color="#CDCDCD", text_color="black", command=show_payment_page)
    arrow5_button.place(x=0, y=5)

def show_payment_confirmation_page():
    hide_all_frames()
    payment_confirmation_frame.place(x=480,y=230)

    for widget in payment_confirmation_frame.winfo_children():
        widget.destroy()
    
    # Membuat frame baru di dalam frame utama
    inner_frame = ctk.CTkFrame(payment_confirmation_frame, width=600, height=320, fg_color="#ebac4e", corner_radius=10)
    inner_frame.place(relx=0.5, rely=0.5, anchor='center')

    save_booking_data(selected_seat, username, selected_date, origin_city, destination_city, selected_bus[4], booking_code)

    ctk.CTkLabel(inner_frame, text="Pembayaran Telah Terkonfirmasi",text_color="black", font=("Prata", 20), bg_color="#ebac4e").place(relx=0.5, rely=0.25, anchor='n')
    ctk.CTkLabel(inner_frame, text="Terima Kasih Telah Menggunakan Amour Biz!",text_color="black", font=("Prata", 20), bg_color="#ebac4e").place(relx=0.5, rely=0.35, anchor='n')

    ctk.CTkButton(payment_confirmation_frame, text="Cetak e-Ticket", font=("Arial", 12),bg_color="#ebac4e", command=display_eticket).place(relx=0.5, rely=0.7, anchor='center')
    ctk.CTkButton(payment_confirmation_frame, text="Menu Utama", font=("Arial", 12),bg_color="#ebac4e", command=show_menu_frame).place(relx=0.5, rely=0.8, anchor='center')


def get_user_data():
    user_data = {}
    with open('Kelompok-16/user_data.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            user_data[row['username']] = row
    return user_data

def display_eticket():
    ticket_window = Toplevel()
    ticket_window.title("e-Ticket")
    ticket_window.geometry("400x400")

    header_label = Label(ticket_window, text="e-Ticket", font=("Arial", 16, "bold"))
    header_label.place(relx=0.5, rely=0.05, anchor='n')

    user_data = get_user_data()
    username = entry_login_username.get()
    if username in user_data:
        data = user_data[username]
        info_labels = [
            Label(ticket_window, text=f"Name: {data['name']}", font=("Arial", 12)),
            Label(ticket_window, text=f"Phone: {data['phone']}", font=("Arial", 12)),
            Label(ticket_window, text=f"NIK: {data['nik']}", font=("Arial", 12))
        ]
        for i, label in enumerate(info_labels):
            label.place(relx=0.5, rely=0.1 + i*0.05, anchor='n')
    else:
        Label(ticket_window, text="User information not found", font=("Arial", 12)).place(relx=0.5, rely=0.25, anchor='n')

    details_labels = [
        Label(ticket_window, text=f"Bus Class: {selected_bus[4]}", font=("Arial", 12)),
        Label(ticket_window, text=f"From: {selected_bus[0]}", font=("Arial", 12)),
        Label(ticket_window, text=f"To: {selected_bus[1]}", font=("Arial", 12)),
        Label(ticket_window, text=f"Departure: {selected_bus[2]}", font=("Arial", 12)),
        Label(ticket_window, text=f"Estimasi Tiba: {selected_bus[3]}", font=("Arial", 12)),
        Label(ticket_window, text=f"Seats: {', '.join(selected_seat)}", font=("Arial", 12)),
        Label(ticket_window, text=f"Booking Code: {booking_code}", font=("Arial", 12))
    ]
    for i, label in enumerate(details_labels):
        label.place(relx=0.5, rely=0.5 + i*0.05, anchor='n')

    close_button = Button(ticket_window, text="Close", command=ticket_window.destroy)
    close_button.place(relx=0.5, rely=0.9, anchor='n')

    header_label.config(fg="blue")  
    close_button.config(bg="red", fg="white")  


def show_cancel_seat_page():
    hide_all_frames()
    cancel_seat_frame.place(x=480, y=230)

    for widget in cancel_seat_frame.winfo_children():
        widget.destroy()

    cancel_image_path = "Kelompok-16/BG CANCEL.png"

    cancel_image = Image.open(cancel_image_path)
    resized_cancel_image = cancel_image.resize((960, 560), Image.LANCZOS)
    photo = ImageTk.PhotoImage(resized_cancel_image)

    cancel_image_label = tk.Label(cancel_seat_frame, image=photo, bg='#CDCDCD')
    cancel_image_label.image = photo
    cancel_image_label.place(x=0, y=0)

    ctk.CTkLabel(cancel_seat_frame, height=2,text="Pembatalan Tiket", text_color="black", font=("Prata", 16), fg_color="#ebac4e").place(x=330,y=19)

    arrow_image = Image.open("Kelompok-16/BG ARROW.png")  # Ganti dengan path gambar tanda panah
    arrow_image = arrow_image.resize((30, 30), Image.Resampling.LANCZOS)

    # Mengonversi gambar ke format yang digunakan oleh CTkImage
    arrow_ctk_image = ctk.CTkImage(light_image=arrow_image, size=(30, 30))

    # Membuat tombol dengan gambar tanda panah
    arrow_button = ctk.CTkButton(cancel_seat_frame, image=arrow_ctk_image, text="Menu Utama", fg_color="#CDCDCD", text_color="black", command=show_menu_frame)
    arrow_button.place(x=0, y=5)

    booked_seats = load_user_booked_seats(username)
    if not booked_seats:
        ctk.CTkLabel(cancel_seat_frame, height=1, text="You have no booked seats.", text_color="black", font=("Prata", 14), fg_color="#ebac4e").place(relx=0.5, rely=0.38, anchor='center')
        return

    y_offset = 0.2
    for seat_info in booked_seats:
        seat_details = f"Bus: {seat_info[2]} to {seat_info[3]} | Tanggal: {seat_info[1]} | Tipe: {seat_info[5]} | Kursi: {seat_info[4]} | Kode Pemesanan: {seat_info[6]}"
        ctk.CTkLabel(cancel_seat_frame, height=1, text=seat_details, text_color="black", font=("Prata", 13), fg_color="#ebac4e").place(relx=0.07, rely=y_offset + 0.03, anchor='w')
        ctk.CTkButton(cancel_seat_frame, text="Batalkan", font=("Arial", 12),bg_color="#ebac4e", command=lambda s=seat_info: cancel_seat_booking(s)).place(relx=0.79, rely=y_offset)
        y_offset += 0.1


def load_user_booked_seats(username):
    booked_seats = []
    try:
        with open('Kelompok-16/selected_seats.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row and row[0] == username:
                    booked_seats.append(row)
    except FileNotFoundError:
        pass
    except Exception as e:
        print(f"Error loading booked seats: {e}")
    return booked_seats

def cancel_seat_booking(seat_info):
    updated_rows = []
    try:
        with open('Kelompok-16/selected_seats.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row != seat_info:
                    updated_rows.append(row)
        
        with open('Kelompok-16/selected_seats.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(updated_rows)
        
        messagebox.showinfo("Success", f"Seat {seat_info[4]} has been successfully canceled.")
        show_cancel_seat_page()  # Refresh the cancel seat page

    except Exception as e:
        print(f"Error canceling seat booking: {e}")
        messagebox.showerror("Error", f"Failed to cancel seat {seat_info[4]}: {e}")

def hide_all_frames():
    for frame in [login_frame, register_frame, menu_frame, city_selection_frame, bus_selection_frame, seat_selection_frame, payment_frame, confirmation_frame, payment_confirmation_frame, cancel_seat_frame]:
        frame.place_forget()


root = ctk.CTk()
root.title("Amour Biz")
root.geometry("925x500+300+299")
root.configure(bg="#fff")


create_user_table() 

background_image_path = "Kelompok-16/bg_home.png"
background_image = Image.open(background_image_path)
resized_background_image = background_image.resize((1920, 1000), Image.LANCZOS)
background_photo = ImageTk.PhotoImage(resized_background_image)


background_label = tk.Label(root, image=background_photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)


login_frame = Frame(root, width=950, height=550,bg="white")

side_image_path = "Kelompok-16/Amour Biz (1).png"

side_image = Image.open(side_image_path)
resized_side_image = side_image.resize((950, 550), Image.LANCZOS)
photo = ImageTk.PhotoImage(resized_side_image)


side_image_label = tk.Label(login_frame, image=photo, bg='#CDCDCD')
side_image_label.image = photo 
side_image_label.place(x=0, y=0)

heading=Label(login_frame,text='Sign in',fg='#57a1f8',bg='#CDCDCD',font=('Microsoft YaHei UI Light',23,'bold'))
heading.place(x=620,y=90)

def on_enter_username(e):
    entry_login_username.delete(0, 'end')

def on_leave_username(e):
    name=entry_login_username.get()
    if name=='':
        entry_login_username.insert(0,'Username')

entry_login_username = Entry(login_frame,width=25,fg='black',border=0,bg='#CDCDCD',font=('Microsoft YaHei UI Light',11))
entry_login_username.place(x=535,y=180)
entry_login_username.insert(0,'Username')
entry_login_username.bind('<FocusIn>', on_enter_username)
entry_login_username.bind('<FocusOut>', on_leave_username)

Frame(login_frame,width=295,height=2,bg='black').place(x=535,y=207)

def on_enter_password(e):
    entry_login_password.delete(0, 'end')

def on_leave_password(e):
    name=entry_login_password.get()
    if name=='':
        entry_login_password.insert(0, 'Password')

entry_login_password = Entry(login_frame,width=25,fg='black',border=0,bg='#CDCDCD',font=('Microsoft YaHei UI Light',11))
entry_login_password.place(x=540,y=250)
entry_login_password.insert(0,'Password')
entry_login_password.bind('<FocusIn>', on_enter_password)
entry_login_password.bind('<FocusOut>', on_leave_password)

Frame(login_frame,width=295,height=2,bg='black').place(x=535,y=277)

Button(login_frame,width=39,pady=7,text="Sign in",bg='#57a1f8',fg='white',border=0,command=login).place(x=545,y=304)
label=Label(login_frame,text="Don't have an account?",fg='black',bg='#CDCDCD',font=('Microsoft YaHei UI Light',9))
label.place(x=575,y=370)

sign_up = Button(login_frame,width=6,text='Sign up',border=0,bg='#CDCDCD',cursor='hand2',fg='#57a1f8',command=show_register_frame)
sign_up.place(x=715,y=370)


sign_up = Button(login_frame,width=6,text='Sign up',border=0,bg='#CDCDCD',cursor='hand2',fg='#57a1f8',command=show_register_frame)
sign_up.place(x=1520,y=370)


register_frame = Frame(root, width=950, height=600,bg="#CDCDCD")

side_image_path = "Kelompok-16/Amour Biz (1).png"

side_image = Image.open(side_image_path)
resized_side_image = side_image.resize((950, 550), Image.LANCZOS) 
photo = ImageTk.PhotoImage(resized_side_image)


side_image_label = tk.Label(register_frame, image=photo, bg='#CDCDCD')
side_image_label.image = photo 
side_image_label.place(x=0, y=0)

def on_enter_name(e):
    entry_name.delete(0, 'end')

def on_leave_name(e):
    name=entry_name.get()
    if name=='':
        entry_name.insert(0,'Name')

entry_name = ctk.CTkEntry(register_frame, font=('Arial', 12), justify='center',width=170)
entry_name.place(x=500, y=50)
entry_name.insert(0, 'Name')
entry_name.bind('<FocusIn>', on_enter_name)
entry_name.bind('<FocusOut>', on_leave_name)

def on_enter_usernamee(e):
    entry_username.delete(0, 'end')

def on_leave_usernamee(e):
    name=entry_username.get()
    if name=='':
        entry_username.insert(0,'Username')

entry_username = ctk.CTkEntry(register_frame, font=('Arial', 12), justify='center',width=170)
entry_username.place(x=500, y=90)
entry_username.insert(0, 'Username')
entry_username.bind('<FocusIn>', on_enter_usernamee)
entry_username.bind('<FocusOut>', on_leave_usernamee)

def on_enter_email(e):
    entry_email.delete(0, 'end')

def on_leave_email(e):
    name=entry_email.get()
    if name=='':
        entry_email.insert(0,'Email')

entry_email = ctk.CTkEntry(register_frame, font=('Arial', 12), justify='center',width=170)
entry_email.place(x=500, y=130)
entry_email.insert(0, 'Email')
entry_email.bind('<FocusIn>', on_enter_email)
entry_email.bind('<FocusOut>', on_leave_email)

def on_enter_phone(e):
    if entry_phone.get() == 'Phone':
        entry_phone.delete(0, 'end')

def on_leave_phone(e):
    name = entry_phone.get()
    if name == '':
        entry_phone.insert(0, 'Phone')

error_var_phone = ctk.StringVar()
entry_phone = ctk.CTkEntry(register_frame, font=('Arial', 12), justify='center', width=170, textvariable=error_var_phone)
entry_phone.place(x=500, y=170)
entry_phone.insert(0, 'Phone')
entry_phone.bind('<FocusIn>', on_enter_phone)
entry_phone.bind('<FocusOut>', on_leave_phone)


def on_enter_password(e):
    entry_password.delete(0, 'end')

def on_leave_password(e):
    name=entry_password.get()
    if name=='':
        entry_password.insert(0,'Password')

entry_password = ctk.CTkEntry(register_frame, font=('Arial', 12), justify='center',width=170)
entry_password.place(x=500, y=210)
entry_password.insert(0, 'Password')
entry_password.bind('<FocusIn>', on_enter_password)
entry_password.bind('<FocusOut>', on_leave_password)

def on_enter_nik(e):
    if entry_nik.get() == 'NIK':
        entry_nik.delete(0, 'end')

def on_leave_nik(e):
    name = entry_nik.get()
    if name == '':
        entry_nik.insert(0, 'NIK')

error_var_nik = ctk.StringVar()
entry_nik = ctk.CTkEntry(register_frame, font=('Arial', 12), justify='center',width=170, textvariable=error_var_nik)
entry_nik.place(x=500, y=250)
entry_nik.insert(0, 'NIK')
entry_nik.bind('<FocusIn>', on_enter_nik)
entry_nik.bind('<FocusOut>', on_leave_nik)


def on_enter_otp(e):
    entry_otp.delete(0, 'end')

def on_leave_otp(e):
    name=entry_otp.get()
    if name=='':
        entry_otp.insert(0,'OTP')

entry_otp = ctk.CTkEntry(register_frame, font=('Arial', 12), justify='center',width=170)
entry_otp.place(x=500, y=330)
entry_otp.insert(0, 'OTP')
entry_otp.bind('<FocusIn>', on_enter_otp)
entry_otp.bind('<FocusOut>', on_leave_otp)


ctk.CTkButton(register_frame, text="Send OTP", font=("Arial", 12),width=100, command=register_user).place(x=535, y=290)
ctk.CTkButton(register_frame, text="Verify OTP", font=("Arial", 12),width=100, command=verify_otp).place(x=535, y=370)

ctk.CTkButton(register_frame, text="Back to Login", font=("Arial", 12), command=show_login_frame).place(x=517, y=410)

menu_frame = Frame(root, width=960, height=560,bg="#ebac4e")

city_selection_frame = Frame(root, width=960, height=560,bg="#CDCDCD")

home_image_path = "Kelompok-16/BG HOME PAGE.png"

home_image = Image.open(home_image_path)
resized_home_image = home_image.resize((960, 560), Image.LANCZOS)
photo = ImageTk.PhotoImage(resized_home_image)


home_image_label = tk.Label(city_selection_frame, image=photo, bg='#CDCDCD')
home_image_label.image = photo
home_image_label.place(x=0, y=0)


ctk.CTkLabel(city_selection_frame, text="Pilih Kota Asal", height=10, font=("Arial", 12), text_color="black", fg_color="#ebac4e").place(x=350, y=60)
origin_combobox = ttk.Combobox(city_selection_frame, values=get_cities(), font=("Arial", 12))
origin_combobox.place(x=385, y=100)


ctk.CTkLabel(city_selection_frame, text="Pilih Kota Tujuan", height=10, font=("Arial", 12), text_color="black", fg_color="#ebac4e").place(x=350, y=120)
destination_combobox = ttk.Combobox(city_selection_frame, values=get_cities(), font=("Arial", 12))
destination_combobox.place(x=385, y=175)


ctk.CTkLabel(city_selection_frame, text="Pilih Tanggal Keberangkatan", height=10, font=("Arial", 12,), text_color="black", fg_color="#ebac4e").place(x=320, y=180)

date_frame = ctk.CTkFrame(city_selection_frame, width=185, height=20, bg_color="#ebac4e")
date_frame.place(x=300, y=200)

days = list(range(1, 32))
months = list(range(1, 13))
years = list(range(2023, 2025))

day_combobox = ttk.Combobox(date_frame, values=days, width=5, font=("Arial", 12))
day_combobox.place(x=0, y=0)
month_combobox = ttk.Combobox(date_frame, values=months, width=5, font=("Arial", 12))
month_combobox.place(x=70, y=0)
year_combobox = ttk.Combobox(date_frame, values=years, width=7, font=("Arial", 12))
year_combobox.place(x=140, y=0)

ctk.CTkLabel(city_selection_frame, text="Pilih Kelas Bis", height=10, font=("Arial", 12,), text_color="black", fg_color="#ebac4e").place(x=350, y=237)

class_frame = ctk.CTkFrame(city_selection_frame, width=300, height=90) 
class_frame.place(x=340, y=265)


gold_var = tk.BooleanVar()
silver_var = tk.BooleanVar()
bronze_var = tk.BooleanVar()


gold_checkbutton = ctk.CTkCheckBox(class_frame, text="Gold", variable=gold_var, font=("Arial", 12), text_color="black", bg_color="#ebac4e", corner_radius=15)
gold_checkbutton.pack(anchor="w")

silver_checkbutton = ctk.CTkCheckBox(class_frame, text="Silver", variable=silver_var, font=("Arial", 12), text_color="black", bg_color="#ebac4e", corner_radius=15)
silver_checkbutton.pack(anchor="w")

bronze_checkbutton = ctk.CTkCheckBox(class_frame, text="Bronze", variable=bronze_var, font=("Arial", 12), text_color="black", bg_color="#ebac4e", corner_radius=15)
bronze_checkbutton.pack(anchor="w")

ctk.CTkButton(city_selection_frame, text="Cari Tiket", font=("Arial", 12),bg_color="#ebac4e", command=show_selection).place(x=320, y=370)
arrow6_image = Image.open("Kelompok-16/BG ARROW.png")  # Ganti dengan path gambar tanda panah
arrow6_image = arrow6_image.resize((30, 30), Image.Resampling.LANCZOS)

# Mengonversi gambar ke format yang digunakan oleh CTkImage
arrow6_ctk_image = ctk.CTkImage(light_image=arrow6_image, size=(30, 30))

# Membuat tombol dengan gambar tanda panah
arrow6_button = ctk.CTkButton(city_selection_frame, image=arrow6_ctk_image, text="Menu Utama", fg_color="#CDCDCD", text_color="black", command=show_menu_frame)
arrow6_button.place(x=0, y=5)

bus_selection_frame = Frame(root, width=960, height=560,bg="#CDCDCD")

ctk.CTkButton(bus_selection_frame, text="Close", font=("Arial", 12), command=close_bus_selection).place(x=200, y=200) 

cancel_seat_frame = Frame(root, width=960, height=560, bg="#CDCDCD")

seat_selection_frame = Frame(root, width=960, height=560,bg="#CDCDCD")

payment_frame = Frame(root, width=960, height=560,bg="#CDCDCD")

confirmation_frame = Frame(root, width=960, height=560,bg="#CDCDCD")

payment_confirmation_frame = Frame(root, width=960, height=560,bg="#CDCDCD")


show_login_frame()
root.mainloop()
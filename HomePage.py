import csv
from tkinter import *
from tkinter import ttk, messagebox

# Fungsi untuk membaca daftar kota dari file CSV
def get_cities():
    with open('cities_and_buses.csv', 'r') as file:
        reader = csv.reader(file)
        cities = [row[0] for row in reader if row[0] in ["Jakarta", "Tangerang", "Depok", "Bogor", "Bandung"]]
    return cities

# Fungsi untuk menampilkan pilihan kota asal dan tujuan
def show_selection():
    origin_city = origin_combobox.get()
    destination_city = destination_combobox.get()
    departure_date = f"{day_combobox.get()}-{month_combobox.get()}-{year_combobox.get()}"

    selected_classes = []
    if gold_var.get():
        selected_classes.append("Gold")
    if silver_var.get():
        selected_classes.append("Silver")
    if bronze_var.get():
        selected_classes.append("Bronze")
    bus_classes = ", ".join(selected_classes)

    messagebox.showinfo("Selected Details", f"Origin: {origin_city}\nDestination: {destination_city}\nDeparture Date: {departure_date}\nBus Classes: {bus_classes}")

# Ambil daftar kota dari file CSV
cities = get_cities()

# GUI dengan Tkinter
root = Tk()
root.title("City Selection")
root.geometry("400x600")

Label(root, text="Select Origin City:", font=("Arial", 12)).pack(pady=10)
origin_combobox = ttk.Combobox(root, values=cities, font=("Arial", 12))
origin_combobox.pack(pady=5)

Label(root, text="Select Destination City:", font=("Arial", 12)).pack(pady=10)
destination_combobox = ttk.Combobox(root, values=cities, font=("Arial", 12))
destination_combobox.pack(pady=5)

Label(root, text="Select Departure Date:", font=("Arial", 12)).pack(pady=10)

date_frame = Frame(root)
date_frame.pack(pady=5)

days = list(range(1, 32))
months = list(range(1, 13))
years = list(range(2023, 2033))

day_combobox = ttk.Combobox(date_frame, values=days, width=5, font=("Arial", 12))
day_combobox.grid(row=0, column=0, padx=5)
month_combobox = ttk.Combobox(date_frame, values=months, width=5, font=("Arial", 12))
month_combobox.grid(row=0, column=1, padx=5)
year_combobox = ttk.Combobox(date_frame, values=years, width=7, font=("Arial", 12))
year_combobox.grid(row=0, column=2, padx=5)

Label(root, text="Select Bus Classes:", font=("Arial", 12)).pack(pady=10)

class_frame = Frame(root)
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

Button(root, text="Show Selection", font=("Arial", 12), command=show_selection).pack(pady=20)

root.mainloop()



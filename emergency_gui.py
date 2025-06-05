import tkinter as tk
from tkinter import messagebox
import mysql.connector
import re

# Emergency numbers dictionary
emergency_numbers = {
    "Police": "100",
    "Fire": "101",
    "Ambulance": "102",
    "Women Helpline": "1091",
    "Child Helpline": "1098",
    "Traffic Police": "103",
    "Disaster Management": "1078",
    "Health Helpline": "104",
    "Tourist Helpline": "1363",
    "Road Accident Helpline": "1073",
    "Air Accident Helpline": "1071",
    "Gas Leakage": "1906",
    "Earthquake Helpline": "1072",
    "Anti-Terrorism Helpline": "1090",
    "Anti-Drug Helpline": "1093",
    "Anti-Human Trafficking Helpline": "1094",
    "Anti-Corruption Helpline": "1095",
    "Anti-Smuggling Helpline": "1096",
    "Anti-Black Money Helpline": "1097",
    "Anti-Child Labour Helpline": "1099",
    "National Emergency Number": "112"
}

# Validate phone number
def validate_and_format_phone_number(phone_number):
    phone_number = re.sub(r'\D', '', phone_number)
    if len(phone_number) == 10 and phone_number.isdigit():
        return phone_number
    else:
        messagebox.showerror("Error", "Invalid phone number. Enter 10 digits only.")
        return None

# Get emergency number based on problem
def get_emergency_number(problem):
    return emergency_numbers.get(problem, "Service not found.")

# Save user info to MySQL
def save_user_info():
    name = entry_name.get()
    age = entry_age.get()
    phone_number = entry_phone_number.get()
    problem = combo_problem.get()

    if name == "" or age == "" or phone_number == "" or problem == "":
        messagebox.showerror("Error", "Please fill in all fields.")
        return

    formatted_phone = validate_and_format_phone_number(phone_number)
    if formatted_phone is None:
        return

    emergency_number = get_emergency_number(problem)

    try:
        # Connect to MySQL
        conn = mysql.connector.connect(
            host="localhost",
            user="root",       # <-- Replace this
            password="0910",   # <-- Replace this
            database="emergency_system"
        )
        cursor = conn.cursor()
        query = """
            INSERT INTO user_info (name, age, phone_number, problem, emergency_number)
            VALUES (%s, %s, %s, %s, %s)
        """
        data = (name, age, formatted_phone, problem, emergency_number)
        cursor.execute(query, data)
        conn.commit()
        cursor.close()
        conn.close()

        label_result.config(text=f"Emergency Number for {problem}: {emergency_number}")
        messagebox.showinfo("Success", "Information saved to database successfully!")

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", str(err))

# GUI Setup
root = tk.Tk()
root.title("Emergency Information System")

label_name = tk.Label(root, text="Enter your Name:")
label_name.pack(pady=5)
entry_name = tk.Entry(root)
entry_name.pack(pady=5)

label_age = tk.Label(root, text="Enter your Age:")
label_age.pack(pady=5)
entry_age = tk.Entry(root)
entry_age.pack(pady=5)

label_phone = tk.Label(root, text="Enter your Phone Number:")
label_phone.pack(pady=5)
entry_phone_number = tk.Entry(root)
entry_phone_number.pack(pady=5)

label_problem = tk.Label(root, text="Select the Problem (e.g., Police, Fire, Ambulance):")
label_problem.pack(pady=5)

combo_problem = tk.StringVar()
combo_problem.set("Police")
dropdown = tk.OptionMenu(root, combo_problem, *emergency_numbers.keys())
dropdown.pack(pady=5)

button_submit = tk.Button(root, text="Submit", command=save_user_info)
button_submit.pack(pady=10)

label_result = tk.Label(root, text="Emergency Number will appear here", fg="blue")
label_result.pack(pady=10)

root.mainloop()

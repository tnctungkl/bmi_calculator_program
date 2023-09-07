import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sys
import re
from tkcalendar import DateEntry
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

personal_info = {
    'Name': '',
    'Surname': '',
    'Date of Birth': '',
    'Age': '',
    'Telephone': '',
    'Mail': ''
}

personal_info_complete = False

name_pattern = r'^[A-Za-z\s]+$'
telephone_pattern = r'^\d+$'
age_pattern = r'^\d+$'
mail_pattern = r'^[\w\.-]+@[\w\.-]+$'
dob_pattern = r'^\d{2}/\d{2}/\d{4}$'

bmi_decimal = 0.0
bmi_percentage = 0.0
category = ""


def validate_input(pattern, input_str):
    return re.match(pattern, input_str)


def show_gender_selection():
    def close_messagebox():
        messagebox._show("Gender Selection", "")

    result = messagebox.askquestion("Gender Selection", "Please, select gender:", icon='warning', type='yesno')
    if result == 'yes':
        var_gender.set("Male")
        messagebox.showinfo("Confirmation", "Your selection is confirmed!")
        root.after(1000, close_messagebox)
    elif result == 'no':
        var_gender.set("Female")
        messagebox.showinfo("Confirmation", "Your selection is confirmed!")
        root.after(1000, close_messagebox)


def collect_personal_info():
    personal_info_window = tk.Toplevel(root)
    personal_info_window.title("Personal Information")

    ttk.Label(personal_info_window, text="Name:").pack()
    name_entry = ttk.Entry(personal_info_window)
    name_entry.pack()

    ttk.Label(personal_info_window, text="Surname:").pack()
    surname_entry = ttk.Entry(personal_info_window)
    surname_entry.pack()

    ttk.Label(personal_info_window, text="Date of Birth (MM/DD/YYYY):").pack()
    dob_entry = DateEntry(personal_info_window, date_pattern="mm/dd/yyyy")
    dob_entry.pack()

    ttk.Label(personal_info_window, text="Age:").pack()
    age_entry = ttk.Entry(personal_info_window)
    age_entry.pack()

    ttk.Label(personal_info_window, text="Telephone:").pack()
    telephone_entry = ttk.Entry(personal_info_window)
    telephone_entry.pack()

    ttk.Label(personal_info_window, text="Mail:").pack()
    mail_entry = ttk.Entry(personal_info_window)
    mail_entry.pack()

    def get_personal_info():
        global personal_info_complete
        name = name_entry.get()
        surname = surname_entry.get()
        dob = dob_entry.get()
        age = age_entry.get()
        telephone = telephone_entry.get()
        mail = mail_entry.get()

        if all([name, surname, dob, age, telephone, mail]):
            if (validate_input(name_pattern, name) and
                    validate_input(name_pattern, surname) and
                    validate_input(age_pattern, age) and
                    validate_input(telephone_pattern, telephone) and
                    validate_input(mail_pattern, mail)):

                personal_info['Name'] = name
                personal_info['Surname'] = surname
                personal_info['Date of Birth'] = dob
                personal_info['Age'] = age
                personal_info['Telephone'] = telephone
                personal_info['Mail'] = mail

                personal_info_complete = True
                personal_info_window.destroy()
            else:
                messagebox.showwarning("Warning", "Please enter valid information.")
        else:
            messagebox.showwarning("Warning", "Please fill in all fields.")

    submit_button = ttk.Button(personal_info_window, text="Submit", command=get_personal_info)
    submit_button.pack()


def calculate_bmi():
    global category, bmi_decimal, bmi_percentage
    gender = var_gender.get()
    height = entry_height.get().strip()
    weight = entry_weight.get().strip()

    if not height:
        messagebox.showwarning("Warning", "Please enter your 'Height'!")
        entry_height.delete(0, tk.END)
        return
    elif not weight:
        messagebox.showwarning("Warning", "Please enter your 'Weight!")
        entry_weight.delete(0, tk.END)
        return
    elif not gender:
        messagebox.showwarning("Warning", "Please enter your 'Gender'!")
        var_gender.set("")
        return

    height = float(height)
    weight = float(weight)

    if height <= 0 or weight <= 0:
        messagebox.showwarning("Warning", "Please enter valid values!")
        entry_height.delete(0, tk.END)
        entry_weight.delete(0, tk.END)
        return

    if not personal_info_complete:
        messagebox.showwarning("Warning",
                               "Please complete the personal information in the 'Enter Personal Info' section.")
        return

    bmi_decimal = weight / (height * height)
    bmi_percentage = bmi_decimal * 100

    if gender == "Male":
        if bmi_decimal < 20.7:
            category = "Underweight"
        elif 20.7 <= bmi_decimal < 26.4:
            category = "Healthy"
        else:
            category = "Overweight"

    if gender == "Female":
        if bmi_decimal < 19.1:
            category = "Underweight"
        elif 19.1 <= bmi_decimal < 25.8:
            category = "Healthy"
        else:
            category = "Overweight"

    result_label.config(text=f"Name: {personal_info['Name']}\n"
                             f"Surname: {personal_info['Surname']}\n"
                             f"Date of Birth: {personal_info['Date of Birth']}\n"
                             f"Age: {personal_info['Age']}\n"
                             f"Telephone: {personal_info['Telephone']}\n"
                             f"Mail: {personal_info['Mail']}\n\n"
                             f"Your BMI (0.0): {bmi_decimal:.2f}\n"
                             f"Your BMI (%): {bmi_percentage:.2f}\n"
                             f"Category: {category}")


def reset_fields():
    entry_height.delete(0, tk.END)
    entry_weight.delete(0, tk.END)
    var_gender.set("")
    result_label.config(text="")
    global personal_info_complete
    personal_info_complete = False


def quit_program():
    root.destroy()
    sys.exit()


def save_as_pdf():
    if not personal_info_complete:
        messagebox.showwarning("Warning", "Please complete the personal information first.")
        return

    file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])

    if file_path:
        c = canvas.Canvas(file_path, pagesize=letter)

        content = [
            f"Name: {personal_info['Name']}",
            f"Surname: {personal_info['Surname']}",
            f"Date of Birth: {personal_info['Date of Birth']}",
            f"Age: {personal_info['Age']}",
            f"Telephone: {personal_info['Telephone']}",
            f"Mail: {personal_info['Mail']}",
            "",
            f"Your BMI (0.0): {bmi_decimal:.2f}",
            f"Your BMI (%): {bmi_percentage:.2f}",
            f"Category: {category}"
        ]

        x_offset = 50
        y_offset = 750
        line_height = 20

        for line in content:
            c.drawString(x_offset, y_offset, line)
            y_offset -= line_height

        c.showPage()
        c.save()

        messagebox.showinfo("Save as PDF", "The results have been saved as a PDF.")


root = tk.Tk()
root.title("BMI Calculator Program")

personal_info_button = ttk.Button(root, text="Enter Personal Info", command=collect_personal_info)
personal_info_button.grid(row=0, column=0, padx=10, pady=10, sticky="w")

label_height = ttk.Label(root, text="Height (m):")
label_weight = ttk.Label(root, text="Weight (kg):")
label_gender = ttk.Label(root, text="Gender:")

entry_height = ttk.Entry(root)
entry_weight = ttk.Entry(root)
var_gender = tk.StringVar()
var_gender.set("")

male_radio = ttk.Radiobutton(root, text="Male", variable=var_gender, value="Male")
female_radio = ttk.Radiobutton(root, text="Female", variable=var_gender, value="Female")

calculate_button = ttk.Button(root, text="Calculate BMI", command=calculate_bmi)
reset_button = ttk.Button(root, text="Reset", command=reset_fields)
quit_button = ttk.Button(root, text="Quit", command=quit_program)

result_label = ttk.Label(root, text="", wraplength=400)

label_height.grid(row=1, column=0, padx=10, pady=5, sticky="e")
entry_height.grid(row=1, column=1, padx=10, pady=5)

label_weight.grid(row=2, column=0, padx=10, pady=5, sticky="e")
entry_weight.grid(row=2, column=1, padx=10, pady=5)

label_gender.grid(row=3, column=0, padx=10, pady=5, sticky="e")

male_radio.grid(row=3, column=1, padx=5, pady=10, sticky="w")
female_radio.grid(row=4, column=1, padx=5, pady=10, sticky="w")

calculate_button.grid(row=5, column=0, padx=10, pady=10, sticky="w")
reset_button.grid(row=6, column=0, padx=10, pady=10, sticky="w")
quit_button.grid(row=7, column=0, padx=10, pady=10, sticky="w")

result_label.grid(row=1, column=2, rowspan=7, padx=10, pady=5, sticky="nsew")
result_label.grid_columnconfigure(0, weight=1)

save_pdf_button = ttk.Button(root, text="Save as PDF", command=save_as_pdf)
save_pdf_button.grid(row=7, column=2, padx=10, pady=10, sticky="se")

root.columnconfigure(1, weight=1)

root.mainloop()

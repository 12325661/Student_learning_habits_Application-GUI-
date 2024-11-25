import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import re
import matplotlib.pyplot as plt
from collections import Counter

# Function to create the database and the table if it doesn't exist
def create_db():
    try:
        conn = sqlite3.connect('survey.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS responses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER NOT NULL,
                gender TEXT NOT NULL,
                preferred_learning_environment TEXT NOT NULL,
                study_hours_per_week INTEGER NOT NULL,
                study_time TEXT NOT NULL,
                study_tools TEXT NOT NULL,
                primary_device TEXT NOT NULL,
                learning_style TEXT NOT NULL,
                study_satisfaction INTEGER NOT NULL
            )
        ''')
        conn.commit()
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"Error creating database: {str(e)}")
    finally:
        conn.close()

# Function to validate email address
def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

# Function to handle login
def handle_login():
    email = email_entry.get()
    password = password_entry.get()

    # Validate email format
    if not validate_email(email):
        messagebox.showerror("Error", "Please enter a valid email address!")
        return

    # Check if both email and password are entered
    if not email or not password:
        messagebox.showerror("Error", "Please enter both email and password!")
        return

    messagebox.showinfo("Login Successful", "Welcome to the Survey!")
    login_frame.pack_forget()
    survey_frame.pack(fill="both", expand=True)

# Function to validate numeric input
def validate_numeric(value):
    if value.strip() == "":
        return False
    try:
        int(value)
        return True
    except ValueError:
        return False

# Function to clear form fields
def clear_form():
    name_entry.delete(0, tk.END)
    age_entry.delete(0, tk.END)
    gender_var.set("")
    preferred_learning_environment_var.set("")
    study_hours_entry.delete(0, tk.END)
    study_time_var.set("")
    study_tools_entry.delete(0, tk.END)
    primary_device_var.set("")
    learning_style_var.set("")
    study_satisfaction_scale.set(1)

# Function to show graphs
def show_graphs():
    try:
        conn = sqlite3.connect('survey.db')
        cursor = conn.cursor()
        cursor.execute("SELECT primary_device, preferred_learning_environment, study_time, study_satisfaction FROM responses")
        data = cursor.fetchall()
        conn.close()

        if not data:
            messagebox.showerror("Error", "No data available to generate graphs!")
            return

        # Extract data
        devices = [row[0] for row in data]
        environments = [row[1] for row in data]
        study_times = [row[2] for row in data]
        satisfaction = [row[3] for row in data]

        # Graph 1: Most Used Device
        plt.figure(figsize=(10, 8))
        plt.subplot(2, 2, 1)
        device_counts = Counter(devices)
        plt.bar(device_counts.keys(), device_counts.values(), color="skyblue")
        plt.title("Most Used Device")
        plt.xlabel("Device")
        plt.ylabel("Count")

        # Graph 2: Preferred Learning Environment
        plt.subplot(2, 2, 2)
        env_counts = Counter(environments)
        plt.pie(env_counts.values(), labels=env_counts.keys(), autopct='%1.1f%%', startangle=140, colors=["gold", "lightcoral", "lightskyblue"])
        plt.title("Preferred Learning Environment")

        # Graph 3: Study Time Preference
        plt.subplot(2, 2, 3)
        time_counts = Counter(study_times)
        plt.bar(time_counts.keys(), time_counts.values(), color="lightgreen")
        plt.title("Study Time Preference")
        plt.xlabel("Time")
        plt.ylabel("Count")

        # Graph 4: Study Satisfaction
        plt.subplot(2, 2, 4)
        plt.hist(satisfaction, bins=10, color="mediumpurple", edgecolor="black")
        plt.title("Study Satisfaction Levels")
        plt.xlabel("Satisfaction (1-10)")
        plt.ylabel("Count")

        plt.tight_layout()
        plt.show()
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"Error fetching data: {str(e)}")

# Function to handle form submission
def submit_form():
    try:
        # Collect user responses
        name = name_entry.get().strip()
        age = age_entry.get().strip()
        gender = gender_var.get()
        learning_env = preferred_learning_environment_var.get()
        study_hours = study_hours_entry.get().strip()
        study_time = study_time_var.get()
        study_tools = study_tools_entry.get().strip()
        primary_device = primary_device_var.get()
        learning_style = learning_style_var.get()
        satisfaction = int(study_satisfaction_scale.get())

        # Validate all fields are filled
        if not all([name, age, gender, learning_env, study_hours, 
                    study_time, study_tools, primary_device, learning_style]):
            messagebox.showerror("Error", "Please fill all fields before submitting!")
            return

        # Validate numeric fields
        if not validate_numeric(age) or not validate_numeric(study_hours):
            messagebox.showerror("Error", "Age and study hours must be valid numbers!")
            return

        # Convert to integers
        age = int(age)
        study_hours = int(study_hours)

        # Store in database
        conn = sqlite3.connect('survey.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO responses (
                name, age, gender, preferred_learning_environment,
                study_hours_per_week, study_time, study_tools,
                primary_device, learning_style, study_satisfaction
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (name, age, gender, learning_env, study_hours, study_time,
              study_tools, primary_device, learning_style, satisfaction))
        
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Thank you for completing the survey!")
        clear_form()  # Clear the form after successful submission

    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"Error saving response: {str(e)}")
    except ValueError as e:
        messagebox.showerror("Input Error", f"Please check your input values: {str(e)}")
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")

# Create the main Tkinter window
root = tk.Tk()
root.title("Student Learning Habits Analysis")
root.geometry("800x600")
root.configure(bg="#f0f2f5")

# Create the database
create_db()

# ---------------- Styled Login Page ----------------
login_frame = tk.Frame(root, bg="#f0f2f5")
login_frame.pack(fill="both", expand=True)

# Center container for login form
center_frame = tk.Frame(login_frame, bg="white", padx=40, pady=40,
                        highlightthickness=1, highlightbackground="#dddfe2")
center_frame.place(relx=0.5, rely=0.5, anchor="center")

# Login header
tk.Label(center_frame, text="Student learning Habits Analysis",
         font=("Arial", 24, "bold"), bg="white", fg="#1877f2").pack(pady=(0, 20))

tk.Label(center_frame, text="Login to continue",
         font=("Arial", 14), bg="white", fg="#606770").pack(pady=(0, 20))

# Email input
email_container = tk.Frame(center_frame, bg="white")
email_container.pack(fill="x", pady=5)
tk.Label(email_container, text="Email:", font=("Arial", 12), bg="white", fg="#606770").pack(anchor="w")
email_entry = tk.Entry(email_container, width=35, font=("Arial", 12))
email_entry.pack(fill="x", pady=(5, 0))
email_entry.configure(relief="solid", bd=1)

# Password input
password_container = tk.Frame(center_frame, bg="white")
password_container.pack(fill="x", pady=15)
tk.Label(password_container, text="Password:", font=("Arial", 12), bg="white", fg="#606770").pack(anchor="w")
password_entry = tk.Entry(password_container, width=35, font=("Arial", 12), show="•")
password_entry.pack(fill="x", pady=(5, 0))
password_entry.configure(relief="solid", bd=1)

# Login button with hover effect
class HoverButton(tk.Button):
    def __init__(self, master, **kw):
        tk.Button.__init__(self, master=master, **kw)
        self.defaultBackground = self["background"]
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        self["background"] = self["activebackground"]

    def on_leave(self, e):
        self["background"] = self.defaultBackground

login_button = HoverButton(center_frame, text="Login", command=handle_login,
                           bg="#1877f2", fg="white", font=("Arial", 14, "bold"),
                           width=20, pady=8, border=0, cursor="hand2")
login_button.pack(pady=(15, 0))
login_button.configure(activebackground="#145dbf")

# ---------------- Survey Page ----------------
survey_frame = tk.Frame(root, bg="#f0f2f5")
survey_frame.pack_forget()

# Survey form fields
tk.Label(survey_frame, text="Student learning Habits Analysis",
         font=("Arial", 24, "bold"), bg="#f0f2f5", fg="#1877f2").pack(pady=(20, 10))

form_frame = tk.Frame(survey_frame, bg="white", padx=40, pady=40,
                      highlightthickness=1, highlightbackground="#dddfe2")
form_frame.pack(fill="x", padx=80, pady=(0, 20))

tk.Label(form_frame, text="Name:", font=("Arial", 12), bg="white", fg="#606770").grid(row=0, column=0, pady=5, sticky="w")
name_entry = tk.Entry(form_frame, width=30, font=("Arial", 12))
name_entry.grid(row=0, column=1, pady=5)

tk.Label(form_frame, text="Age:", font=("Arial", 12), bg="white", fg="#606770").grid(row=1, column=0, pady=5, sticky="w")
age_entry = tk.Entry(form_frame, width=30, font=("Arial", 12))
age_entry.grid(row=1, column=1, pady=5)

tk.Label(form_frame, text="Gender:", font=("Arial", 12), bg="white", fg="#606770").grid(row=2, column=0, pady=5, sticky="w")
gender_var = tk.StringVar()
gender_combobox = ttk.Combobox(form_frame, textvariable=gender_var, font=("Arial", 12),
                               values=["Male", "Female", "Other"], state="readonly", width=28)
gender_combobox.grid(row=2, column=1, pady=5)

tk.Label(form_frame, text="Preferred Learning Environment:", font=("Arial", 12), bg="white", fg="#606770").grid(row=3, column=0, pady=5, sticky="w")
preferred_learning_environment_var = tk.StringVar()
preferred_learning_environment_combobox = ttk.Combobox(form_frame, textvariable=preferred_learning_environment_var, font=("Arial", 12),
                                                       values=["Online", "Classroom", "Hybrid"], state="readonly", width=28)
preferred_learning_environment_combobox.grid(row=3, column=1, pady=5)

tk.Label(form_frame, text="Study Hours Per Week:", font=("Arial", 12), bg="white", fg="#606770").grid(row=4, column=0, pady=5, sticky="w")
study_hours_entry = tk.Entry(form_frame, width=30, font=("Arial", 12))
study_hours_entry.grid(row=4, column=1, pady=5)

tk.Label(form_frame, text="Study Time Preference:", font=("Arial", 12), bg="white", fg="#606770").grid(row=5, column=0, pady=5, sticky="w")
study_time_var = tk.StringVar()
study_time_combobox = ttk.Combobox(form_frame, textvariable=study_time_var, font=("Arial", 12),
                                   values=["Morning", "Afternoon", "Evening", "Night"], state="readonly", width=28)
study_time_combobox.grid(row=5, column=1, pady=5)

tk.Label(form_frame, text="Preferred Study Tools:", font=("Arial", 12), bg="white", fg="#606770").grid(row=6, column=0, pady=5, sticky="w")
study_tools_entry = tk.Entry(form_frame, width=30, font=("Arial", 12))
study_tools_entry.grid(row=6, column=1, pady=5)

tk.Label(form_frame, text="Primary Device Used:", font=("Arial", 12), bg="white", fg="#606770").grid(row=7, column=0, pady=5, sticky="w")
primary_device_var = tk.StringVar()
primary_device_combobox = ttk.Combobox(form_frame, textvariable=primary_device_var, font=("Arial", 12),
                                       values=["Laptop", "Desktop", "Tablet", "Smartphone"], state="readonly", width=28)
primary_device_combobox.grid(row=7, column=1, pady=5)

tk.Label(form_frame, text="Learning Style:", font=("Arial", 12), bg="white", fg="#606770").grid(row=8, column=0, pady=5, sticky="w")
learning_style_var = tk.StringVar()
learning_style_combobox = ttk.Combobox(form_frame, textvariable=learning_style_var, font=("Arial", 12),
                                       values=["Visual", "Auditory", "Kinesthetic", "Reading/Writing"], state="readonly", width=28)
learning_style_combobox.grid(row=8, column=1, pady=5)

tk.Label(form_frame, text="Study Satisfaction (1-10):", font=("Arial", 12), bg="white", fg="#606770").grid(row=9, column=0, pady=5, sticky="w")
study_satisfaction_scale = tk.Scale(form_frame, from_=1, to=10, orient="horizontal", bg="white", length=220)
study_satisfaction_scale.grid(row=9, column=1, pady=5)

# Buttons for form actions
submit_button = HoverButton(survey_frame, text="Submit", command=submit_form,
                            bg="#1877f2", fg="white", font=("Arial", 14, "bold"),
                            width=25, pady=8, border=0, cursor="hand2")
submit_button.pack(pady=(5, 20))

show_graphs_button = HoverButton(survey_frame, text="Show Graphs", command=show_graphs,
                                 bg="#28a745", fg="white", font=("Arial", 14, "bold"),
                                 width=25, pady=8, border=0, cursor="hand2")
show_graphs_button.pack(pady=(0, 20))

# Start the Tkinter event loop
root.mainloop()

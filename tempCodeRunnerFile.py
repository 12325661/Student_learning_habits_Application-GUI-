
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

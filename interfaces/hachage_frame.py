from tkinter import filedialog, ttk, ttk, Tk, Frame, Label, Entry, Button, Radiobutton, StringVar

import customtkinter


def hash_function(value,):
    return value % 29


def hash_function2(value):

    return 7 - (value % 7)




def find_value(chosen_strategy, value_entry, cells):
    value = int(value_entry.get())  # Get the integer value from the entry widget

    # Initialize a list to store the indices where the value is found
    found_indices = []

    # Calculate the hash index using the hash function
    index = hash_function(value)

    # Iterate through the hash table cells based on the chosen strategy
    if chosen_strategy == "Linear Probing: f(i) = i":
        while cells[index].get():
            if int(cells[index].get()) == value:
                # Change the background color of the cell to indicate that the value is found
                cells[index].configure(border_color="red")
                found_indices.append(index)
            index = (index + 1) % 29
    elif chosen_strategy == "Quadratic Probing: f(i) = i * i":
        i = 1
        while cells[index].get():
            if int(cells[index].get()) == value:
                # Change the background color of the cell to indicate that the value is found
                cells[index].configure(border_color="red")
                found_indices.append(index)
            index = (index + i ** 2) % 29
            i += 1
    elif chosen_strategy == "Double Hashing: f(i) = i * hash2(elem)":
        # Calculate the step size using another hash function (hash2)
        step_size = hash_function2(value)
        while cells[index].get():
            if int(cells[index].get()) == value:
                # Change the background color of the cell to indicate that the value is found
                cells[index].configure(border_color="red")
                found_indices.append(index)
            # Update the index using double hashing
            index = (index + step_size) % 29

    # Check if the value is found at least once
    if found_indices:
        return f"Value {value} found at indices: {', '.join(map(str, found_indices))}."
    else:
        return f"Value {value} not found in the hash table."




def delete_value(chosen_strategy, value_entry, cells):
    value = int(value_entry.get())  # Get the integer value from the entry widget
    index = hash_function(value)  # Calculate the index using the hash function

    # Flag to track if the value is found
    value_found = False

    # Resolve collision based on the chosen strategy
    if chosen_strategy == "Linear Probing: f(i) = i":
        while cells[index].get() != str(value):
            index = (index + 1) % 29
    elif chosen_strategy == "Quadratic Probing: f(i) = i * i":
        i = 1
        while cells[index].get() != str(value):
            index = (index + i ** 2) % 29  # Square the index to resolve collisions
            i += 1
    elif chosen_strategy == "Double Hashing: f(i) = i * hash2(elem)":
        # Calculate the step size using another hash function (hash2)
        step_size = hash_function2(value)
        while cells[index].get() != str(value):
            # Update the index using double hashing
            index = (index + step_size) % 29
            # Recalculate the step size for the next iteration
            step_size = hash_function2(value)

    # Check if the value is found
    if cells[index].get() == str(value):
        # Once the value is found, remove it by setting the cell to an empty string
        cells[index].delete(0, 'end')
        cells[index].configure(border_color="grey")
        value_found = True

    if value_found:
        print("Value deleted.")
    else:
        print("Value not found.")





def add_value(chosen_strategy, value_entry, cells):
    value = int(value_entry.get())
    index = hash_function(value)

    if not cells[index].get():  # Check if the cell is not occupied
        cells[index].insert(0, str(value))
        cells[index].configure(border_color="blue")
    else:
        if chosen_strategy == "Linear Probing: f(i) = i":
            while cells[index].get():
                index = (index + 1) % 29
        elif chosen_strategy == "Quadratic Probing: f(i) = i * i":
            i = 1
            while cells[(index + i ** 2) % 29].get():
                i += 1
            index = (index + i ** 2) % 29
        elif chosen_strategy == "Double Hashing: f(i) = i * hash2(elem)":
            hash2_value = hash_function2(value)
            step_size = hash2_value if hash2_value != 0 else 1  # Ensure step size is not zero
            while cells[index].get():
                index = (index + step_size) % 29

        cells[index].insert(0, str(value))
        cells[index].configure(border_color="blue")


def handle_linear_probing(cells):
        print("hiiiiii")
        # Add your event handling code here
        for cell in cells:
            cell.delete(0, 'end')
            cell.configure(border_color="grey")


def handle_Quadratic_probing(cells):
    print("hiiiiii")
    # Add your event handling code here
    for cell in cells:
        cell.delete(0, 'end')
        cell.configure(border_color="grey")


def create_hachage_frame(app):
    main_frame = customtkinter.CTkFrame(master=app, fg_color="#ffffff")
    main_frame.rowconfigure(0, weight=0)

    main_frame.columnconfigure(0, weight=1)
    main_frame.rowconfigure(1, weight=1)

    main_frame.grid(sticky=customtkinter.EW + customtkinter.NS)

    row1 = customtkinter.CTkFrame(master=main_frame, fg_color="#add8e6")
    row2 = customtkinter.CTkFrame(master=main_frame, fg_color="#e7f2f7")

    row1.grid(row=0, column=0, sticky="nsew", pady=10)
    row2.grid(row=1, column=0, sticky="nsew", pady=10)

    # Créer deux sous-cadres à l'intérieur de row1
    subframe1 = customtkinter.CTkFrame(master=row1, fg_color="#add8e6")
    subframe2 = customtkinter.CTkFrame(master=row1, fg_color="#add8e6")

    # Grille des sous-cadres
    subframe1.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
    subframe2.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

    # Elements pour le premier sous-cadre
    value1_entry = customtkinter.CTkEntry(subframe1)
    value1_entry.grid(row=0, column=0, padx=5, pady=5)
    value = value1_entry.get()

    value2_entry = customtkinter.CTkEntry(subframe1)
    value2_entry.grid(row=0, column=2, padx=5, pady=5)

    value3_entry = customtkinter.CTkEntry(subframe1)
    value3_entry.grid(row=0, column=4, padx=5, pady=5)

    collision_strategy_var = StringVar()
    chosen_strategy = collision_strategy_var.get()
    customtkinter.CTkLabel(subframe2, text="Collision Strategy:").grid(row=0, column=0, padx=5, pady=5)




    customtkinter.CTkRadioButton(subframe2, text="Quadratic Probing: f(i) = i * i", variable=collision_strategy_var,
                                 value="Quadratic Probing: f(i) = i * i").grid(row=0, column=1, padx=5, pady=5)
    # @customtkinter.CTkRadioButton(subframe2, text="Double Hashing: f(i) = i * hash2(elem)",
    # variable=collision_strategy_var,
    # value="Double Hashing: f(i) = i * hash2(elem)").grid(row=0, column=2, padx=5, pady=5)

    # Create the frame for row 2
    hash_table_frame = customtkinter.CTkFrame(master=row2, fg_color="#e7f2f7")
    hash_table_frame.grid(row=0, column=0, sticky="nsew")

    # Create entries to represent the cells
    cells = []
    for i in range(29):
        # Calculate row and column indices
        row_index = i // 7  # Integer division to get row index
        col_index = i % 7  # Modulo operation to get column index

        cell = customtkinter.CTkEntry(hash_table_frame, width=90, height=40)
        cell.grid(row=row_index, column=col_index, padx=5, pady=5)  # Add padx and pady for spacing
        cells.append(cell)

        index_label = customtkinter.CTkLabel(hash_table_frame, text=str(i))
        index_label.grid(row=row_index, column=col_index, padx=0, pady=(49, 0))  # Adjust pady for spacing

        customtkinter.CTkRadioButton(subframe2, text="Linear Probing: f(i) = i", variable=collision_strategy_var,
                                     value="Linear Probing: f(i) = i", command=lambda :handle_linear_probing(cells)).grid(row=0,
                                                                           column=0,
                                                                                                                  padx=5,
                                                                                                                  pady=5)
        customtkinter.CTkRadioButton(subframe2, text="Quadratic Probing: f(i) = i * i", variable=collision_strategy_var,
                                     value="Quadratic Probing: f(i) = i * i",command=lambda :handle_Quadratic_probing(cells)).grid(row=0, column=1, padx=5, pady=5)
        customtkinter.CTkButton(subframe1, text="Insert",
                                command=lambda: add_value(collision_strategy_var.get(), value1_entry, cells)).grid(
            row=0,
            column=1,
            padx=5,
            pady=5)
        customtkinter.CTkRadioButton(subframe2, text="Double Hashing: f(i) = i * hash2(elem)", variable=collision_strategy_var,
                                     value="Double Hashing: f(i) = i * hash2(elem)",command=lambda :handle_Quadratic_probing(cells)).grid(row=0, column=2, padx=5, pady=5)
        customtkinter.CTkButton(subframe1, text="Insert",
                                command=lambda: add_value(collision_strategy_var.get(), value1_entry, cells)).grid(
            row=0,
            column=1,
            padx=5,
            pady=5)
        customtkinter.CTkButton(subframe1, text="Delete",
                                command=lambda: delete_value(collision_strategy_var.get(), value2_entry, cells)).grid(
            row=0, column=3, padx=5, pady=5)
        customtkinter.CTkButton(subframe1, text="Find",
                                command=lambda: find_value(collision_strategy_var.get(), value3_entry, cells)).grid(
            row=0, column=5, padx=5, pady=5)

    return main_frame, cells

from tkinter import filedialog, ttk, ttk, Tk, Frame, Label, Entry, Button, Radiobutton, StringVar

import customtkinter


def hash_function(value):
    return value % 29


def find_value(value_entry, cells):
    value = int(value_entry.get())  # Get the integer value from the entry widget
    index = hash_function(value)  # Calculate the index using the hash function

    # Iterate through the hash table cells starting from the calculated index
    while cells[index].get():
        # Check if the value matches the one in the current cell
        if int(cells[index].get()) == value:
            # Change the background color of the cell to indicate that the value is found
            cells[index].configure(border_color="red")
            return f"Value {value} found at index {index}."

    # Value not found
    return f"Value {value} not found in the hash table."


def delete_value(value_entry, cells):
    value = int(value_entry.get())  # Get the integer value from the entry widget
    index = hash_function(value)  # Calculate the index using the hash function

    # Search for the value in the hash table

    # Once the value is found, remove it by setting the cell to an empty string
    cells[index].delete(0, 'end')
    cells[index].configure(border_color="grey")


def add_value( value_entry, cells):

    print(value_entry.get())
    print(cells)
    value = int(value_entry.get())
    index = hash_function(value)
    print(index)
    if not cells[index].get():  # Check if the cell is not occupied
        cells[index].insert(0, str(value))
        cells[index].configure(border_color="blue")



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

        customtkinter.CTkButton(subframe1, text="Insert",
                                command=lambda: add_value(value1_entry, cells)).grid(
            row=0,
            column=1,
            padx=5,
            pady=5)
        customtkinter.CTkButton(subframe1, text="Delete",
                                command=lambda: delete_value(value2_entry, cells)).grid(
            row=0, column=3, padx=5, pady=5)
        customtkinter.CTkButton(subframe1, text="Find",
                                command=lambda: find_value(value3_entry, cells)).grid(
            row=0, column=5, padx=5, pady=5)

    return main_frame, cells

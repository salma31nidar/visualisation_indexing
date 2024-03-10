from tkinter import StringVar

import customtkinter
import tkinter.messagebox

def hash_function(value):
    return value % 29


def add_value(value, hash_table, colors):
    index = hash_function(value)
    color = colors[index % len(colors)]

    original_index = index  # Store the original index for checking if we've looped around

    while True:
        cell_var = hash_table[index]["var"]
        current_value = cell_var.get()

        if current_value == "":
            # If the cell is empty, insert the value and break the loop
            cell_var.set(str(value))
            cell_border_color = hash_table[index]["border_color"]
            cell_entry = hash_table[index]["entry"]
            break
        else:
            # If the cell is not empty, move to the next index with the same color
            index = (index + 1) % len(hash_table)
            if index == original_index:
                # If we've looped around without finding an empty cell, break the loop
                break
            # If the next cell has a different color, find the next cell with the same color
            while hash_table[index]["border_color"] != color:
                index = (index + 1) % len(hash_table)
                if index == original_index:
                    # If we've looped around without finding a cell with the same color, break the loop
                    break


def delete_value(value, hash_table, colors):
    index = hash_function(value)
    color = colors[index % len(colors)]

    original_index = index  # Store the original index for checking if we've looped around

    while True:
        cell_var = hash_table[index]["var"]
        current_value = cell_var.get()

        if current_value == str(value):
            # If the cell contains the value to delete, delete it and break the loop
            cell_var.set("")  # Clear the cell
            break
        else:
            # Move to the next index with the same color
            index = (index + 1) % len(hash_table)
            if index == original_index:
                # If we've looped around without finding the value, it doesn't exist in the hash table
                break
            # If the next cell has a different color, find the next cell with the same color
            while hash_table[index]["border_color"] != color:
                index = (index + 1) % len(hash_table)
                if index == original_index:
                    # If we've looped around without finding a cell with the same color, break the loop
                    break


def find_value(value, hash_table, colors):
    index = hash_function(value)
    color = colors[index % len(colors)]
    original_index = index  # Store the original index for checking if we've looped around
    found_indices = []

    while True:
        cell_var = hash_table[index]["var"]
        current_value = cell_var.get()

        if current_value == str(value):
            # If the current value matches the search value, add the index to the list of found indices
            found_indices.append(index)

        # Move to the next index with the same color or the next empty cell
        index = (index + 1) % len(hash_table)

        if index == original_index:
            # If we've looped around without finding the value, break the loop
            break

        # If the next cell has a different color, find the next cell with the same color or the next empty cell
        while hash_table[index]["border_color"] != color and hash_table[index]["var"].get() != "":
            index = (index + 1) % len(hash_table)
            if index == original_index:
                # If we've looped around without finding a cell with the same color or an empty cell, break the loop
                break

    if found_indices:
        # If the value is found, display a message box showing the found indices
        tkinter.messagebox.showinfo("Value Found",
                                    f"Value {value} found at indices: {', '.join(map(str, found_indices))}")
    else:
        # If the value is not found, display a message box indicating that the value is not in the hash table
        tkinter.messagebox.showinfo("Value Not Found", f"Value {value} not found in the hash table")


def create_buckets(app):
    main_frame = customtkinter.CTkFrame(master=app, fg_color="#ffffff")
    main_frame.rowconfigure(1, weight=1)
    main_frame.columnconfigure(0, weight=1)

    main_frame.grid(sticky=customtkinter.EW + customtkinter.NS)

    row1 = customtkinter.CTkFrame(master=main_frame, fg_color="#add8e6")
    row2 = customtkinter.CTkFrame(master=main_frame, fg_color="#e7f2f7")

    row1.grid(row=0, column=0, sticky="nsew", pady=10)
    row2.grid(row=1, column=0, sticky="nsew", pady=10)

    hash_table = {}  # Dictionary to store the entries and their colors

    # Create the frame for row 2
    hash_table_frame = customtkinter.CTkFrame(master=row2, fg_color="#e7f2f7")
    hash_table_frame.grid(row=0, column=0, sticky="nsew")
    colors = ["#ff0000", "#00ff00", "#0000ff", "#ffff00", "#00ffff", "#ff00ff", "#ffa500"]
    # Create entries to represent the cells
    for i in range(29):
        row_index = i // 7
        col_index = i % 7

        cell_var = StringVar()  # Create a StringVar for each cell
        entry = customtkinter.CTkEntry(hash_table_frame, width=90, height=40, textvariable=cell_var)
        entry.grid(row=row_index, column=col_index, padx=5, pady=5)

        # Assign border color to the entry based on its index
        border_color = colors[i % len(colors)]
        entry.configure(border_color=border_color)

        # Store the StringVar and border color in the hash_table
        hash_table[i] = {"var": cell_var, "border_color": border_color, "entry": entry}

        index_label = customtkinter.CTkLabel(hash_table_frame, text=str(i))
        index_label.grid(row=row_index, column=col_index, padx=0, pady=(49, 0))

    value1_entry = customtkinter.CTkEntry(row1)
    value1_entry.grid(row=0, column=0, padx=5, pady=5)

    value2_entry = customtkinter.CTkEntry(row1)
    value2_entry.grid(row=0, column=2, padx=5, pady=5)

    value3_entry = customtkinter.CTkEntry(row1)
    value3_entry.grid(row=0, column=4, padx=5, pady=5)

    customtkinter.CTkButton(row1, text="Insert", command=lambda: add_value(int(value1_entry.get()), hash_table, colors)
                            ).grid(
        row=0,
        column=1,
        padx=5,
        pady=5)

    customtkinter.CTkButton(row1, text="Delete",command=lambda: delete_value(int(value2_entry.get()), hash_table,colors)
                            ).grid(
        row=0, column=3, padx=5, pady=5)

    customtkinter.CTkButton(row1, text="Find",command=lambda : find_value(int(value3_entry.get()),hash_table,colors)
                            ).grid(
        row=0, column=5, padx=5, pady=5)

    return main_frame, hash_table

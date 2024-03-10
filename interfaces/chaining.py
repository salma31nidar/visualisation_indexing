from PIL import Image
import customtkinter


# Global variables
values_global = []
added_cells = []
arrow_labels = []


# Hash function
def hash_function(value):
    return value % 10


def add_value(value, cells):
    global values_global, added_cells, arrow_labels
    # Hash the value to get the index
    index = hash_function(int(value))

    # Check if the cell is empty
    if not cells[index].get():
        cells[index].insert(0, str(value))  # Insert the value directly into the cell
        cells[index].configure(border_color="blue")
    else:
        print("hi")
        new_entry = customtkinter.CTkEntry(cells[index].master, width=70)
        new_entry.insert(0, str(value))  # Insert the new value into the new entry

        # Calculate the next available row in the cell
        next_row = cells[index].grid_size()[1] + 1  # Adjusted for the number of columns

        # Place the new entry underneath the existing one in the same cell
        new_entry.grid(row=next_row, column=cells[index].grid_info()["column"], padx=10, pady=5)
        print("hi2")
        # Add an arrow between the old and new entries
        arrow = customtkinter.CTkImage(Image.open("Images/arrow-removebg-preview.png"), size=(100, 100))
        arrow_label = customtkinter.CTkLabel(cells[index].master, image=arrow, text="")
        arrow_label.image = arrow  # Keep a reference to avoid garbage collection
        arrow_label.grid(row=next_row - 1, column=cells[index].grid_info()["column"], padx=10, pady=5)
        print("hi3")
        cells[index].configure(border_color="blue")
        cells[index].grid_rowconfigure(next_row, weight=1)

        # Update the added_cells list with the newly added cell and arrow label
        added_cells.append((new_entry, arrow_label, value))

    values_global.append((index, value))


# Function to delete a value from the cells
def delete_value(value, cells):
    global values_global, added_cells
    print("before", values_global)
    index = hash_function(int(value))

    # Check if the value is present in the cells
    if cells[index].get() == str(value):
        print("1")
        cells[index].delete(0, 'end')
        cells[index].configure(border_color="grey")  # Set the border color to grey
        # Delete the value from values_global
        for idx, val in values_global:
            # Check if the value matches the one to be deleted and if it hasn't been removed yet
            if val == value:
                # Remove the first occurrence of the value
                values_global.remove((idx, val))
                print("Value found and deleted from the cells.", values_global)

        # Find the next value from the added cells
        next_value = None
        for entry, arrow_label, cell_value in added_cells:
            if hash_function(int(cell_value)) == index:
                next_value = cell_value
                break

        # Update the cell with the next value
        if next_value:
            cells[index].delete(0, 'end')
            cells[index].insert(0, str(next_value))
            print("Value replaced with the next one from added cells.")

            # Delete the entry and arrow_label associated with the next value
            for entry, arrow_label, cell_value in added_cells:
                if cell_value == next_value:
                    entry.grid_forget()
                    arrow_label.grid_forget()
                    added_cells.remove((entry, arrow_label, cell_value))  # Remove the entry from added_cells
                    print("Entry and arrow label removed.")
                    break

            print("after", values_global)

    else:
        print("2")
        # If the value was not found in the cells, check the added cells

        for entry, arrow_label, cell_value in added_cells:
            print("added_cells", added_cells)
            print("cell", cell_value)
            print("value", value)

            # Check if the value in added_cells is still present in cells
            if cells[hash_function(int(cell_value))].get() == str(cell_value):
                # If yes, check if its index matches the index we are trying to delete
                if hash_function(int(cell_value)) == index:
                    print("hi2")
                    values_global = [(idx, val) for idx, val in values_global if val != value]

                    # Forget both the entry and the associated arrow label
                    entry.grid_forget()
                    arrow_label.grid_forget()

                    # Remove the entry from added_cells
                    added_cells.remove((entry, arrow_label, cell_value))

                    print("Value found and deleted from the added cells.", values_global)
                    break


def find_value(value, cells):
    index = hash_function(int(value))
    if cells[index].get() == str(value):
        cells[index].configure(border_color="red")
        print("Value found in the cells.")
    else:
        found = False
        for entry, _, cell_value in added_cells:
            if cell_value == value:
                entry.configure(border_color="red")
                found = True
                break
        if found:
            print("Value found in the added cells.")
        else:
            print("Value not found.")





# Function to create the GUI
def create_chaining(app):
    global added_cells
    main_frame = customtkinter.CTkFrame(master=app, fg_color="#ffffff")
    main_frame.rowconfigure(1, weight=1)
    main_frame.columnconfigure(0, weight=1)
    main_frame.grid(sticky=customtkinter.EW + customtkinter.NS)

    row1 = customtkinter.CTkFrame(master=main_frame, fg_color="#add8e6")
    row2 = customtkinter.CTkFrame(master=main_frame, fg_color="#e7f2f7")

    row1.grid(row=0, column=0, sticky="nsew", pady=10)
    row2.grid(row=1, column=0, sticky="nsew", pady=10)

    value1_entry = customtkinter.CTkEntry(row1)
    value1_entry.grid(row=0, column=0, padx=5, pady=5)
    value = value1_entry.get()

    value2_entry = customtkinter.CTkEntry(row1)
    value2_entry.grid(row=0, column=2, padx=5, pady=5)

    value3_entry = customtkinter.CTkEntry(row1)
    value3_entry.grid(row=0, column=4, padx=5, pady=5)

    hash_table_frame = customtkinter.CTkFrame(master=row2, fg_color="#e7f2f7")
    hash_table_frame.grid(row=0, column=0, sticky="nsew")

    # Create entries to represent the cells
    cells = []
    for i in range(10):
        # Calculate row and column indices
        row_index = i // 10  # Integer division to get row index
        col_index = i % 10  # Modulo operation to get column index

        cell = customtkinter.CTkEntry(hash_table_frame, width=70, height=40)
        cell.grid(row=row_index, column=col_index, padx=10, pady=10)  # Add padx and pady for spacing
        cells.append(cell)

        index_label = customtkinter.CTkLabel(hash_table_frame, text=str(i))
        index_label.grid(row=row_index, column=col_index, padx=0, pady=(29, 0))  #

    customtkinter.CTkButton(row1, text="Insert", command=lambda: add_value(value1_entry.get(), cells)
                            ).grid(
        row=0,
        column=1,
        padx=5,
        pady=5)
    customtkinter.CTkButton(row1, text="Delete", command=lambda: delete_value(value2_entry.get(), cells)
                            ).grid(
        row=0, column=3, padx=5, pady=5)
    customtkinter.CTkButton(row1, text="Find",command=lambda: find_value(value3_entry.get(), cells)
                            ).grid(
        row=0, column=5, padx=5, pady=5)

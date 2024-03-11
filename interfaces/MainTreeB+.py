import os
import tkinter
import customtkinter
from PIL import Image, ImageTk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

from treebb import BPlusTree

MAX_DEGREE = 3
INSERT = None
FIND = None
DELETE = None

def draw_tree(row2):
    image_path = "tree_image.png"
    if os.path.exists(image_path):
        # Load the image if it exists
        bbtree = Image.open(image_path)
        #bbtree = ImageTk.PhotoImage(bbtree)

        figure = Figure(figsize=(10, 4), dpi=100)
        canvas = FigureCanvasTkAgg(figure, master=row2)
        canvas.get_tk_widget().place(relx=0.5, rely=0.5, anchor="center")
        axes = figure.add_subplot(111)
        axes.imshow(bbtree, aspect="auto")
        axes.axis('off')
        canvas.draw()

        #canvas = customtkinter.CTkCanvas(master=row2, width=800, height=600)
        #canvas.create_image(400, 300, image=bbtree)  # Place the image at the center of the canvas
        #canvas.place(relx=0.5, rely=0.5, anchor="center")


def getOptionMaxDegree(op):
    """
        Recuperer la valeur de optimmenu
        param:
            op: la valeur choisi par user
    """
    global MAX_DEGREE
    MAX_DEGREE = op


def getInsertValue(val, tree, row):
    """
        Recuperer la valeur a ajouter
        param:
            op: la valeur entrer par user
    """
    global INSERT
    INSERT = val.get()
    tree.insert(INSERT)
    dot_tree = tree.to_dot()
    dot_tree.render("tree_image", format="png", cleanup=True)

    draw_tree(row)


def getDeleteValue(val, tree, row):
    """
        Recuperer la valeur a supprimer
        param:
            op: la valeur entrer par user
    """
    global DELETE
    DELETE = val.get()
    tree.delete(DELETE)
    dot_tree = tree.to_dot()
    dot_tree.render("tree_image", format="png", cleanup=True)
    draw_tree(row)

def getFindValue(val):
    """
        Recuperer la valeur a trouver
        param:
            op: la valeur entrer par user
    """
    global FIND
    FIND = val.get()

def create_main_frame(app):
    main_frame = customtkinter.CTkFrame(master=app)
    btree = BPlusTree(MAX_DEGREE)
    canvas_frame = customtkinter.CTkFrame(master=main_frame)
    canvas_frame.grid(row=2, column=0, sticky=customtkinter.EW + customtkinter.NS)

    main_frame.columnconfigure(0, weight=1)
    main_frame.rowconfigure(2, weight=1)

    main_frame.grid(sticky=customtkinter.EW + customtkinter.NS)

    row1 = customtkinter.CTkFrame(master=main_frame)
    row2 = customtkinter.CTkFrame(master=main_frame)

    row2.columnconfigure(0, weight=1)
    row2.columnconfigure(1, weight=1)
    row2.columnconfigure(2, weight=1)
    row2.columnconfigure(3, weight=1)
    row2.columnconfigure(4, weight=1)



    row1.grid(row=0, column=0, sticky="nsew", pady=10)
    row2.grid(row=1, column=0, sticky="nsew", pady=10)

    IASD = customtkinter.CTkImage(Image.open("../Images/IASD.png"), size=(100, 100))
    FSTT = customtkinter.CTkImage(Image.open("../Images/FSTT.png"), size=(100, 100))

    customtkinter.CTkLabel(master=row1, image=IASD, text="").pack(side="left", padx=10, pady=20)
    customtkinter.CTkLabel(master=row1, image=FSTT, text="").pack(side="right", padx=10, pady=20)

    # customtkinter.CTkLabel(master=row2, text="Import your Dataset", font=("Arial", 25)).pack(pady=50)
    # customtkinter.CTkButton(master=row2, text="Browse File").pack(pady=10)

    # Insert
    entry_var1 = tkinter.IntVar(value=0)
    customtkinter.CTkLabel(master=row2, text="Insert", font=("Arial", 20)).grid(row=0, column=0, sticky="nsew", padx=10,
                                                                                pady=10)
    customtkinter.CTkEntry(master=row2, placeholder_text="Entrer un nombre", textvariable=entry_var1).grid(row=1,
                                                                                                           column=0,
                                                                                                           sticky="nsew",
                                                                                                           padx=10,
                                                                                                           pady=10)
    customtkinter.CTkButton(master=row2, text="Insert", command=lambda: getInsertValue(entry_var1, btree, canvas_frame)).grid(row=2,
                                                                                                         column=0,
                                                                                                         sticky="nsew",
                                                                                                         padx=10,
                                                                                                         pady=10)

    # Delete
    entry_var2 = tkinter.IntVar(value=0)
    customtkinter.CTkLabel(master=row2, text="Delete", font=("Arial", 20)).grid(row=0, column=1, sticky="nsew", padx=10,
                                                                                pady=10)
    customtkinter.CTkEntry(master=row2, placeholder_text="Entrer un nombre", textvariable=entry_var2).grid(row=1,
                                                                                                           column=1,
                                                                                                           sticky="nsew",
                                                                                                           padx=10,
                                                                                                           pady=10)
    customtkinter.CTkButton(master=row2, text="DELETE", command=lambda :getDeleteValue(entry_var2, btree, canvas_frame)).grid(row=2, column=1, sticky="nsew", padx=10, pady=10)

    # Find
    entry_var3 = tkinter.IntVar(value=0)
    customtkinter.CTkLabel(master=row2, text="Find", font=("Arial", 20)).grid(row=0, column=2, sticky="nsew", padx=10,
                                                                              pady=10)
    customtkinter.CTkEntry(master=row2, placeholder_text="Entrer un nombre", textvariable=entry_var3).grid(row=1,
                                                                                                           column=2,
                                                                                                           sticky="nsew",
                                                                                                           padx=10,
                                                                                                           pady=10)
    customtkinter.CTkButton(master=row2, text="Find", command=lambda :getFindValue(entry_var3)).grid(row=2, column=2, sticky="nsew", padx=10, pady=10)

    # Max Degree
    customtkinter.CTkLabel(master=row2, text="Max Degre", font=("Arial", 20)).grid(row=0, column=3, sticky="nsew",
                                                                                   padx=10, pady=10)
    combobox = customtkinter.CTkOptionMenu(master=row2,
                                           values=["3", "4", "5", "6"],
                                           command=lambda option: getOptionMaxDegree(option)
                                           )
    combobox.grid(row=1, column=3, sticky="nsew")

    # Clear tree
    customtkinter.CTkButton(master=row2, text="Clear").grid(row=1, column=4, sticky="nsew", padx=10, pady=10)








if __name__ == "__main__":
    root = customtkinter.CTk()
    root.title("Arbre B++")
    root.geometry("720x700")

    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    # Your GUI widgets and logic would go here
    create_main_frame(root)

    root.mainloop()

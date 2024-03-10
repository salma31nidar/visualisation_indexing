from tkinter import filedialog, ttk

import customtkinter
from PIL import Image
import subprocess
import os
import pandas as pd
from options import display_options
from hachage_frame import create_hachage_frame
from tkinter import messagebox



def create_main_frame(app):
    main_frame = customtkinter.CTkFrame(master=app, fg_color="#ffffff")

    main_frame.columnconfigure(0, weight=1)
    main_frame.rowconfigure(1, weight=1)

    main_frame.grid(sticky=customtkinter.EW + customtkinter.NS)

    row1 = customtkinter.CTkFrame(master=main_frame, fg_color="#add8e6")
    row2 = customtkinter.CTkFrame(master=main_frame, fg_color="#e7f2f7")

    row1.grid(row=0, column=0, sticky="nsew", pady=10)
    row2.grid(row=1, column=0, sticky="nsew", pady=10)

    # APPEARANCE MODE

    switch_var = customtkinter.StringVar(value="light")
    customtkinter.set_appearance_mode(switch_var.get())


    # END OF APPEARANCE MODE

    IASD = customtkinter.CTkImage(Image.open("Images/IASD.png"), size=(100, 100))
    FSTT = customtkinter.CTkImage(Image.open("Images/FSTT.png"), size=(100, 100))


    customtkinter.CTkLabel(master=row1, image=IASD, text="").pack(side="left", padx=10, pady=20)
    customtkinter.CTkLabel(master=row1, image=FSTT, text="").pack(side="right", padx=10, pady=20)


    customtkinter.CTkLabel(master=row2, text="START <3", font=("Arial", 25)).pack(pady=(30, 0))

    customtkinter.CTkButton(master=row2, text="Hachage ",
                            command=lambda: switch_to_options(app, main_frame)).pack(pady=(50, 10), side='top',
                                                                                    anchor='center', padx=30)

    customtkinter.CTkButton(master=row2, text="Arbre b++",
                            ).pack(pady=10, side='top', anchor='center',
                                                                                  padx=30)


    # Help button callback function


def switch_to_hachage(main_app, main_frame):
    main_frame.grid_forget()

    # Create and pack the new frame
    create_hachage_frame(main_app).grid(sticky=customtkinter.EW + customtkinter.NS)


def switch_to_options(main_app,main_frame):
    main_frame.grid_forget()

    display_options(main_app).grid(sticky=customtkinter.EW + customtkinter.NS)








if __name__ == "__main__":
    app = customtkinter.CTk()
    app.title("Projet Python")
    app.geometry("720x700")

    app.columnconfigure(0, weight=1)
    app.rowconfigure(0, weight=1)

    create_main_frame(app)

    app.mainloop()

import customtkinter
from PIL import Image
from hachage_frame import create_hachage_frame
from chaining import create_chaining
from buckets import create_buckets

def display_options(app):
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

    customtkinter.CTkLabel(master=row2, text="START HACHAGE <3", font=("Arial", 25)).pack(pady=(30, 30))

    # Add buttons for the options

    customtkinter.CTkButton(master=row2, text="Résolution avec OPEN ADDRESSING", command=lambda: switch_to_hachage(app, main_frame)).pack( side='top',
                                                                                    anchor='center', pady=5, padx=5)
    customtkinter.CTkButton(master=row2, text="Résolution avec CLOSED ADDRESSING", command=lambda: switch_to_chaining(app, main_frame)).pack( side='top',
                                                                                    anchor='center', pady=5, padx=5)
    customtkinter.CTkButton(master=row2, text="Buckets", command=lambda: switch_to_buckets(app,main_frame)).pack( side='top',
                                                                                    anchor='center', pady=5, padx=5)
    return main_frame


def switch_to_hachage(main_app, main_frame):
    main_frame.grid_forget()

    # Create and pack the new frame
    create_hachage_frame(main_app).grid(sticky=customtkinter.EW + customtkinter.NS)

def switch_to_chaining(main_app, main_frame):
    main_frame.grid_forget()

    # Create and pack the new frame
    create_chaining(main_app).grid(sticky=customtkinter.EW + customtkinter.NS)

def switch_to_buckets(main_app, main_frame):
    main_frame.grid_forget()

    # Create and pack the new frame
    create_buckets(main_app).grid(sticky=customtkinter.EW + customtkinter.NS)
import os
import sys
import customtkinter
from tkinter import messagebox
import UploadBot
from tkinter import *
sys.path.insert(1, os.getcwd() + "\\venv\\Lib\\site-packages")


customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("dark-blue")

root = customtkinter.CTk()
root.title("CyberGuru_UploadBOT by A.A. (v1.0)")
root.geometry("900x750")

instance = ""
MY_USERNAME = ""
can_close = False


def stop_bot():
    root.destroy()


def start_bot():
    global instance
    global can_close
    error_found = False
    if not list.curselection() and not entry_instace.get():
        messagebox.showerror("No instance", "Please select an instance")
        error_found = True
    if optionmenu_1.get() == "Operazione da eseguire" and error_found == False:
        messagebox.showerror("No action", "Please select an action to perform")
        error_found = True
    if not entry0.get() and error_found == False:
        messagebox.showerror("No module/trophy", "Please select a module/trophy")
        error_found = True
    if not entry1.get() and error_found == False:
        messagebox.showerror("No username", "Please input Username")
        error_found = True
    else:
        set_username(entry1.get())
    if not entry2.get() and error_found == False:
        messagebox.showerror("No password", "Please input Password")
        error_found = True
    if not error_found:
        #can_close = True
        for element in list.curselection():
            set_instance(element)
            bot = UploadBot.UploadBot(optionmenu_1.get(), entry0.get(), instance, MY_USERNAME, entry2.get(), optionmenu_2.get())
            bot.start_bot()
        if entry_instace.get():
            istanza = entry_instace.get().replace("https://", "").replace("www", "")
            bot = UploadBot.UploadBot(optionmenu_1.get(), entry0.get(), istanza, MY_USERNAME, entry2.get(), optionmenu_2.get())
            bot.start_bot()

def set_instance(choice):
    global instance
    match choice:
        case 0:
            instance = "dev.enterprise.cyberguru.it"
        case 1:
            instance = "enterprise.cyberguru.it"
        case 2:
            instance = "enterprise-ww.cyberguru.it"
        case 3:
            instance = "pirelli.cyberguru.it"
        case 4:
            instance = "awareness.cyberguru.it"
        case 5:
            instance = "international.cyberguru.it"
        case 6:
            instance = "acsdatasystems.cyberguru.it"
        case 7:
            instance = "axsym.cyberguru.it"
        case 8:
            instance = "pentaqo.cyberguru.it"
        case 9:
            instance = "cyberawareness.aeronautica.difesa.it"
        case _:
            print("No instance selected....Closing application")
            start_bot()

def set_username(username):
    global MY_USERNAME
    match username:
        case "1":
            MY_USERNAME = "axel.antoci@cyberguru.eu"
        case "5":
            MY_USERNAME = "vincenzo.matrone@cyberguru.eu"
        case "9":
            MY_USERNAME = "marco.calvieri@cyberguru.eu"
        case _:
            MY_USERNAME = username

frame_top1 = customtkinter.CTkFrame(master=root)
frame_top1.pack(pady=20, padx=40, fill="both", expand=True, side="top")
# frame_top2 = customtkinter.CTkFrame(master=root)
# frame_top2.pack(pady=20, padx=40, fill="both", expand=True, side="top")
frame = customtkinter.CTkFrame(master=root)
frame.pack(pady=20, padx=40, fill="both", expand=True, side="bottom")

label_top = customtkinter.CTkLabel(master=frame_top1, text="Instance")
label_top.pack(pady=12, padx=10)

label = customtkinter.CTkLabel(master=frame, text="Upload System")
label.pack(pady=12, padx=10)
# ==========================================================



# Choosing selectmode as multiple
# for selecting multiple options
list = Listbox(master=frame_top1, selectmode="multiple", width=50, fg="cornsilk")

# Widget expands horizontally and
# vertically by assigning both to
# fill option
list.pack(expand=YES)

# Taking a list 'x' with the items
x = ["Dev", "Enterprise", "Enterprise-ww", "Pirelli", "Awareness",
     "International", "Acsdatasystems", "Axsym", "Pentaqo", "Resia"]

for each_item in range(len(x)):
    list.insert(END, x[each_item])

    # coloring alternative lines of listbox
    list.itemconfig(each_item,
                    bg="grey25" if each_item % 2 == 0 else "grey30")

entry_instace=customtkinter.CTkEntry(master=frame_top1, placeholder_text="Istanza non presente in lista (Es. enterprise.cyberguru.it)", width=800)
entry_instace.pack(pady=12, padx=10)
# ==========================================================

optionmenu_1 = customtkinter.CTkOptionMenu(frame, values=["Upload quiz", "Upload coppe", "Upload video"], width=800)
optionmenu_1.pack(pady=10, padx=10, expand=True)
optionmenu_1.set("Action")

optionmenu_2 = customtkinter.CTkOptionMenu(frame, values=["1", "2", "3"], width=400)
optionmenu_2.pack(pady=10, padx=10, expand=True)
optionmenu_2.set("Level")

entry0=customtkinter.CTkEntry(master=frame, placeholder_text="Modulo (es. M01) o Coppa (es. C02) - "
                                                             "Selezione multima separando ID con virgola (es.M01,M02)", width=800)
entry0.pack(pady=12, padx=10)

entry1=customtkinter.CTkEntry(master=frame, placeholder_text="Username", width=800)
entry1.pack(pady=12, padx=10)
entry2=customtkinter.CTkEntry(master=frame, placeholder_text="Password", show="*", width=800)
entry2.pack(pady=12, padx=10)

button = customtkinter.CTkButton(master=frame, text="Start bot", command=start_bot)
button.pack(pady=6, padx=10)

button_stop = customtkinter.CTkButton(master=frame, text="Exit", command=stop_bot)
button_stop.pack(pady=12, padx=10)


import os
import sys
sys.path.insert(1, os.getcwd() + "\\venv\\Lib\\site-packages")
import upload_quiz_level_1
import upload_trophies_level_1
import customtkinter
from tkinter import messagebox

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("dark-blue")

root = customtkinter.CTk()
root.title("CyberGuru_UploadBOT by A.A. (v1.0)")
root.geometry("800x650")

instance = ""
MY_USERNAME = ""
can_close = False
def start_bot():
    global instance
    global can_close
    error_found = False
    if radiobutton_var.get() == -1:
        messagebox.showerror("No instance", "Please select an instance")
        error_found = True
    else:
        set_instance(radiobutton_var.get())

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
        can_close = True
        match optionmenu_1.get():
            case "Upload quiz (LVL 1)":
                upload_quiz_level_1.uploadQuizMain(instance, MY_USERNAME, entry2.get(), entry0.get())
            case "Upload coppe (LVL 1)":
                upload_trophies_level_1.uploadTrophyMain(instance, MY_USERNAME, entry2.get(), entry0.get())
    if can_close:
        root.destroy()

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
        case _:
            print("No instance selected....Closing application")

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


frame = customtkinter.CTkFrame(master=root)
frame.pack(pady=20, padx=40, fill="both", expand=True)

label = customtkinter.CTkLabel(master=frame, text="Upload System")
label.pack(pady=12, padx=10)

radiobutton_var = customtkinter.IntVar(value=-1)

radiobutton_1 = customtkinter.CTkRadioButton(master=frame, text="Dev", variable=radiobutton_var, value=0)
radiobutton_1.pack(pady=10, padx=10)

radiobutton_2 = customtkinter.CTkRadioButton(master=frame,  text="Enterprise", variable=radiobutton_var, value=1)
radiobutton_2.pack(pady=10, padx=10)

radiobutton_3 = customtkinter.CTkRadioButton(master=frame, text="Enterprise-ww", variable=radiobutton_var, value=2)
radiobutton_3.pack(pady=10, padx=10)

radiobutton_4 = customtkinter.CTkRadioButton(master=frame, text="Pirelli", variable=radiobutton_var, value=3)
radiobutton_4.pack(pady=10, padx=10)

radiobutton_5 = customtkinter.CTkRadioButton(master=frame, text="Awareness", variable=radiobutton_var, value=4)
radiobutton_5.pack(pady=10, padx=10)

radiobutton_6 = customtkinter.CTkRadioButton(master=frame, text="International", variable=radiobutton_var, value=5)
radiobutton_6.pack(pady=10, padx=10)

optionmenu_1 = customtkinter.CTkOptionMenu(frame, values=["Upload quiz (LVL 1)", "Upload coppe (LVL 1)"], width=800)
optionmenu_1.pack(pady=10, padx=10, expand=True)
optionmenu_1.set("Operazione da eseguire")

entry0=customtkinter.CTkEntry(master=frame, placeholder_text="Modulo (es. M01) o Coppa (es. C02)", width=800)
entry0.pack(pady=12, padx=10)

entry1=customtkinter.CTkEntry(master=frame, placeholder_text="Username", width=800)
entry1.pack(pady=12, padx=10)
entry2=customtkinter.CTkEntry(master=frame, placeholder_text="Password", show="*", width=800)
entry2.pack(pady=12, padx=10)

button = customtkinter.CTkButton(master=frame, text="Start bot", command=start_bot)
button.pack(pady=12,padx=10)

# checkbox = customtkinter.CTkCheckBox(master=frame, text="Remeber me")
# checkbox.pack(pady=12, padx=10)

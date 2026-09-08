import socket
import customtkinter
import threading
from PIL import Image


app = customtkinter.CTk()
app.title("Port Scanner")
app.configure(fg_color="#212529")
app.geometry("500x500")


def port_scanner():

    target_ip = ip_entry.get()

    for port in range(1, 65535):
        so = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        so.settimeout(1)
        result = so.connect_ex((target_ip, port))


        if result == 0:
            result_box.insert("end", ("[+] Port {} is open\n".format(port)))

        so.close()


def start_scan_thread():
    t = threading.Thread(target=port_scanner)
    t.start()


logo_image = customtkinter.CTkImage(
    light_image=Image.open("images/logo.png"),
    dark_image=Image.open("images/logo.png"),
    size=(100, 100)
)


logo_label = customtkinter.CTkLabel(app, image=logo_image, text="")
logo_label.pack(pady=20)


ip_entry = customtkinter.CTkEntry(app, placeholder_text="IP Address")
ip_entry.pack()


button = customtkinter.CTkButton(app, text="Target", command=start_scan_thread)
button.configure(fg_color="red")
button.pack(padx=20, pady=20)


result_label = customtkinter.CTkLabel(app, text="Result")
result_label.configure(font=("Arial", 15))
result_label.pack()


result_box = customtkinter.CTkTextbox(app, width=150, height=150)
result_box.configure(fg_color="black")
result_box.pack()


app.mainloop()
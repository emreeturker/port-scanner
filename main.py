import socket
import customtkinter
import threading
from PIL import Image
from concurrent.futures import ThreadPoolExecutor
import queue


app = customtkinter.CTk()
app.title("Port Scanner")
app.configure(fg_color="#212529")
app.geometry("500x600")

open_ports = []
result_queue = queue.Queue()


def port_scanner():
    target_ip = ip_entry.get()
    result_box.delete("1.0", "end")
    open_ports.clear()
    status_info.configure(text="Scanning for open ports...", text_color="blue")

    with ThreadPoolExecutor(max_workers=100) as executor:
        for port in range(1, 65535):
            executor.submit(scan_port, target_ip, port)

    status_info.configure(text="Port scan completed", text_color="green")

def scan_port(target_ip, ports):
    so = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    so.settimeout(1)
    result = so.connect_ex((target_ip, ports))

    if result == 0:
        result_queue.put(ports)

    so.close()


def start_scan_thread():
    t = threading.Thread(target=port_scanner)
    t.start()


logo_image = customtkinter.CTkImage(
    light_image=Image.open("images/logo.png"),
    dark_image=Image.open("images/logo.png"),
    size=(100, 100)
)


def check_queue():

    new_data = False

    while True:
        try:
            message = result_queue.get_nowait()
            open_ports.append(message)

            new_data = True

        except queue.Empty:
            break

    if new_data:
        open_ports.sort()
        result_box.delete("1.0", "end")

        for port in open_ports:
            result_box.insert("end", "[+] Port {} is open\n".format(port))

    app.after(100, check_queue)


logo_label = customtkinter.CTkLabel(app, image=logo_image, text="")
logo_label.pack(pady=20)


ip_entry = customtkinter.CTkEntry(app, placeholder_text="IP Address")
ip_entry.pack()


button = customtkinter.CTkButton(app, text="Target", command=start_scan_thread)
button.configure(fg_color="red")
button.pack(padx=20, pady=20)


result_label = customtkinter.CTkLabel(app, text="Result")
result_label.configure(font=("Arial", 17))
result_label.pack()


result_box = customtkinter.CTkTextbox(app, width=250, height=150)
result_box.configure(fg_color="black")
result_box.pack()


status_info = customtkinter.CTkLabel(app, text="Waiting for scan")
status_info.configure(font=("Arial", 15),text_color="yellow")
status_info.pack()


check_queue()
app.mainloop()
import customtkinter
import customtkinter as ctk
import requests
import asyncio
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
    
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue") 

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Custom Interface Portify")
        self.geometry(f"{1000}x{600}")

        self.frame = customtkinter.CTkFrame(master=self)
        self.frame.pack(pady=20, padx=60, fill="both", expand=True)

        self.label1 = customtkinter.CTkLabel(master=self.frame, text="Login System", font=("Roboto", 24))
        self.label1.pack(pady=12, padx=10)

        self.entry1 = customtkinter.CTkEntry(master=self.frame, placeholder_text="Username")
        self.entry1.pack(pady=6, padx=10)

        self.entry2 = customtkinter.CTkEntry(master=self.frame, placeholder_text="Password", show="*")
        self.entry2.pack(pady=6, padx=10)

        self.label2 = customtkinter.CTkLabel(master=self.frame, text="", font=("Roboto", 16, "normal"), text_color="red")
        self.label2.pack()

        self.button = customtkinter.CTkButton(master=self.frame, text="Login", command=self.login)
        self.button.pack(pady=12, padx=10)

        self.checkbox = customtkinter.CTkCheckBox(master=self.frame, text="Remember Me")
        self.checkbox.pack()

        self.interface_page()

    def login(self):
        username = self.entry1.get()
        password = self.entry2.get()

        credentials = ["Kev", "Orion"]

        if username == credentials[0] and password == credentials[1]:
            self.interface_page()

        else:
            self.label2.configure(text="Invalid Credentials")

    def logout(self):
        self.__init__()

    def interface_page(self): 
        for widget in self.winfo_children():
            widget.destroy()       

        self.side = customtkinter.CTkFrame(master=self, width=300, corner_radius=0)
        self.side.pack(side="left", fill="y")

        self.label = customtkinter.CTkLabel(master=self.side, text="Profile", font=("Roboto", 24))
        self.label.pack(pady=20, padx=10)

        self.button1 = customtkinter.CTkButton(master=self.side, text="Logout", command=self.logout)
        self.button1.pack(pady=12, padx=10)

        self.main_content = customtkinter.CTkFrame(master=self, corner_radius=0)
        self.main_content.pack(fill="both", expand=True)

        self.main_content.grid_rowconfigure(0, weight=1)
        self.main_content.grid_rowconfigure(0, weight=3)
        self.main_content.grid_columnconfigure((0, 2), weight=1)
        self.main_content.grid_columnconfigure(1, weight=3)

        self.box1 = customtkinter.CTkFrame(master=self.main_content)
        self.box1.grid(row=0, column=0, padx=(20, 10), pady=20, sticky="nsew")

        self.box2 = customtkinter.CTkFrame(master=self.main_content)
        self.box2.grid(row=0, column=1, padx=10, pady=20, sticky="nsew")

        self.box3 = customtkinter.CTkFrame(master=self.main_content)
        self.box3.grid(row=0, column=2, padx=(10, 20), pady=20, sticky="nsew")

        self.box4 = ctk.CTkFrame(self.main_content)
        self.box4.grid(row=1, column=0, columnspan=3, padx=(20, 20), pady=20)

        asyncio.create_task(self.import_port_data(3000, 3007))  # Start async task for ports
        asyncio.create_task(self.import_port_data(3011, 3014)) 

    # Function to check if the website is online on a specific port and retrieve the title
    def check_port(self, port, online_ports):
        url = f"http://83.77.148.163:{port}/"
        try:
            response = requests.get(url, timeout=5)  # Set a timeout to avoid long waits
            if response.status_code == 200:
                # Parse the page content to get the title
                soup = BeautifulSoup(response.text, 'html.parser')
                title = soup.title.string if soup.title else "No Title"
                online_ports.append((port, title))  # Add port and title to the list
                print(port, ": ", title)
        except requests.exceptions.RequestException:
            pass  # Do nothing if the port is down

    # Function to check multiple ports in parallel
    def import_port_data(self, start_port, end_port):
        #check_ports_in_parallel(3011, 3014)
        
        online_ports = []  # List to hold the ports and their titles that are online
        with ThreadPoolExecutor(max_workers=1) as executor:  # 10 threads for parallel checks
            executor.map(lambda port: self.check_port(port, online_ports), range(start_port, end_port + 1))
        
        # Sort the online ports numerically based on the port number
        online_ports.sort(key=lambda x: x[0])
        
        for online_port in online_ports:
            label = ctk.CTkLabel(self.box1, text=f"Port {online_port[0]}: {online_port[1]}")
            label.pack(pady=5)

    def update_ports(self, port, title):
        # Create and display the port and title in the GUI
        label = ctk.CTkLabel(self.box1, text=f"Port {port}: {title}")
        label.pack(pady=5)


if __name__ == "__main__":
    app = App()
    app.mainloop()
print("starting app")

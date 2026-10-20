import requests
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup

# Function to check if the website is online on a specific port and retrieve the title
def check_port(port, online_ports):
    url = f"http://83.77.148.163:{port}/"
    try:
        response = requests.get(url, timeout=5)  # Set a timeout to avoid long waits
        if response.status_code == 200:
            # Parse the page content to get the title
            soup = BeautifulSoup(response.text, 'html.parser')
            title = soup.title.string if soup.title else "No Title"
            online_ports.append((port, title))  # Add port and title to the list
            print(port,"", title)
    except requests.exceptions.RequestException:
        pass  # Do nothing if the port is down

# Function to check multiple ports in parallel
def check_ports_in_parallel(start_port, end_port):
    online_ports = []  # List to hold the ports and their titles that are online
    with ThreadPoolExecutor(max_workers=1) as executor:  # 10 threads for parallel checks
        executor.map(lambda port: check_port(port, online_ports), range(start_port, end_port + 1))
    
    # Sort the online ports numerically based on the port number
    online_ports.sort(key=lambda x: x[0])
    
    return online_ports

online_ports = check_ports_in_parallel(3000, 3020)


"""

# Check ports 3000-3100 concurrently and get sorted list of online ports with titles

# Print the sorted list of online ports and their titles
print("Online ports and website titles:")
#for port, title in online_ports:
#    print(f"Port {port}: {title}")

import requests
from concurrent.futures import ThreadPoolExecutor

# Function to check if the website is online on a specific port
def check_port(port, online_ports):
    url = f"http://83.77.148.163:{port}/"
    try:
        response = requests.get(url, timeout=5)  # Set a timeout to avoid long waits
        if response.status_code == 200:
            online_ports.append(port)  # Add port to the list of online ports
    except requests.exceptions.RequestException:
        pass  # Do nothing if the port is down

# Function to check multiple ports in parallel
def check_ports_in_parallel(start_port, end_port):
    online_ports = []  # List to hold the ports that are online
    with ThreadPoolExecutor(max_workers=39) as executor:  # 10 threads for parallel checks
        executor.map(lambda port: check_port(port, online_ports), range(start_port, end_port + 1))
    
    # Sort the online ports numerically
    online_ports.sort()
    
    return online_ports

# Check ports 3000-3100 concurrently and get sorted list of online ports
online_ports = check_ports_in_parallel(3000, 3020)

# Print the sorted list of online ports
print("Online ports:", online_ports)

"""
import asyncio
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import cpu_count
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from threading import Lock

print_lock = Lock()

def scan_port(ip, port, driver_path):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--ignore-certificate-errors")  # Ignore SSL errors
    service = Service(driver_path)

    url = f"http://{ip}:{port}"
    
    with print_lock:
        print(f"Scanning {url}")
        
    try:
        with webdriver.Chrome(service=service, options=chrome_options) as driver:
            driver.get(url)
            title = driver.title
            with print_lock:
                print(f"Port: {port}, Title: {title}")
    except WebDriverException as e:
        with print_lock:
            print(f"Error on port {port}: {e}")



async def scan_ports(ip, start_port, end_port, driver_path, max_threads):
    loop = asyncio.get_running_loop()
    with ThreadPoolExecutor(max_threads) as executor:
        tasks = []
        for port in range(start_port, end_port + 1):
            # Schedule scan_port as a task to run in the thread pool
            tasks.append(loop.run_in_executor(executor, scan_port, ip, port, driver_path))
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    ip_address = "83.77.148.163"
    start_port = 3000
    end_port = 3010
    max_threads = cpu_count() * 2  # Adjusting the number of threads based on available cores
    driver_path = ChromeDriverManager().install()  # This automatically installs the ChromeDriver

    asyncio.run(scan_ports(ip_address, start_port, end_port, driver_path, max_threads))

█──█────████────█──█────████────█───█────███
██─█────█──█────██─█────█──█────██─██─────█─
█─██────█──█────█─██────████────█─█─█─────█─
█──█────█──█────█──█────█──█────█───█─────█─
█──█────████────█──█────█──█────█───█────███

import socket
from concurrent.futures import ThreadPoolExecutor
import platform

def scan_port(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    
    try:
        result = sock.connect_ex((host, port))
        if result == 0:
            print(f"Port {port} is open")
            try:
                service_version = get_service_version(host, port)
                print(f"  Service on port {port}: {service_version}")
            except Exception as e:
                print(f"  Could not determine service version on port {port}: {str(e)}")
    except socket.error:
        pass 
    finally:
        sock.close()

def get_service_version(host, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        sock.connect((host, port))
        sock.send(b'HELLO\r\n')
        banner = sock.recv(1024)
        sock.close()
        return banner.decode('utf-8', 'ignore').strip()
    except:
        return "Unknown Service"

def detect_os(host):
    try:
        if platform.system() == "Linux":
            return "Linux OS (detected by local system)"
        else:
            return "Operating System could not be determined"
    except Exception as e:
        return f"Error detecting OS: {str(e)}"

def scan_ports(host, start_port, end_port):
    with ThreadPoolExecutor(max_workers=10) as executor:  
        for port in range(start_port, end_port + 1):
            executor.submit(scan_port, host, port)

def start_scan():
    target_host = input("Enter the host to scan (e.g., 127.0.0.1 or example.com): ")
    start_port = int(input("Enter the starting port (e.g., 20): "))
    end_port = int(input("Enter the ending port (e.g., 1024): "))
    
    print(f"\nScanning ports {start_port}-{end_port} on {target_host}...")
    scan_ports(target_host, start_port, end_port)

    print("\nDetecting OS...")
    os_info = detect_os(target_host)
    print(f"OS Info: {os_info}")

if __name__ == "__main__":
    start_scan()



import socket
import threading
from datetime import datetime

# Lock for clean output
print_lock = threading.Lock()

# Log file
LOG_FILE = "scan_results.txt"


def log_result(message):
    with open(LOG_FILE, "a") as file:
        file.write(message + "\n")


def scan_port(host, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)

        result = sock.connect_ex((host, port))
        sock.close()

        with print_lock:
            if result == 0:
                msg = f"[OPEN] Port {port}"
            else:
                msg = f"[CLOSED] Port {port}"

            print(msg)
            log_result(msg)

    except socket.timeout:
        msg = f"[TIMEOUT] Port {port}"
        print(msg)
        log_result(msg)

    except Exception as e:
        msg = f"[ERROR] Port {port} - {e}"
        print(msg)
        log_result(msg)


def start_scan(host, start_port, end_port):
    print(f"\nStarting TCP Port Scan on {host}")
    print(f"Port Range: {start_port} - {end_port}")
    print(f"Scan started at: {datetime.now()}\n")

    log_result(f"\nScan started on {host} at {datetime.now()}")

    threads = []

    for port in range(start_port, end_port + 1):
        t = threading.Thread(target=scan_port, args=(host, port))
        threads.append(t)
        t.start()

        # Limit active threads
        if len(threads) >= 100:
            for thread in threads:
                thread.join()
            threads = []

    for thread in threads:
        thread.join()

    print(f"\nScan completed at: {datetime.now()}")
    log_result(f"Scan completed at {datetime.now()}\n")


if __name__ == "__main__":
    target_host = input("Enter target host (IP or domain): ")
    start_port = int(input("Enter start port: "))
    end_port = int(input("Enter end port: "))

    start_scan(target_host, start_port, end_port)

import subprocess
import random
import sys

def generate_random_bdaddr():
    """Generate a random Bluetooth MAC address."""
    return ':'.join(f"{random.randint(0x00, 0xFF):02X}" for _ in range(6))

def set_bdaddr(interface, new_addr):
    """Set the Bluetooth MAC address using hciconfig."""
    try:
        # Bring down the interface
        subprocess.run(['sudo', 'hciconfig', interface, 'down'], check=True)

        # Set the new address using hciconfig
        subprocess.run(['sudo', 'hciconfig', interface, 'up', new_addr], check=True)

        print(f"Bluetooth address for {interface} changed to {new_addr}.")
    except subprocess.CalledProcessError as e:
        print("Error changing Bluetooth address:", e)
        sys.exit(1)

def get_bluetooth_interface():
    """Detect the active Bluetooth interface."""
    try:
        result = subprocess.run(['hciconfig'], stdout=subprocess.PIPE, text=True)
        for line in result.stdout.splitlines():
            if line.startswith("hci"):
                return line.split(":")[0]
    except FileNotFoundError:
        print("Error: 'hciconfig' not found. Ensure Bluetooth tools are installed.")
        sys.exit(1)
    return None

def verify_bdaddr(interface):
    """Verify the current Bluetooth address."""
    try:
        result = subprocess.run(['hciconfig', interface], stdout=subprocess.PIPE, text=True)
        for line in result.stdout.splitlines():
            if "BD Address" in line:
                print(f"Current Bluetooth Address: {line.strip()}")
                return
    except FileNotFoundError:
        print("Error: 'hciconfig' not found. Ensure Bluetooth tools are installed.")
        sys.exit(1)

if __name__ == "__main__":
    # Generate a random Bluetooth address
    new_addr = generate_random_bdaddr()
    print(f"Generated random Bluetooth address: {new_addr}")

    # Detect the Bluetooth interface
    interface = get_bluetooth_interface()
    if not interface:
        print("No Bluetooth interface found.")
        sys.exit(1)
    
    print(f"Detected Bluetooth interface: {interface}")

    # Set the new random address
    set_bdaddr(interface, new_addr)
    verify_bdaddr(interface)

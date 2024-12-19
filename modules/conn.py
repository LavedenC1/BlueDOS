import subprocess
import asyncio
import signal
from bleak import BleakClient
from colorama import *
init()

def bt_control(name, mac):
    def get_name():
        try:
            result = subprocess.run(["bluetoothctl", "show"], text=True, capture_output=True, check=True)
            for line in result.stdout.splitlines():
                if "Name:" in line:
                    return line.split("Name:")[1].strip()
        except subprocess.CalledProcessError:
            return None

    def set_name(new_name):
        try:
            subprocess.run(["bluetoothctl", "system-alias", new_name], check=True, text=True)
        except subprocess.CalledProcessError as e:
            print(f"{Fore.RED}Failed to set name: {e.stderr}{Style.RESET_ALL}")

    async def connect():
        try:
            async with BleakClient(mac) as client:
                if client.is_connected:
                    print(f"{Fore.GREEN}Connected to {mac}! Device is now trusted!{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}Failed to connect to {mac}{Style.RESET_ALL}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}The device has refused the connection or an terrible error has occured...{Style.RESET_ALL}")
            print("e")

    def reset_name():
        if default_name:
            set_name(default_name)
            print(f"{Fore.WHITE}Name reset to: {default_name}{Style.RESET_ALL}")

    def handle_exit(sig, frame):
        print(f"\n{Fore.RED}Exiting...{Style.RESET_ALL}")
        reset_name()
        exit(0)

    # Setup
    default_name = get_name()
    if not default_name:
        print(f"{Fore.RED}Failed to get default name.{Style.RESET_ALL}")
        return
    set_name(name)
    signal.signal(signal.SIGINT, handle_exit)

    # Run
    asyncio.run(connect())
    reset_name()
if __name__ == "__main__":
    bt_control("myPhone", input("Enter address: "))

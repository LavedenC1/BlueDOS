import bluetooth
from colorama import *
import shutil

def findServices(mac_address):
    print(f"{Fore.WHITE}Searching for services on {mac_address}...{Style.RESET_ALL}")
    size = shutil.get_terminal_size()
    print(f"{Style.RESET_ALL}{Fore.WHITE}─{Style.RESET_ALL}" * size.columns)
    
    services = bluetooth.find_service(address=mac_address)
    
    if not services:
        print(f"{Fore.RED}No services found.{Style.RESET_ALL}")
        return
    
    for service in services:
        print(f"{Fore.BLUE}Service found...{Style.RESET_ALL}")
        for key, value in service.items():
            print(f"{Fore.BLUE}{key}: {Fore.YELLOW}{Style.BRIGHT}{value}{Style.RESET_ALL}")
        size = shutil.get_terminal_size()
        print("─" * size.columns)

if __name__ == '__main__':
    mac_address = "XX:XX:wXX:XX:XX:XX"
    findServices(mac_address)


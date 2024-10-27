#!/usr/bin/env python3
'''
Author: Double Sine
License: GPLv3
'''
import os
import sys
import zipfile
import psutil
import shutil
import time
import itertools
import ctypes
import random
import subprocess
from colorama import Fore, Back, Style, init

# Initialize colorama
init(autoreset=True)

VariantBase64Table = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/='
VariantBase64Dict = {i: VariantBase64Table[i] for i in range(len(VariantBase64Table))}
VariantBase64ReverseDict = {VariantBase64Table[i]: i for i in range(len(VariantBase64Table))}

def variant_base64_encode(bs: bytes):
    result = b''
    blocks_count, left_bytes = divmod(len(bs), 3)

    for i in range(blocks_count):
        coding_int = int.from_bytes(bs[3 * i:3 * i + 3], 'little')
        block = VariantBase64Dict[coding_int & 0x3f]
        block += VariantBase64Dict[(coding_int >> 6) & 0x3f]
        block += VariantBase64Dict[(coding_int >> 12) & 0x3f]
        block += VariantBase64Dict[(coding_int >> 18) & 0x3f]
        result += block.encode()

    if left_bytes == 0:
        return result
    elif left_bytes == 1:
        coding_int = int.from_bytes(bs[3 * blocks_count:], 'little')
        block = VariantBase64Dict[coding_int & 0x3f]
        block += VariantBase64Dict[(coding_int >> 6) & 0x3f]
        result += block.encode()
        return result
    else:
        coding_int = int.from_bytes(bs[3 * blocks_count:], 'little')
        block = VariantBase64Dict[coding_int & 0x3f]
        block += VariantBase64Dict[(coding_int >> 6) & 0x3f]
        block += VariantBase64Dict[(coding_int >> 12) & 0x3f]
        result += block.encode()
        return result

def variant_base64_decode(s: str):
    result = b''
    blocks_count, left_bytes = divmod(len(s), 4)

    for i in range(blocks_count):
        block = VariantBase64ReverseDict[s[4 * i]]
        block += VariantBase64ReverseDict[s[4 * i + 1]] << 6
        block += VariantBase64ReverseDict[s[4 * i + 2]] << 12
        block += VariantBase64ReverseDict[s[4 * i + 3]] << 18
        result += block.to_bytes(3, 'little')

    if left_bytes == 0:
        return result
    elif left_bytes == 2:
        block = VariantBase64ReverseDict[s[4 * blocks_count]]
        block += VariantBase64ReverseDict[s[4 * blocks_count + 1]] << 6
        result += block.to_bytes(1, 'little')
        return result
    elif left_bytes == 3:
        block = VariantBase64ReverseDict[s[4 * blocks_count]]
        block += VariantBase64ReverseDict[s[4 * blocks_count + 1]] << 6
        block += VariantBase64ReverseDict[s[4 * blocks_count + 2]] << 12
        result += block.to_bytes(2, 'little')
        return result
    else:
        raise ValueError('Invalid encoding.')

def encrypt_bytes(key: int, bs: bytes):
    result = bytearray()
    for i in range(len(bs)):
        result.append(bs[i] ^ ((key >> 8) & 0xff))
        key = (result[-1] & key) | 0x482D
    return bytes(result)

def decrypt_bytes(key: int, bs: bytes):
    result = bytearray()
    for i in range(len(bs)):
        result.append(bs[i] ^ ((key >> 8) & 0xff))
        key = (bs[i] & key) | 0x482D
    return bytes(result)

def is_mobaxterm_running():
    return [p for p in psutil.process_iter(['pid', 'name']) if p.info['name'] and 'mobaxterm' in p.info['name'].lower()]

def get_mobaxterm_version(version_file):
    try:
        with open(version_file, 'r') as file:
            version_line = file.readline().strip()
            major_version, minor_version = version_line.split('.')[:2]
            return major_version, minor_version
    except Exception:
        return None, None

def generate_license(user_name: str, major_version: int, minor_version: int):
    license_string = f'1#{user_name}|{major_version}{minor_version}#1#{major_version}3{minor_version}6{minor_version}#0#0#0#'
    encoded_license_string = variant_base64_encode(encrypt_bytes(0x787, license_string.encode())).decode()
    print(f'{Fore.LIGHTGREEN_EX}[Base64 Key] {encoded_license_string}{Style.RESET_ALL}')
    with zipfile.ZipFile('custom.mxtpro', 'w') as f:
        f.writestr('Pro.key', data=encoded_license_string)

def print_header():
    header_effect = [
        "###############################################",
        "#        MobaXterm Keygen by ARIAZONAA        #",
        "###############################################"
    ]
    for line in header_effect:
        for char in line:
            sys.stdout.write(f'{Fore.LIGHTGREEN_EX}{char}{Style.RESET_ALL}')
            sys.stdout.flush()
            time.sleep(random.uniform(0.005, 0.02))
        print()
    time.sleep(0.5)

def loading_animation():
    loading = itertools.cycle(['|', '/', '-', '\\'])
    for _ in range(50):
        sys.stdout.write(f'\r{Fore.LIGHTYELLOW_EX}[+] Hacking... {next(loading)}{Style.RESET_ALL}')
        sys.stdout.flush()
        time.sleep(0.05)
    sys.stdout.write(f'\r{Fore.LIGHTGREEN_EX}[+] Access Granted!{Style.RESET_ALL}\n')
    sys.stdout.flush()

def request_admin_rights():
    user_input = input(f'{Fore.LIGHTRED_EX}[!] Administrator rights required. Restart the script as administrator? (y/n): {Style.RESET_ALL}')
    if user_input.lower() == 'y':
        command = f'powershell -Command "Start-Process -FilePath \"{sys.executable}\" -ArgumentList \"{" ".join(sys.argv)}\" -Verb RunAs"'
        subprocess.run(command, shell=True)
        sys.exit(0)

def get_system_info():
    try:
        command = 'wmic os get Caption,CSDVersion,OSArchitecture,Version /format:list'
        output = subprocess.check_output(command, shell=True, text=True).strip()
        print(f'{Fore.LIGHTCYAN_EX}[+] System Information:{Style.RESET_ALL}')
        for line in output.split('\n'):
            if line:
                print(f'{Fore.LIGHTCYAN_EX}{line.strip()}{Style.RESET_ALL}')
    except subprocess.SubprocessError as e:
        print(f'{Fore.LIGHTRED_EX}[-] Failed to retrieve system information: {e}{Style.RESET_ALL}')

def main():
    try:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin()
    except:
        is_admin = False

    if not is_admin:
        request_admin_rights()

    print_header()
    loading_animation()
    get_system_info()
    moba_path = r'C:\Program Files (x86)\Mobatek\MobaXterm'
    version_file = os.path.join(moba_path, 'version.dat')

    if not os.path.exists(version_file):
        print(f'{Fore.LIGHTRED_EX}[-] version.dat not found. Please make sure MobaXterm is installed.{Style.RESET_ALL}')
        sys.exit(1)

    running_processes = is_mobaxterm_running()
    if running_processes:
        user_input = input(f'{Fore.LIGHTYELLOW_EX}[!] MobaXterm is still running. Terminate all MobaXterm processes? (y/n): {Style.RESET_ALL}')
        if user_input.lower() == 'y':
            for process in running_processes:
                os.kill(process.info['pid'], 9)
                print(f'{Fore.LIGHTGREEN_EX}[+] Process {process.info["pid"]} ({process.info["name"]}) terminated successfully.{Style.RESET_ALL}')
        else:
            print(f'{Fore.LIGHTRED_EX}[-] Operation aborted.{Style.RESET_ALL}')
            sys.exit(1)

    user_name = input(f'{Fore.LIGHTCYAN_EX}[?] Please enter your username: {Style.RESET_ALL}')
    major_version, minor_version = get_mobaxterm_version(version_file)

    if major_version is None or minor_version is None:
        print(f'{Fore.LIGHTRED_EX}[-] Could not determine the MobaXterm version.{Style.RESET_ALL}')
        sys.exit(1)

    print(f'{Fore.LIGHTGREEN_EX}[+] Creating license file for version {major_version}.{minor_version}...{Style.RESET_ALL}')
    loading_animation()
    generate_license(user_name, int(major_version), int(minor_version))
    print(f'{Fore.LIGHTGREEN_EX}[+] License file created successfully: custom.mxtpro{Style.RESET_ALL}')

    target_dir = moba_path
    try:
        print(f'{Fore.LIGHTGREEN_EX}[+] Copying custom.mxtpro to {target_dir}...{Style.RESET_ALL}')
        loading_animation()
        shutil.copy('custom.mxtpro', target_dir)
        print(f'{Fore.LIGHTGREEN_EX}[+] File copied successfully.{Style.RESET_ALL}')
    except PermissionError:
        print(f'{Fore.LIGHTRED_EX}[-] No permission to write to the directory: {target_dir}{Style.RESET_ALL}')
        print(f'{Fore.LIGHTYELLOW_EX}[!] Please run the script with administrator rights to copy the license file correctly.{Style.RESET_ALL}')
        sys.exit(1)

    print(f'{Fore.LIGHTGREEN_EX}[+] Operation completed.{Style.RESET_ALL}')

if __name__ == '__main__':
    main()
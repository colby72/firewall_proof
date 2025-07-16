from colorama import Fore, Style
#import colorama


def print_info(text):
    print(f"{Fore.WHITE} [+] {text}")
    print(Style.RESET_ALL, end="")

def print_success(text):
    print(f"{Fore.GREEN} [+] {text}")
    print(Style.RESET_ALL, end="")

def print_error(text):
    print(f"{Fore.RED} [/!\] {text}")
    print(Style.RESET_ALL, end="")

def print_warning(text):
    print(f"{Fore.YELLOW} [!] {text}")
    print(Style.RESET_ALL, end="")

def print_debug(text):
    print(f"{Fore.CYAN} [DEBUG] {text}")
    print(Style.RESET_ALL, end="")
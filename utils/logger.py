from datetime import datetime
from colorama import Fore, Style

def log_event(actor, message, color = Fore.CYAN):
    tiempo = datatime.now().strftime("%H:%m:$S")
    print(f"{color}[{tiempo}] {actor}: {message}{Style.RESET_ALL}")
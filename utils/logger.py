import datetime

def log_event(msg: str):
    """Imprime y guarda logs básicos"""
    timestamp = datetime.datetime.now().strftime("[%H:%M:%S]")
    print(timestamp, msg)

import threading
import time
from random import randint

class Escritor(threading.Thread):
    def __init__(self, id_escritor, recurso, semaforo_lectura):
        super().__init__()
        self.id = id_escritor
        self.recurso = recurso
        self.semaforo_lectura = semaforo_lectura

    def run(self):
        while True:
            time.sleep(randint(2, 4))  # simula trabajo previo

            # --- Sección crítica ---
            self.semaforo_lectura.acquire()
            nuevo_valor = randint(100, 999)
            print(f"✍️ Escritor {self.id} escribiendo: {nuevo_valor}")
            self.recurso['dato'] = nuevo_valor
            time.sleep(randint(1, 2))
            self.semaforo_lectura.release()

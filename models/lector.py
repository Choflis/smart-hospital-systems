import threading
import time
from random import randint

class Lector(threading.Thread):
    def __init__(self, id_lector, recurso, mutex, semaforo_lectura, contador_lectores):
        super().__init__()
        self.id = id_lector
        self.recurso = recurso
        self.mutex = mutex
        self.semaforo_lectura = semaforo_lectura
        self.contador_lectores = contador_lectores

    def run(self):
        while True:
            time.sleep(randint(1, 3))  # simula tiempo entre lecturas

            # --- Entrada sección crítica ---
            with self.mutex:
                self.contador_lectores[0] += 1
                if self.contador_lectores[0] == 1:
                    self.semaforo_lectura.acquire()  # bloquea escritores

            # --- Lectura ---
            print(f"📖 Lector {self.id} leyendo: {self.recurso['dato']}")
            time.sleep(randint(1, 2))

            # --- Salida sección crítica ---
            with self.mutex:
                self.contador_lectores[0] -= 1
                if self.contador_lectores[0] == 0:
                    self.semaforo_lectura.release()

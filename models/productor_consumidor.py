#descripción: Simula el flujo de pacientes en un hospital donde los productores generan pacientes y los consumidores los atienden

import threading
import time
import random
import queue
from utils.logger import log_event
from config import BUFFER_SIZE

#Buffer compartido

buffer = queue.Queue(maxsize=BUFFER_SIZE)

#Clases principales

class Productor(threading.Thread):
    def __init__(self, id_productor):
        super().__init__(daemon=True)
        self.id = id_productor
        self.running = True

    def run(self):
        while self.running:
            if not buffer.full():
                paciente = f"Paciente-{random.randint(1000, 9999)}"
                buffer.put(paciente)
                log_event(f"[Productor {self.id}] Generó {paciente}")
                time.sleep(random.uniform(0.5, 1.5))
            else:
                time.sleep(0.5)

    def stop(self):
        self.running = False


class Consumidor(threading.Thread):
    def __init__(self, id_consumidor):
        super().__init__(daemon=True)
        self.id = id_consumidor
        self.running = True

    def run(self):
        while self.running:
            try:
                paciente = buffer.get(timeout=1)
                log_event(f"[Consumidor {self.id}] Atendiendo a {paciente}")
                time.sleep(random.uniform(1, 2))
                log_event(f"[Consumidor {self.id}] Terminó con {paciente}")
                buffer.task_done()
            except queue.Empty:
                time.sleep(0.5)

    def stop(self):
        self.running = False

#Funciones de control global

productores = []
consumidores = []


def iniciar_sistema(num_productores=2, num_consumidores=3):
    """Inicia los hilos productores y consumidores"""
    global productores, consumidores

    productores = [Productor(i) for i in range(num_productores)]
    consumidores = [Consumidor(i) for i in range(num_consumidores)]

    for p in productores: p.start()
    for c in consumidores: c.start()

    log_event("Sistema Productor–Consumidor iniciado")
def detener_sistema():
    """Detiene todos los hilos activos"""
    for p in productores: p.stop()
    for c in consumidores: c.stop()
    log_event("Sistema detenido")


def obtener_estado_buffer():
    """Devuelve una lista con los elementos actuales del buffer"""
    return list(buffer.queue)
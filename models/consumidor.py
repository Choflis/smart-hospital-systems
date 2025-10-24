# models/consumidor.py
import threading
import time

class Consumidor(threading.Thread):
    def __init__(self, id, buffer):
        super().__init__()
        self.id = id
        self.buffer = buffer
        self._activo = True

    def run(self):
        while self._activo:
            paciente = self.buffer.obtener_paciente()
            if paciente:
                print(f"[Médico {self.id}] Atendiendo a {paciente.nombre}...")
                time.sleep(2)  # Simula tiempo de atención
                print(f"[Médico {self.id}] Terminó con {paciente.nombre}.")
            else:
                time.sleep(1)

    def detener(self):
        self._activo = False

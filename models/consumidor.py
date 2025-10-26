# models/consumidor.py
import threading
import time

class Consumidor(threading.Thread):
    def __init__(self, id, buffer):
        super().__init__()
        self.id = id
        self.buffer = buffer
        self._activo = True
        self.daemon = True  # Hacer el hilo daemon para que se cierre con el programa

    def run(self):
        while self._activo:
            try:
                paciente = self.buffer.obtener_paciente(timeout=1)  # Timeout para verificar _activo
                if paciente and self._activo:
                    print(f"[Médico {self.id}] Atendiendo a {paciente.nombre}...")
                    time.sleep(2)  # Simula tiempo de atención
                    print(f"[Médico {self.id}] Terminó con {paciente.nombre}.")
            except:
                # Timeout o error, verificar si debe seguir activo
                if not self._activo:
                    break
                time.sleep(0.5)
        
        print(f"[Médico {self.id}] Hilo detenido correctamente.")

    def detener(self):
        """Detiene el hilo del médico"""
        self._activo = False

# models/productor.py
"""
Módulo Productor
----------------
Hilo que gestiona la recepción de pacientes y los coloca en el buffer.
En modo interactivo, espera que se agreguen pacientes manualmente.
"""

import threading
import time

class Productor(threading.Thread):
    def __init__(self, buffer):
        super().__init__()
        self.buffer = buffer
        self._activo = True
        self.daemon = True

    def run(self):
        """El productor espera de forma pasiva (no genera automáticamente)"""
        print("[Productor] Iniciado - esperando pacientes...")
        while self._activo:
            time.sleep(1)

    def detener(self):
        """Detiene el hilo productor"""
        self._activo = False
        print("[Productor] Detenido.")

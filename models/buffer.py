# models/buffer.py
from queue import Queue
from threading import Lock

class Buffer:
    """
    Clase que representa el buffer compartido entre productores y consumidores.
    En este caso, simula una sala de espera donde se almacenan los pacientes.
    """

    def __init__(self, capacidad=5):
        self.cola = Queue(maxsize=capacidad)
        self.lock = Lock()  # Para evitar condiciones de carrera

    def agregar_paciente(self, paciente):
        """
        Agrega un paciente al buffer si hay espacio disponible.
        Retorna True si se agregó correctamente, False si está lleno.
        """
        with self.lock:
            if not self.cola.full():
                self.cola.put(paciente)
                print(f"[BUFFER] Paciente agregado: {paciente.nombre}")
                return True
            else:
                print("[BUFFER] No se pudo agregar, buffer lleno")
                return False

    def obtener_paciente(self, timeout=None):
        """
        Retira un paciente del buffer si hay alguno disponible.
        
        Args:
            timeout: Tiempo máximo de espera en segundos (None = no esperar)
        
        Retorna el paciente o None si está vacío o timeout.
        """
        try:
            if timeout is not None:
                # Intenta obtener con timeout
                if not self.cola.empty():
                    with self.lock:
                        paciente = self.cola.get(timeout=timeout)
                        print(f"[BUFFER] Paciente retirado: {paciente.nombre}")
                        return paciente
                return None
            else:
                # Sin timeout (comportamiento original)
                with self.lock:
                    if not self.cola.empty():
                        paciente = self.cola.get()
                        print(f"[BUFFER] Paciente retirado: {paciente.nombre}")
                        return paciente
                    else:
                        return None
        except:
            return None

    def esta_vacio(self):
        """
        Devuelve True si el buffer está vacío.
        """
        return self.cola.empty()

    def esta_lleno(self):
        """
        Devuelve True si el buffer está lleno.
        """
        return self.cola.full()

    def obtener_lista_pacientes(self):
        """
        Devuelve una lista con los nombres de los pacientes actualmente en el buffer.
        (Solo para visualización en consola o UI)
        """
        with self.lock:
            return list(self.cola.queue)

    def __len__(self):
        """
        Retorna la cantidad actual de pacientes en el buffer.
        """
        return self.cola.qsize()

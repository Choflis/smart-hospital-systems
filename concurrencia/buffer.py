# concurrencia/buffer.py
"""
Buffer de pacientes con sincronización manual usando semáforos
Implementa el problema Productor-Consumidor
"""

import threading
import logging
from typing import Optional
from core.paciente import Paciente

class BufferPacientes:
    """
    Buffer circular con capacidad limitada para almacenar pacientes
    Usa semáforos para sincronización manual (sin Queue)
    
    Sincronización:
    - mutex: Exclusión mutua para acceso al buffer
    - empty: Cuenta espacios vacíos disponibles
    - full: Cuenta elementos disponibles para consumir
    """
    
    def __init__(self, capacidad: int = 5):
        """
        Inicializa el buffer con capacidad limitada
        
        Args:
            capacidad: Número máximo de pacientes en el buffer
        """
        self.capacidad = capacidad
        self.buffer = []
        
        # Semáforos para sincronización MANUAL
        self.mutex = threading.Lock()  # Exclusión mutua
        self.empty = threading.Semaphore(capacidad)  # Espacios vacíos
        self.full = threading.Semaphore(0)  # Elementos disponibles
        
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"Buffer inicializado con capacidad: {capacidad}")
    
    def agregar(self, paciente: Paciente) -> bool:
        """
        Agrega un paciente al buffer (operación de PRODUCTOR)
        
        Args:
            paciente: Paciente a agregar
            
        Returns:
            True si se agregó exitosamente
        """
        # Esperar a que haya espacio disponible
        self.empty.acquire()
        
        # Sección crítica
        with self.mutex:
            self.buffer.append(paciente)
            self.logger.info(
                f"✅ Paciente {paciente.id} agregado al buffer | "
                f"Buffer: {len(self.buffer)}/{self.capacidad}"
            )
        
        # Señalar que hay un elemento disponible
        self.full.release()
        return True
    
    def extraer(self) -> Optional[Paciente]:
        """
        Extrae un paciente del buffer (operación de CONSUMIDOR)
        
        Returns:
            Paciente extraído o None si el buffer está vacío
        """
        # Esperar a que haya elementos disponibles
        self.full.acquire()
        
        # Sección crítica
        paciente = None
        with self.mutex:
            if self.buffer:
                paciente = self.buffer.pop(0)
                self.logger.info(
                    f"📤 Paciente {paciente.id} extraído del buffer | "
                    f"Buffer: {len(self.buffer)}/{self.capacidad}"
                )
        
        # Señalar que hay un espacio disponible
        self.empty.release()
        return paciente
    
    def esta_vacio(self) -> bool:
        """Verifica si el buffer está vacío"""
        with self.mutex:
            return len(self.buffer) == 0
    
    def esta_lleno(self) -> bool:
        """Verifica si el buffer está lleno"""
        with self.mutex:
            return len(self.buffer) >= self.capacidad
    
    def obtener_tamano(self) -> int:
        """Obtiene el tamaño actual del buffer"""
        with self.mutex:
            return len(self.buffer)
    
    def __str__(self) -> str:
        """Representación del buffer"""
        with self.mutex:
            return f"Buffer({len(self.buffer)}/{self.capacidad})"

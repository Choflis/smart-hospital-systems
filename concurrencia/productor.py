# concurrencia/productor.py
"""
Productor de pacientes - Thread que genera pacientes automáticamente
"""

import threading
import time
import random
import logging
from core.paciente import Paciente
from concurrencia.buffer import BufferPacientes

class ProductorPacientes(threading.Thread):
    """
    Thread productor que genera pacientes automáticamente
    y los agrega al buffer compartido
    """
    
    # Datos de ejemplo para generar pacientes
    NOMBRES = [
        "Juan Pérez", "María García", "Carlos López", "Ana Martínez",
        "Luis Rodríguez", "Carmen Sánchez", "José Hernández", "Laura Torres",
        "Miguel Ramírez", "Isabel Flores", "Pedro Jiménez", "Rosa Morales",
        "Antonio Díaz", "Lucía Castro", "Francisco Ruiz"
    ]
    
    DIAGNOSTICOS = [
        "Fractura de brazo", "Dolor abdominal agudo", "Fiebre alta",
        "Dolor de pecho", "Herida profunda", "Dificultad respiratoria",
        "Mareos y náuseas", "Dolor de cabeza severo", "Esguince de tobillo",
        "Reacción alérgica", "Presión arterial alta", "Deshidratación"
    ]
    
    def __init__(self, nombre: str, buffer: BufferPacientes, 
                 intervalo_min: int = 2, intervalo_max: int = 5):
        """
        Inicializa el productor
        
        Args:
            nombre: Nombre identificador del productor
            buffer: Buffer compartido donde agregar pacientes
            intervalo_min: Tiempo mínimo entre generaciones (segundos)
            intervalo_max: Tiempo máximo entre generaciones (segundos)
        """
        super().__init__(name=nombre, daemon=True)
        self.buffer = buffer
        self.intervalo_min = intervalo_min
        self.intervalo_max = intervalo_max
        self._detener = threading.Event()
        self.pacientes_generados = 0
        self.logger = logging.getLogger(self.name)
    
    def run(self):
        """Ejecuta el thread productor"""
        self.logger.info(f"🟢 {self.name} iniciado")
        
        while not self._detener.is_set():
            try:
                # Generar un paciente aleatorio
                paciente = self._generar_paciente()
                
                # Agregar al buffer (bloqueante si está lleno)
                self.buffer.agregar(paciente)
                self.pacientes_generados += 1
                
                self.logger.info(
                    f"👤 {self.name} generó: {paciente.nombre} "
                    f"(Prioridad: {paciente.prioridad}, ID: {paciente.id})"
                )
                
                # Esperar un tiempo aleatorio antes de generar el siguiente
                tiempo_espera = random.uniform(self.intervalo_min, self.intervalo_max)
                self._detener.wait(tiempo_espera)
                
            except Exception as e:
                self.logger.error(f"❌ Error en {self.name}: {e}")
                break
        
        self.logger.info(f"🔴 {self.name} detenido. Pacientes generados: {self.pacientes_generados}")
    
    def _generar_paciente(self) -> Paciente:
        """
        Genera un paciente con datos aleatorios
        
        Returns:
            Nuevo paciente generado
        """
        paciente_id = int(time.time() * 1000) % 1000000  # ID basado en timestamp
        nombre = random.choice(self.NOMBRES)
        prioridad = random.choices([1, 2, 3], weights=[20, 50, 30])[0]  # 20% urgente, 50% normal, 30% baja
        diagnostico = random.choice(self.DIAGNOSTICOS)
        
        return Paciente(paciente_id, nombre, prioridad, diagnostico)
    
    def detener(self):
        """Solicita la detención del thread"""
        self.logger.info(f"⏸️ Solicitando detención de {self.name}")
        self._detener.set()

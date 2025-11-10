# concurrencia/consumidor.py
"""
Consumidor (Médico) - Thread que atiende pacientes del buffer
"""

import threading
import time
import random
import logging
from concurrencia.buffer import BufferPacientes
from concurrencia.lector_escritor import SistemaExpedientes
from core.paciente import Paciente

class Medico(threading.Thread):
    """
    Thread consumidor que extrae pacientes del buffer
    y los atiende (simulando tiempo de atención)
    """
    
    def __init__(self, nombre: str, buffer: BufferPacientes, 
                 sistema_expedientes: SistemaExpedientes):
        """
        Inicializa el médico
        
        Args:
            nombre: Nombre del médico
            buffer: Buffer compartido de donde extraer pacientes
            sistema_expedientes: Sistema para registrar expedientes
        """
        super().__init__(name=nombre, daemon=True)
        self.buffer = buffer
        self.sistema_expedientes = sistema_expedientes
        self._detener = threading.Event()
        self.pacientes_atendidos = 0
        self.logger = logging.getLogger(self.name)
    
    def run(self):
        """Ejecuta el thread del médico"""
        self.logger.info(f"🟢 {self.name} iniciado y listo para atender")
        
        while not self._detener.is_set():
            try:
                # Extraer paciente del buffer (bloqueante si está vacío)
                paciente = self.buffer.extraer()
                
                if paciente:
                    self._atender_paciente(paciente)
                    self.pacientes_atendidos += 1
                
            except Exception as e:
                self.logger.error(f"❌ Error en {self.name}: {e}")
                if self._detener.is_set():
                    break
        
        self.logger.info(f"🔴 {self.name} detenido. Pacientes atendidos: {self.pacientes_atendidos}")
    
    def _atender_paciente(self, paciente: Paciente):
        """
        Atiende un paciente (simula tiempo de atención)
        
        Args:
            paciente: Paciente a atender
        """
        # Asignar médico al paciente
        paciente.asignar_medico(self.name)
        
        self.logger.info(
            f"🩺 {self.name} atendiendo a {paciente.nombre} "
            f"(ID: {paciente.id}, Prioridad: {paciente.prioridad})"
        )
        
        # Simular tiempo de atención según prioridad
        tiempo_atencion = self._calcular_tiempo_atencion(paciente.prioridad)
        time.sleep(tiempo_atencion)
        
        # Completar atención
        paciente.completar_atencion()
        
        # Registrar en sistema de expedientes
        self.sistema_expedientes.escribir_expediente(paciente)
        
        self.logger.info(
            f"✅ {self.name} completó atención de {paciente.nombre} "
            f"en {tiempo_atencion:.1f}s"
        )
    
    def _calcular_tiempo_atencion(self, prioridad: int) -> float:
        """
        Calcula tiempo de atención según prioridad
        
        Args:
            prioridad: Prioridad del paciente (1-3)
            
        Returns:
            Tiempo de atención en segundos
        """
        if prioridad == 1:  # Urgente
            return random.uniform(3, 5)
        elif prioridad == 2:  # Normal
            return random.uniform(2, 4)
        else:  # Baja
            return random.uniform(1, 3)
    
    def detener(self):
        """Solicita la detención del thread"""
        self.logger.info(f"⏸️ Solicitando detención de {self.name}")
        self._detener.set()

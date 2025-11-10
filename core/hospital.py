# core/hospital.py
"""
Clase Hospital - Coordinador principal del sistema
Gestiona todos los componentes del sistema hospitalario
"""

import logging
import os
from typing import List
from concurrencia.buffer import BufferPacientes
from concurrencia.productor import ProductorPacientes
from concurrencia.consumidor import Medico
from concurrencia.lector_escritor import SistemaExpedientes

class Hospital:
    """
    Clase principal que coordina todo el sistema hospitalario
    
    Gestiona:
    - Buffer de pacientes (Productor-Consumidor)
    - Productores de pacientes (threads)
    - Médicos consumidores (threads)
    - Sistema de expedientes (Lectores-Escritores)
    - Servidor de eventos para interfaces
    """
    
    def __init__(self, capacidad_buffer: int = 5, num_productores: int = 2, num_medicos: int = 3, verbose: bool = True):
        """
        Inicializa el hospital con sus componentes
        
        Args:
            capacidad_buffer: Capacidad máxima del buffer de pacientes
            num_productores: Número de threads productores
            num_medicos: Número de médicos (threads consumidores)
            verbose: Si es True, muestra logs en consola; si es False, solo en archivo
        """
        # Configurar logging
        os.makedirs('data/logs', exist_ok=True)
        handlers = [logging.FileHandler('data/logs/hospital.log', encoding='utf-8')]
        if verbose:
            handlers.append(logging.StreamHandler())
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(threadName)-15s - %(levelname)-8s - %(message)s',
            handlers=handlers,
            force=True
        )
        self.logger = logging.getLogger(__name__)
        
        # Guardar capacidad del buffer
        self.capacidad_buffer = capacidad_buffer
        
        # Servidor de eventos (se asignará externamente)
        self.event_server = None
        
        # Inicializar componentes
        self.buffer = BufferPacientes(capacidad_buffer)
        self.sistema_expedientes = SistemaExpedientes()
        
        # Crear productores
        self.productores: List[ProductorPacientes] = []
        for i in range(num_productores):
            productor = ProductorPacientes(
                nombre=f"Productor-{i+1}",
                buffer=self.buffer,
                intervalo_min=2,
                intervalo_max=5
            )
            self.productores.append(productor)
        
        # Crear médicos
        self.medicos: List[Medico] = []
        nombres_medicos = ["Dr. García", "Dra. Martínez", "Dr. López", "Dra. Rodríguez", "Dr. Sánchez"]
        for i in range(num_medicos):
            medico = Medico(
                nombre=nombres_medicos[i] if i < len(nombres_medicos) else f"Dr. Médico-{i+1}",
                buffer=self.buffer,
                sistema_expedientes=self.sistema_expedientes
            )
            self.medicos.append(medico)
        
        self.logger.info(f"🏥 Hospital inicializado: {num_productores} productores, {num_medicos} médicos")
    
    def iniciar(self):
        """Inicia todos los threads del hospital"""
        self.logger.info("🚀 Iniciando sistema hospitalario...")
        
        # Iniciar productores
        for productor in self.productores:
            productor.start()
            self.logger.info(f"✅ {productor.name} iniciado")
        
        # Iniciar médicos
        for medico in self.medicos:
            medico.start()
            self.logger.info(f"✅ {medico.name} iniciado")
        
        self.logger.info("🟢 Sistema hospitalario en funcionamiento")
    
    def detener(self):
        """Detiene todos los threads del hospital de forma ordenada"""
        self.logger.info("🛑 Deteniendo sistema hospitalario...")
        
        # Detener productores
        for productor in self.productores:
            productor.detener()
        
        # Detener médicos
        for medico in self.medicos:
            medico.detener()
        
        # Esperar a que terminen todos los threads
        for productor in self.productores:
            if productor.is_alive():
                productor.join(timeout=2)
            self.logger.info(f"🔴 {productor.name} detenido")
        
        for medico in self.medicos:
            if medico.is_alive():
                medico.join(timeout=2)
            self.logger.info(f"🔴 {medico.name} detenido")
        
        self.logger.info("✅ Sistema hospitalario detenido correctamente")
    
    def get_estadisticas(self) -> dict:
        """
        Obtiene estadísticas del sistema
        
        Returns:
            Diccionario con estadísticas del hospital
        """
        estadisticas_expedientes = self.sistema_expedientes.obtener_estadisticas()
        
        return {
            'pacientes_en_buffer': self.buffer.obtener_tamano(),
            'capacidad_buffer': self.buffer.capacidad,
            'productores_activos': sum(1 for p in self.productores if p.is_alive()),
            'medicos_activos': sum(1 for m in self.medicos if m.is_alive()),
            'pacientes_generados': sum(p.pacientes_generados for p in self.productores),
            'pacientes_atendidos': sum(m.pacientes_atendidos for m in self.medicos),
            'expedientes': estadisticas_expedientes
        }
    
    def __enter__(self):
        """Context manager: entrada"""
        self.iniciar()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager: salida"""
        self.detener()

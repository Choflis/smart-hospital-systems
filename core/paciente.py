# core/paciente.py
"""
Clase Paciente - Modelo de dominio
Representa un paciente en el sistema hospitalario
"""

from datetime import datetime
from typing import Optional

class Paciente:
    """
    Representa un paciente en el sistema hospitalario
    
    Atributos:
        id: Identificador único del paciente
        nombre: Nombre completo del paciente
        prioridad: Nivel de prioridad (1=Urgente, 2=Normal, 3=Baja)
        diagnostico: Diagnóstico médico del paciente
        estado: Estado actual del paciente
        hora_llegada: Momento en que el paciente llegó
        hora_atencion: Momento en que fue atendido (opcional)
    """
    
    def __init__(self, id: int, nombre: str, prioridad: int, diagnostico: str):
        """
        Inicializa un nuevo paciente
        
        Args:
            id: Identificador único
            nombre: Nombre del paciente
            prioridad: Nivel de prioridad (1-3)
            diagnostico: Diagnóstico inicial
        """
        self.id = id
        self.nombre = nombre
        self.prioridad = prioridad
        self.diagnostico = diagnostico
        self.estado = "En espera"
        self.hora_llegada = datetime.now()
        self.hora_atencion: Optional[datetime] = None
        self.medico_asignado: Optional[str] = None
    
    def asignar_medico(self, nombre_medico: str):
        """Asigna un médico al paciente"""
        self.medico_asignado = nombre_medico
        self.estado = "En atención"
        self.hora_atencion = datetime.now()
    
    def completar_atencion(self):
        """Marca la atención del paciente como completada"""
        self.estado = "Atendido"
    
    def get_tiempo_espera(self) -> float:
        """
        Calcula el tiempo de espera del paciente en segundos
        
        Returns:
            Tiempo en segundos desde la llegada hasta ahora o hasta la atención
        """
        if self.hora_atencion:
            return (self.hora_atencion - self.hora_llegada).total_seconds()
        return (datetime.now() - self.hora_llegada).total_seconds()
    
    def to_dict(self) -> dict:
        """
        Convierte el paciente a diccionario para serialización
        
        Returns:
            Diccionario con los datos del paciente
        """
        return {
            'id': self.id,
            'nombre': self.nombre,
            'prioridad': self.prioridad,
            'diagnostico': self.diagnostico,
            'estado': self.estado,
            'hora_llegada': self.hora_llegada.isoformat(),
            'hora_atencion': self.hora_atencion.isoformat() if self.hora_atencion else None,
            'medico_asignado': self.medico_asignado,
            'tiempo_espera': self.get_tiempo_espera()
        }
    
    def __str__(self) -> str:
        """Representación en string del paciente"""
        return f"Paciente(id={self.id}, nombre={self.nombre}, prioridad={self.prioridad}, estado={self.estado})"
    
    def __repr__(self) -> str:
        """Representación técnica del paciente"""
        return self.__str__()
    
    def __lt__(self, other: 'Paciente') -> bool:
        """Comparación para ordenamiento por prioridad (menor prioridad = más urgente)"""
        if self.prioridad != other.prioridad:
            return self.prioridad < other.prioridad
        return self.hora_llegada < other.hora_llegada

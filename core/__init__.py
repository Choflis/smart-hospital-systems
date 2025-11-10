# core/__init__.py
"""
Módulo core del sistema hospitalario
Contiene las clases fundamentales del dominio
"""

from .paciente import Paciente
from .hospital import Hospital

__all__ = ['Paciente', 'Hospital']

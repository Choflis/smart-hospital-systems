# concurrencia/__init__.py
"""
Módulo de concurrencia del sistema hospitalario
Implementa sincronización con semáforos manuales
"""

from .buffer import BufferPacientes
from .productor import ProductorPacientes
from .consumidor import Medico
from .lector_escritor import SistemaExpedientes

__all__ = ['BufferPacientes', 'ProductorPacientes', 'Medico', 'SistemaExpedientes']

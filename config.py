# config.py
"""
Archivo de configuración del sistema hospitalario
"""

# Configuración del buffer
BUFFER_CAPACITY = 5

# Configuración de productores
NUM_PRODUCTORES = 2
PRODUCTOR_INTERVALO_MIN = 2  # segundos
PRODUCTOR_INTERVALO_MAX = 5  # segundos

# Configuración de médicos (consumidores)
NUM_MEDICOS = 3

# Configuración de expedientes
EXPEDIENTES_FILE = "data/expedientes.json"

# Configuración de logs
LOG_FILE = "data/logs/hospital.log"
LOG_LEVEL = "INFO"

# Configuración de UI
UI_REFRESH_INTERVAL = 2  # segundos

"""
Archivo de configuración global del sistema Smart Hospital
"""

# ---- Configuración del buffer (para Productor–Consumidor) ----
BUFFER_SIZE = 5          # Tamaño máximo de la cola (buffer)

# ---- Configuración de hilos ----
NUM_PRODUCTORES = 2       # Cantidad de productores (p. ej., recepción de pacientes)
NUM_CONSUMIDORES = 3      # Cantidad de consumidores (p. ej., médicos que atienden)

# ---- Configuración de API REST ----
API_HOST = "0.0.0.0"
API_PORT = 8000

# ---- Interfaz gráfica ----
UI_ENABLED = True         # Si se activa la interfaz visual (PyQt/Tkinter)
UI_REFRESH_INTERVAL = 1000  # ms

# ---- Logging ----
LOG_FILE = "eventos.log"  # Archivo donde se guardan los logs (opcional)

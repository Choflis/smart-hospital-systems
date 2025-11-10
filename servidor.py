#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Servidor del Sistema Hospitalario
==================================

Núcleo principal del sistema que gestiona:
- Hilos productores y consumidores
- Patrón Lectores-Escritores para expedientes
- Buffers sincronizados
- Coordinación entre procesos
- Servidor de eventos para interfaces gráficas

Este servidor permite que las interfaces (panel_hospital.py y registro_paciente.py)
se ejecuten de forma independiente y en paralelo.

Uso:
    python servidor.py [opciones]

Autor: Equipo de Desarrollo
Fecha: 2025
"""

import sys
import argparse
import signal
import time
from core.hospital import Hospital
from core.event_server import EventServer

# Variables globales para manejo de señales
hospital_instance = None
event_server_instance = None

def signal_handler(sig, frame):
    """Maneja las señales de interrupción (Ctrl+C)"""
    if event_server_instance:
        event_server_instance.detener()
    if hospital_instance:
        hospital_instance.detener()
    sys.exit(0)

def main():
    """Función principal del servidor"""
    global hospital_instance, event_server_instance
    
    # Configurar manejador de señales
    signal.signal(signal.SIGINT, signal_handler)
    
    # Parsear argumentos de línea de comandos
    parser = argparse.ArgumentParser(
        description="Servidor del Sistema Hospitalario con Concurrencia"
    )
    parser.add_argument(
        "--buffer-size",
        type=int,
        default=5,
        help="Capacidad del buffer de pacientes (default: 5)"
    )
    parser.add_argument(
        "--productores",
        type=int,
        default=2,
        help="Número de hilos productores (default: 2)"
    )
    parser.add_argument(
        "--medicos",
        type=int,
        default=3,
        help="Número de hilos médicos/consumidores (default: 3)"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=5555,
        help="Puerto del servidor de eventos (default: 5555)"
    )
    
    args = parser.parse_args()
    
    try:
        # Crear instancia del hospital con configuración (sin logs en consola)
        hospital_instance = Hospital(
            capacidad_buffer=args.buffer_size,
            num_productores=args.productores,
            num_medicos=args.medicos,
            verbose=False
        )
        
        # Crear servidor de eventos para comunicación con interfaces
        event_server_instance = EventServer(hospital_instance, port=args.port)
        
        # Iniciar el hospital (hilos productores y consumidores)
        hospital_instance.iniciar()
        
        # Iniciar servidor de eventos
        event_server_instance.iniciar()
        
        print(f"🏥 Servidor corriendo en puerto {args.port}")
        
        # Mantener el servidor corriendo
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            pass
        
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"\n❌ Error: {e}")
    finally:
        # Detener servidor de eventos
        if event_server_instance:
            event_server_instance.detener()
        
        # Detener hospital (hilos productores y consumidores)
        if hospital_instance:
            hospital_instance.detener()
        
        print("\n🛑 Servidor detenido")

if __name__ == "__main__":
    main()

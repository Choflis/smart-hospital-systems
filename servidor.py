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
    print("\n\n⏸️  Interrupción del usuario detectada")
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
    
    # Banner de inicio
    print("=" * 80)
    print(" 🏥 SERVIDOR DEL SISTEMA HOSPITALARIO")
    print("=" * 80)
    print()
    print(" Configuración:")
    print(f" - Buffer de pacientes: capacidad {args.buffer_size}")
    print(f" - Productores: {args.productores} hilos generando pacientes")
    print(f" - Médicos/Consumidores: {args.medicos} hilos atendiendo")
    print(f" - Puerto servidor eventos: {args.port}")
    print()
    print(" Patrones implementados:")
    print(" - Productor-Consumidor con buffer sincronizado")
    print(" - Lectores-Escritores para expedientes médicos")
    print(" - Sincronización con semáforos y locks")
    print()
    print(" 💡 Interfaces disponibles:")
    print("    python ui/panel_hospital.py      (Panel de visualización)")
    print("    python ui/registro_paciente.py   (Registro de pacientes)")
    print("    • Puedes abrir múltiples ventanas de cada tipo")
    print("    • Se actualizan en tiempo real (event-driven)")
    print()
    print("=" * 80)
    print()
    
    try:
        # Crear instancia del hospital con configuración
        print("🚀 Inicializando sistema hospitalario...")
        hospital_instance = Hospital(
            capacidad_buffer=args.buffer_size,
            num_productores=args.productores,
            num_medicos=args.medicos
        )
        
        # Crear servidor de eventos para comunicación con interfaces
        print("🌐 Inicializando servidor de eventos...")
        event_server_instance = EventServer(hospital_instance, port=args.port)
        
        # Iniciar el hospital (hilos productores y consumidores)
        print("▶️  Iniciando hilos del hospital...")
        hospital_instance.iniciar()
        
        # Iniciar servidor de eventos
        print("▶️  Iniciando servidor de eventos...")
        event_server_instance.iniciar()
        
        print()
        print("=" * 80)
        print("✅ SERVIDOR ACTIVO Y FUNCIONANDO")
        print("=" * 80)
        print()
        print(f"🌐 Servidor de eventos escuchando en puerto {args.port}")
        print()
        print("📊 Estado del sistema:")
        stats = hospital_instance.get_estadisticas()
        print(f"   • Buffer: {stats['pacientes_en_buffer']}/{stats['capacidad_buffer']} pacientes")
        print(f"   • Productores activos: {stats['productores_activos']}")
        print(f"   • Médicos activos: {stats['medicos_activos']}")
        print()
        print("📋 Las interfaces gráficas pueden conectarse ahora:")
        print("   Terminal 2: python ui/panel_hospital.py")
        print("   Terminal 3: python ui/registro_paciente.py")
        print()
        print("⏸️  Presiona Ctrl+C para detener el servidor")
        print("=" * 80)
        print()
        
        # Mantener el servidor corriendo
        # Loop infinito (signal.pause() no funciona en Windows)
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            pass
        
    except KeyboardInterrupt:
        print("\n\n⏸️  Interrupción del usuario detectada")
    except Exception as e:
        print(f"\n\n❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print()
        print("=" * 80)
        print("🛑 DETENIENDO SERVIDOR")
        print("=" * 80)
        
        # Detener servidor de eventos
        if event_server_instance:
            print("🔴 Deteniendo servidor de eventos...")
            event_server_instance.detener()
        
        # Detener hospital (hilos productores y consumidores)
        if hospital_instance:
            print("🔴 Deteniendo hilos del hospital...")
            hospital_instance.detener()
            
            # Mostrar estadísticas finales
            print()
            print("📊 Estadísticas finales:")
            stats = hospital_instance.get_estadisticas()
            print(f"   • Pacientes generados: {stats['pacientes_generados']}")
            print(f"   • Pacientes atendidos: {stats['pacientes_atendidos']}")
            print(f"   • Expedientes registrados: {stats['expedientes']['total']}")
        
        print()
        print("✅ Servidor detenido correctamente")
        print("¡Hasta pronto! 👋")
        print("=" * 80)
        print()

if __name__ == "__main__":
    main()

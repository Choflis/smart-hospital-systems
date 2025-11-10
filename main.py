#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema Hospitalario con Concurrencia
=====================================

Proyecto de Sistemas Operativos
Demuestra:
- Problema Productor-Consumidor con semáforos manuales
- Problema Lectores-Escritores para expedientes médicos
- Sincronización con threads en Python

Funcionalidad original: Interfaces Terminal y GUI

NOTA: Para ejecutar el servidor del sistema, use servidor.py
      Este archivo (main.py) mantiene la funcionalidad original

Autor: Equipo de Desarrollo
Fecha: 2025
"""

import sys
import argparse
from core.hospital import Hospital
from ui.terminal_ui import TerminalUI
from ui.gui_app import GUIApp

def main():
    """Función principal del sistema"""
    
    # Parsear argumentos
    parser = argparse.ArgumentParser(
        description="Sistema Hospitalario con Concurrencia - Funcionalidad Original"
    )
    parser.add_argument(
        "--mode",
        choices=["terminal", "gui"],
        default="gui",
        help="Modo de interfaz: 'terminal' para consola o 'gui' para interfaz gráfica (default: gui)"
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
        help="Número de productores (default: 2)"
    )
    parser.add_argument(
        "--medicos",
        type=int,
        default=3,
        help="Número de médicos (default: 3)"
    )
    
    args = parser.parse_args()
    
    # Banner de inicio
    print("=" * 80)
    print(" 🏥 SISTEMA HOSPITALARIO - FUNCIONALIDAD ORIGINAL")
    print("=" * 80)
    print()
    print(f" Configuración:")
    print(f" - Modo: {args.mode.upper()}")
    print(f" - Buffer de pacientes: capacidad {args.buffer_size}")
    print(f" - Productores: {args.productores} threads generando pacientes")
    print(f" - Médicos: {args.medicos} threads atendiendo pacientes")
    print(f" - Sistema de expedientes con Lectores-Escritores")
    print()
    print(" 💡 Nota:")
    print("    Para usar el nuevo servidor con interfaces independientes,")
    print("    ejecute: python servidor.py")
    print()
    print("=" * 80)
    print()
    
    try:
        # Crear hospital con configuración
        hospital = Hospital(
            capacidad_buffer=args.buffer_size,
            num_productores=args.productores,
            num_medicos=args.medicos
        )
        
        # Elegir interfaz según el modo
        if args.mode == "terminal":
            print("\n📟 Ejecutando en modo TERMINAL")
            input("Presiona ENTER para iniciar el sistema...")
            
            # Iniciar el hospital
            hospital.iniciar()
            
            # Crear interfaz de terminal
            ui = TerminalUI(hospital)
            
            # Ejecutar interfaz (bloqueante)
            ui.ejecutar(intervalo=2)
            
        else:  # gui
            print("\n🖥️  Ejecutando en modo GUI (Interfaz Gráfica)")
            print("📌 Se abrirán 2 ventanas:")
            print("   1. Panel de Control - Controles y estadísticas")
            print("   2. Visualización de Flujo - Diagrama animado")
            print()
            input("Presiona ENTER para abrir las ventanas...")
            
            # Crear y ejecutar GUI
            app = GUIApp(hospital)
            app.ejecutar()
        
    except KeyboardInterrupt:
        print("\n\n⏸️  Interrupción del usuario detectada")
    except Exception as e:
        print(f"\n\n❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("\n🛑 Deteniendo sistema...")
        hospital.detener()
        print("\n✅ Sistema detenido correctamente")
        print("\n📊 Estadísticas finales:")
        stats = hospital.get_estadisticas()
        print(f"   - Pacientes generados: {stats['pacientes_generados']}")
        print(f"   - Pacientes atendidos: {stats['pacientes_atendidos']}")
        print(f"   - Expedientes registrados: {stats['expedientes']['total']}")
        print("\n¡Hasta pronto! 👋\n")

if __name__ == "__main__":
    main()

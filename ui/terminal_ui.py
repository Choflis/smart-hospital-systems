# ui/terminal_ui.py
"""
Interfaz de terminal para el sistema hospitalario
Muestra estadísticas en tiempo real
"""

import time
import os
import sys
from core.hospital import Hospital

class TerminalUI:
    """
    Interfaz de usuario en terminal
    Muestra estadísticas del hospital en tiempo real
    """
    
    def __init__(self, hospital: Hospital):
        """
        Inicializa la interfaz
        
        Args:
            hospital: Instancia del hospital a monitorear
        """
        self.hospital = hospital
    
    def limpiar_pantalla(self):
        """Limpia la pantalla de la terminal"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def mostrar_banner(self):
        """Muestra el banner del sistema"""
        print("=" * 80)
        print(" 🏥  SISTEMA HOSPITALARIO - GESTIÓN DE PACIENTES CON CONCURRENCIA")
        print("=" * 80)
        print(" 📊 Demostra Concurrencia: Productor-Consumidor + Lectores-Escritores")
        print("=" * 80)
        print()
    
    def mostrar_estadisticas(self):
        """Muestra las estadísticas del sistema"""
        stats = self.hospital.get_estadisticas()
        
        print(f"⏰ Hora: {time.strftime('%H:%M:%S')}")
        print()
        
        # Buffer
        print("📦 BUFFER DE PACIENTES")
        print(f"   └─ Pacientes en buffer: {stats['pacientes_en_buffer']}/{stats['capacidad_buffer']}")
        print()
        
        # Threads
        print("🔄 THREADS ACTIVOS")
        print(f"   ├─ Productores activos: {stats['productores_activos']}/{len(self.hospital.productores)}")
        print(f"   └─ Médicos activos: {stats['medicos_activos']}/{len(self.hospital.medicos)}")
        print()
        
        # Producción/Consumo
        print("📈 ESTADÍSTICAS DE OPERACIÓN")
        print(f"   ├─ Pacientes generados: {stats['pacientes_generados']}")
        print(f"   └─ Pacientes atendidos: {stats['pacientes_atendidos']}")
        print()
        
        # Expedientes
        if stats['expedientes']['total'] > 0:
            exp = stats['expedientes']
            print("📄 EXPEDIENTES MÉDICOS")
            print(f"   ├─ Total registrados: {exp['total']}")
            if 'por_prioridad' in exp:
                print(f"   ├─ Urgentes: {exp['por_prioridad']['urgente']}")
                print(f"   ├─ Normales: {exp['por_prioridad']['normal']}")
                print(f"   └─ Baja prioridad: {exp['por_prioridad']['baja']}")
            print()
        
        # Información de productores
        print("👥 PRODUCTORES")
        for i, prod in enumerate(self.hospital.productores, 1):
            estado = "🟢" if prod.is_alive() else "🔴"
            print(f"   {estado} {prod.name}: {prod.pacientes_generados} pacientes generados")
        print()
        
        # Información de médicos
        print("🩺 MÉDICOS")
        for i, med in enumerate(self.hospital.medicos, 1):
            estado = "🟢" if med.is_alive() else "🔴"
            print(f"   {estado} {med.name}: {med.pacientes_atendidos} pacientes atendidos")
        print()
        
        print("=" * 80)
        print(" Presiona Ctrl+C para detener el sistema")
        print("=" * 80)
    
    def ejecutar(self, intervalo: int = 2):
        """
        Ejecuta la interfaz en un loop
        
        Args:
            intervalo: Tiempo entre actualizaciones (segundos)
        """
        try:
            while True:
                self.limpiar_pantalla()
                self.mostrar_banner()
                self.mostrar_estadisticas()
                time.sleep(intervalo)
                
        except KeyboardInterrupt:
            print("\n\n🛑 Deteniendo sistema...")

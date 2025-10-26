"""
Sistema de Gestión Hospitalaria - Nueva UI Profesional
Punto de entrada para la interfaz modernizada
"""

import sys
import time
from models.buffer import Buffer
from models.consumidor import Consumidor
from models.productor import Productor


class HospitalSystem:
    """Sistema hospitalario completo"""
    
    def __init__(self):
        self.buffer = Buffer(capacidad=10)
        self.consumidores = []
        self.productor = None
        self.medicos = []
        
    def iniciar(self):
        """Iniciar sistema"""
        print("🏥 Iniciando Smart Hospital System...")
        
        # Crear consumidores (médicos)
        self.consumidores = [Consumidor(id=i, buffer=self.buffer) for i in range(5)]
        for c in self.consumidores:
            c.start()
        
        # Crear productor
        self.productor = Productor(self.buffer)
        self.productor.start()
        
        print("✅ Sistema iniciado correctamente")
    
    def detener(self):
        """Detener sistema"""
        print("🛑 Deteniendo sistema...")
        
        if self.productor:
            self.productor.detener()
        
        for c in self.consumidores:
            c.detener()
        
        print("✅ Sistema detenido")


def main():
    """Punto de entrada principal"""
    print("""
╔══════════════════════════════════════════════════════════╗
║      🏥 SMART HOSPITAL MANAGEMENT SYSTEM 🏥             ║
║                                                          ║
║  Sistema Profesional de Gestión Hospitalaria            ║
║  Proyecto de Sistemas Operativos - UNSA                 ║
╚══════════════════════════════════════════════════════════╝
    """)
    
    try:
        from ui.main_window import MainWindow
    except ImportError as e:
        print(f"❌ Error al importar UI: {e}")
        print("Asegúrate de que tkinter esté instalado.")
        return
    
    # Crear sistema hospitalario
    hospital = HospitalSystem()
    hospital.iniciar()
    
    # Crear y ejecutar ventana principal
    try:
        print("🚀 Abriendo interfaz gráfica...")
        app = MainWindow(hospital)
        app.mainloop()
    except KeyboardInterrupt:
        print("\n⚠️ Interrupción detectada")
    except Exception as e:
        print(f"❌ Error en la interfaz: {e}")
        import traceback
        traceback.print_exc()
    finally:
        hospital.detener()
        print("👋 Hasta luego!")


if __name__ == "__main__":
    main()

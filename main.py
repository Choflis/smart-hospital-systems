# main.py
"""
Sistema de Gestión Hospitalaria
--------------------------------
Punto de entrada principal del sistema.
Soporta dos modos: consola y UI gráfica.
"""
import sys
import time
from models.buffer import Buffer
from models.paciente import Paciente
from models.consumidor import Consumidor
from models.productor import Productor

def modo_consola():
    """Ejecuta el sistema en modo consola (CLI)"""
    print("=== SISTEMA DE GESTIÓN DE PACIENTES (MODO CONSOLA) ===")

    # Crear buffer compartido
    buffer = Buffer(capacidad=5)

    # Crear e iniciar consumidores (médicos)
    consumidores = [Consumidor(id=i, buffer=buffer) for i in range(3)]
    for c in consumidores:
        c.start()

    # Crear productor (personal de admisión)
    productor = Productor(buffer)
    productor.start()

    # Bucle principal de interacción
    while True:
        print("\n1. Agregar paciente")
        print("2. Ver pacientes en espera")
        print("3. Detener sistema")
        print("========================================")
        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            try:
                nombre = input("Nombre del paciente: ")
                edad = int(input("Edad del paciente: "))
                genero = input("Género (Masculino/Femenino/Otro): ")
                sintomas = input("Síntomas: ")

                nuevo_paciente = Paciente(nombre, edad, genero, sintomas)
                exito = buffer.agregar_paciente(nuevo_paciente)
                if exito:
                    print(f"✅ Paciente '{nombre}' agregado correctamente.")
                else:
                    print("⚠️  No se pudo agregar el paciente. Buffer lleno.")
            except ValueError:
                print("❌ Error: La edad debe ser un número.")

        elif opcion == "2":
            pacientes = buffer.obtener_lista_pacientes()
            if pacientes:
                print("\n👥 Pacientes en espera:")
                for p in pacientes:
                    print(f"- {p.nombre} ({p.edad} años, {p.genero}) - {p.sintomas}")
            else:
                print("📭 No hay pacientes en espera.")

        elif opcion == "3":
            print("🛑 Deteniendo el sistema...")
            productor.detener()
            for c in consumidores:
                c.detener()
            break

        else:
            print("❌ Opción no válida. Intenta nuevamente.")

        time.sleep(0.5)

    print("Sistema detenido correctamente.")

def modo_ui():
    """Ejecuta el sistema con interfaz gráfica"""
    print("=== SISTEMA DE GESTIÓN DE PACIENTES (MODO UI) ===")
    
    try:
        from ui.hospital_ui import HospitalUI
    except ImportError:
        print("❌ Error: No se pudo importar la UI.")
        print("Asegúrate de que tkinter esté instalado.")
        return
    
    # Crear buffer compartido
    buffer = Buffer(capacidad=5)
    
    # Crear e iniciar consumidores (médicos)
    consumidores = [Consumidor(id=i, buffer=buffer) for i in range(3)]
    for c in consumidores:
        c.start()
    
    # Crear productor (personal de admisión)
    productor = Productor(buffer)
    productor.start()
    
    # Iniciar interfaz gráfica
    print("🚀 Abriendo interfaz gráfica...")
    ui = HospitalUI(buffer, consumidores, productor)
    ui.run()
    
    print("Sistema cerrado correctamente.")

def main():
    """Punto de entrada principal"""
    print("""
╔══════════════════════════════════════════════════════════╗
║      🏥 SMART HOSPITAL MANAGEMENT SYSTEM 🏥             ║
║                                                          ║
║  Sistema de Gestión Hospitalaria con Concurrencia       ║
║  Proyecto de Sistemas Operativos - UNSA                 ║
╚══════════════════════════════════════════════════════════╝
    """)
    
    # Determinar modo de ejecución
    if len(sys.argv) > 1:
        modo = sys.argv[1].lower()
        if modo == "--consola" or modo == "-c":
            modo_consola()
        elif modo == "--ui" or modo == "-u":
            modo_ui()
        elif modo == "--help" or modo == "-h":
            print("Uso: python main.py [OPCIÓN]")
            print("\nOpciones:")
            print("  --ui, -u       Inicia con interfaz gráfica (por defecto)")
            print("  --consola, -c  Inicia en modo consola")
            print("  --help, -h     Muestra esta ayuda")
        else:
            print(f"❌ Opción desconocida: {modo}")
            print("Usa --help para ver las opciones disponibles.")
    else:
        # Por defecto, usar UI
        print("💡 Consejo: Usa 'python main.py --consola' para modo consola")
        print("Iniciando en modo UI en 2 segundos...\n")
        time.sleep(2)
        modo_ui()

if __name__ == "__main__":
    main()

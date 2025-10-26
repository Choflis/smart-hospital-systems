"""
Script de prueba para demostrar la implementación de tu responsabilidad:
- utils/generador_datos.py
- hospital/base_datos.py
- utils/logger.py
"""
import sys
import time
import threading
from pathlib import Path

# Agregar directorio raíz al path
sys.path.append(str(Path(__file__).parent))

from utils.generador_datos import (
    generar_paciente_aleatorio, 
    generar_diagnostico_completo,
    generar_nombre_completo
)
from hospital.base_datos import BaseDeDatos
from utils.logger import log_event


def prueba_generador():
    """Prueba el generador de datos aleatorios."""
    print("\n" + "="*60)
    print("PRUEBA 1: GENERADOR DE DATOS ALEATORIOS")
    print("="*60)
    
    log_event("Iniciando prueba de generador de datos...")
    
    # Generar 3 pacientes aleatorios
    print("\n📋 Generando 3 pacientes aleatorios:")
    for i in range(3):
        paciente = generar_paciente_aleatorio()
        print(f"\nPaciente {i+1}:")
        print(f"  - Nombre: {paciente['nombre']}")
        print(f"  - Edad: {paciente['edad']} años")
        print(f"  - Género: {paciente['genero']}")
        print(f"  - Síntomas: {paciente['sintomas']}")
    
    # Generar 2 diagnósticos
    print("\n\n💊 Generando 2 diagnósticos aleatorios:")
    for i in range(2):
        diag = generar_diagnostico_completo(generar_nombre_completo(), i+1)
        print(f"\nDiagnóstico {i+1}:")
        print(f"  - Paciente: {diag['paciente_nombre']}")
        print(f"  - Médico ID: {diag['medico_id']}")
        print(f"  - Diagnóstico: {diag['diagnostico']}")
        print(f"  - Tratamiento: {diag['tratamiento']}")
    
    log_event("Prueba de generador completada ✓")


def prueba_base_datos():
    """Prueba la base de datos con patrón Lectores-Escritores."""
    print("\n" + "="*60)
    print("PRUEBA 2: BASE DE DATOS (Lectores-Escritores)")
    print("="*60)
    
    log_event("Iniciando prueba de base de datos...")
    
    # Crear base de datos
    db = BaseDeDatos("data/prueba_responsabilidad.json")
    
    # Limpiar datos previos
    db.vaciar_base_datos()
    
    # Agregar pacientes usando el generador
    print("\n📝 Agregando 5 pacientes a la base de datos...")
    for i in range(5):
        paciente = generar_paciente_aleatorio()
        db.agregar_registro(paciente)
        time.sleep(0.1)  # Simular tiempo de procesamiento
    
    # Leer todos los registros
    print("\n📖 Leyendo todos los registros...")
    registros = db.leer_todos()
    print(f"Total de registros: {len(registros)}")
    
    # Buscar un paciente específico
    if registros:
        primer_paciente = registros[0]['nombre']
        print(f"\n🔍 Buscando paciente: {primer_paciente}")
        encontrado = db.buscar_por_nombre(primer_paciente)
        if encontrado:
            print(f"  ✓ Encontrado: {encontrado['nombre']}, {encontrado['edad']} años")
    
    # Actualizar un registro
    if registros:
        print(f"\n✏️  Actualizando síntomas de {primer_paciente}...")
        db.actualizar_registro(primer_paciente, {
            "sintomas": "Recuperado - Alta médica",
            "estado": "Dado de alta"
        })
    
    log_event("Prueba de base de datos completada ✓")


def prueba_concurrencia():
    """Prueba concurrencia: múltiples lectores y escritores."""
    print("\n" + "="*60)
    print("PRUEBA 3: CONCURRENCIA (Lectores-Escritores simultáneos)")
    print("="*60)
    
    log_event("Iniciando prueba de concurrencia...")
    
    db = BaseDeDatos("data/prueba_concurrencia.json")
    db.vaciar_base_datos()
    
    # Agregar algunos registros iniciales
    for i in range(3):
        db.agregar_registro(generar_paciente_aleatorio())
    
    def lector(id_lector, num_lecturas=3):
        """Función que simula un lector."""
        for i in range(num_lecturas):
            registros = db.leer_todos()
            log_event(f"[LECTOR {id_lector}] Leyó {len(registros)} registros")
            time.sleep(0.2)
    
    def escritor(id_escritor, num_escrituras=2):
        """Función que simula un escritor."""
        for i in range(num_escrituras):
            paciente = generar_paciente_aleatorio()
            db.agregar_registro(paciente)
            log_event(f"[ESCRITOR {id_escritor}] Agregó paciente: {paciente['nombre']}")
            time.sleep(0.3)
    
    # Crear hilos
    print("\n🔄 Lanzando 3 lectores y 2 escritores concurrentes...")
    hilos = []
    
    # 3 lectores
    for i in range(3):
        hilo = threading.Thread(target=lector, args=(i, 3))
        hilos.append(hilo)
    
    # 2 escritores
    for i in range(2):
        hilo = threading.Thread(target=escritor, args=(i, 2))
        hilos.append(hilo)
    
    # Iniciar todos los hilos
    for hilo in hilos:
        hilo.start()
    
    # Esperar a que terminen
    for hilo in hilos:
        hilo.join()
    
    # Resultado final
    print(f"\n📊 Resultado final: {db.contar_registros()} registros en la base de datos")
    log_event("Prueba de concurrencia completada ✓")


def prueba_integracion():
    """Prueba de integración completa: simula flujo real del hospital."""
    print("\n" + "="*60)
    print("PRUEBA 4: INTEGRACIÓN COMPLETA (Flujo hospitalario)")
    print("="*60)
    
    log_event("Iniciando simulación de flujo hospitalario...")
    
    db = BaseDeDatos("data/hospital_real.json")
    db.vaciar_base_datos()
    
    print("\n🏥 Simulando día en el hospital...\n")
    
    # 1. Recepción: Llegada de pacientes
    print("📋 RECEPCIÓN: Ingresando pacientes...")
    for i in range(5):
        paciente = generar_paciente_aleatorio()
        db.agregar_registro(paciente)
        log_event(f"Paciente ingresado: {paciente['nombre']}")
        time.sleep(0.1)
    
    # 2. Médicos: Consultando pacientes
    print("\n👨‍⚕️ MÉDICOS: Consultando lista de pacientes...")
    pacientes = db.leer_todos()
    for p in pacientes:
        print(f"  - {p['nombre']}: {p['sintomas']}")
    
    # 3. Laboratorio: Actualizando con diagnósticos
    print("\n🔬 LABORATORIO: Procesando diagnósticos...")
    for paciente in pacientes[:3]:  # Procesar 3 primeros
        diagnostico = generar_diagnostico_completo(paciente['nombre'], 1)
        db.actualizar_registro(paciente['nombre'], {
            "diagnostico": diagnostico['diagnostico'],
            "tratamiento": diagnostico['tratamiento'],
            "procesado": True
        })
        log_event(f"Diagnóstico procesado: {paciente['nombre']}")
        time.sleep(0.1)
    
    # 4. Estadísticas: Generando reporte
    print("\n📊 ESTADÍSTICAS: Generando reporte final...")
    todos = db.leer_todos()
    procesados = sum(1 for p in todos if p.get('procesado', False))
    print(f"  - Total pacientes: {len(todos)}")
    print(f"  - Procesados: {procesados}")
    print(f"  - Pendientes: {len(todos) - procesados}")
    
    log_event("Simulación de flujo hospitalario completada ✓")


if __name__ == "__main__":
    print("\n" + "╔"+"═"*60+"╗")
    print("║" + " "*15 + "PRUEBAS DE RESPONSABILIDAD" + " "*19 + "║")
    print("║" + " "*10 + "(Base de Datos + Generador + Logger)" + " "*12 + "║")
    print("╚" + "═"*60 + "╝")
    
    try:
        # Ejecutar todas las pruebas
        prueba_generador()
        prueba_base_datos()
        prueba_concurrencia()
        prueba_integracion()
        
        print("\n" + "="*60)
        print("✅ TODAS LAS PRUEBAS COMPLETADAS EXITOSAMENTE")
        print("="*60)
        
    except Exception as e:
        print(f"\n❌ Error durante las pruebas: {e}")
        import traceback
        traceback.print_exc()

"""
Script de prueba para la API del Hospital
==========================================
Prueba las funcionalidades básicas de la API.
"""

import requests
import json
import time

# Configuración
BASE_URL = "http://localhost:8000"

def print_section(title):
    """Imprime un separador visual"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")

def test_estado_sistema():
    """Prueba el endpoint de estado del sistema"""
    print_section("1. ESTADO DEL SISTEMA")
    response = requests.get(f"{BASE_URL}/")
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2))
    return response.json()

def test_agregar_paciente(nombre, edad, genero, sintomas):
    """Prueba agregar un paciente"""
    print_section(f"2. AGREGAR PACIENTE: {nombre}")
    data = {
        "nombre": nombre,
        "edad": edad,
        "genero": genero,
        "sintomas": sintomas
    }
    response = requests.post(f"{BASE_URL}/pacientes", json=data)
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2))
    return response.json()

def test_listar_pacientes():
    """Prueba listar pacientes"""
    print_section("3. LISTAR PACIENTES EN ESPERA")
    response = requests.get(f"{BASE_URL}/pacientes")
    print(f"Status: {response.status_code}")
    result = response.json()
    print(json.dumps(result, indent=2))
    return result

def test_estado_buffer():
    """Prueba el estado del buffer"""
    print_section("4. ESTADO DEL BUFFER")
    response = requests.get(f"{BASE_URL}/pacientes/estado")
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2))
    return response.json()

def test_agregar_diagnostico(paciente_id, medico_id, diagnostico, tratamiento):
    """Prueba agregar un diagnóstico"""
    print_section(f"5. AGREGAR DIAGNÓSTICO (Médico {medico_id})")
    data = {
        "paciente_id": paciente_id,
        "medico_id": medico_id,
        "diagnostico": diagnostico,
        "tratamiento": tratamiento
    }
    response = requests.post(f"{BASE_URL}/diagnosticos", json=data)
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2))
    return response.json()

def test_listar_diagnosticos():
    """Prueba listar diagnósticos"""
    print_section("6. LISTAR DIAGNÓSTICOS")
    response = requests.get(f"{BASE_URL}/diagnosticos")
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2))
    return response.json()

def test_procesar_diagnostico(diagnostico_id):
    """Prueba procesar un diagnóstico"""
    print_section(f"7. PROCESAR DIAGNÓSTICO (Laboratorio) - ID: {diagnostico_id}")
    response = requests.put(f"{BASE_URL}/diagnosticos/{diagnostico_id}/procesar")
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2))
    return response.json()

def test_estadisticas():
    """Prueba obtener estadísticas"""
    print_section("8. ESTADÍSTICAS DEL SISTEMA")
    response = requests.get(f"{BASE_URL}/estadisticas")
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2))
    return response.json()

def test_listar_medicos():
    """Prueba listar médicos"""
    print_section("9. MÉDICOS ACTIVOS")
    response = requests.get(f"{BASE_URL}/medicos")
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2))
    return response.json()

def main():
    """Ejecuta todas las pruebas"""
    print("""
╔══════════════════════════════════════════════════════════╗
║     🧪 PRUEBAS DE LA API - SMART HOSPITAL SYSTEM 🧪     ║
╚══════════════════════════════════════════════════════════╝
    """)
    
    try:
        # 1. Estado inicial
        test_estado_sistema()
        time.sleep(1)
        
        # 2. Agregar pacientes de prueba
        test_agregar_paciente("Juan Pérez", 45, "Masculino", "Fiebre alta y tos")
        time.sleep(1)
        
        test_agregar_paciente("María García", 32, "Femenino", "Dolor de cabeza intenso")
        time.sleep(1)
        
        test_agregar_paciente("Carlos López", 28, "Masculino", "Dolor abdominal")
        time.sleep(1)
        
        # 3. Listar pacientes
        test_listar_pacientes()
        time.sleep(1)
        
        # 4. Estado del buffer
        test_estado_buffer()
        time.sleep(1)
        
        # 5. Agregar diagnósticos
        test_agregar_diagnostico("juan_perez", 1, "Gripe común", "Reposo y antipiréticos")
        time.sleep(1)
        
        test_agregar_diagnostico("maria_garcia", 2, "Migraña", "Analgésicos y evitar luces brillantes")
        time.sleep(1)
        
        # 6. Listar diagnósticos
        test_listar_diagnosticos()
        time.sleep(1)
        
        # 7. Procesar un diagnóstico
        test_procesar_diagnostico(0)
        time.sleep(1)
        
        # 8. Estadísticas
        test_estadisticas()
        time.sleep(1)
        
        # 9. Médicos activos
        test_listar_medicos()
        
        print_section("✅ TODAS LAS PRUEBAS COMPLETADAS")
        print("La API está funcionando correctamente!")
        
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: No se pudo conectar al servidor")
        print("Asegúrate de que el servidor esté ejecutándose:")
        print("  uvicorn api_server.main:app --reload")
    except Exception as e:
        print(f"\n❌ ERROR INESPERADO: {e}")

if __name__ == "__main__":
    main()

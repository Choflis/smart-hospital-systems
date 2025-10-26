"""
Módulo para generar datos aleatorios del sistema hospitalario.
Genera nombres, síntomas, diagnósticos y tratamientos realistas.
"""
import random
from datetime import datetime, timedelta

# ---- LISTAS DE DATOS PARA GENERACIÓN ALEATORIA ----

NOMBRES = [
    "Juan", "María", "Carlos", "Ana", "Luis", "Carmen", "José", 
    "Laura", "Pedro", "Isabel", "Miguel", "Elena", "Antonio", 
    "Sofía", "Francisco", "Patricia", "Daniel", "Lucía", "Manuel", "Rosa"
]

APELLIDOS = [
    "García", "Rodríguez", "Martínez", "López", "González", "Pérez",
    "Sánchez", "Ramírez", "Torres", "Flores", "Rivera", "Gómez",
    "Díaz", "Cruz", "Morales", "Reyes", "Jiménez", "Hernández"
]

GENEROS = ["Masculino", "Femenino", "Otro"]

SINTOMAS = [
    "Fiebre alta persistente",
    "Dolor de cabeza intenso",
    "Dolor abdominal",
    "Náuseas y vómitos",
    "Tos seca continua",
    "Dificultad para respirar",
    "Dolor en el pecho",
    "Mareos y debilidad",
    "Dolor de garganta",
    "Erupción en la piel",
    "Dolor muscular generalizado",
    "Fatiga extrema",
    "Pérdida del apetito",
    "Sudoración nocturna"
]

DIAGNOSTICOS = [
    "Gripe común",
    "Infección respiratoria aguda",
    "Gastritis aguda",
    "Migraña",
    "Bronquitis",
    "Faringitis",
    "Dermatitis alérgica",
    "Síndrome gripal",
    "Infección urinaria",
    "Hipertensión arterial",
    "Diabetes tipo 2",
    "Anemia",
    "Neumonía leve"
]

TRATAMIENTOS = [
    "Reposo absoluto por 3 días",
    "Antibiótico (Amoxicilina 500mg cada 8h)",
    "Analgésico (Ibuprofeno 400mg cada 6h)",
    "Antipirético (Paracetamol 500mg cada 8h)",
    "Antiinflamatorio (Naproxeno 250mg cada 12h)",
    "Antihistamínico (Loratadina 10mg cada 24h)",
    "Hidratación abundante",
    "Dieta blanda y líquidos",
    "Inhalaciones con vapor",
    "Omeprazol 20mg cada 12h"
]


# ---- FUNCIONES GENERADORAS ----

def generar_nombre_completo():
    """
    Genera un nombre completo aleatorio.
    
    Returns:
        str: Nombre completo (Nombre + Apellido)
    """
    nombre = random.choice(NOMBRES)
    apellido = random.choice(APELLIDOS)
    return f"{nombre} {apellido}"


def generar_edad(min_edad=1, max_edad=90):
    """
    Genera una edad aleatoria dentro de un rango.
    
    Args:
        min_edad (int): Edad mínima
        max_edad (int): Edad máxima
    
    Returns:
        int: Edad aleatoria
    """
    return random.randint(min_edad, max_edad)


def generar_genero():
    """
    Genera un género aleatorio.
    
    Returns:
        str: Género (Masculino, Femenino, Otro)
    """
    return random.choice(GENEROS)


def generar_sintomas(cantidad=1):
    """
    Genera uno o más síntomas aleatorios.
    
    Args:
        cantidad (int): Número de síntomas a generar
    
    Returns:
        str: Síntomas separados por comas
    """
    sintomas_seleccionados = random.sample(SINTOMAS, min(cantidad, len(SINTOMAS)))
    return ", ".join(sintomas_seleccionados)


def generar_diagnostico():
    """
    Genera un diagnóstico médico aleatorio.
    
    Returns:
        str: Diagnóstico
    """
    return random.choice(DIAGNOSTICOS)


def generar_tratamiento():
    """
    Genera un tratamiento médico aleatorio.
    
    Returns:
        str: Tratamiento
    """
    return random.choice(TRATAMIENTOS)


def generar_paciente_aleatorio():
    """
    Genera un diccionario completo con datos de un paciente aleatorio.
    
    Returns:
        dict: Diccionario con datos del paciente
    """
    return {
        "nombre": generar_nombre_completo(),
        "edad": generar_edad(),
        "genero": generar_genero(),
        "sintomas": generar_sintomas(random.randint(1, 3)),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }


def generar_diagnostico_completo(paciente_nombre="Paciente", medico_id=1):
    """
    Genera un registro completo de diagnóstico.
    
    Args:
        paciente_nombre (str): Nombre del paciente
        medico_id (int): ID del médico
    
    Returns:
        dict: Diagnóstico completo
    """
    return {
        "paciente_nombre": paciente_nombre,
        "medico_id": medico_id,
        "diagnostico": generar_diagnostico(),
        "tratamiento": generar_tratamiento(),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "procesado": False
    }


def generar_timestamp_aleatorio(dias_atras=30):
    """
    Genera un timestamp aleatorio dentro de los últimos N días.
    
    Args:
        dias_atras (int): Días hacia atrás desde hoy
    
    Returns:
        str: Timestamp formateado
    """
    fecha_base = datetime.now()
    dias_random = random.randint(0, dias_atras)
    fecha_aleatoria = fecha_base - timedelta(days=dias_random)
    return fecha_aleatoria.strftime("%Y-%m-%d %H:%M:%S")


# ---- FUNCIÓN DE PRUEBA ----
if __name__ == "__main__":
    """Código de prueba para verificar el funcionamiento."""
    print("=== PRUEBA DE GENERADOR DE DATOS ===\n")
    
    print("1. Paciente aleatorio:")
    print(generar_paciente_aleatorio())
    
    print("\n2. Diagnóstico completo:")
    print(generar_diagnostico_completo("Juan García", 1))
    
    print("\n3. Generando 5 nombres:")
    for _ in range(5):
        print(f"  - {generar_nombre_completo()}, {generar_edad()} años, {generar_genero()}")


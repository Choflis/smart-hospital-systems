# Arquitectura del Sistema Hospitalario

## 📐 Estructura del Proyecto

```
smart-hospital-systems/
│
├── 📁 core/                    # Lógica de negocio
│   ├── __init__.py
│   ├── paciente.py             # Modelo Paciente
│   └── hospital.py             # Coordinador principal
│
├── 📁 concurrencia/            # Componentes de sincronización
│   ├── __init__.py
│   ├── buffer.py               # Buffer con semáforos (Productor-Consumidor)
│   ├── productor.py            # Thread productor de pacientes
│   ├── consumidor.py           # Thread médico (consumidor)
│   └── lector_escritor.py      # Sistema de expedientes (Lectores-Escritores)
│
├── 📁 data/                    # Datos y logs
│   ├── expedientes.json        # Base de datos de expedientes
│   └── logs/
│       └── hospital.log        # Logs del sistema
│
├── 📁 ui/                      # Interfaz de usuario
│   ├── __init__.py
│   └── terminal_ui.py          # Interfaz en terminal
│
├── 📁 docs/                    # Documentación
│   ├── ARQUITECTURA.md         # Este archivo
│   ├── CONCURRENCIA.md         # Explicación de sincronización
│   └── COMO_EJECUTAR.md        # Guía de uso
│
├── main.py                     # Punto de entrada
├── config.py                   # Configuración
└── requirements.txt            # Dependencias
```

## 🏗️ Componentes Principales

### 1. Core (Núcleo)

#### **Paciente** (`core/paciente.py`)
- Representa un paciente en el sistema
- Atributos: id, nombre, prioridad, diagnóstico, estado
- Métodos para gestionar su ciclo de vida

#### **Hospital** (`core/hospital.py`)
- Coordinador principal del sistema
- Inicializa y gestiona todos los componentes
- Provee estadísticas globales

### 2. Concurrencia

#### **BufferPacientes** (`concurrencia/buffer.py`)
- Buffer circular con capacidad limitada
- **Problema: Productor-Consumidor**
- Usa semáforos MANUALES:
  - `mutex`: Exclusión mutua
  - `empty`: Contador de espacios vacíos
  - `full`: Contador de elementos disponibles

#### **ProductorPacientes** (`concurrencia/productor.py`)
- Thread que genera pacientes aleatorios
- Los agrega al buffer compartido
- Se bloquea si el buffer está lleno

#### **Medico** (`concurrencia/consumidor.py`)
- Thread que consume pacientes del buffer
- Simula tiempo de atención
- Se bloquea si el buffer está vacío

#### **SistemaExpedientes** (`concurrencia/lector_escritor.py`)
- Gestiona archivo JSON con expedientes
- **Problema: Lectores-Escritores**
- Permite múltiples lectores simultáneos
- Solo un escritor a la vez

### 3. Interfaz de Usuario

#### **TerminalUI** (`ui/terminal_ui.py`)
- Muestra estadísticas en tiempo real
- Actualiza cada 2 segundos
- Información de threads, buffer y expedientes

## 🔄 Flujo de Ejecución

1. **Inicio**: `main.py` crea instancia de `Hospital`
2. **Inicialización**: Se crean buffer, productores, médicos y sistema de expedientes
3. **Inicio de threads**: Se lanzan 2 productores y 3 médicos
4. **Loop principal**:
   - Productores generan pacientes → agregan al buffer
   - Médicos extraen del buffer → atienden → guardan expediente
   - UI muestra estadísticas
5. **Detención**: Ctrl+C detiene ordenadamente todos los threads

## 🧵 Sincronización

### Productor-Consumidor (Buffer)
```python
# PRODUCTOR
empty.acquire()     # Espera espacio disponible
mutex.acquire()     # Sección crítica
buffer.append(x)
mutex.release()
full.release()      # Señala elemento disponible

# CONSUMIDOR
full.acquire()      # Espera elemento disponible
mutex.acquire()     # Sección crítica
x = buffer.pop(0)
mutex.release()
empty.release()     # Señala espacio disponible
```

### Lectores-Escritores (Expedientes)
```python
# LECTOR
mutex.acquire()
lectores++
if (lectores == 1):
    escritor_lock.acquire()  # Primer lector bloquea escritores
mutex.release()
# ... LEER ...
mutex.acquire()
lectores--
if (lectores == 0):
    escritor_lock.release()  # Último lector libera escritores
mutex.release()

# ESCRITOR
escritor_lock.acquire()  # Exclusión total
# ... ESCRIBIR ...
escritor_lock.release()
```

## 📊 Modelo de Datos

### Paciente
```json
{
    "id": 123456,
    "nombre": "Juan Pérez",
    "prioridad": 1,
    "diagnostico": "Fractura de brazo",
    "estado": "Atendido",
    "hora_llegada": "2024-01-10T10:30:00",
    "hora_atencion": "2024-01-10T10:35:00",
    "medico_asignado": "Dr. García",
    "tiempo_espera": 300.5
}
```

### Expediente
```json
{
    "expedientes": [
        {
            "id": 123456,
            "nombre": "Juan Pérez",
            "prioridad": 1,
            "diagnostico": "Fractura de brazo",
            "estado": "Atendido",
            "hora_llegada": "2024-01-10T10:30:00",
            "hora_atencion": "2024-01-10T10:35:00",
            "medico_asignado": "Dr. García",
            "tiempo_espera": 300.5,
            "fecha_registro": "2024-01-10T10:36:00"
        }
    ],
    "metadata": {
        "creado": "2024-01-10T10:00:00"
    }
}
```

## 🎯 Conceptos de Sistemas Operativos Demostrados

1. **Threads**: Múltiples hilos de ejecución concurrente
2. **Semáforos**: Sincronización con contadores
3. **Locks/Mutex**: Exclusión mutua en secciones críticas
4. **Productor-Consumidor**: Patrón clásico de sincronización
5. **Lectores-Escritores**: Control de acceso concurrente a recursos compartidos
6. **Condiciones de carrera**: Evitadas con sincronización apropiada
7. **Deadlock**: Prevenido con orden de adquisición de locks
8. **Starvation**: Mitigada con prioridades en pacientes

## 🔍 Puntos Clave de la Implementación

- ✅ **NO usa `queue.Queue`**: Implementación manual con semáforos
- ✅ **Semáforos explícitos**: `threading.Semaphore` usado manualmente
- ✅ **Locks explícitos**: `threading.Lock` para mutex
- ✅ **Threads propios**: `threading.Thread` extendido
- ✅ **Sincronización clara**: Patrones clásicos bien implementados
- ✅ **Logging completo**: Trazabilidad de todas las operaciones
- ✅ **Modular y escalable**: Fácil de extender y modificar

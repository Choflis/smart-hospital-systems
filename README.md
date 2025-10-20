# 🏥 Smart Hospital Systems - Sistema Hospitalario Inteligente

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![OS](https://img.shields.io/badge/OS-Concepts-orange.svg)
![Status](https://img.shields.io/badge/Status-Active-success.svg)

**Simulación avanzada de sincronización de procesos en un sistema hospitalario digital**

[Características](#-características) • [Instalación](#-instalación) • [Uso](#-uso) • [Arquitectura](#-arquitectura) • [Contribuir](#-contribuir)

</div>

---

## 📋 Descripción

**Smart Hospital Systems** es un proyecto de simulación desarrollado en Python que representa la interacción concurrente entre múltiples módulos de un sistema hospitalario digital. El sistema implementa conceptos fundamentales de sistemas operativos para gestionar de manera segura y eficiente los datos hospitalarios críticos.

Este proyecto demuestra cómo los mecanismos de sincronización de procesos son esenciales en sistemas de salud donde múltiples servicios deben acceder y modificar información de pacientes, historiales médicos, inventarios y recursos hospitalarios de forma concurrente sin comprometer la integridad de los datos.

## ✨ Características

### 🎯 Funcionalidades Principales

- **🔄 Productores y Consumidores**: Simulación del modelo productor-consumidor para gestión de citas, admisiones y registros médicos
- **📖 Lectores y Escritores**: Implementación del problema de lectores-escritores para acceso concurrente a historiales clínicos
- **💾 Almacenamiento Compartido**: Sistema de memoria compartida para datos hospitalarios críticos
- **🔒 Sincronización Robusta**: Mecanismos de protección contra condiciones de carrera y deadlocks

### 🛠️ Conceptos de Sistemas Operativos Implementados

- **Semáforos**: Control de acceso a recursos limitados (camas, quirófanos, equipamiento)
- **Mutex (Mutual Exclusion)**: Protección de secciones críticas en actualizaciones de datos
- **Variables de Condición**: Coordinación de procesos en operaciones complejas
- **Bloqueos de Lectura/Escritura**: Optimización de acceso concurrente a información
- **Productor-Consumidor**: Gestión de colas de pacientes y servicios hospitalarios
- **Lectores-Escritores**: Acceso eficiente a registros médicos electrónicos

## 🏗️ Arquitectura

### Componentes del Sistema

```
┌─────────────────────────────────────────────────────────────┐
│                    SMART HOSPITAL SYSTEM                     │
└─────────────────────────────────────────────────────────────┘
                               │
        ┌──────────────────────┼──────────────────────┐
        │                      │                      │
   ┌────▼────┐          ┌──────▼──────┐       ┌──────▼──────┐
   │ Módulo  │          │   Módulo    │       │   Módulo    │
   │Productor│          │  Consumidor │       │   Lector    │
   └────┬────┘          └──────┬──────┘       └──────┬──────┘
        │                      │                      │
        │    ┌─────────────────┴───────┐             │
        │    │                         │             │
        └────►  ALMACENAMIENTO COMPARTIDO ◄──────────┘
             │  (Semáforos & Mutex)     │
             └──────────┬────────────────┘
                        │
                  ┌─────▼─────┐
                  │  Módulo   │
                  │ Escritor  │
                  └───────────┘
```

### 🎭 Módulos del Sistema

#### 1. 🏭 Módulo Productor
Genera y agrega información al sistema hospitalario:
- Registro de nuevos pacientes
- Programación de citas médicas
- Ingreso de resultados de laboratorio
- Actualización de inventario de medicamentos

#### 2. 🔍 Módulo Consumidor
Procesa y consume información del sistema:
- Asignación de recursos hospitalarios
- Procesamiento de solicitudes de servicios
- Gestión de colas de emergencia
- Distribución de tareas al personal médico

#### 3. 📚 Módulo Lector
Acceso concurrente de solo lectura:
- Consulta de historiales clínicos
- Visualización de estadísticas hospitalarias
- Generación de reportes
- Monitoreo en tiempo real

#### 4. ✍️ Módulo Escritor
Modificación exclusiva de datos críticos:
- Actualización de diagnósticos
- Registro de procedimientos quirúrgicos
- Modificación de tratamientos
- Actualización de estados de pacientes

#### 5. 💿 Almacenamiento Compartido
Sistema centralizado protegido con:
- Semáforos para control de acceso
- Mutex para exclusión mutua
- Buffers circulares para colas
- Estructuras de datos thread-safe

## 🚀 Instalación

### Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Sistema operativo compatible: Linux, macOS, Windows

### Pasos de Instalación

```bash
# Clonar el repositorio
git clone https://github.com/Choflis/smart-hospital-systems.git

# Navegar al directorio del proyecto
cd smart-hospital-systems

# Crear un entorno virtual (recomendado)
python -m venv venv

# Activar el entorno virtual
# En Linux/macOS:
source venv/bin/activate
# En Windows:
venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

## 💻 Uso

### Ejecución Básica

```bash
# Ejecutar la simulación completa del sistema hospitalario
python main.py

# Ejecutar módulos individuales
python modules/producer.py
python modules/consumer.py
python modules/reader.py
python modules/writer.py
```

### Ejemplos de Uso

#### Ejemplo 1: Simulación de Registro de Pacientes

```python
from modules.producer import PatientProducer
from modules.shared_storage import HospitalStorage

# Crear almacenamiento compartido
storage = HospitalStorage(capacity=100)

# Crear productor de pacientes
producer = PatientProducer(storage)

# Generar registros de pacientes
producer.register_patient("Juan Pérez", "Consulta General")
producer.register_patient("María García", "Emergencia")
```

#### Ejemplo 2: Lectura Concurrente de Historiales

```python
from modules.reader import MedicalRecordReader
from modules.shared_storage import HospitalStorage

# Múltiples lectores pueden acceder simultáneamente
reader1 = MedicalRecordReader(storage, reader_id=1)
reader2 = MedicalRecordReader(storage, reader_id=2)

# Lectura concurrente sin bloqueos
record1 = reader1.read_medical_record(patient_id="12345")
record2 = reader2.read_medical_record(patient_id="67890")
```

#### Ejemplo 3: Actualización Segura con Escritores

```python
from modules.writer import MedicalRecordWriter
from modules.shared_storage import HospitalStorage

# Escritor tiene acceso exclusivo durante la actualización
writer = MedicalRecordWriter(storage)

# Actualización atómica de información crítica
writer.update_diagnosis(
    patient_id="12345",
    diagnosis="Hipertensión arterial",
    treatment="Enalapril 10mg"
)
```

## 🔧 Configuración

El sistema puede configurarse mediante el archivo `config.json`:

```json
{
  "storage": {
    "max_capacity": 1000,
    "buffer_size": 50
  },
  "synchronization": {
    "max_readers": 10,
    "semaphore_timeout": 30,
    "mutex_timeout": 10
  },
  "simulation": {
    "num_producers": 3,
    "num_consumers": 2,
    "num_readers": 5,
    "num_writers": 2,
    "simulation_time": 300
  }
}
```

## 📊 Estructura del Proyecto

```
smart-hospital-systems/
├── README.md
├── requirements.txt
├── config.json
├── main.py
├── modules/
│   ├── __init__.py
│   ├── producer.py          # Módulo productor
│   ├── consumer.py          # Módulo consumidor
│   ├── reader.py            # Módulo lector
│   ├── writer.py            # Módulo escritor
│   ├── shared_storage.py    # Almacenamiento compartido
│   └── synchronization.py   # Primitivas de sincronización
├── utils/
│   ├── __init__.py
│   ├── logger.py            # Sistema de logging
│   └── metrics.py           # Métricas de rendimiento
├── tests/
│   ├── __init__.py
│   ├── test_producer.py
│   ├── test_consumer.py
│   ├── test_reader.py
│   ├── test_writer.py
│   └── test_synchronization.py
└── docs/
    ├── architecture.md       # Documentación de arquitectura
    ├── api.md               # Documentación de API
    └── examples.md          # Ejemplos adicionales
```

## 🎓 Conceptos Educativos

Este proyecto es ideal para:

- **Estudiantes de Sistemas Operativos**: Comprender sincronización de procesos en un contexto real
- **Desarrolladores de Sistemas**: Aprender patrones de concurrencia aplicados
- **Profesionales de TI en Salud**: Entender requisitos de sistemas hospitalarios críticos
- **Investigadores**: Base para simulaciones de sistemas distribuidos

### 🧠 Problemas Clásicos Implementados

1. **Problema del Productor-Consumidor**
   - Cola de pacientes en espera
   - Buffer limitado para servicios

2. **Problema de Lectores-Escritores**
   - Múltiples doctores consultando historiales
   - Actualizaciones exclusivas de información crítica

3. **Problema de la Sección Crítica**
   - Actualización de recursos compartidos
   - Prevención de condiciones de carrera

## 📈 Métricas y Monitoreo

El sistema proporciona métricas en tiempo real:

- **Throughput**: Operaciones por segundo
- **Latencia**: Tiempo de respuesta promedio
- **Utilización**: Uso de recursos compartidos
- **Deadlock Detection**: Detección de bloqueos mutuos
- **Concurrencia**: Número de procesos activos

## 🧪 Testing

```bash
# Ejecutar todos los tests
python -m pytest tests/

# Ejecutar tests con cobertura
python -m pytest --cov=modules tests/

# Ejecutar tests específicos
python -m pytest tests/test_synchronization.py
```

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Por favor sigue estos pasos:

1. 🍴 Fork el proyecto
2. 🌿 Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. 💾 Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. 📤 Push a la rama (`git push origin feature/AmazingFeature`)
5. 🔀 Abre un Pull Request

### Guías de Contribución

- Sigue las convenciones de código PEP 8
- Añade tests para nuevas funcionalidades
- Actualiza la documentación según corresponda
- Asegura que todos los tests pasen antes de enviar PR

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 👥 Autores

- **Choflis** - *Desarrollo inicial* - [GitHub](https://github.com/Choflis)

## 🙏 Agradecimientos

- Inspirado en problemas clásicos de sistemas operativos
- Comunidad de Python por las excelentes bibliotecas de concurrencia
- Profesionales de la salud por sus insights sobre sistemas hospitalarios

## 📚 Referencias

- Tanenbaum, A. S. - *Modern Operating Systems*
- Silberschatz, A. - *Operating System Concepts*
- Python Threading Documentation
- Semaphore and Mutex Patterns

## 📞 Contacto

Para preguntas, sugerencias o colaboraciones:

- 📧 Email: [Crear issue en GitHub](https://github.com/Choflis/smart-hospital-systems/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/Choflis/smart-hospital-systems/discussions)

---

<div align="center">

**⭐ Si este proyecto te resulta útil, considera darle una estrella en GitHub ⭐**

Hecho con ❤️ para la comunidad de desarrollo y educación en sistemas operativos

</div>

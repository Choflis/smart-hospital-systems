# 🏥 Smart Hospital Systems - Sistema de Concurrencia

Sistema hospitalario que demuestra conceptos de **Sistemas Operativos** utilizando **concurrencia** en Python con **2 interfaces**: Terminal y GUI.

## 📋 Descripción

Este proyecto implementa un sistema hospitalario que simula:
- **Problema Productor-Consumidor**: Generación y atención de pacientes
- **Problema Lectores-Escritores**: Gestión de expedientes médicos
- **Sincronización con Threads**: Coordinación entre múltiples procesos

## 🚀 Características

### ✅ Concurrencia Implementada
- ✅ Semáforos manuales (sin usar `threading.Semaphore`)
- ✅ Locks para exclusión mutua
- ✅ Variables de condición
- ✅ Buffer circular con productores y consumidores
- ✅ Sistema de lectores-escritores para expedientes

### 🎯 Componentes del Sistema
1. **Productores** (Threads): Generan pacientes aleatoriamente
2. **Buffer**: Cola de espera con capacidad limitada (problema del buffer limitado)
3. **Consumidores/Médicos** (Threads): Atienden pacientes del buffer
4. **Sistema de Expedientes**: Almacenamiento con control de concurrencia (Lectores-Escritores)

### 🖥️ Interfaces Disponibles
- **Terminal UI**: Interfaz en consola con actualización en tiempo real
- **GUI (2 Ventanas)**: 
  - **Ventana 1**: Panel de Control con estadísticas y controles
  - **Ventana 2**: Visualización animada del flujo de datos

## 📁 Estructura del Proyecto

```
smart-hospital-systems/
├── core/                      # Lógica principal
│   ├── hospital.py           # Gestión del sistema hospitalario
│   ├── paciente.py           # Modelo de paciente
│   └── expedientes.py        # Sistema de expedientes (Lectores-Escritores)
├── concurrencia/             # Primitivas de concurrencia
│   ├── semaforo_manual.py    # Implementación de semáforo sin usar threading.Semaphore
│   └── buffer.py             # Buffer circular con sincronización
├── ui/                       # Interfaces de usuario
│   ├── terminal_ui.py        # Interfaz en terminal
│   └── gui_app.py           # Interfaz gráfica con 2 ventanas
├── data/                     # Datos persistentes
│   └── expedientes.json      # Expedientes médicos guardados
├── docs/                     # Documentación
│   └── explicacion_concurrencia.md
├── tests/                    # Pruebas
│   └── test_concurrencia.py
├── main.py                   # Punto de entrada
├── config.py                 # Configuración
└── requirements.txt          # Dependencias
```

## 🔧 Instalación

### Requisitos Previos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- tkinter (viene incluido con Python en Windows y Mac)

### Pasos de Instalación

1. **Clonar el repositorio**
```bash
git clone <url-del-repositorio>
cd smart-hospital-systems
```

2. **Crear entorno virtual** (recomendado)
```bash
python -m venv venv

# En Windows:
venv\Scripts\activate

# En Linux/Mac:
source venv/bin/activate
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

## 🎮 Uso

### 🖥️ Opción 1: Interfaz Gráfica (GUI) - RECOMENDADO

```bash
python main.py
```
o explícitamente:
```bash
python main.py --mode gui
```

Se abrirán **2 ventanas**:
1. **Panel de Control**: Controles, estadísticas, buffer visual, log de eventos
2. **Visualización de Flujo**: Diagrama animado del flujo de concurrencia

**Controles en el Panel:**
- ▶️ **INICIAR**: Inicia el sistema hospitalario
- ⏸️ **PAUSAR**: Pausa la simulación
- ⏹️ **DETENER**: Detiene completamente el sistema

### 📟 Opción 2: Interfaz de Terminal

```bash
python main.py --mode terminal
```

El sistema mostrará:
- Estado del buffer en tiempo real
- Pacientes siendo generados
- Médicos atendiendo pacientes
- Estadísticas de concurrencia
- Log de eventos

**Controles:**
- **ENTER**: Actualizar vista
- **Ctrl+C**: Detener el sistema de forma segura

### ⚙️ Opciones Avanzadas

```bash
# Cambiar tamaño del buffer
python main.py --buffer-size 10

# Cambiar número de productores
python main.py --productores 3

# Cambiar número de médicos
python main.py --medicos 5

# Combinación de opciones
python main.py --mode gui --buffer-size 8 --productores 3 --medicos 4
```

**Ayuda:**
```bash
python main.py --help
```

## 📊 Conceptos de Sistemas Operativos Demostrados

### 1. Problema Productor-Consumidor
- **Productores**: Threads que generan pacientes
- **Buffer limitado**: Cola de espera con capacidad máxima
- **Consumidores**: Médicos que atienden pacientes
- **Sincronización**: Semáforos para evitar condiciones de carrera

### 2. Problema Lectores-Escritores
- **Escritores**: Médicos registrando expedientes
- **Lectores**: Consultas de expedientes
- **Prioridad**: Los escritores tienen prioridad
- **Exclusión mutua**: Solo un escritor a la vez

### 3. Semáforos Manuales
Implementación propia sin usar `threading.Semaphore`:
```python
class SemaforoManual:
    def __init__(self, valor_inicial):
        self.valor = valor_inicial
        self.lock = threading.Lock()
        self.condition = threading.Condition(self.lock)
    
    def wait(self):
        with self.condition:
            while self.valor <= 0:
                self.condition.wait()
            self.valor -= 1
    
    def signal(self):
        with self.condition:
            self.valor += 1
            self.condition.notify()
```

## 🧪 Pruebas

Ejecutar pruebas de concurrencia:
```bash
python -m pytest tests/
```

## 📈 Ejemplos de Salida

### Terminal UI:
```
================================================================================
 🏥 SISTEMA HOSPITALARIO - MONITOR DE CONCURRENCIA
================================================================================

📦 BUFFER DE PACIENTES (3/5):
┌─────────┬─────────┬─────────┬─────────┬─────────┐
│ [👤]    │ [👤]    │ [👤]    │ [  ]    │ [  ]    │
└─────────┴─────────┴─────────┴─────────┴─────────┘

📊 ESTADÍSTICAS:
• Pacientes generados: 45
• Pacientes atendidos: 42
• En buffer: 3
• Expedientes registrados: 42

👥 PRODUCTORES:
🟢 Productor-1: 23 pacientes generados
🟢 Productor-2: 22 pacientes generados

🩺 MÉDICOS:
🟢 Dr. García: 15 pacientes atendidos
🟢 Dra. Martínez: 14 pacientes atendidos
🟢 Dr. López: 13 pacientes atendidos
```

### GUI:
- **Ventana 1 (Panel de Control)**: Muestra el buffer visual con cuadros de colores, botones interactivos, estadísticas en tiempo real
- **Ventana 2 (Visualización)**: Diagrama de flujo animado: Productores → Buffer → Médicos → Expedientes

## 🛠️ Tecnologías Utilizadas

- **Python 3.8+**: Lenguaje principal
- **threading**: Manejo de hilos
- **tkinter**: Interfaz gráfica (GUI)
- **dataclasses**: Modelado de datos
- **json**: Persistencia de expedientes
- **argparse**: Parsing de argumentos CLI
- **typing**: Type hints para mejor documentación

## 📝 Configuración

Editar `config.py` para modificar:
```python
# Configuración del buffer
CAPACIDAD_BUFFER = 5

# Número de threads
NUM_PRODUCTORES = 2
NUM_MEDICOS = 3

# Tiempos de simulación (segundos)
TIEMPO_GENERACION_MIN = 1
TIEMPO_GENERACION_MAX = 3
TIEMPO_ATENCION_MIN = 2
TIEMPO_ATENCION_MAX = 5
```

## 🎨 Capturas de Pantalla

### Interfaz Gráfica (GUI)
- Panel de Control con buffer visual
- Visualización animada del flujo de datos
- Estadísticas en tiempo real

### Interfaz de Terminal
- Vista en tiempo real con colores
- Buffer ASCII art
- Log de eventos

## 👥 Autores

- **Equipo de Desarrollo** - Proyecto de Sistemas Operativos

## 📄 Licencia

Este proyecto es de uso educativo para la asignatura de Sistemas Operativos.

## 🎓 Referencias

- Silberschatz, Galvin, Gagne - "Operating System Concepts"
- Tanenbaum - "Modern Operating Systems"
- Python Threading Documentation
- Python Tkinter Documentation

## 🚧 Roadmap

- [x] Interfaz de Terminal
- [x] Interfaz Gráfica (GUI) con 2 ventanas
- [x] Visualización animada del flujo
- [ ] Agregar gráficos de rendimiento
- [ ] Implementar algoritmo de planificación de CPU
- [ ] Agregar deadlock detection
- [ ] Dashboard web con Flask
- [ ] Métricas de rendimiento detalladas

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:
1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add: AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

---

⭐ Si te gusta este proyecto, no olvides darle una estrella!

## 📞 Contacto

Proyecto de Sistemas Operativos - Universidad

---

**¡Gracias por usar Smart Hospital Systems!** 🏥💙

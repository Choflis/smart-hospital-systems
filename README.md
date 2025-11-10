# 🏥 Smart Hospital Systems - Sistema de Concurrencia

Sistema hospitalario que demuestra conceptos de **Sistemas Operativos** utilizando **concurrencia** en Python con arquitectura **cliente-servidor** e **interfaces independientes**.

## 📋 Descripción

Este proyecto implementa un sistema hospitalario que simula:
- **Problema Productor-Consumidor**: Generación y atención de pacientes con buffer sincronizado
- **Problema Lectores-Escritores**: Gestión de expedientes médicos
- **Sincronización con Threads**: Coordinación entre múltiples procesos
- **Arquitectura Cliente-Servidor**: Comunicación entre procesos vía sockets
- **Interfaces Independientes**: Ventanas que pueden ejecutarse standalone

## 🏗️ Arquitectura

### Componentes Principales

1. **main.py** - Servidor Principal
   - Inicia hilos productores y consumidores
   - Gestiona buffer de pacientes y expedientes
   - Servidor de eventos para comunicación con interfaces

2. **panel_hospital.py** - Panel de Visualización
   - Interfaz gráfica independiente
   - Se conecta al servidor si está activo
   - Muestra logs y médicos en tiempo real
   - Actualización event-driven (no polling)

3. **registro_paciente.py** - Formulario de Registro
   - Interfaz gráfica independiente
   - Registra pacientes en el sistema
   - Modo demo si no hay conexión

## 🚀 Uso Rápido

### Sistema Completo

1. **Iniciar el servidor principal:**
   ```bash
   python main.py
   ```

2. **Abrir panel(es) de hospital (terminales separadas):**
   ```bash
   python ui/panel_hospital.py
   ```

3. **Abrir ventana(s) de registro (terminales separadas):**
   ```bash
   python ui/registro_paciente.py
   ```

✨ **Puedes abrir múltiples ventanas de cada tipo simultáneamente**

### Modo Independiente (Demo)

Las interfaces pueden ejecutarse sin el servidor:

```bash
python ui/panel_hospital.py      # Modo sin conexión
python ui/registro_paciente.py   # Modo demo
```

## ⚙️ Opciones de Configuración

```bash
python main.py --buffer-size 10 --productores 3 --medicos 5 --port 5555
```

**Opciones disponibles:**
- `--buffer-size N` - Capacidad del buffer (default: 5)
- `--productores N` - Número de productores (default: 2)
- `--medicos N` - Número de médicos (default: 3)
- `--port N` - Puerto del servidor (default: 5555)

## 🎯 Características Principales

### ✅ Concurrencia Implementada
- ✅ Semáforos manuales para buffer sincronizado
- ✅ Locks para exclusión mutua
- ✅ Problema Productor-Consumidor
- ✅ Sistema Lectores-Escritores para expedientes

### ✅ Arquitectura Cliente-Servidor
- ✅ Servidor de eventos basado en sockets
- ✅ Comunicación asíncrona mediante JSON
- ✅ Múltiples clientes simultáneos
- ✅ Actualizaciones en tiempo real (event-driven)

### ✅ Interfaces Independientes
- ✅ Ejecución standalone sin dependencias
- ✅ Conexión automática al servidor
- ✅ Modo demo cuando no hay servidor
- ✅ Múltiples ventanas sin interferencia

## 📊 Flujo de Datos

```
main.py (Servidor)
    ├── Productores (threads) → Generan pacientes
    ├── Buffer (sincronizado) → Cola de pacientes
    ├── Médicos (threads) → Consumen pacientes
    ├── Expedientes → Sistema Lectores-Escritores
    └── Event Server → Comunicación con UIs

panel_hospital.py (Cliente 1, 2, 3...)
    └── Socket → Recibe eventos en tiempo real

registro_paciente.py (Cliente 1, 2, 3...)
    └── Socket → Envía nuevos pacientes
```

## 📁 Estructura del Proyecto

```
smart-hospital-systems/
├── main.py                    # Servidor principal ⭐
├── core/
│   ├── hospital.py           # Lógica del hospital
│   ├── event_server.py       # Servidor de eventos ⭐
│   ├── paciente.py           # Modelo de paciente
│   └── __init__.py
├── concurrencia/
│   ├── buffer.py             # Buffer con semáforos
│   ├── productor.py          # Threads productores
│   ├── consumidor.py         # Threads médicos
│   ├── lector_escritor.py   # Sistema de expedientes
│   └── __init__.py
├── ui/
│   ├── panel_hospital.py     # Panel principal ⭐
│   ├── registro_paciente.py # Registro ⭐
│   ├── terminal_ui.py        # UI terminal (legacy)
│   └── gui_app.py            # GUI (legacy)
├── data/
│   └── logs/                 # Logs del sistema
├── docs/
│   └── ARQUITECTURA.md       # Documentación detallada
├── config.py                 # Configuraciones
└── requirements.txt          # Dependencias
```

## 🔧 Instalación

### Requisitos
- Python 3.8 o superior
- pip
- tkinter (incluido con Python)

### Pasos

1. **Clonar repositorio**
```bash
git clone <url>
cd smart-hospital-systems
```

2. **Crear entorno virtual** (opcional pero recomendado)
```bash
python -m venv venv

# Windows:
venv\Scripts\activate

# Linux/Mac:
source venv/bin/activate
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

## 📊 Conceptos de Sistemas Operativos

### 1. Problema Productor-Consumidor
- Productores generan pacientes
- Buffer limitado sincronizado con semáforos
- Médicos consumen pacientes del buffer

### 2. Problema Lectores-Escritores
- Expedientes médicos con control de concurrencia
- Múltiples lectores simultáneos
- Un solo escritor a la vez

### 3. Sincronización de Threads
- Locks para exclusión mutua
- Semáforos para control de capacidad
- Variables de condición

### 4. IPC (Inter-Process Communication)
- Comunicación vía sockets TCP
- Serialización JSON
- Event-driven architecture

## 💡 Ventajas de la Arquitectura

1. **Desacoplamiento**: Interfaces independientes del servidor
2. **Escalabilidad**: Múltiples clientes sin conflictos
3. **Eficiencia**: Actualizaciones event-driven
4. **Flexibilidad**: Modo demo cuando no hay servidor
5. **Modularidad**: Componentes independientes

## 🔍 Debugging

Los logs se guardan en:
```
data/logs/hospital.log
```

Ver logs en tiempo real:
```bash
# Windows PowerShell
Get-Content data\logs\hospital.log -Wait

# Linux/Mac
tail -f data/logs/hospital.log
```

## 📝 Notas Importantes

- El archivo `main_nuevas_interfaces.py` es legacy (renombrado a `.old`)
- Puerto por defecto: 5555 (configurable)
- Las interfaces manejan desconexiones automáticamente
- Múltiples ventanas funcionan sin interferencia
- Eventos se transmiten en tiempo real a todos los clientes

## 🛠️ Tecnologías

- **Python 3.8+**: Lenguaje principal
- **threading**: Manejo de hilos
- **socket**: Comunicación cliente-servidor
- **tkinter**: Interfaces gráficas
- **json**: Serialización de datos
- **logging**: Sistema de logs

## 👥 Autores

**Equipo de Desarrollo** - Proyecto de Sistemas Operativos 2025

## 📄 Licencia

Proyecto educativo para la asignatura de Sistemas Operativos.

## 🎓 Referencias

- Silberschatz, Galvin, Gagne - "Operating System Concepts"
- Tanenbaum - "Modern Operating Systems"
- Python Threading Documentation
- Python Socket Programming

## 📞 Documentación Adicional

Ver [docs/ARQUITECTURA.md](docs/ARQUITECTURA.md) para documentación detallada de la arquitectura.

---

⭐ **¡Sistema hospitalario con concurrencia real!** 🏥💙

**¡Gracias por usar Smart Hospital Systems!**

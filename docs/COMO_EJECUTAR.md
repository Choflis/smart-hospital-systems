# Guía de Ejecución - Sistema Hospitalario

## 🚀 Cómo Ejecutar el Proyecto

### 1. Requisitos Previos

- **Python 3.8 o superior**
- **Sistema Operativo**: Windows, Linux o macOS
- **Terminal/CMD**

### 2. Instalación

#### Opción A: Con entorno virtual (Recomendado)

```bash
# 1. Navegar al directorio del proyecto
cd smart-hospital-systems

# 2. Crear entorno virtual
python -m venv venv

# 3. Activar entorno virtual
# En Windows:
venv\Scripts\activate
# En Linux/macOS:
source venv/bin/activate

# 4. Instalar dependencias (si las hay)
pip install -r requirements.txt
```

#### Opción B: Sin entorno virtual

```bash
# Solo navegar al directorio
cd smart-hospital-systems

# Instalar dependencias (si las hay)
pip install -r requirements.txt
```

### 3. Ejecutar el Sistema

```bash
python main.py
```

### 4. Interactuar con el Sistema

1. **Al iniciar**: Verás la configuración del sistema
2. **Presiona ENTER**: Para comenzar la simulación
3. **Observa**: La interfaz se actualiza cada 2 segundos mostrando:
   - Pacientes en el buffer
   - Threads activos (productores y médicos)
   - Estadísticas de generación y atención
   - Expedientes registrados
4. **Detener**: Presiona `Ctrl+C` para detener de forma ordenada

## 📊 Salida Esperada

```
================================================================================
 🏥  SISTEMA HOSPITALARIO - GESTIÓN DE PACIENTES CON CONCURRENCIA
================================================================================
 📊 Demostra Concurrencia: Productor-Consumidor + Lectores-Escritores
================================================================================

⏰ Hora: 14:30:45

📦 BUFFER DE PACIENTES
   └─ Pacientes en buffer: 3/5

🔄 THREADS ACTIVOS
   ├─ Productores activos: 2/2
   └─ Médicos activos: 3/3

📈 ESTADÍSTICAS DE OPERACIÓN
   ├─ Pacientes generados: 25
   └─ Pacientes atendidos: 22

📄 EXPEDIENTES MÉDICOS
   ├─ Total registrados: 22
   ├─ Urgentes: 5
   ├─ Normales: 12
   └─ Baja prioridad: 5

👥 PRODUCTORES
   🟢 Productor-1: 13 pacientes generados
   🟢 Productor-2: 12 pacientes generados

🩺 MÉDICOS
   🟢 Dr. García: 8 pacientes atendidos
   🟢 Dra. Martínez: 7 pacientes atendidos
   🟢 Dr. López: 7 pacientes atendidos

================================================================================
 Presiona Ctrl+C para detener el sistema
================================================================================
```

## 🗂️ Archivos Generados

### 1. Expedientes Médicos
- **Ubicación**: `data/expedientes.json`
- **Formato**: JSON
- **Contenido**: Todos los pacientes atendidos

Ejemplo:
```json
{
  "expedientes": [
    {
      "id": 123456,
      "nombre": "Juan Pérez",
      "prioridad": 1,
      "diagnostico": "Fractura de brazo",
      "estado": "Atendido",
      "medico_asignado": "Dr. García",
      "tiempo_espera": 5.2
    }
  ]
}
```

### 2. Logs del Sistema
- **Ubicación**: `data/logs/hospital.log`
- **Formato**: Texto plano
- **Contenido**: Registro completo de todas las operaciones

Ejemplo:
```
2024-01-10 14:30:00 - Productor-1     - INFO     - 👤 Productor-1 generó: Juan Pérez (Prioridad: 1, ID: 123456)
2024-01-10 14:30:01 - Dr. García      - INFO     - 🩺 Dr. García atendiendo a Juan Pérez (ID: 123456, Prioridad: 1)
2024-01-10 14:30:05 - Dr. García      - INFO     - ✅ Dr. García completó atención de Juan Pérez en 4.0s
```

## ⚙️ Configuración Personalizada

### Modificar Parámetros

Edita el archivo `config.py`:

```python
# Configuración del buffer
BUFFER_CAPACITY = 5  # Cambiar capacidad del buffer

# Configuración de productores
NUM_PRODUCTORES = 2  # Cambiar número de productores
PRODUCTOR_INTERVALO_MIN = 2  # Intervalo mínimo de generación
PRODUCTOR_INTERVALO_MAX = 5  # Intervalo máximo de generación

# Configuración de médicos
NUM_MEDICOS = 3  # Cambiar número de médicos

# Configuración de UI
UI_REFRESH_INTERVAL = 2  # Intervalo de actualización de UI
```

O modificar directamente en `main.py`:

```python
hospital = Hospital(
    capacidad_buffer=10,    # Cambiar aquí
    num_productores=3,      # Cambiar aquí
    num_medicos=5           # Cambiar aquí
)
```

## 🐛 Solución de Problemas

### Problema: "ModuleNotFoundError"
**Solución**: Asegúrate de estar en el directorio correcto
```bash
cd smart-hospital-systems
python main.py
```

### Problema: "Permission denied" en data/
**Solución**: Crear directorios manualmente
```bash
mkdir -p data/logs
```

### Problema: El programa no se detiene con Ctrl+C
**Solución**: Presiona Ctrl+C dos veces o usa Ctrl+Break (Windows)

### Problema: Encoding errors en Windows
**Solución**: Ejecuta con codificación UTF-8
```bash
chcp 65001
python main.py
```

## 📝 Notas Importantes

1. ✅ **No requiere instalación de dependencias externas** (solo Python estándar)
2. ✅ **Los datos se guardan automáticamente** en `data/expedientes.json`
3. ✅ **Los logs se acumulan** en `data/logs/hospital.log`
4. ✅ **El sistema se detiene de forma ordenada** con Ctrl+C
5. ⚠️ **No cierres la terminal abruptamente** (usa Ctrl+C)

## 🎯 Casos de Uso Comunes

### Caso 1: Observar Productor-Consumidor
1. Ejecuta el sistema
2. Observa cómo el buffer se llena y vacía
3. Nota cuando productores esperan (buffer lleno)
4. Nota cuando médicos esperan (buffer vacío)

### Caso 2: Observar Lectores-Escritores
1. Revisa el archivo `data/logs/hospital.log`
2. Busca mensajes de "Escribiendo expediente"
3. Observa que no hay conflictos de escritura
4. Los expedientes se guardan correctamente

### Caso 3: Prueba de Estrés
1. Modifica `config.py`:
   ```python
   BUFFER_CAPACITY = 2  # Buffer pequeño
   NUM_PRODUCTORES = 5  # Muchos productores
   NUM_MEDICOS = 1      # Pocos consumidores
   ```
2. Observa cómo el buffer se satura
3. Productores esperarán frecuentemente

## 📚 Próximos Pasos

Después de ejecutar:
1. Revisa los logs en `data/logs/hospital.log`
2. Abre `data/expedientes.json` para ver expedientes
3. Lee `ARQUITECTURA.md` para entender el diseño
4. Lee `CONCURRENCIA.md` para teoría de sincronización
5. Experimenta modificando parámetros

## 🆘 Ayuda

Si tienes problemas:
1. Revisa que Python 3.8+ esté instalado: `python --version`
2. Verifica que estés en el directorio correcto
3. Lee los mensajes de error en la terminal
4. Revisa el archivo de log: `data/logs/hospital.log`

---

**¿Listo para empezar?** 🚀

```bash
python main.py
```

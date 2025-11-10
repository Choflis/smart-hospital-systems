# Guía Rápida - Smart Hospital System

## 🚀 Instalación y Configuración

### 1. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 2. Iniciar el servidor API
```bash
# Opción 1: Servidor local (solo esta computadora)
uvicorn api_server.main:app --reload

# Opción 2: Servidor en red (accesible desde otros dispositivos)
uvicorn api_server.main:app --host 0.0.0.0 --port 8000 --reload
```

### 3. Probar la API
```bash
# En otra terminal
python test_api.py
```

### 4. Ver documentación interactiva
Abre tu navegador en:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## Uso desde Múltiples Dispositivos

### Caso de Uso: Hospital con 3 terminales

#### Terminal 1: Recepción (Agregar Pacientes)
```python
import requests

# Agregar paciente
response = requests.post("http://192.168.1.100:8000/pacientes", json={
    "nombre": "Juan Pérez",
    "edad": 45,
    "genero": "Masculino",
    "sintomas": "Fiebre alta"
})
print(response.json())
```

#### Terminal 2: Médicos (Consultar y Diagnosticar)
```python
import requests

# Ver pacientes en espera
pacientes = requests.get("http://192.168.1.100:8000/pacientes").json()
print(f"Pacientes esperando: {pacientes['total']}")

# Agregar diagnóstico
requests.post("http://192.168.1.100:8000/diagnosticos", json={
    "paciente_id": "juan_perez",
    "medico_id": 1,
    "diagnostico": "Gripe común",
    "tratamiento": "Reposo"
})
```

#### Terminal 3: Estadísticas (Solo Lectura)
```python
import requests

# Obtener estadísticas en tiempo real
stats = requests.get("http://192.168.1.100:8000/estadisticas").json()
print(f"Pacientes en espera: {stats['reporte']['total_pacientes_espera']}")
print(f"Diagnósticos procesados: {stats['reporte']['diagnosticos_procesados']}")
```

---

## 🔧 Conceptos de SO Implementados

### 1. Productor-Consumidor
- **Buffer compartido** con capacidad limitada (10 pacientes)
- **Productores**: Personal de admisión agrega pacientes
- **Consumidores**: Médicos (3 hilos) atienden pacientes
- **Sincronización**: Locks protegen acceso concurrente

### 2. Lectores-Escritores
- **Lectores**: Departamento de estadísticas (pueden leer varios a la vez)
- **Escritores**: Dirección médica (acceso exclusivo para configuración)
- **Recurso compartido**: Base de datos de diagnósticos

### 3. Concurrencia
- Los médicos (consumidores) son **hilos separados**
- El buffer es **thread-safe** (usa locks de Python)
- Múltiples clientes API pueden acceder **simultáneamente**

---

## 📊 Arquitectura del Sistema

```
┌─────────────────────────────────────────────────┐
│          FASTAPI REST API (Puerto 8000)         │
│  ┌───────────────────────────────────────────┐  │
│  │      Buffer Compartido (Capacidad: 10)    │  │
│  └───────────────────────────────────────────┘  │
│         ↑                              ↓         │
│    Productores                   Consumidores    │
│   (Recepción)                    (3 Médicos)     │
└─────────────────────────────────────────────────┘
         ↑                                ↓
    Dispositivo 1               Dispositivos 2, 3, 4
   (Agregar datos)              (Leer estadísticas)
```

---

## 💡 Ejemplos Prácticos

### Simular alta carga de pacientes
```bash
# Agregar 5 pacientes rápidamente
for i in {1..5}; do
  curl -X POST http://localhost:8000/pacientes \
    -H "Content-Type: application/json" \
    -d "{\"nombre\":\"Paciente $i\",\"edad\":30,\"genero\":\"Otro\",\"sintomas\":\"Test\"}"
done
```

### Monitorear sistema en tiempo real
```bash
# Ver estado cada 2 segundos
watch -n 2 'curl -s http://localhost:8000/estadisticas | jq .reporte'
```

---

## 🐛 Solución de Problemas

### Error: "Cannot connect to API"
- Verifica que el servidor esté corriendo
- Verifica el firewall (debe permitir puerto 8000)

### Error: "Buffer lleno"
- Los médicos están atendiendo pacientes (espera unos segundos)
- Aumenta la capacidad del buffer en `api_server/main.py`

### Error: "Import errors"
- Ejecuta: `pip install -r requirements.txt`
- Verifica que estés en el directorio correcto

---

## 📝 Notas del Proyecto

Este sistema demuestra:
- ✅ Sincronización de procesos concurrentes
- ✅ Protección de recursos compartidos
- ✅ Prevención de condiciones de carrera
- ✅ Comunicación entre dispositivos via API REST
- ✅ Modelos clásicos de SO (Productor-Consumidor, Lectores-Escritores)

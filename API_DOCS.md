# Documentación de la API - Smart Hospital System

## 🚀 Iniciar el Servidor API

Para iniciar el servidor API que permite conectar múltiples dispositivos:

```bash
# Desde la raíz del proyecto
uvicorn api_server.main:app --host 0.0.0.0 --port 8000 --reload
```

**Parámetros importantes:**
- `--host 0.0.0.0`: Permite conexiones desde otros dispositivos en la red
- `--port 8000`: Puerto donde escucha el servidor
- `--reload`: Reinicia automáticamente al detectar cambios (desarrollo)

## 📱 Conectar desde Otros Dispositivos

1. Encuentra la IP de tu computadora:
   - Windows: `ipconfig` (busca IPv4)
   - Linux/Mac: `ifconfig` o `ip addr`

2. Accede desde otros dispositivos usando: `http://TU_IP:8000`
   - Ejemplo: `http://192.168.1.100:8000`

3. Documentación interactiva:
   - Swagger UI: `http://TU_IP:8000/docs`
   - ReDoc: `http://TU_IP:8000/redoc`

## 🔌 Endpoints Disponibles

### 1. Estado del Sistema
```
GET /
```
Devuelve el estado general del sistema hospitalario.

**Respuesta:**
```json
{
  "message": "Servidor Smart Hospital activo",
  "pacientes_en_espera": 3,
  "medicos_activos": 3,
  "timestamp": "2024-01-15 10:30:00"
}
```

---

### 2. Gestión de Pacientes (Buffer Compartido)

#### Listar Pacientes en Espera
```
GET /pacientes
```

**Respuesta:**
```json
{
  "total": 2,
  "capacidad": 10,
  "pacientes": [
    {
      "nombre": "Juan Pérez",
      "edad": 45,
      "genero": "Masculino",
      "sintomas": "Fiebre alta",
      "timestamp": "2024-01-15 10:15:00"
    }
  ]
}
```

#### Agregar Nuevo Paciente
```
POST /pacientes
Content-Type: application/json

{
  "nombre": "María García",
  "edad": 32,
  "genero": "Femenino",
  "sintomas": "Dolor de cabeza intenso"
}
```

**Respuesta:**
```json
{
  "status": "ok",
  "mensaje": "Paciente 'María García' agregado correctamente",
  "paciente": { ... }
}
```

#### Estado del Buffer
```
GET /pacientes/estado
```

**Respuesta:**
```json
{
  "vacio": false,
  "lleno": false,
  "cantidad": 3,
  "capacidad": 10
}
```

---

### 3. Diagnósticos (Modelo Productor-Consumidor)

#### Listar Diagnósticos
```
GET /diagnosticos
```

#### Agregar Diagnóstico (Médicos)
```
POST /diagnosticos
Content-Type: application/json

{
  "paciente_id": "pac_001",
  "medico_id": 1,
  "diagnostico": "Gripe común",
  "tratamiento": "Reposo y antipiréticos"
}
```

#### Procesar Diagnóstico (Laboratorio)
```
PUT /diagnosticos/{id}/procesar
```

---

### 4. Estadísticas (Modelo Lectores-Escritores)

#### Obtener Reporte Actual
```
GET /estadisticas
```

**Respuesta:**
```json
{
  "status": "ok",
  "reporte": {
    "total_pacientes_espera": 5,
    "total_diagnosticos": 12,
    "diagnosticos_procesados": 8,
    "diagnosticos_pendientes": 4,
    "medicos_activos": 3,
    "capacidad_buffer": 10,
    "fecha": "2024-01-15 10:30:00"
  }
}
```

#### Historial de Reportes
```
GET /estadisticas/historico
```

---

### 5. Médicos

#### Listar Médicos Activos
```
GET /medicos
```

**Respuesta:**
```json
{
  "total": 3,
  "medicos": [
    {"id": 0, "activo": true},
    {"id": 1, "activo": true},
    {"id": 2, "activo": true}
  ]
}
```

---

### 6. Configuración (Dirección Médica - Escritor Exclusivo)

#### Actualizar Configuración
```
POST /configuracion
Content-Type: application/json

{
  "capacidad_buffer": 15,
  "tiempo_atencion": 120
}
```

---

## 💡 Ejemplo de Uso - Flujo Completo

### 1. Doctor agrega paciente desde su dispositivo:
```bash
curl -X POST http://192.168.1.100:8000/pacientes \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Carlos López",
    "edad": 28,
    "genero": "Masculino",
    "sintomas": "Dolor abdominal"
  }'
```

### 2. Médico revisa pacientes en espera:
```bash
curl http://192.168.1.100:8000/pacientes
```

### 3. Laboratorio consulta estadísticas:
```bash
curl http://192.168.1.100:8000/estadisticas
```

### 4. Médico agrega diagnóstico:
```bash
curl -X POST http://192.168.1.100:8000/diagnosticos \
  -H "Content-Type: application/json" \
  -d '{
    "paciente_id": "carlos_lopez",
    "medico_id": 1,
    "diagnostico": "Gastritis aguda",
    "tratamiento": "Omeprazol 20mg cada 12h"
  }'
```

### 5. Laboratorio procesa diagnóstico:
```bash
curl -X PUT http://192.168.1.100:8000/diagnosticos/0/procesar
```

---

## 🔐 Conceptos de Sistemas Operativos Implementados

### Productor-Consumidor
- **Productores**: Personal de admisión/doctores agregan pacientes
- **Buffer**: Cola compartida (capacidad limitada)
- **Consumidores**: Médicos atienden pacientes del buffer

### Lectores-Escritores
- **Lectores**: Departamento de estadísticas consulta datos (concurrente)
- **Escritores**: Dirección médica actualiza configuración (exclusivo)
- **Recurso compartido**: Base de datos de diagnósticos y configuración

### Sincronización
- **Locks**: Protegen el acceso al buffer compartido
- **Thread-safe**: Todos los endpoints son seguros para acceso concurrente
- **Estado compartido**: Todos los dispositivos ven la misma información en tiempo real

---

## 🧪 Probar la API

Ejecuta estos comandos para probar que todo funciona:

```bash
# 1. Verificar estado del sistema
curl http://localhost:8000/

# 2. Agregar un paciente de prueba
curl -X POST http://localhost:8000/pacientes \
  -H "Content-Type: application/json" \
  -d '{"nombre":"Test","edad":30,"genero":"Masculino","sintomas":"Prueba"}'

# 3. Ver pacientes
curl http://localhost:8000/pacientes

# 4. Ver estadísticas
curl http://localhost:8000/estadisticas
```

---

## 📊 Integración con la UI

La UI del proyecto puede conectarse a esta API para mostrar datos en tiempo real desde múltiples dispositivos. Los médicos, laboratorio y estadísticas verán la misma información sincronizada.

# 🏥 Nuevas Interfaces Gráficas del Sistema Hospitalario

## 📋 Descripción

Se han implementado **dos interfaces gráficas complementarias** para el sistema de gestión hospitalaria:

### 1️⃣ **Ventana de Registro de Pacientes**
Formulario completo para registrar nuevos pacientes en el sistema.

### 2️⃣ **Panel Principal del Hospital**
Visualización en tiempo real de médicos, pacientes y logs del sistema.

---

## 🎨 Características de las Interfaces

### 📝 Ventana de Registro de Pacientes

**Campos del formulario:**
- ✅ Nombre
- ✅ Apellidos
- ✅ DNI
- ✅ Número telefónico
- ✅ Edad
- ✅ Género (Masculino / Femenino / Otro)
- ✅ Síntomas (área de texto)
- ✅ Doctor asignado (menú desplegable)

**Funcionalidades:**
- ✅ Validación completa de campos
- ✅ Botón "Registrar Paciente" → envía datos al sistema
- ✅ Botón "Limpiar Formulario" → resetea campos
- ✅ Contador de pacientes registrados
- ✅ Mensajes de confirmación
- ✅ Actualización automática del panel principal

**Salida:**
- Consola: Imprime datos detallados del paciente
- Panel principal: Actualiza la lista de médicos y pacientes

---

### 🏥 Panel Principal del Hospital

**Distribución:**
```
┌─────────────────────────────────────────────────────────┐
│              🏥 PANEL PRINCIPAL DEL HOSPITAL            │
├──────────┬──────────────────────────────────────────────┤
│          │                                              │
│ CONSOLA  │        MÉDICOS Y PACIENTES                  │
│   DE     │                                              │
│  LOGS    │  ┌────────────────────────────────┐         │
│  (15%)   │  │ 👨‍⚕️ Dr. García                │         │
│          │  │ Pacientes: 2                   │         │
│ [logs    │  │ ● Disponible                   │         │
│  en      │  ├────────────────────────────────┤         │
│  tiempo  │  │ 👤 Juan Pérez                  │         │
│  real]   │  │ DNI: 12345678                  │         │
│          │  │ Edad: 45 años                  │         │
│          │  │ 📅 Registro: 2024-01-10 10:30  │         │
│          │  │ 🔔 En espera                   │         │
│          │  └────────────────────────────────┘         │
│          │                                              │
└──────────┴──────────────────────────────────────────────┘
```

**Sección Izquierda (15%):** Consola de Logs
- 📋 Eventos en tiempo real
- 🕐 Timestamp de cada evento
- 🎨 Colores según tipo de log:
  - 🔵 Info (azul)
  - 🟢 Success (verde)
  - 🟡 Warning (amarillo)
  - 🔴 Error (rojo)

**Ejemplos de logs:**
```
[10:30:15] Paciente Juan Pérez registrado
[10:30:15] Asignado a Dr. García
[10:31:22] Paciente Ana Torres registrado
[10:31:22] Asignado a Dra. Martínez
```

**Sección Derecha (85%):** Médicos y Pacientes
- 👨‍⚕️ Lista de médicos con sus datos
- 📊 Contador de pacientes por médico
- 🔔 Estado del médico (Libre / Disponible / Ocupado)
- 🎴 Tarjetas de pacientes con:
  - Nombre completo
  - DNI
  - Edad
  - Fecha y hora de registro
  - Estado (En espera / En atención / Atendido)
- 🔄 Actualización automática cada 2 segundos

---

## 🚀 Cómo Ejecutar

### Opción 1: Comando Rápido
```bash
python main_nuevas_interfaces.py
```

### Opción 2: Desde el directorio ui
```bash
cd ui
python ../main_nuevas_interfaces.py
```

---

## 📦 Estructura de Archivos Nuevos

```
smart-hospital-systems/
├── ui/
│   ├── registro_paciente.py      # Nueva: Ventana de registro
│   └── panel_hospital.py          # Nueva: Panel principal
├── main_nuevas_interfaces.py      # Nueva: Punto de entrada
└── docs/
    └── NUEVAS_INTERFACES.md       # Este archivo
```

---

## 🎯 Flujo de Uso

1. **Ejecutar la aplicación**
   ```bash
   python main_nuevas_interfaces.py
   ```

2. **Se abren 2 ventanas:**
   - Ventana 1: Registro de Pacientes
   - Ventana 2: Panel Principal del Hospital

3. **Registrar un paciente:**
   - Completar formulario en Ventana 1
   - Seleccionar doctor del menú desplegable
   - Click en "Registrar Paciente"

4. **Observar cambios:**
   - Consola del sistema: Muestra datos detallados
   - Panel Principal: Actualiza lista de médicos
   - Logs: Registra el evento en tiempo real

5. **Registrar más pacientes:**
   - Los datos se acumulan
   - El contador aumenta
   - El panel se actualiza automáticamente

---

## 💡 Ejemplos de Uso

### Ejemplo 1: Registrar Paciente de Urgencia

**Formulario:**
```
Nombre: Carlos
Apellidos: Rodríguez
DNI: 12345678
Teléfono: 987654321
Edad: 28
Género: Masculino
Síntomas: Dolor de pecho agudo, dificultad para respirar
Doctor: Dr. García
```

**Resultado en consola:**
```
============================================================
✅ NUEVO PACIENTE REGISTRADO
============================================================
ID: 834567
Nombre: Carlos Rodríguez
DNI: 12345678
Teléfono: 987654321
Edad: 28 años
Género: Masculino
Síntomas: Dolor de pecho agudo, dificultad para respirar
Doctor asignado: Dr. García
Fecha de registro: 2024-01-10 10:30:45
============================================================
```

**Resultado en Panel Principal:**
- Log: `[10:30:45] Paciente Carlos Rodríguez registrado`
- Log: `[10:30:45] Asignado a Dr. García`
- Tarjeta del paciente aparece en el bloque del Dr. García

---

## 🎨 Diseño Visual

### Colores Utilizados

| Elemento | Color | Uso |
|----------|-------|-----|
| Encabezado | `#3498db` | Azul - Título de registro |
| Encabezado Panel | `#2c3e50` | Gris oscuro - Panel principal |
| Consola Logs | `#1c2833` | Negro - Fondo de logs |
| Botón Registrar | `#27ae60` | Verde - Acción principal |
| Botón Limpiar | `#e67e22` | Naranja - Acción secundaria |
| Estado Libre | `#27ae60` | Verde - Médico sin pacientes |
| Estado Disponible | `#f39c12` | Amarillo - Médico con pocos pacientes |
| Estado Ocupado | `#e74c3c` | Rojo - Médico con muchos pacientes |

### Tipografía
- **Encabezados**: Arial Bold, 18-22pt
- **Etiquetas**: Arial Bold, 11pt
- **Campos**: Arial Regular, 10pt
- **Logs**: Consolas, 9pt (monoespaciada)

---

## 🔄 Sincronización en Tiempo Real

### ¿Cómo funciona?

1. **Registro de paciente** (Ventana 1)
   - Se valida el formulario
   - Se crea objeto `paciente_data`
   - Se imprime en consola
   - Se llama a `panel_hospital.agregar_paciente()`

2. **Actualización del panel** (Ventana 2)
   - Se recibe `paciente_data`
   - Se agrega al médico correspondiente
   - Se registra en logs
   - Se redibuja la lista de médicos

3. **Actualización automática**
   - Thread en background actualiza cada 2 segundos
   - Redibuja bloques de médicos
   - Mantiene sincronización con el sistema

---

## 🧪 Probar el Sistema

### Test 1: Registrar múltiples pacientes
```python
# Registrar 3 pacientes con diferentes doctores
Paciente 1 → Dr. García
Paciente 2 → Dra. Martínez  
Paciente 3 → Dr. López

# Resultado esperado:
# - Panel muestra 1 paciente por médico
# - 6 líneas en logs (3 registros + 3 asignaciones)
```

### Test 2: Sobrecargar un médico
```python
# Registrar 5 pacientes con el mismo doctor
Paciente 1-5 → Dr. García

# Resultado esperado:
# - Estado del Dr. García cambia a "Ocupado"
# - Color del estado cambia a rojo
# - Contador muestra "Pacientes asignados: 5"
```

### Test 3: Validación de formulario
```python
# Intentar registrar sin completar campos
Campo "Nombre" vacío → Error: "Por favor ingrese el nombre"
Campo "Edad" = "abc" → Error: "La edad debe ser un número"
Campo "Edad" = 200 → Error: "Edad inválida"
```

---

## 📊 Datos del Paciente

### Estructura del objeto `paciente_data`:
```python
{
    'id': 834567,
    'nombre': 'Carlos Rodríguez',
    'dni': '12345678',
    'telefono': '987654321',
    'edad': 28,
    'genero': 'Masculino',
    'sintomas': 'Dolor de pecho agudo, dificultad para respirar',
    'doctor_asignado': 'Dr. García',
    'fecha_registro': '2024-01-10 10:30:45',
    'estado': 'En espera'
}
```

---

## 🐛 Solución de Problemas

### Problema: Las ventanas no aparecen
**Solución:**
```bash
# Verificar que tkinter esté instalado
python -m tkinter

# Si aparece una ventana, tkinter está instalado correctamente
```

### Problema: Error "No module named 'core'"
**Solución:**
```bash
# Ejecutar desde el directorio raíz del proyecto
cd smart-hospital-systems
python main_nuevas_interfaces.py
```

### Problema: Los datos no se actualizan en el panel
**Solución:**
- Verificar que ambas ventanas estén abiertas
- Esperar 2 segundos para la actualización automática
- Revisar logs en la consola del sistema

---

## 📝 Notas Técnicas

### Threading
- El panel principal usa un thread de actualización
- Se ejecuta cada 2 segundos
- Es un daemon thread (se cierra con la aplicación)

### Validaciones
- Todos los campos son obligatorios
- Edad debe ser número entre 0 y 150
- DNI y teléfono son campos de texto libre

### Persistencia
- Los datos se mantienen en memoria durante la sesión
- Al cerrar la aplicación se pierden los datos
- Para persistencia: integrar con el sistema de expedientes existente

---

## 🚀 Mejoras Futuras

- [ ] Persistencia en base de datos
- [ ] Búsqueda de pacientes
- [ ] Edición de datos de pacientes
- [ ] Filtros por estado
- [ ] Exportar a PDF/Excel
- [ ] Notificaciones sonoras
- [ ] Gráficos estadísticos
- [ ] Modo oscuro
- [ ] Multi-idioma

---

## 📸 Capturas de Pantalla

### Ventana de Registro
```
┌─────────────────────────────────────┐
│     📋 REGISTRO DE PACIENTES        │
├─────────────────────────────────────┤
│ Nombre:      [_______________]      │
│ Apellidos:   [_______________]      │
│ DNI:         [_______________]      │
│ Teléfono:    [_______________]      │
│ Edad:        [_______________]      │
│ Género:      ○ M  ○ F  ○ Otro       │
│ Síntomas:    [_______________]      │
│              [_______________]      │
│ Doctor:      [Dr. García    ▼]      │
│                                     │
│  [✅ REGISTRAR]  [🔄 LIMPIAR]       │
│                                     │
│    Pacientes registrados: 5         │
└─────────────────────────────────────┘
```

---

## 👥 Créditos

Desarrollado como extensión del **Sistema Hospitalario de Concurrencia**  
Proyecto de Sistemas Operativos - 2024

---

**¡Disfruta del sistema hospitalario!** 🏥💙

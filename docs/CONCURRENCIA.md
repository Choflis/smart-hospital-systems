# Concurrencia en el Sistema Hospitalario

## 🧵 Introducción a la Concurrencia

Este proyecto implementa dos problemas clásicos de sincronización en sistemas operativos:
1. **Productor-Consumidor** (Buffer de pacientes)
2. **Lectores-Escritores** (Sistema de expedientes)

## 1️⃣ Problema Productor-Consumidor

### 📖 Descripción del Problema

- **Productores**: Threads que generan pacientes
- **Consumidores**: Threads (médicos) que atienden pacientes
- **Buffer compartido**: Espacio limitado para almacenar pacientes temporalmente

### 🎯 Objetivos

1. Productores no pueden agregar si el buffer está lleno
2. Consumidores no pueden extraer si el buffer está vacío
3. Solo un thread puede modificar el buffer a la vez (exclusión mutua)

### 🔧 Implementación con Semáforos

```python
class BufferPacientes:
    def __init__(self, capacidad):
        self.buffer = []
        self.capacidad = capacidad
        
        # Semáforos
        self.mutex = threading.Lock()           # Exclusión mutua
        self.empty = threading.Semaphore(capacidad)  # Espacios vacíos
        self.full = threading.Semaphore(0)      # Elementos disponibles
```

#### Operación PRODUCTOR (agregar paciente)

```python
def agregar(self, paciente):
    # 1. Esperar a que haya espacio disponible
    self.empty.acquire()  # Decrementa empty
    
    # 2. Sección crítica (exclusión mutua)
    with self.mutex:
        self.buffer.append(paciente)
        # Solo este thread puede estar aquí
    
    # 3. Señalar que hay un elemento disponible
    self.full.release()  # Incrementa full
```

**Explicación paso a paso:**
1. `empty.acquire()`: Si empty = 0 (buffer lleno), el thread se bloquea y espera
2. `mutex.acquire()`: Garantiza que solo un thread modifique el buffer
3. `buffer.append()`: Agrega el paciente al buffer
4. `mutex.release()`: Libera el acceso al buffer
5. `full.release()`: Incrementa full para indicar que hay un elemento más

#### Operación CONSUMIDOR (extraer paciente)

```python
def extraer(self):
    # 1. Esperar a que haya elementos disponibles
    self.full.acquire()  # Decrementa full
    
    # 2. Sección crítica (exclusión mutua)
    with self.mutex:
        paciente = self.buffer.pop(0)
        # Solo este thread puede estar aquí
    
    # 3. Señalar que hay un espacio disponible
    self.empty.release()  # Incrementa empty
    
    return paciente
```

**Explicación paso a paso:**
1. `full.acquire()`: Si full = 0 (buffer vacío), el thread se bloquea y espera
2. `mutex.acquire()`: Garantiza que solo un thread modifique el buffer
3. `buffer.pop(0)`: Extrae el primer paciente del buffer
4. `mutex.release()`: Libera el acceso al buffer
5. `empty.release()`: Incrementa empty para indicar que hay un espacio más

### 📊 Ejemplo de Ejecución

```
Estado inicial: Buffer capacidad = 3
empty = 3 (3 espacios libres)
full = 0 (0 elementos)
buffer = []

Thread P1 (Productor): agregar paciente A
├─ empty.acquire() → empty = 2
├─ mutex.acquire()
├─ buffer.append(A) → buffer = [A]
├─ mutex.release()
└─ full.release() → full = 1

Thread C1 (Consumidor): extraer paciente
├─ full.acquire() → full = 0
├─ mutex.acquire()
├─ x = buffer.pop(0) → buffer = [], x = A
├─ mutex.release()
└─ empty.release() → empty = 3
```

### ⚠️ Problemas Evitados

#### Sin sincronización:
```python
# Thread 1: agregar("Paciente A")
# Thread 2: agregar("Paciente B")
# Ambos leen len(buffer) = 0 simultáneamente
# Ambos escriben en buffer[0]
# Resultado: Se pierde un paciente ❌
```

#### Con sincronización:
```python
# Thread 1: agregar("Paciente A")
#   mutex.acquire() ✅
#   ... agrega A ...
#   mutex.release()
# Thread 2: agregar("Paciente B")
#   mutex.acquire() ⏸️ (espera a Thread 1)
#   ... agrega B ...
#   mutex.release()
# Resultado: Ambos pacientes agregados correctamente ✅
```

## 2️⃣ Problema Lectores-Escritores

### 📖 Descripción del Problema

- **Lectores**: Threads que leen expedientes médicos
- **Escritores**: Threads (médicos) que escriben expedientes
- **Recurso compartido**: Archivo JSON con expedientes

### 🎯 Objetivos

1. Múltiples lectores pueden leer simultáneamente
2. Solo un escritor puede escribir a la vez
3. Si hay un escritor, no puede haber lectores
4. Si hay lectores, no puede haber escritores

### 🔧 Implementación

```python
class SistemaExpedientes:
    def __init__(self):
        self.lectores = 0  # Contador de lectores activos
        self.mutex = threading.Lock()  # Protege contador de lectores
        self.escritor_lock = threading.Lock()  # Exclusión mutua para escritores
```

#### Operación LECTOR (leer expediente)

```python
def leer_expediente(self, id):
    # ENTRADA
    self.mutex.acquire()
    self.lectores += 1
    if self.lectores == 1:  # Primer lector
        self.escritor_lock.acquire()  # Bloquea escritores
    self.mutex.release()
    
    # LEER (sección crítica compartida con otros lectores)
    with open(self.archivo, 'r') as f:
        data = json.load(f)
        # Múltiples lectores pueden estar aquí simultáneamente
    
    # SALIDA
    self.mutex.acquire()
    self.lectores -= 1
    if self.lectores == 0:  # Último lector
        self.escritor_lock.release()  # Libera escritores
    self.mutex.release()
```

**Explicación:**
- El **primer lector** bloquea a los escritores
- Mientras haya lectores, los escritores esperan
- El **último lector** desbloquea a los escritores
- Múltiples lectores pueden leer simultáneamente

#### Operación ESCRITOR (escribir expediente)

```python
def escribir_expediente(self, paciente):
    # Adquirir lock de escritor (exclusión total)
    self.escritor_lock.acquire()
    
    # ESCRIBIR (exclusión total)
    with open(self.archivo, 'r') as f:
        data = json.load(f)
    
    data['expedientes'].append(paciente.to_dict())
    
    with open(self.archivo, 'w') as f:
        json.dump(data, f)
    
    # Liberar lock de escritor
    self.escritor_lock.release()
```

**Explicación:**
- El escritor adquiere `escritor_lock`
- Si hay lectores, espera a que terminen
- Si hay otro escritor, espera a que termine
- Una vez que escribe, libera el lock

### 📊 Ejemplo de Ejecución

```
Estado inicial:
lectores = 0
escritor_lock = libre

Thread L1 (Lector): leer expediente 123
├─ mutex.acquire()
├─ lectores++ → lectores = 1
├─ escritor_lock.acquire() ✅ (primer lector bloquea escritores)
├─ mutex.release()
├─ ... leyendo ... 📖
├─ mutex.acquire()
├─ lectores-- → lectores = 0
├─ escritor_lock.release() ✅ (último lector libera escritores)
└─ mutex.release()

Thread L2 (Lector): leer expediente 456 (simultáneamente con L1)
├─ mutex.acquire()
├─ lectores++ → lectores = 2
├─ (NO adquiere escritor_lock porque ya está adquirido)
├─ mutex.release()
├─ ... leyendo ... 📖 (al mismo tiempo que L1)
├─ mutex.acquire()
├─ lectores-- → lectores = 1
├─ (NO libera escritor_lock porque aún hay lectores)
└─ mutex.release()

Thread E1 (Escritor): escribir expediente paciente
├─ escritor_lock.acquire() ⏸️ (espera a que lectores = 0)
├─ ... (L1 y L2 terminan, lectores = 0)
├─ escritor_lock.acquire() ✅ (ahora puede escribir)
├─ ... escribiendo ... ✍️
└─ escritor_lock.release() ✅
```

### ⚠️ Problemas Evitados

#### Sin sincronización:
```python
# Thread L: leyendo archivo
# Thread E: escribiendo archivo
# Resultado: Datos corruptos ❌
```

#### Con sincronización:
```python
# Thread L1: leyendo ✅
# Thread L2: leyendo ✅ (simultáneamente con L1)
# Thread E: esperando ⏸️
# ... L1 y L2 terminan ...
# Thread E: escribiendo ✅ (ahora puede escribir)
```

## 🔍 Conceptos Clave

### Semáforo
- Contador entero no negativo
- `acquire()`: Decrementa y espera si es 0
- `release()`: Incrementa y despierta threads

### Mutex (Lock)
- Semáforo binario (0 o 1)
- Garantiza exclusión mutua
- Solo un thread en sección crítica

### Sección Crítica
- Código que accede a recurso compartido
- Debe estar protegida con mutex

### Deadlock
- Situación donde threads esperan indefinidamente
- Prevención: Orden consistente de adquisición de locks

### Starvation
- Thread nunca obtiene recurso
- Mitigación: Prioridades, fairness

## 📈 Ventajas de la Implementación

✅ **Productor-Consumidor**:
- Desacoplamiento entre productores y consumidores
- Buffer actúa como amortiguador
- Productores y consumidores trabajan a su propio ritmo

✅ **Lectores-Escritores**:
- Múltiples lecturas simultáneas (mejor rendimiento)
- Escrituras seguras y consistentes
- Previene corrupción de datos

## 🧪 Verificación de Sincronización

### Para verificar que funciona:

1. **Revisa los logs**: Busca concurrencia real
```
14:30:01 - Productor-1 - generó paciente 123
14:30:01 - Productor-2 - generó paciente 124  # ← Simultáneo
14:30:02 - Dr. García - atendiendo 123
14:30:02 - Dra. Martínez - atendiendo 124    # ← Simultáneo
```

2. **Observa el buffer**: Debe llenarse y vaciarse
3. **Verifica expedientes**: No debe haber corrupción
4. **Prueba con muchos threads**: Debe seguir funcionando

## 📚 Referencias Teóricas

- **Dijkstra, E. W.** - "Cooperating Sequential Processes" (1965)
- **Courtois, P. J., et al.** - "Concurrent Control with Readers and Writers" (1971)
- **Tanenbaum, A. S.** - "Modern Operating Systems"
- **Silberschatz, A., et al.** - "Operating System Concepts"

---

**Este sistema demuestra concurrencia real con sincronización apropiada** 🎯

# Simulación de Concurrencia en un Hospital Digital
![Banner](https://www.python.org/static/community_logos/python-logo-master-v3-TM.png)

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![Estado](https://img.shields.io/badge/Estado-Prototipo-green)](https://github.com/Choflis/smart-hospital-systems)

---

Índice
- Descripción general
- Objetivos
- Características y motivación
- Estructura del proyecto
- Arquitectura y diagramas
- Explicación de los módulos
- Modelos teóricos aplicados
- Técnicas de sincronización y prevención de fallos
- Ejecución y ejemplos de salida
- Pruebas y validación
- Conclusiones
- Recursos e imágenes

---

Descripción general
-------------------
Esta entrega contiene el README del proyecto: "Simulación de procesos concurrentes en un sistema hospitalario digital". La simulación representa actores típicos de un entorno hospitalario digital (productores de eventos, consumidores/servicios, lectores de historiales y escritores que actualizan expedientes) y demuestra, de forma práctica, cómo se usan los conceptos de Sistemas Operativos —concurrencia, sincronización, semáforos, mutex, procesos/hilos y recursos compartidos— para garantizar integridad y coherencia de datos.

El proyecto está pensado como una herramienta didáctica y demostrativa: reproduce contenciones reales sobre un recurso compartido (un archivo JSON que actúa como base de datos simulada) usando primitivos de Python (threading / multiprocessing) y protocolos clásicos (Productor–Consumidor, Lectores–Escritores).

Objetivos
---------
Objetivo general
- Diseñar una simulación que demuestre la coordinación segura de procesos concurrentes en un hospital digital, evitando pérdida o duplicación de datos.

Objetivos específicos
- Implementar módulos independientes: productor, consumidor, lector, escritor y almacenamiento.
- Controlar acceso concurrente a una base de datos simulada (JSON) mediante semáforos y locks.
- Documentar las técnicas para evitar condiciones de carrera y deadlocks.
- Mostrar resultados reproducibles y trazas claras de ejecución.

Características y motivación
----------------------------
- Simulación modular (cada rol en su propio módulo).
- Uso de semáforos, Locks y protocolo Lectores–Escritores.
- Buffer limitado (bounded buffer) para Productor–Consumidor.
- Mensajes de trazabilidad: cada módulo imprime inicio, procesamiento y finalización.
- Enfoque pedagógico: reproducible, fácil de entender y extender.

Estructura del proyecto
-----------------------
Raíz propuesta:

1. main.py
   - Entrada principal que inicializa la simulación y los hilos.

2. config.py
   - Configuraciones generales: tamaño del buffer, número de médicos, tiempos de espera.

3. models/
   - __init__.py
   - productor_consumidor.py
     - Implementa el modelo Productor–Consumidor usando threading.Semaphore y Lock.
   - lectores_escritor.py
     - Implementa el modelo Lectores–Escritor con contador de lectores y exclusión mutua para escritores.

4. hospital/
   - __init__.py
   - medico.py
     - Clase Médico, genera diagnósticos aleatorios.
   - laboratorio.py
     - Clase Laboratorio, consume diagnósticos y devuelve resultados.
   - base_datos.py
     - Clase BaseDeDatos, buffer compartido thread-safe.
   - estadisticas.py
     - Clase Estadisticas, lectores concurrentes que leen datos.
   - direccion_medica.py
     - Clase DireccionMedica, escritor exclusivo.

5. utils/
   - __init__.py
   - logger.py
     - Funciones para imprimir logs o eventos de la simulación.
   - generador_datos.py
     - Funciones para generar diagnósticos aleatorios.

6. tests/
   - test_productor_consumidor.py
     - Pruebas unitarias del modelo Productor–Consumidor.
   - test_lectores_escritor.py
     - Pruebas unitarias del modelo Lectores–Escritor.
```

Arquitectura y diagramas (visual)
---------------------------------
Diagrama general (Productores ↔ Buffer ↔ Consumidores; Lectores/Escritores ↔ Almacenamiento):

![Diagrama Productor-Consumidor](https://upload.wikimedia.org/wikipedia/commons/1/12/Producerconsumer.svg)

Esquema Lectores–Escritores:

![Diagrama Lectores-Escritores](https://miro.medium.com/v2/resize:fit:786/1*2JQn4vR0e-gj60mK1j6mXw.png)

Representación temática (hospital digital):

![Hospital Digital - ejemplo](https://cdn.pixabay.com/photo/2018/01/14/23/12/hospital-3081724_1280.jpg)

Diseño tipo "mini-banner" (logo Python para identidad visual):

![Python logo](https://www.python.org/static/community_logos/python-logo-master-v3-TM.png)

Explicación de los módulos
--------------------------
- almacenamiento.py  
  - Encapsula acceso al recurso compartido (data/pacientes.json). Implementa un mutex (Lock) para lecturas/escrituras atómicas al archivo y funciones: leer_todos(), agregar_registro(), actualizar_registro().
  - Proporciona API mínima para ser usada por productores, consumidores y escritores.

- productor.py  
  - Simula generación de eventos clínicos (ingresos, lecturas de monitor, órdenes). Usa semáforos y mutex para insertar en el buffer limitado.
  - Mensajes: inicio, producido (con id), finalización.

- consumidor.py  
  - Procesa eventos del buffer (simula tratamiento, notificación, cálculo). Consume sin duplicar; registra acciones en almacenamiento si aplica.
  - Mensajes: inicio, consumiendo (id), procesado, finalización.

- lector.py  
  - Accede solo en modo lectura al almacenamiento (consultas de historial). Implementa el protocolo lectores–escritores: permite lectores concurrentes mientras no haya escritor activo.
  - Mensajes: inicio, leyó N registros, finalización.

- escritor.py  
  - Realiza modificaciones al almacenamiento (actualizar expediente, crear anotaciones). Requiere acceso exclusivo.
  - Mensajes: inicio, escribió registro, finalización.

- main.py  
  - Orquesta la simulación: instancia almacenamiento, buffer, semáforos/locks, crea hilos y los lanza. Permite parametrizar número de productores/consumidores/lectores/escritores y tiempos de producción/consumo.

Modelos teóricos aplicados
--------------------------
- Productor–Consumidor (bounded buffer)
  - Semáforos: empty (espacios libres, inicializado a buffer_size), full (elementos presentes, inicializado a 0).
  - Mutex para proteger la estructura del buffer.
  - Garantiza que productores no sobreescriban y consumidores no lean de buffer vacío.

- Lectores–Escritores
  - Contador de lectores protegido por un lock (reader_count_lock).
  - writer_lock para exclusión de escritores.
  - Primer lector adquiere writer_lock; último lector lo libera. Escritores adquieren writer_lock para exclusión.

Técnicas de sincronización y prevención de fallos
-------------------------------------------------
1. Protecciones básicas
   - Locks (threading.Lock) para secciones críticas.
   - Semáforos (threading.Semaphore) para coordinar conteos en buffer.
2. Evitar condiciones de carrera
   - Toda lectura-modificación-escritura en estructuras compartidas ocurre dentro de una sección crítica protegida.
   - Contadores compartidos (p. ej., reader_count) solo se modifican con su lock.
3. Evitar deadlocks
   - Orden global para adquisición de locks (por ejemplo: buffer_lock → file_lock).
   - Mantener secciones críticas lo más cortas posible.
   - Uso de timeouts para diagnósticos (opcional).
4. Evitar pérdida y duplicación de datos
   - Cada ítem producido recibe un identificador único (uuid).
   - Consumidores marcan o registran el consumo en almacenamiento si procede.
   - Transacciones atómicas simuladas con file_lock rodeando lectura-modificación-escritura al JSON.

Fragmentos de código (resumen atractivo)
----------------------------------------
Un ejemplo de sección crítica en almacenamiento:

```python
# src/almacenamiento.py (extracto)
import json, threading
from pathlib import Path

class AlmacenamientoJSON:
    def __init__(self, ruta):
        self.ruta = Path(ruta)
        self.file_lock = threading.Lock()
        if not self.ruta.exists():
            self.ruta.write_text("[]", encoding="utf-8")

    def leer_todos(self):
        with self.file_lock:
            with self.ruta.open("r", encoding="utf-8") as f:
                return json.load(f)

    def agregar_registro(self, registro):
        with self.file_lock:
            datos = self.leer_todos()  # lectura segura dentro del lock
            datos.append(registro)
            with self.ruta.open("w", encoding="utf-8") as f:
                json.dump(datos, f, indent=2)
```

Ejecución y ejemplos de salida
------------------------------
Instrucciones rápidas
1. Crear entorno y dependencias (opcional):
   - python3 -m venv venv
   - source venv/bin/activate
   - pip install -r requirements.txt (si aplica)
2. Preparar datos:
   - mkdir -p data
   - echo '[]' > data/pacientes.json
3. Ejecutar:
   - python src/main.py

Mensajes esperados en consola (traza):
```
[Productor 0] Iniciado
[Productor 0] Producido: 8a3f2b...
[Consumidor 1] Consumiendo: 8a3f2b...
[Lector 0] Inició lectura concurrente
[Lector 0] Leyó 12 registros
[Escritor 1] Iniciado - adquiriendo acceso exclusivo
[Escritor 1] Escribió un registro
[Productor 0] Finalizado
```

Resultados esperados
- Igual número de ítems producidos y consumidos (bajo condiciones correctas de parada).
- No deben aparecer duplicados en el procesamiento por consumidores.
- Lectores concurrentes no bloquean entre sí, salvo la presencia de un escritor activo.
- Escritores acceden de forma exclusiva.

Pruebas y validación
--------------------
- Prueba de conteo: ejecutar N productores que generen M ítems y validar que almacenamiento contiene N×M registros (o que consumidores han procesado N×M).
- Prueba de contención: buffer pequeño (p. ej., 2) y muchos productores para forzar semáforos.
- Prueba Lectores–Escritores: lanzar múltiples lectores concurrentes con escritores programados y validar exclusión.


Conclusiones
-----------
La simulación ilustra cómo aplicar mecanismos de sincronización para coordinar actores concurrentes en un sistema hospitalario digital. Los patrones Productor–Consumidor y Lectores–Escritores, junto con semáforos y mutex, permiten garantizar integridad de datos y evitar condiciones de carrera y deadlocks si se aplican correctamente. Este repositorio actúa como recurso de aprendizaje y base para experimentación y ampliación hacia entornos más realistas.

Recursos e imágenes (referencias)
--------------------------------
- Python logo: https://www.python.org/static/community_logos/python-logo-master-v3-TM.png
- Diagrama Productor–Consumidor: https://upload.wikimedia.org/wikipedia/commons/1/12/Producerconsumer.svg
- Diagrama Lectores–Escritores: https://miro.medium.com/v2/resize:fit:786/1*2JQn4vR0e-gj60mK1j6mXw.png
- Hospital (ejemplo visual): https://cdn.pixabay.com/photo/2018/01/14/23/12/hospital-3081724_1280.jpg


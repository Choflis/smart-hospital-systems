from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime
import sys
from pathlib import Path

# Agregar el directorio raíz al path para importar módulos del proyecto
sys.path.append(str(Path(__file__).parent.parent))

from models.buffer import Buffer
from models.paciente import Paciente
from models.consumidor import Consumidor
from models.productor import Productor

# Modelos Pydantic para validación
class PacienteCreate(BaseModel):
    nombre: str
    edad: int
    genero: str
    sintomas: str

class DiagnosticoCreate(BaseModel):
    paciente_id: str
    medico_id: int
    diagnostico: str
    tratamiento: Optional[str] = None

# Estado global del hospital (compartido entre todos los dispositivos)
buffer_compartido = Buffer(capacidad=10)
diagnosticos_db: List[Dict] = []
estadisticas_db: List[Dict] = []
consumidores_activos: List[Consumidor] = []
productor_activo: Optional[Productor] = None

app = FastAPI(title="Smart Hospital API", version="1.0.0")

# --- CORS (permite conexión desde otros dispositivos y la UI) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Puedes cambiar esto a ["http://localhost:5173"] por ejemplo
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- INICIALIZACIÓN DEL SISTEMA ---
@app.on_event("startup")
async def startup_event():
    """Inicializa los consumidores (médicos) al arrancar el servidor."""
    global consumidores_activos, productor_activo
    
    # Crear e iniciar consumidores (médicos)
    consumidores_activos = [Consumidor(id=i, buffer=buffer_compartido) for i in range(3)]
    for c in consumidores_activos:
        c.start()
    
    # Crear e iniciar productor
    productor_activo = Productor(buffer_compartido)
    productor_activo.start()
    
    print("✅ Sistema hospitalario iniciado con 3 médicos activos")

@app.on_event("shutdown")
async def shutdown_event():
    """Detiene los hilos al cerrar el servidor."""
    if productor_activo:
        productor_activo.detener()
    for c in consumidores_activos:
        c.detener()
    print("🛑 Sistema hospitalario detenido")

# --- RUTAS PRINCIPALES DEL SERVIDOR ---
@app.get("/")
def root():
    """Ruta base de verificación."""
    return {
        "message": "Servidor Smart Hospital activo",
        "pacientes_en_espera": len(buffer_compartido),
        "medicos_activos": len(consumidores_activos),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

# --- GESTIÓN DE PACIENTES (BUFFER COMPARTIDO) ---
@app.get("/pacientes")
def listar_pacientes():
    """Devuelve todos los pacientes en el buffer de espera."""
    pacientes = buffer_compartido.obtener_lista_pacientes()
    return {
        "total": len(pacientes),
        "capacidad": buffer_compartido.cola.maxsize,
        "pacientes": [
            {
                "nombre": p.nombre,
                "edad": p.edad,
                "genero": p.genero,
                "sintomas": p.sintomas,
                "timestamp": p.timestamp
            } for p in pacientes
        ]
    }

@app.post("/pacientes")
def agregar_paciente(paciente_data: PacienteCreate):
    """Permite agregar un nuevo paciente al buffer (productor)."""
    nuevo_paciente = Paciente(
        nombre=paciente_data.nombre,
        edad=paciente_data.edad,
        genero=paciente_data.genero,
        sintomas=paciente_data.sintomas
    )
    
    exito = buffer_compartido.agregar_paciente(nuevo_paciente)
    if exito:
        return {
            "status": "ok",
            "mensaje": f"Paciente '{paciente_data.nombre}' agregado correctamente",
            "paciente": {
                "nombre": nuevo_paciente.nombre,
                "edad": nuevo_paciente.edad,
                "genero": nuevo_paciente.genero,
                "sintomas": nuevo_paciente.sintomas,
                "timestamp": nuevo_paciente.timestamp
            }
        }
    else:
        raise HTTPException(status_code=503, detail="Buffer lleno, no se puede agregar más pacientes")

@app.get("/pacientes/estado")
def estado_buffer():
    """Devuelve el estado actual del buffer."""
    return {
        "vacio": buffer_compartido.esta_vacio(),
        "lleno": buffer_compartido.esta_lleno(),
        "cantidad": len(buffer_compartido),
        "capacidad": buffer_compartido.cola.maxsize
    }

# --- MODELO PRODUCTOR-CONSUMIDOR (DIAGNÓSTICOS) ---
@app.get("/diagnosticos")
def listar_diagnosticos():
    """Devuelve todos los diagnósticos almacenados."""
    return {"total": len(diagnosticos_db), "data": diagnosticos_db}

@app.post("/diagnosticos")
def agregar_diagnostico(data: DiagnosticoCreate):
    """Permite a los médicos (productores) agregar un diagnóstico."""
    nuevo_diagnostico = {
        "id": len(diagnosticos_db),
        "paciente_id": data.paciente_id,
        "medico_id": data.medico_id,
        "diagnostico": data.diagnostico,
        "tratamiento": data.tratamiento,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "procesado": False
    }
    diagnosticos_db.append(nuevo_diagnostico)
    return {"status": "ok", "mensaje": "Diagnóstico agregado", "nuevo": nuevo_diagnostico}

@app.put("/diagnosticos/{id}/procesar")
def procesar_diagnostico(id: int):
    """Simula que el laboratorio (consumidor) procesa un diagnóstico."""
    if id < 0 or id >= len(diagnosticos_db):
        raise HTTPException(status_code=404, detail="Diagnóstico no encontrado")
    diagnosticos_db[id]["procesado"] = True
    diagnosticos_db[id]["fecha_procesamiento"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return {"status": "procesado", "diagnostico": diagnosticos_db[id]}

# --- MODELO LECTORES-ESCRITOR (ESTADÍSTICAS) ---
@app.get("/estadisticas")
def leer_estadisticas():
    """Lectores (Departamento de Estadísticas) obtienen datos concurrentemente."""
    diagnosticos_procesados = sum(1 for d in diagnosticos_db if d.get("procesado", False))
    
    reporte = {
        "total_pacientes_espera": len(buffer_compartido),
        "total_diagnosticos": len(diagnosticos_db),
        "diagnosticos_procesados": diagnosticos_procesados,
        "diagnosticos_pendientes": len(diagnosticos_db) - diagnosticos_procesados,
        "medicos_activos": len(consumidores_activos),
        "capacidad_buffer": buffer_compartido.cola.maxsize,
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    estadisticas_db.append(reporte)
    return {"status": "ok", "reporte": reporte}

@app.get("/estadisticas/historico")
def historico_estadisticas():
    """Devuelve el historial de reportes estadísticos."""
    return {"total": len(estadisticas_db), "reportes": estadisticas_db}

@app.post("/configuracion")
def actualizar_configuracion(data: Dict):
    """Escritor (Dirección Médica) actualiza configuraciones."""
    return {"status": "actualizado", "nueva_configuracion": data, "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

@app.get("/medicos")
def listar_medicos():
    """Devuelve información sobre los médicos (consumidores) activos."""
    return {
        "total": len(consumidores_activos),
        "medicos": [
            {
                "id": c.id,
                "activo": c.is_alive()
            } for c in consumidores_activos
        ]
    }

# --- FIN DE ARCHIVO ---
# Puedes ejecutar con:
# uvicorn api_server.main:app --host 0.0.0.0 --port 8000

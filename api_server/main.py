from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict
from datetime import datetime

# Simulación temporal de datos (puede reemplazarse con base de datos real)
diagnosticos: List[Dict] = []
reportes_estadisticos: List[Dict] = []

app = FastAPI(title="Smart Hospital API", version="1.0.0")

# --- CORS (permite conexión desde otros dispositivos y la UI) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Puedes cambiar esto a ["http://localhost:5173"] por ejemplo
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- RUTAS PRINCIPALES DEL SERVIDOR ---
@app.get("/")
def root():
    """Ruta base de verificación."""
    return {"message": "Servidor Smart Hospital activo "}

# --- MODELO PRODUCTOR-CONSUMIDOR ---
@app.get("/diagnosticos")
def listar_diagnosticos():
    """Devuelve todos los diagnósticos almacenados."""
    return {"total": len(diagnosticos), "data": diagnosticos}

@app.post("/diagnosticos")
def agregar_diagnostico(data: Dict):
    """Permite a los médicos (productores) agregar un diagnóstico."""
    data["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    diagnosticos.append(data)
    return {"status": "ok", "mensaje": "Diagnóstico agregado", "nuevo": data}

@app.delete("/diagnosticos/{id}")
def eliminar_diagnostico(id: int):
    """Simula que el laboratorio (consumidor) procesa y elimina un diagnóstico."""
    if id < 0 or id >= len(diagnosticos):
        raise HTTPException(status_code=404, detail="Diagnóstico no encontrado")
    eliminado = diagnosticos.pop(id)
    return {"status": "procesado", "diagnostico": eliminado}

# --- MODELO LECTORES-ESCRITOR ---
@app.get("/estadisticas")
def leer_estadisticas():
    """Lectores (Departamento de Estadísticas) obtienen datos concurrentemente."""
    total = len(diagnosticos)
    reporte = {
        "total_diagnosticos": total,
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    reportes_estadisticos.append(reporte)
    return {"status": "ok", "reporte": reporte}

@app.post("/configuracion")
def actualizar_configuracion(data: Dict):
    """Escritor (Dirección Médica) actualiza configuraciones."""
    # Aquí solo simulamos la acción
    return {"status": "actualizado", "nueva_configuracion": data}

# --- FIN DE ARCHIVO ---
# Puedes ejecutar con:
# uvicorn api_server.main:app --host 0.0.0.0 --port 8000

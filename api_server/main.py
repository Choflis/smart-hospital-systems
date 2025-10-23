#api_server

from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI(title="Smart Hospital API")

# Modelos de Datos

class Diagnostico(BaseModel):
    id: int
    paciente: str
    descripción: str
    estado: str

#Base de Datos en memoria
diagnosticos_db: List[Diagnostico] = []

#endpoints

@app.get("/")
def root():
    return {"message" : "Servidor Smart Hospital activo"}

@app.get("/diagnosticos")
def listar_diagnosticos():
    return diagnosticos_db


@app.post("/diagnosticos")
def agregar_diagnostico(diagnostico: Diagnostico):
    diagnosticos_db.append(diagnostico)
    return {"status": "ok", "total": len(diagnosticos_db)}

@app.put("/diagnosticos/{id}")
def actualizar_diagnostico(id: int, nuevo: Diagnostico):
    for i, d in enumerate(diagnosticos_db):
        if d.id == id:
            diagnosticos_db[i] = nuevo
            return {"status": "actualizado"}
    return {"error": "no encontrado"}
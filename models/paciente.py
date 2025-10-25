# models/paciente.py
from datetime import datetime

class Paciente:
    """
    Representa a un paciente dentro del sistema hospitalario.
    """

    def __init__(self, nombre, edad, genero, sintomas):
        self.nombre = nombre
        self.edad = edad
        self.genero = genero
        self.sintomas = sintomas
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def __str__(self):
        return f"{self.nombre} ({self.edad} años, {self.genero}) - Síntomas: {self.sintomas}"

# models/paciente.py

class Paciente:
    """
    Representa a un paciente dentro del sistema hospitalario.
    """

    def __init__(self, nombre, edad, genero, sintomas):
        self.nombre = nombre
        self.edad = edad
        self.genero = genero
        self.sintomas = sintomas

    def __str__(self):
        return f"{self.nombre} ({self.edad} años, {self.genero}) - Síntomas: {self.sintomas}"

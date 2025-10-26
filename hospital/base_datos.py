"""
Módulo de Base de Datos compartida del sistema hospitalario.
Implementa el patrón Lectores-Escritores para acceso concurrente seguro.
"""
import json
import threading
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime


class BaseDeDatos:
    """
    Clase que gestiona el almacenamiento persistente en archivo JSON.
    Implementa el patrón Lectores-Escritores:
    - Múltiples lectores pueden acceder simultáneamente
    - Escritores tienen acceso exclusivo
    - Usa locks para evitar condiciones de carrera
    """
    
    def __init__(self, ruta_archivo="data/pacientes.json"):
        """
        Inicializa la base de datos.
        
        Args:
            ruta_archivo (str): Ruta del archivo JSON donde se guardan los datos
        """
        self.ruta = Path(ruta_archivo)
        
        # ---- LOCKS PARA SINCRONIZACIÓN ----
        # Lock para proteger el contador de lectores
        self.reader_count_lock = threading.Lock()
        
        # Lock para exclusión mutua de escritores
        self.writer_lock = threading.Lock()
        
        # Contador de lectores activos
        self.reader_count = 0
        
        # Crear directorio y archivo si no existen
        self._inicializar_archivo()
    
    def _inicializar_archivo(self):
        """
        Crea el directorio y archivo JSON si no existen.
        Inicializa con una lista vacía.
        """
        # Crear directorio data/ si no existe
        self.ruta.parent.mkdir(parents=True, exist_ok=True)
        
        # Crear archivo con lista vacía si no existe
        if not self.ruta.exists():
            with open(self.ruta, "w", encoding="utf-8") as f:
                json.dump([], f, indent=2)
            print(f"[BASE_DATOS] Archivo creado: {self.ruta}")
    
    # ---- MÉTODOS DE LECTURA (Múltiples lectores concurrentes) ----
    
    def leer_todos(self) -> List[Dict]:
        """
        Lee todos los registros del archivo.
        Permite múltiples lectores concurrentes.
        
        Returns:
            List[Dict]: Lista de todos los registros
        """
        # Protocolo de entrada para LECTORES
        with self.reader_count_lock:
            self.reader_count += 1
            if self.reader_count == 1:
                # Primer lector bloquea a escritores
                self.writer_lock.acquire()
        
        try:
            # SECCIÓN CRÍTICA DE LECTURA
            with open(self.ruta, "r", encoding="utf-8") as f:
                datos = json.load(f)
            print(f"[BASE_DATOS] Lectura exitosa: {len(datos)} registros")
            return datos
        
        finally:
            # Protocolo de salida para LECTORES
            with self.reader_count_lock:
                self.reader_count -= 1
                if self.reader_count == 0:
                    # Último lector libera el lock para escritores
                    self.writer_lock.release()
    
    def buscar_por_nombre(self, nombre: str) -> Optional[Dict]:
        """
        Busca un registro por nombre del paciente.
        
        Args:
            nombre (str): Nombre del paciente a buscar
        
        Returns:
            Optional[Dict]: Registro encontrado o None
        """
        registros = self.leer_todos()
        for registro in registros:
            if registro.get("nombre", "").lower() == nombre.lower():
                return registro
        return None
    
    def contar_registros(self) -> int:
        """
        Cuenta el total de registros en la base de datos.
        
        Returns:
            int: Número de registros
        """
        registros = self.leer_todos()
        return len(registros)
    
    # ---- MÉTODOS DE ESCRITURA (Acceso exclusivo) ----
    
    def agregar_registro(self, nuevo_registro: Dict) -> bool:
        """
        Agrega un nuevo registro a la base de datos.
        Requiere acceso exclusivo (bloquea lectores y otros escritores).
        
        Args:
            nuevo_registro (Dict): Registro a agregar
        
        Returns:
            bool: True si se agregó correctamente
        """
        # ESCRITOR adquiere acceso exclusivo
        with self.writer_lock:
            try:
                # Leer datos actuales
                with open(self.ruta, "r", encoding="utf-8") as f:
                    datos = json.load(f)
                
                # Agregar timestamp si no existe
                if "timestamp" not in nuevo_registro:
                    nuevo_registro["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                # Agregar nuevo registro
                datos.append(nuevo_registro)
                
                # Escribir de vuelta al archivo
                with open(self.ruta, "w", encoding="utf-8") as f:
                    json.dump(datos, f, indent=2, ensure_ascii=False)
                
                print(f"[BASE_DATOS] Registro agregado: {nuevo_registro.get('nombre', 'sin nombre')}")
                return True
            
            except Exception as e:
                print(f"[BASE_DATOS] Error al agregar registro: {e}")
                return False
    
    def actualizar_registro(self, nombre: str, datos_actualizados: Dict) -> bool:
        """
        Actualiza un registro existente por nombre.
        Requiere acceso exclusivo.
        
        Args:
            nombre (str): Nombre del paciente a actualizar
            datos_actualizados (Dict): Nuevos datos del registro
        
        Returns:
            bool: True si se actualizó correctamente
        """
        # ESCRITOR adquiere acceso exclusivo
        with self.writer_lock:
            try:
                # Leer datos actuales
                with open(self.ruta, "r", encoding="utf-8") as f:
                    datos = json.load(f)
                
                # Buscar y actualizar
                actualizado = False
                for i, registro in enumerate(datos):
                    if registro.get("nombre", "").lower() == nombre.lower():
                        # Actualizar campos
                        datos[i].update(datos_actualizados)
                        datos[i]["ultima_modificacion"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        actualizado = True
                        break
                
                if actualizado:
                    # Escribir de vuelta al archivo
                    with open(self.ruta, "w", encoding="utf-8") as f:
                        json.dump(datos, f, indent=2, ensure_ascii=False)
                    print(f"[BASE_DATOS] Registro actualizado: {nombre}")
                    return True
                else:
                    print(f"[BASE_DATOS] Registro no encontrado: {nombre}")
                    return False
            
            except Exception as e:
                print(f"[BASE_DATOS] Error al actualizar registro: {e}")
                return False
    
    def eliminar_registro(self, nombre: str) -> bool:
        """
        Elimina un registro por nombre.
        Requiere acceso exclusivo.
        
        Args:
            nombre (str): Nombre del paciente a eliminar
        
        Returns:
            bool: True si se eliminó correctamente
        """
        # ESCRITOR adquiere acceso exclusivo
        with self.writer_lock:
            try:
                # Leer datos actuales
                with open(self.ruta, "r", encoding="utf-8") as f:
                    datos = json.load(f)
                
                # Filtrar (eliminar el registro)
                datos_nuevos = [r for r in datos if r.get("nombre", "").lower() != nombre.lower()]
                
                if len(datos_nuevos) < len(datos):
                    # Escribir de vuelta al archivo
                    with open(self.ruta, "w", encoding="utf-8") as f:
                        json.dump(datos_nuevos, f, indent=2, ensure_ascii=False)
                    print(f"[BASE_DATOS] Registro eliminado: {nombre}")
                    return True
                else:
                    print(f"[BASE_DATOS] Registro no encontrado: {nombre}")
                    return False
            
            except Exception as e:
                print(f"[BASE_DATOS] Error al eliminar registro: {e}")
                return False
    
    def vaciar_base_datos(self) -> bool:
        """
        Elimina todos los registros de la base de datos.
        CUIDADO: Esta operación no se puede deshacer.
        
        Returns:
            bool: True si se vació correctamente
        """
        with self.writer_lock:
            try:
                with open(self.ruta, "w", encoding="utf-8") as f:
                    json.dump([], f, indent=2)
                print("[BASE_DATOS] Base de datos vaciada")
                return True
            except Exception as e:
                print(f"[BASE_DATOS] Error al vaciar base de datos: {e}")
                return False


# ---- PRUEBAS DEL MÓDULO ----
if __name__ == "__main__":
    """Código de prueba para verificar el funcionamiento."""
    print("=== PRUEBA DE BASE DE DATOS ===\n")
    
    # Crear instancia
    db = BaseDeDatos("data/test_pacientes.json")
    
    # Agregar registros de prueba
    print("1. Agregando registros...")
    db.agregar_registro({
        "nombre": "Juan Pérez",
        "edad": 45,
        "genero": "Masculino",
        "sintomas": "Fiebre alta"
    })
    
    db.agregar_registro({
        "nombre": "María García",
        "edad": 32,
        "genero": "Femenino",
        "sintomas": "Dolor de cabeza"
    })
    
    # Leer todos
    print("\n2. Leyendo todos los registros...")
    registros = db.leer_todos()
    print(f"Total: {len(registros)}")
    
    # Buscar uno
    print("\n3. Buscando 'Juan Pérez'...")
    encontrado = db.buscar_por_nombre("Juan Pérez")
    print(f"Encontrado: {encontrado}")
    
    # Actualizar
    print("\n4. Actualizando registro...")
    db.actualizar_registro("Juan Pérez", {"sintomas": "Recuperado"})
    
    # Contar
    print(f"\n5. Total de registros: {db.contar_registros()}")

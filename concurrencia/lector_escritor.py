# concurrencia/lector_escritor.py
"""
Sistema de expedientes con problema Lectores-Escritores
Permite múltiples lectores simultáneos pero un solo escritor a la vez
"""

import threading
import json
import os
import logging
from datetime import datetime
from typing import Optional, Dict, List
from core.paciente import Paciente

class SistemaExpedientes:
    """
    Sistema para gestionar expedientes médicos usando el patrón Lectores-Escritores
    
    Reglas:
    - Múltiples lectores pueden leer simultáneamente
    - Solo un escritor puede escribir a la vez
    - Escritores tienen prioridad sobre lectores
    """
    
    def __init__(self, archivo: str = "data/expedientes.json"):
        """
        Inicializa el sistema de expedientes
        
        Args:
            archivo: Ruta del archivo JSON para almacenar expedientes
        """
        self.archivo = archivo
        self.lectores = 0  # Contador de lectores activos
        
        # Locks para sincronización Lectores-Escritores
        self.mutex = threading.Lock()  # Protege el contador de lectores
        self.escritor_lock = threading.Lock()  # Exclusión mutua para escritores
        
        self.logger = logging.getLogger(__name__)
        
        # Crear archivo si no existe
        self._inicializar_archivo()
        
        self.logger.info(f"Sistema de expedientes inicializado: {archivo}")
    
    def _inicializar_archivo(self):
        """Crea el archivo de expedientes si no existe"""
        os.makedirs(os.path.dirname(self.archivo), exist_ok=True)
        if not os.path.exists(self.archivo):
            with open(self.archivo, 'w', encoding='utf-8') as f:
                json.dump({"expedientes": [], "metadata": {"creado": datetime.now().isoformat()}}, f, indent=2)
    
    def escribir_expediente(self, paciente: Paciente):
        """
        Escribe un expediente médico (ESCRITOR)
        Solo un escritor a la vez
        
        Args:
            paciente: Paciente cuyo expediente se va a escribir
        """
        # Adquirir lock de escritor (exclusión mutua total)
        self.escritor_lock.acquire()
        
        try:
            self.logger.info(f"📝 Escribiendo expediente de paciente {paciente.id}")
            
            # Leer datos existentes
            with open(self.archivo, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Agregar nuevo expediente
            expediente = paciente.to_dict()
            expediente['fecha_registro'] = datetime.now().isoformat()
            data['expedientes'].append(expediente)
            
            # Escribir de vuelta
            with open(self.archivo, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"✅ Expediente de paciente {paciente.id} guardado")
            
        except Exception as e:
            self.logger.error(f"❌ Error escribiendo expediente: {e}")
        finally:
            # Liberar lock de escritor
            self.escritor_lock.release()
    
    def leer_expediente(self, paciente_id: int) -> Optional[Dict]:
        """
        Lee un expediente específico (LECTOR)
        Múltiples lectores pueden leer simultáneamente
        
        Args:
            paciente_id: ID del paciente a buscar
            
        Returns:
            Diccionario con datos del expediente o None si no existe
        """
        # Protocolo de entrada de LECTOR
        self.mutex.acquire()
        self.lectores += 1
        if self.lectores == 1:
            # Primer lector bloquea escritores
            self.escritor_lock.acquire()
        self.mutex.release()
        
        try:
            # Leer datos
            with open(self.archivo, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Buscar expediente
            for expediente in data['expedientes']:
                if expediente['id'] == paciente_id:
                    self.logger.info(f"📖 Expediente {paciente_id} leído")
                    return expediente
            
            self.logger.info(f"⚠️ Expediente {paciente_id} no encontrado")
            return None
            
        except Exception as e:
            self.logger.error(f"❌ Error leyendo expediente: {e}")
            return None
        finally:
            # Protocolo de salida de LECTOR
            self.mutex.acquire()
            self.lectores -= 1
            if self.lectores == 0:
                # Último lector libera escritores
                self.escritor_lock.release()
            self.mutex.release()
    
    def leer_todos_expedientes(self) -> List[Dict]:
        """
        Lee todos los expedientes (LECTOR)
        
        Returns:
            Lista de todos los expedientes
        """
        # Protocolo de entrada de LECTOR
        self.mutex.acquire()
        self.lectores += 1
        if self.lectores == 1:
            self.escritor_lock.acquire()
        self.mutex.release()
        
        try:
            with open(self.archivo, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.logger.info(f"📖 Leídos {len(data['expedientes'])} expedientes")
            return data['expedientes']
            
        except Exception as e:
            self.logger.error(f"❌ Error leyendo expedientes: {e}")
            return []
        finally:
            # Protocolo de salida de LECTOR
            self.mutex.acquire()
            self.lectores -= 1
            if self.lectores == 0:
                self.escritor_lock.release()
            self.mutex.release()
    
    def obtener_estadisticas(self) -> Dict:
        """
        Obtiene estadísticas de los expedientes
        
        Returns:
            Diccionario con estadísticas
        """
        expedientes = self.leer_todos_expedientes()
        
        if not expedientes:
            return {"total": 0}
        
        return {
            "total": len(expedientes),
            "por_prioridad": {
                "urgente": len([e for e in expedientes if e['prioridad'] == 1]),
                "normal": len([e for e in expedientes if e['prioridad'] == 2]),
                "baja": len([e for e in expedientes if e['prioridad'] == 3])
            },
            "atendidos": len([e for e in expedientes if e['estado'] == 'Atendido'])
        }

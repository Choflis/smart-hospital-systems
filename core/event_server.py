# core/event_server.py
"""
Servidor de eventos para comunicación con interfaces
Permite que múltiples ventanas se conecten y reciban actualizaciones
"""

import socket
import threading
import json
import logging
from typing import List, Dict, Any

class EventServer:
    """
    Servidor que permite a las interfaces conectarse y recibir eventos
    del sistema hospitalario en tiempo real
    """
    
    def __init__(self, hospital, host='localhost', port=5555):
        """
        Inicializa el servidor de eventos
        
        Args:
            hospital: Instancia del hospital
            host: Host del servidor
            port: Puerto del servidor
        """
        self.hospital = hospital
        self.host = host
        self.port = port
        self.server_socket = None
        self.activo = False
        self.clientes = []
        self.lock = threading.Lock()
        self.logger = logging.getLogger(__name__)
        
        # Callbacks para eventos
        self.callbacks = {
            'paciente_registrado': [],
            'paciente_atendido': [],
            'estado_actualizado': []
        }
    
    def iniciar(self):
        """Inicia el servidor de eventos"""
        self.activo = True
        thread = threading.Thread(target=self._run_server, daemon=True)
        thread.start()
        self.logger.info(f"🌐 Servidor de eventos iniciado en {self.host}:{self.port}")
    
    def detener(self):
        """Detiene el servidor de eventos"""
        self.activo = False
        with self.lock:
            for cliente in self.clientes:
                try:
                    cliente.close()
                except:
                    pass
            self.clientes.clear()
        
        if self.server_socket:
            try:
                self.server_socket.close()
            except:
                pass
        
        self.logger.info("🔴 Servidor de eventos detenido")
    
    def _run_server(self):
        """Ejecuta el servidor en un thread"""
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            self.server_socket.settimeout(1.0)
            
            while self.activo:
                try:
                    cliente_socket, addr = self.server_socket.accept()
                    self.logger.info(f"📱 Nueva conexión desde {addr}")
                    
                    with self.lock:
                        self.clientes.append(cliente_socket)
                    
                    # Enviar estado inicial
                    self._enviar_estado_inicial(cliente_socket)
                    
                    # Manejar cliente en un thread
                    thread = threading.Thread(
                        target=self._manejar_cliente,
                        args=(cliente_socket,),
                        daemon=True
                    )
                    thread.start()
                    
                except socket.timeout:
                    continue
                except Exception as e:
                    if self.activo:
                        self.logger.error(f"Error en servidor: {e}")
        
        except Exception as e:
            self.logger.error(f"Error al iniciar servidor: {e}")
    
    def _enviar_estado_inicial(self, cliente_socket):
        """Envía el estado inicial del hospital al cliente"""
        try:
            estado = {
                'tipo': 'estado_inicial',
                'medicos': [
                    {
                        'nombre': m.name,
                        'pacientes_atendidos': m.pacientes_atendidos
                    }
                    for m in self.hospital.medicos
                ],
                'estadisticas': self.hospital.get_estadisticas()
            }
            self._enviar_mensaje(cliente_socket, estado)
        except Exception as e:
            self.logger.error(f"Error al enviar estado inicial: {e}")
    
    def _manejar_cliente(self, cliente_socket):
        """Maneja las peticiones de un cliente"""
        try:
            while self.activo:
                try:
                    data = cliente_socket.recv(4096)
                    if not data:
                        break
                    
                    # Procesar comando del cliente
                    mensaje = json.loads(data.decode('utf-8'))
                    self._procesar_comando(cliente_socket, mensaje)
                    
                except socket.timeout:
                    continue
                except Exception as e:
                    break
        
        except Exception as e:
            self.logger.error(f"Error manejando cliente: {e}")
        finally:
            with self.lock:
                if cliente_socket in self.clientes:
                    self.clientes.remove(cliente_socket)
            try:
                cliente_socket.close()
            except:
                pass
    
    def _procesar_comando(self, cliente_socket, mensaje):
        """Procesa un comando del cliente"""
        comando = mensaje.get('comando')
        
        if comando == 'registrar_paciente':
            # Registrar paciente desde la UI
            paciente_data = mensaje.get('datos')
            self.notificar_paciente_registrado(paciente_data)
            
            # Confirmar al cliente
            respuesta = {
                'tipo': 'confirmacion',
                'estado': 'ok',
                'mensaje': 'Paciente registrado correctamente'
            }
            self._enviar_mensaje(cliente_socket, respuesta)
        
        elif comando == 'obtener_estado':
            # Enviar estado actual
            self._enviar_estado_inicial(cliente_socket)
        
        elif comando == 'obtener_medicos':
            # Enviar lista de médicos
            medicos = [{'nombre': m.name} for m in self.hospital.medicos]
            respuesta = {'tipo': 'medicos', 'medicos': medicos}
            self._enviar_mensaje(cliente_socket, respuesta)
    
    def _enviar_mensaje(self, cliente_socket, mensaje):
        """Envía un mensaje a un cliente"""
        try:
            data = json.dumps(mensaje).encode('utf-8')
            cliente_socket.sendall(data + b'\n')
        except Exception as e:
            self.logger.error(f"Error al enviar mensaje: {e}")
    
    def notificar_paciente_registrado(self, paciente_data):
        """Notifica a todos los clientes que se registró un paciente"""
        mensaje = {
            'tipo': 'paciente_registrado',
            'paciente': paciente_data
        }
        self._broadcast(mensaje)
    
    def notificar_paciente_atendido(self, paciente_data):
        """Notifica que un paciente fue atendido"""
        mensaje = {
            'tipo': 'paciente_atendido',
            'paciente': paciente_data
        }
        self._broadcast(mensaje)
    
    def notificar_actualizacion(self):
        """Notifica una actualización general del estado"""
        mensaje = {
            'tipo': 'actualizacion_estado',
            'estadisticas': self.hospital.get_estadisticas()
        }
        self._broadcast(mensaje)
    
    def _broadcast(self, mensaje):
        """Envía un mensaje a todos los clientes conectados"""
        with self.lock:
            clientes_muertos = []
            for cliente in self.clientes:
                try:
                    self._enviar_mensaje(cliente, mensaje)
                except:
                    clientes_muertos.append(cliente)
            
            # Remover clientes desconectados
            for cliente in clientes_muertos:
                self.clientes.remove(cliente)
                try:
                    cliente.close()
                except:
                    pass

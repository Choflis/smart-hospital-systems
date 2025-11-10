#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Panel Principal del Hospital
=============================

Interfaz gráfica que muestra:
- Consola de logs en tiempo real (izquierda, 15%)
- Lista de médicos y sus pacientes (derecha, 85%)

Puede ejecutarse de forma independiente:
    python ui/panel_hospital.py

Si el sistema principal está activo, se conecta automáticamente.
Si no, muestra la interfaz sin conexión funcional.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from datetime import datetime
import threading
import socket
import json
import sys
import os
import random
import time

# Agregar directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Ruta del archivo de expedientes
EXPEDIENTES_FILE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    'data',
    'expedientes.json'
)


class PanelHospital(tk.Toplevel):
    """Panel Principal del Hospital con Logs y Médicos"""
    
    def __init__(self, parent=None, host='localhost', port=5555):
        """
        Inicializar panel del hospital
        
        Args:
            parent: Ventana padre (None para ventana independiente)
            host: Host del servidor
            port: Puerto del servidor
        """
        # Si no hay parent, crear como ventana independiente
        if parent is None:
            # Crear root oculta y usar self como ventana principal
            self._standalone_root = tk.Tk()
            self._standalone_root.withdraw()
            parent = self._standalone_root
            self._is_standalone = True
        else:
            self._standalone_root = None
            self._is_standalone = False
        
        super().__init__(parent)
        
        # Si es standalone, deiconificar
        if self._is_standalone:
            self.protocol("WM_DELETE_WINDOW", self._on_closing_standalone)
        
        self.host = host
        self.port = port
        self.socket = None
        self.conectado = False
        
        # Configuración de la ventana
        self.title("🏥 Panel Principal del Hospital")
        self.geometry("1200x700")
        self.configure(bg="#ecf0f1")
        
        # Datos de médicos y pacientes
        self.medicos_data = {}  # {nombre_medico: [lista_pacientes]}
        
        # Diccionario para tracking de expedientes (para calcular tiempos)
        self.expedientes_tracking = {}  # {paciente_id: datos_temporales}
        
        # Variables de simulación interna
        self.simulacion_activa = False
        self.threads_simulacion = []
        self.paciente_id_counter = 1000
        self.medicos_simulados = ["Dr. García", "Dra. Martínez", "Dr. López"]
        
        self._crear_interfaz()
        self._conectar_servidor()
        
        # Protocol de cierre
        if not self._is_standalone:
            self.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def _conectar_servidor(self):
        """Intenta conectarse al servidor del hospital"""
        def conectar():
            try:
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.socket.settimeout(2.0)
                self.socket.connect((self.host, self.port))
                self.conectado = True
                self._agregar_log("Conectado al sistema hospitalario", "success")
                
                # Iniciar thread para recibir eventos
                thread = threading.Thread(target=self._recibir_eventos, daemon=True)
                thread.start()
                
                # Solicitar estado inicial
                self._enviar_comando({'comando': 'obtener_estado'})
                
            except Exception as e:
                self.conectado = False
                self._agregar_log("Sin conexión al sistema", "warning")
                self._agregar_log("Modo visualización sin datos", "info")
        
        thread = threading.Thread(target=conectar, daemon=True)
        thread.start()
    
    def _enviar_comando(self, comando):
        """Envía un comando al servidor"""
        if not self.conectado or not self.socket:
            return False
        
        try:
            data = json.dumps(comando).encode('utf-8')
            self.socket.sendall(data + b'\n')
            return True
        except Exception as e:
            self.conectado = False
            self._agregar_log("Conexión perdida", "error")
            return False
    
    def _recibir_eventos(self):
        """Recibe eventos del servidor en tiempo real"""
        buffer = ""
        while self.conectado:
            try:
                data = self.socket.recv(4096).decode('utf-8')
                if not data:
                    break
                
                buffer += data
                while '\n' in buffer:
                    linea, buffer = buffer.split('\n', 1)
                    if linea.strip():
                        mensaje = json.loads(linea)
                        self._procesar_evento(mensaje)
            
            except socket.timeout:
                continue
            except Exception as e:
                if self.conectado:
                    self.conectado = False
                    self.after(0, lambda: self._agregar_log("Conexión perdida", "error"))
                break
    
    def _procesar_evento(self, evento):
        """Procesa un evento recibido del servidor"""
        tipo = evento.get('tipo')
        
        if tipo == 'estado_inicial':
            # Inicializar médicos y datos
            medicos = evento.get('medicos', [])
            for medico in medicos:
                self.medicos_data[medico['nombre']] = []
            self.after(0, self._crear_bloques_medicos)
        
        elif tipo == 'paciente_registrado':
            # Nuevo paciente registrado
            paciente = evento.get('paciente')
            self.after(0, lambda: self.agregar_paciente(paciente))
        
        elif tipo == 'paciente_atendido':
            # Paciente atendido
            paciente = evento.get('paciente')
            self.after(0, lambda: self._agregar_log(
                f"Paciente {paciente.get('nombre', 'N/A')} atendido", "success"
            ))
        
        elif tipo == 'actualizacion_estado':
            # Actualización general
            self.after(0, self._crear_bloques_medicos)
    
    def inicializar_medicos(self):
        """Inicializar estructura de datos de médicos"""
        # Se inicializa cuando se recibe el estado del servidor
        pass
    
    def _crear_interfaz(self):
        """Crear la interfaz del panel principal"""
        
        # ===== ENCABEZADO =====
        frame_header = tk.Frame(self, bg="#2c3e50", height=70)
        frame_header.pack(fill=tk.X)
        frame_header.pack_propagate(False)
        
        tk.Label(
            frame_header,
            text="🏥 PANEL PRINCIPAL DEL HOSPITAL",
            font=("Arial", 22, "bold"),
            fg="white",
            bg="#2c3e50"
        ).pack(side=tk.LEFT, padx=30, pady=20)
        
        # Reloj en tiempo real
        self.label_reloj = tk.Label(
            frame_header,
            text="",
            font=("Arial", 14),
            fg="white",
            bg="#2c3e50"
        )
        self.label_reloj.pack(side=tk.RIGHT, padx=30)
        self._actualizar_reloj()
        
        # ===== CONTENEDOR PRINCIPAL =====
        frame_main = tk.Frame(self, bg="#ecf0f1")
        frame_main.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # ===== SECCIÓN IZQUIERDA: CONSOLA DE LOGS (15%) =====
        frame_logs = tk.LabelFrame(
            frame_main,
            text="📋 CONSOLA DE LOGS",
            font=("Arial", 12, "bold"),
            bg="#34495e",
            fg="white",
            relief=tk.RAISED,
            borderwidth=2
        )
        frame_logs.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 5))
        frame_logs.pack_propagate(False)
        frame_logs.config(width=180)
        
        # Scrollbar para logs
        scrollbar_logs = tk.Scrollbar(frame_logs)
        scrollbar_logs.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.text_logs = tk.Text(
            frame_logs,
            font=("Consolas", 9),
            bg="#1c2833",
            fg="#ecf0f1",
            wrap=tk.WORD,
            yscrollcommand=scrollbar_logs.set,
            state=tk.DISABLED
        )
        self.text_logs.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        scrollbar_logs.config(command=self.text_logs.yview)
        
        # Configurar tags para colores
        self.text_logs.tag_config("info", foreground="#3498db")
        self.text_logs.tag_config("success", foreground="#27ae60")
        self.text_logs.tag_config("warning", foreground="#f39c12")
        self.text_logs.tag_config("error", foreground="#e74c3c")
        self.text_logs.tag_config("timestamp", foreground="#95a5a6")
        self.text_logs.tag_config("separator", foreground="#5d6d7e")
        
        # Log inicial
        self._agregar_log("Sistema iniciado", "info")
        self._agregar_log("Esperando pacientes...", "info")
        
        # ===== SECCIÓN DERECHA: MÉDICOS Y PACIENTES (85%) =====
        frame_medicos_container = tk.Frame(frame_main, bg="#ecf0f1")
        frame_medicos_container.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Frame para título y botón
        frame_titulo_medicos = tk.Frame(frame_medicos_container, bg="#3498db")
        frame_titulo_medicos.pack(fill=tk.X)
        
        # Título
        tk.Label(
            frame_titulo_medicos,
            text="👨‍⚕️ MÉDICOS Y PACIENTES ASIGNADOS",
            font=("Arial", 14, "bold"),
            bg="#3498db",
            fg="white",
            pady=10
        ).pack(side=tk.LEFT, padx=20)
        
        # Botón de simulación
        self.btn_simulacion = tk.Button(
            frame_titulo_medicos,
            text="▶️ Iniciar Simulación",
            font=("Arial", 11, "bold"),
            bg="#27ae60",
            fg="white",
            activebackground="#229954",
            activeforeground="white",
            cursor="hand2",
            relief=tk.RAISED,
            borderwidth=3,
            command=self._toggle_simulacion
        )
        self.btn_simulacion.pack(side=tk.RIGHT, padx=20, pady=5)
        
        # Canvas con scrollbar para médicos
        canvas = tk.Canvas(frame_medicos_container, bg="#ecf0f1", highlightthickness=0)
        scrollbar = tk.Scrollbar(frame_medicos_container, orient=tk.VERTICAL, command=canvas.yview)
        self.frame_medicos = tk.Frame(canvas, bg="#ecf0f1")
        
        self.frame_medicos.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.frame_medicos, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Crear bloques de médicos
        self._crear_bloques_medicos()
    
    def _crear_bloques_medicos(self):
        """Crear bloques visuales para cada médico"""
        # Limpiar frame
        for widget in self.frame_medicos.winfo_children():
            widget.destroy()
        
        # Crear un bloque por cada médico
        for idx, (medico_nombre, pacientes) in enumerate(self.medicos_data.items()):
            self._crear_bloque_medico(medico_nombre, pacientes, idx)
    
    def _crear_bloque_medico(self, medico_nombre, pacientes, idx):
        """Crear un bloque individual de médico"""
        # Frame principal del médico
        frame_medico = tk.LabelFrame(
            self.frame_medicos,
            text=f"👨‍⚕️ {medico_nombre}",
            font=("Arial", 12, "bold"),
            bg="white",
            fg="#2c3e50",
            relief=tk.RAISED,
            borderwidth=2,
            padx=10,
            pady=10
        )
        frame_medico.pack(fill=tk.X, padx=10, pady=8)
        
        # Información del médico
        frame_info = tk.Frame(frame_medico, bg="white")
        frame_info.pack(fill=tk.X, pady=5)
        
        tk.Label(
            frame_info,
            text=f"📊 Pacientes asignados: {len(pacientes)}",
            font=("Arial", 10, "bold"),
            bg="white",
            fg="#7f8c8d"
        ).pack(side=tk.LEFT)
        
        # Estado
        if len(pacientes) > 0:
            estado_color = "#e74c3c" if len(pacientes) > 3 else "#f39c12"
            estado_texto = "Ocupado" if len(pacientes) > 3 else "Disponible"
        else:
            estado_color = "#27ae60"
            estado_texto = "Libre"
        
        tk.Label(
            frame_info,
            text=f"● {estado_texto}",
            font=("Arial", 10, "bold"),
            bg="white",
            fg=estado_color
        ).pack(side=tk.RIGHT)
        
        # Separador
        ttk.Separator(frame_medico, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=5)
        
        # Contenedor horizontal para pacientes
        frame_pacientes_container = tk.Frame(frame_medico, bg="white")
        frame_pacientes_container.pack(fill=tk.BOTH, expand=True)
        
        # Lista de pacientes apilados horizontalmente
        if pacientes:
            for paciente in pacientes:
                self._crear_tarjeta_paciente(frame_pacientes_container, paciente)
        else:
            tk.Label(
                frame_pacientes_container,
                text="Sin pacientes asignados",
                font=("Arial", 10, "italic"),
                bg="white",
                fg="#95a5a6"
            ).pack(pady=10)
    
    def _crear_tarjeta_paciente(self, parent, paciente):
        """Crear una tarjeta individual de paciente"""
        # Frame de la tarjeta (apilado horizontalmente)
        frame_tarjeta = tk.Frame(
            parent,
            bg="#ecf0f1",
            relief=tk.SOLID,
            borderwidth=1,
            width=160,
            height=120
        )
        frame_tarjeta.pack(side=tk.LEFT, padx=3, pady=5)
        frame_tarjeta.pack_propagate(False)
        
        # Contenido de la tarjeta
        frame_contenido = tk.Frame(frame_tarjeta, bg="#ecf0f1", padx=6, pady=6)
        frame_contenido.pack(fill=tk.BOTH, expand=True)
        
        # Nombre del paciente
        tk.Label(
            frame_contenido,
            text=f"👤 {paciente['nombre']}",
            font=("Arial", 9, "bold"),
            bg="#ecf0f1",
            fg="#2c3e50",
            anchor="w",
            wraplength=145
        ).pack(fill=tk.X, pady=(0, 4))
        
        # DNI
        tk.Label(
            frame_contenido,
            text=f"DNI: {paciente['dni']}",
            font=("Arial", 8),
            bg="#ecf0f1",
            fg="#7f8c8d",
            anchor="w"
        ).pack(fill=tk.X, pady=1)
        
        # Edad
        tk.Label(
            frame_contenido,
            text=f"Edad: {paciente['edad']} años",
            font=("Arial", 8),
            bg="#ecf0f1",
            fg="#7f8c8d",
            anchor="w"
        ).pack(fill=tk.X, pady=1)
        
        # Estado
        estado = paciente.get('estado', 'En espera')
        color_estado = {
            'En espera': '#f39c12',
            'En atención': '#3498db',
            'Atendido': '#27ae60'
        }.get(estado, '#95a5a6')
        
        tk.Label(
            frame_contenido,
            text=f"● {estado}",
            font=("Arial", 8, "bold"),
            bg="#ecf0f1",
            fg=color_estado,
            anchor="w"
        ).pack(fill=tk.X, pady=(4, 0))
    
    def _actualizar_reloj(self):
        """Actualizar el reloj en tiempo real"""
        if not self.winfo_exists():
            return
        
        ahora = datetime.now().strftime("%H:%M:%S")
        self.label_reloj.config(text=f"🕐 {ahora}")
        self.after(1000, self._actualizar_reloj)
    
    def _cargar_expedientes(self):
        """Cargar expedientes existentes desde el archivo JSON"""
        try:
            os.makedirs(os.path.dirname(EXPEDIENTES_FILE), exist_ok=True)
            if os.path.exists(EXPEDIENTES_FILE):
                with open(EXPEDIENTES_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return data.get('expedientes', [])
            return []
        except Exception as e:
            print(f"Error cargando expedientes: {e}")
            return []
    
    def _guardar_expediente(self, expediente):
        """Guardar un expediente en el archivo JSON"""
        try:
            os.makedirs(os.path.dirname(EXPEDIENTES_FILE), exist_ok=True)
            
            # Cargar expedientes existentes
            expedientes = self._cargar_expedientes()
            
            # Agregar nuevo expediente
            expedientes.append(expediente)
            
            # Guardar todo de vuelta
            with open(EXPEDIENTES_FILE, 'w', encoding='utf-8') as f:
                json.dump({'expedientes': expedientes}, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            print(f"Error guardando expediente: {e}")
    
    def _agregar_log(self, mensaje, tipo="info", agregar_separador=False):
        """Agregar un mensaje al log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        self.text_logs.config(state=tk.NORMAL)
        
        # Agregar separador si se solicita
        if agregar_separador:
            self.text_logs.insert(tk.END, "─" * 30 + "\n", "separator")
        
        self.text_logs.insert(tk.END, f"[{timestamp}] ", "timestamp")
        self.text_logs.insert(tk.END, f"{mensaje}\n", tipo)
        self.text_logs.see(tk.END)
        self.text_logs.config(state=tk.DISABLED)
    
    def agregar_paciente(self, paciente_data):
        """Agregar un nuevo paciente a un médico"""
        doctor = paciente_data.get('doctor_asignado')
        
        if doctor and doctor in self.medicos_data:
            self.medicos_data[doctor].append(paciente_data)
            
            # Log con separador
            self._agregar_log(
                f"🆕 Nuevo paciente registrado",
                "info",
                agregar_separador=True
            )
            self._agregar_log(
                f"Paciente: {paciente_data.get('nombre', 'N/A')}",
                "success"
            )
            self._agregar_log(
                f"Asignado a: {doctor}",
                "info"
            )
            
            # Actualizar vista inmediatamente (event-driven)
            self._crear_bloques_medicos()
    
    def cambiar_estado_paciente(self, paciente_id, nuevo_estado):
        """Cambiar el estado de un paciente"""
        for medico, pacientes in self.medicos_data.items():
            for paciente in pacientes:
                if paciente['id'] == paciente_id:
                    paciente['estado'] = nuevo_estado
                    self._agregar_log(
                        f"📋 Estado actualizado",
                        "warning",
                        agregar_separador=True
                    )
                    self._agregar_log(
                        f"Paciente: {paciente.get('nombre', 'N/A')}",
                        "info"
                    )
                    self._agregar_log(
                        f"Estado: {nuevo_estado}",
                        "warning"
                    )
                    self._crear_bloques_medicos()
                    return
    
    def _iniciar_actualizaciones(self):
        """Ya no se usan actualizaciones por polling - ahora es event-driven"""
        pass
    
    def _toggle_simulacion(self):
        """Alternar entre iniciar y pausar simulación"""
        if not self.simulacion_activa:
            self._iniciar_simulacion()
        else:
            self._pausar_simulacion()
    
    def _iniciar_simulacion(self):
        """Inicia la simulación interna de pacientes"""
        self.simulacion_activa = True
        self.btn_simulacion.config(
            text="⏸️ Pausar Simulación",
            bg="#e74c3c"
        )
        self._agregar_log("🚀 Simulación iniciada", "success", agregar_separador=True)
        
        # Inicializar médicos si no existen
        if not self.medicos_data:
            for medico in self.medicos_simulados:
                self.medicos_data[medico] = []
            self._crear_bloques_medicos()
        
        # Crear threads productores (generadores de pacientes)
        for i in range(2):  # 2 productores
            thread = threading.Thread(
                target=self._productor_pacientes,
                args=(f"Productor-{i+1}",),
                daemon=True
            )
            thread.start()
            self.threads_simulacion.append(thread)
        
        # Crear threads consumidores (médicos atendiendo)
        for medico in self.medicos_simulados:
            thread = threading.Thread(
                target=self._consumidor_pacientes,
                args=(medico,),
                daemon=True
            )
            thread.start()
            self.threads_simulacion.append(thread)
    
    def _pausar_simulacion(self):
        """Pausa la simulación"""
        self.simulacion_activa = False
        self.btn_simulacion.config(
            text="▶️ Iniciar Simulación",
            bg="#27ae60"
        )
        self._agregar_log("⏸️ Simulación pausada", "warning", agregar_separador=True)
        self.threads_simulacion.clear()
    
    def _productor_pacientes(self, nombre_productor):
        """Thread productor que genera pacientes automáticamente"""
        nombres = [
            "Juan Pérez", "María García", "Carlos López", "Ana Martínez",
            "Luis Rodríguez", "Carmen Sánchez", "José Hernández", "Laura Torres",
            "Miguel Ramírez", "Isabel Flores", "Pedro Jiménez", "Rosa Morales"
        ]
        
        diagnosticos = [
            "Fractura de brazo", "Dolor abdominal", "Fiebre alta",
            "Dolor de pecho", "Herida profunda", "Dificultad respiratoria",
            "Mareos y náuseas", "Dolor de cabeza", "Esguince de tobillo"
        ]
        
        while self.simulacion_activa:
            try:
                # Generar paciente aleatorio
                paciente = {
                    'id': self.paciente_id_counter,
                    'nombre': random.choice(nombres),
                    'apellidos': '',
                    'dni': f"{random.randint(10000000, 99999999)}",
                    'telefono': f"9{random.randint(10000000, 99999999)}",
                    'edad': random.randint(18, 85),
                    'genero': random.choice(['Masculino', 'Femenino']),
                    'prioridad': random.choice(['Baja', 'Normal', 'Urgente']),
                    'sintomas': random.choice(diagnosticos),
                    'fecha_registro': datetime.now().strftime("%d/%m/%Y %H:%M"),
                    'estado': 'Esperando',
                    'doctor': random.choice(self.medicos_simulados)
                }
                self.paciente_id_counter += 1
                
                # Agregar a la UI
                self.after(0, lambda p=paciente: self._agregar_paciente_simulado(p, nombre_productor))
                
                # Esperar tiempo aleatorio (2-5 segundos)
                time.sleep(random.uniform(2, 5))
                
            except Exception as e:
                break
    
    def _consumidor_pacientes(self, medico_nombre):
        """Thread consumidor que atiende pacientes"""
        while self.simulacion_activa:
            try:
                # Buscar pacientes del médico
                pacientes = self.medicos_data.get(medico_nombre, [])
                pacientes_esperando = [p for p in pacientes if p['estado'] == 'Esperando']
                
                if pacientes_esperando:
                    # Atender el primer paciente
                    paciente = pacientes_esperando[0]
                    
                    # Cambiar estado a "Atendiendo"
                    self.after(0, lambda: self._cambiar_estado_paciente(paciente['id'], 'Atendiendo', medico_nombre))
                    
                    # Simular tiempo de atención (3-6 segundos)
                    tiempo_atencion = random.uniform(3, 6)
                    time.sleep(tiempo_atencion)
                    
                    # Completar atención
                    self.after(0, lambda: self._completar_atencion(paciente['id'], medico_nombre))
                else:
                    # No hay pacientes, esperar
                    time.sleep(1)
                    
            except Exception as e:
                break
    
    def _agregar_paciente_simulado(self, paciente, productor):
        """Agrega un paciente generado por la simulación"""
        medico = paciente['doctor']
        if medico in self.medicos_data:
            self.medicos_data[medico].append(paciente)
            
            # Registrar hora de llegada para el tracking
            self.expedientes_tracking[paciente['id']] = {
                'nombre': paciente['nombre'],
                'prioridad': self._convertir_prioridad_texto_a_numero(paciente['prioridad']),
                'diagnostico': paciente['sintomas'],
                'hora_llegada': datetime.now().isoformat(),
                'medico_asignado': medico,
                'estado': 'En espera'
            }
            
            self._agregar_log(
                f"🆕 Nuevo paciente generado",
                "success",
                agregar_separador=True
            )
            self._agregar_log(
                f"Productor: {productor}",
                "info"
            )
            self._agregar_log(
                f"Paciente: {paciente['nombre']}",
                "success"
            )
            self._agregar_log(
                f"Prioridad: {paciente['prioridad']}",
                "info"
            )
            self._agregar_log(
                f"Asignado a: {medico}",
                "info"
            )
            
            self._crear_bloques_medicos()
    
    def _convertir_prioridad_texto_a_numero(self, prioridad_texto):
        """Convierte prioridad de texto a número"""
        conversion = {
            'Baja': 1,
            'Normal': 2,
            'Urgente': 3
        }
        return conversion.get(prioridad_texto, 2)
    
    def _cambiar_estado_paciente(self, paciente_id, nuevo_estado, medico_nombre):
        """Cambia el estado de un paciente"""
        if medico_nombre in self.medicos_data:
            for paciente in self.medicos_data[medico_nombre]:
                if paciente['id'] == paciente_id:
                    paciente['estado'] = nuevo_estado
                    
                    # Registrar hora de atención
                    if paciente_id in self.expedientes_tracking:
                        self.expedientes_tracking[paciente_id]['hora_atencion'] = datetime.now().isoformat()
                        self.expedientes_tracking[paciente_id]['estado'] = 'En atención'
                    
                    self._agregar_log(
                        f"🩺 Atención iniciada",
                        "info",
                        agregar_separador=True
                    )
                    self._agregar_log(
                        f"Médico: {medico_nombre}",
                        "info"
                    )
                    self._agregar_log(
                        f"Paciente: {paciente['nombre']}",
                        "info"
                    )
                    
                    self._crear_bloques_medicos()
                    break
    
    def _completar_atencion(self, paciente_id, medico_nombre):
        """Completa la atención y remueve al paciente"""
        if medico_nombre in self.medicos_data:
            pacientes = self.medicos_data[medico_nombre]
            for i, paciente in enumerate(pacientes):
                if paciente['id'] == paciente_id:
                    nombre_paciente = paciente['nombre']
                    
                    # Crear expediente completo
                    if paciente_id in self.expedientes_tracking:
                        tracking = self.expedientes_tracking[paciente_id]
                        hora_llegada = datetime.fromisoformat(tracking['hora_llegada'])
                        hora_atencion = datetime.fromisoformat(tracking['hora_atencion'])
                        hora_fin = datetime.now()
                        
                        # Calcular tiempo de espera
                        tiempo_espera = (hora_atencion - hora_llegada).total_seconds()
                        
                        # Crear expediente con la estructura correcta
                        expediente = {
                            'id': paciente_id,
                            'nombre': tracking['nombre'],
                            'prioridad': tracking['prioridad'],
                            'diagnostico': tracking['diagnostico'],
                            'estado': 'Atendido',
                            'hora_llegada': tracking['hora_llegada'],
                            'hora_atencion': tracking['hora_atencion'],
                            'medico_asignado': tracking['medico_asignado'],
                            'tiempo_espera': round(tiempo_espera, 6),
                            'fecha_registro': hora_fin.isoformat()
                        }
                        
                        # Guardar en el archivo JSON
                        self._guardar_expediente(expediente)
                        
                        # Limpiar tracking
                        del self.expedientes_tracking[paciente_id]
                    
                    del pacientes[i]
                    
                    self._agregar_log(
                        f"✅ Atención completada",
                        "success",
                        agregar_separador=True
                    )
                    self._agregar_log(
                        f"Médico: {medico_nombre}",
                        "success"
                    )
                    self._agregar_log(
                        f"Paciente: {nombre_paciente}",
                        "success"
                    )
                    self._agregar_log(
                        f"📋 Expediente guardado",
                        "info"
                    )
                    
                    self._crear_bloques_medicos()
                    break
    
    def on_closing(self):
        """Manejar cierre de ventana (modo no standalone)"""
        if self.socket:
            try:
                self.socket.close()
            except:
                pass
        self.destroy()
    
    def _on_closing_standalone(self):
        """Manejar cierre de ventana standalone"""
        # Detener simulación
        self.simulacion_activa = False
        
        if self.socket:
            try:
                self.socket.close()
            except:
                pass
        self.destroy()
        if self._standalone_root:
            self._standalone_root.quit()
            self._standalone_root.destroy()


def main():
    """Ejecutar panel de hospital de forma independiente"""
    print("=" * 60)
    print("🏥 PANEL PRINCIPAL DEL HOSPITAL")
    print("=" * 60)
    print("\n💡 Este panel se conecta al sistema hospitalario")
    print("   Si el sistema no está activo, mostrará la interfaz")
    print("   sin conexión funcional.")
    print("\n📋 Para iniciar el servidor:")
    print("   python servidor.py")
    print("\n💡 Para abrir múltiples ventanas:")
    print("   python launcher.py")
    print("\n=" * 60 + "\n")
    
    app = PanelHospital()
    app.mainloop()


if __name__ == "__main__":
    main()

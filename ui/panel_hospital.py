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

# Agregar directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


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
        
        # Log inicial
        self._agregar_log("Sistema iniciado", "info")
        self._agregar_log("Esperando pacientes...", "info")
        
        # ===== SECCIÓN DERECHA: MÉDICOS Y PACIENTES (85%) =====
        frame_medicos_container = tk.Frame(frame_main, bg="#ecf0f1")
        frame_medicos_container.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Título
        tk.Label(
            frame_medicos_container,
            text="👨‍⚕️ MÉDICOS Y PACIENTES ASIGNADOS",
            font=("Arial", 14, "bold"),
            bg="#3498db",
            fg="white",
            pady=10
        ).pack(fill=tk.X)
        
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
        
        # Lista de pacientes
        if pacientes:
            for paciente in pacientes:
                self._crear_tarjeta_paciente(frame_medico, paciente)
        else:
            tk.Label(
                frame_medico,
                text="Sin pacientes asignados",
                font=("Arial", 10, "italic"),
                bg="white",
                fg="#95a5a6"
            ).pack(pady=10)
    
    def _crear_tarjeta_paciente(self, parent, paciente):
        """Crear una tarjeta individual de paciente"""
        # Frame de la tarjeta
        frame_tarjeta = tk.Frame(
            parent,
            bg="#ecf0f1",
            relief=tk.SOLID,
            borderwidth=1
        )
        frame_tarjeta.pack(fill=tk.X, pady=3)
        
        # Contenido de la tarjeta
        frame_contenido = tk.Frame(frame_tarjeta, bg="#ecf0f1", padx=10, pady=8)
        frame_contenido.pack(fill=tk.X)
        
        # Nombre del paciente
        tk.Label(
            frame_contenido,
            text=f"👤 {paciente['nombre']}",
            font=("Arial", 11, "bold"),
            bg="#ecf0f1",
            fg="#2c3e50",
            anchor="w"
        ).grid(row=0, column=0, columnspan=2, sticky="w", pady=2)
        
        # DNI y Edad
        tk.Label(
            frame_contenido,
            text=f"DNI: {paciente['dni']}",
            font=("Arial", 9),
            bg="#ecf0f1",
            fg="#7f8c8d",
            anchor="w"
        ).grid(row=1, column=0, sticky="w")
        
        tk.Label(
            frame_contenido,
            text=f"Edad: {paciente['edad']} años",
            font=("Arial", 9),
            bg="#ecf0f1",
            fg="#7f8c8d",
            anchor="w"
        ).grid(row=1, column=1, sticky="w", padx=10)
        
        # Fecha de registro
        tk.Label(
            frame_contenido,
            text=f"📅 Registro: {paciente['fecha_registro']}",
            font=("Arial", 9),
            bg="#ecf0f1",
            fg="#7f8c8d",
            anchor="w"
        ).grid(row=2, column=0, columnspan=2, sticky="w", pady=2)
        
        # Estado
        estado = paciente.get('estado', 'En espera')
        color_estado = {
            'En espera': '#f39c12',
            'En atención': '#3498db',
            'Atendido': '#27ae60'
        }.get(estado, '#95a5a6')
        
        tk.Label(
            frame_contenido,
            text=f"🔔 {estado}",
            font=("Arial", 9, "bold"),
            bg="#ecf0f1",
            fg=color_estado,
            anchor="w"
        ).grid(row=3, column=0, columnspan=2, sticky="w", pady=2)
    
    def _actualizar_reloj(self):
        """Actualizar el reloj en tiempo real"""
        if not self.winfo_exists():
            return
        
        ahora = datetime.now().strftime("%H:%M:%S")
        self.label_reloj.config(text=f"🕐 {ahora}")
        self.after(1000, self._actualizar_reloj)
    
    def _agregar_log(self, mensaje, tipo="info"):
        """Agregar un mensaje al log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        self.text_logs.config(state=tk.NORMAL)
        self.text_logs.insert(tk.END, f"[{timestamp}] ", "timestamp")
        self.text_logs.insert(tk.END, f"{mensaje}\n", tipo)
        self.text_logs.see(tk.END)
        self.text_logs.config(state=tk.DISABLED)
    
    def agregar_paciente(self, paciente_data):
        """Agregar un nuevo paciente a un médico"""
        doctor = paciente_data.get('doctor_asignado')
        
        if doctor and doctor in self.medicos_data:
            self.medicos_data[doctor].append(paciente_data)
            
            # Log
            self._agregar_log(
                f"Paciente {paciente_data.get('nombre', 'N/A')} registrado",
                "success"
            )
            self._agregar_log(
                f"Asignado a {doctor}",
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
                        f"Paciente ID {paciente_id}: {nuevo_estado}",
                        "warning"
                    )
                    self._crear_bloques_medicos()
                    return
    
    def _iniciar_actualizaciones(self):
        """Ya no se usan actualizaciones por polling - ahora es event-driven"""
        pass
    
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

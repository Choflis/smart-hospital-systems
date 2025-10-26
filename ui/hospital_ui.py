# ui/hospital_ui.py
"""
Interfaz Gráfica Moderna para Smart Hospital System
----------------------------------------------------
UI con diseño profesional tipo hospital con navegación lateral
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
from datetime import datetime

class HospitalUI:
    def __init__(self, buffer, consumidores, productor):
        self.buffer = buffer
        self.consumidores = consumidores
        self.productor = productor
        
        # Crear ventana principal
        self.root = tk.Tk()
        self.root.title("Smart Hospital Management System")
        self.root.geometry("1400x800")
        self.root.state('zoomed')  # Maximizar ventana
        
        # Colores del tema médico profesional
        self.colors = {
            "primary": "#1e3a5f",      # Azul oscuro profesional
            "secondary": "#2ecc71",     # Verde médico
            "accent": "#3498db",        # Azul claro
            "sidebar": "#2c3e50",       # Gris oscuro
            "bg": "#ecf0f1",           # Gris claro fondo
            "card": "#ffffff",          # Blanco
            "text": "#2c3e50",         # Texto oscuro
            "text_light": "#7f8c8d",   # Texto claro
            "danger": "#e74c3c",        # Rojo
            "warning": "#f39c12",       # Naranja
            "success": "#27ae60",       # Verde oscuro
            "hover": "#34495e"          # Hover sidebar
        }
        
        self.current_section = "dashboard"
        self.setup_ui()
        self.show_section("dashboard")
        self.update_stats()
        
    def setup_ui(self):
        """Configura todos los componentes de la interfaz"""
        
        # === HEADER ===
        self.create_header()
        
        # === CONTAINER PRINCIPAL ===
        main_container = tk.Frame(self.root, bg=self.colors["bg"])
        main_container.pack(fill="both", expand=True)
        
        # === SIDEBAR ===
        self.create_sidebar(main_container)
        
        # === CONTENT AREA ===
        self.content_area = tk.Frame(main_container, bg=self.colors["bg"])
        self.content_area.pack(side="right", fill="both", expand=True)
        
        # Crear todas las secciones (ocultas inicialmente)
        self.sections = {}
        self.create_dashboard_section()
        self.create_patients_section()
        self.create_doctors_section()
        self.create_statistics_section()
    
    def create_header(self):
        """Crea el header profesional"""
        header = tk.Frame(self.root, bg=self.colors["primary"], height=70)
        header.pack(fill="x", side="top")
        header.pack_propagate(False)
        
        # Logo y título
        title_frame = tk.Frame(header, bg=self.colors["primary"])
        title_frame.pack(side="left", padx=30, pady=15)
        
        tk.Label(
            title_frame,
            text="SMART HOSPITAL",
            font=("Segoe UI", 20, "bold"),
            bg=self.colors["primary"],
            fg="white"
        ).pack(side="left")
        
        tk.Label(
            title_frame,
            text="Management System",
            font=("Segoe UI", 10),
            bg=self.colors["primary"],
            fg="#95a5a6"
        ).pack(side="left", padx=(10, 0))
        
        # Información de usuario y hora
        info_frame = tk.Frame(header, bg=self.colors["primary"])
        info_frame.pack(side="right", padx=30)
        
        self.time_label = tk.Label(
            info_frame,
            text="",
            font=("Segoe UI", 10),
            bg=self.colors["primary"],
            fg="white"
        )
        self.time_label.pack(side="right", padx=15)
        
        tk.Label(
            info_frame,
            text="Admin User",
            font=("Segoe UI", 10, "bold"),
            bg=self.colors["primary"],
            fg="white"
        ).pack(side="right", padx=15)
    
    def create_sidebar(self, parent):
        """Crea el menú lateral de navegación"""
        sidebar = tk.Frame(parent, bg=self.colors["sidebar"], width=250)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)
        
        # Espaciado superior
        tk.Frame(sidebar, bg=self.colors["sidebar"], height=20).pack()
        
        # Menú items
        menu_items = [
            ("Dashboard", "dashboard"),
            ("Gestión de Pacientes", "patients"),
            ("Médicos Activos", "doctors"),
            ("Estadísticas", "statistics"),
        ]
        
        self.menu_buttons = {}
        
        for text, section in menu_items:
            btn = tk.Button(
                sidebar,
                text=text,
                font=("Segoe UI", 11),
                bg=self.colors["sidebar"],
                fg="white",
                activebackground=self.colors["hover"],
                activeforeground="white",
                bd=0,
                cursor="hand2",
                anchor="w",
                padx=30,
                pady=15,
                command=lambda s=section: self.show_section(s)
            )
            btn.pack(fill="x", pady=2)
            self.menu_buttons[section] = btn
        
        # Espaciador
        tk.Frame(sidebar, bg=self.colors["sidebar"]).pack(fill="both", expand=True)
        
        # Botón de salida
        exit_btn = tk.Button(
            sidebar,
            text="Cerrar Sistema",
            font=("Segoe UI", 10),
            bg="#c0392b",
            fg="white",
            activebackground="#e74c3c",
            activeforeground="white",
            bd=0,
            cursor="hand2",
            pady=12,
            command=self.detener_sistema
        )
        exit_btn.pack(fill="x", side="bottom", pady=20, padx=20)
    
    def show_section(self, section_name):
        """Muestra una sección y oculta las demás"""
        # Ocultar todas las secciones
        for section in self.sections.values():
            section.pack_forget()
        
        # Mostrar la sección seleccionada
        if section_name in self.sections:
            self.sections[section_name].pack(fill="both", expand=True, padx=30, pady=20)
        
        # Actualizar estilos de botones del menú
        for btn_name, btn in self.menu_buttons.items():
            if btn_name == section_name:
                btn.config(bg=self.colors["hover"], font=("Segoe UI", 11, "bold"))
            else:
                btn.config(bg=self.colors["sidebar"], font=("Segoe UI", 11))
        
        self.current_section = section_name
    
    def create_dashboard_section(self):
        """Crea la sección de Dashboard"""
        dashboard = tk.Frame(self.content_area, bg=self.colors["bg"])
        self.sections["dashboard"] = dashboard
        
        # Título de sección
        tk.Label(
            dashboard,
            text="Panel de Control",
            font=("Segoe UI", 24, "bold"),
            bg=self.colors["bg"],
            fg=self.colors["text"]
        ).pack(anchor="w", pady=(0, 20))
        
        # Grid de tarjetas de estadísticas
        stats_grid = tk.Frame(dashboard, bg=self.colors["bg"])
        stats_grid.pack(fill="x", pady=(0, 20))
        
        # Crear tarjetas de métricas
        self.metric_cards = {}
        metrics = [
            ("Pacientes en Espera", "patients_waiting", self.colors["accent"]),
            ("Médicos Activos", "doctors_active", self.colors["success"]),
            ("Capacidad del Sistema", "capacity", self.colors["warning"]),
            ("Estado del Sistema", "system_status", self.colors["primary"])
        ]
        
        for i, (title, key, color) in enumerate(metrics):
            card = self.create_metric_card(stats_grid, title, "0", color)
            card.grid(row=0, column=i, padx=10, sticky="ew")
            stats_grid.columnconfigure(i, weight=1)
            self.metric_cards[key] = card
        
        # Gráfico de actividad reciente
        activity_frame = tk.Frame(dashboard, bg=self.colors["card"], relief="raised", bd=1)
        activity_frame.pack(fill="both", expand=True, pady=(10, 0))
        
        tk.Label(
            activity_frame,
            text="Lista de Pacientes en Tiempo Real",
            font=("Segoe UI", 14, "bold"),
            bg=self.colors["card"],
            fg=self.colors["text"]
        ).pack(anchor="w", padx=20, pady=15)
        
        # Listbox para pacientes en dashboard
        list_frame = tk.Frame(activity_frame, bg=self.colors["card"])
        list_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side="right", fill="y")
        
        self.dashboard_listbox = tk.Listbox(
            list_frame,
            font=("Consolas", 10),
            bg="#f8f9fa",
            fg=self.colors["text"],
            relief="flat",
            yscrollcommand=scrollbar.set,
            selectmode="single",
            height=10
        )
        self.dashboard_listbox.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.dashboard_listbox.yview)
    
    def create_metric_card(self, parent, title, value, color):
        """Crea una tarjeta de métrica"""
        card = tk.Frame(parent, bg=self.colors["card"], relief="raised", bd=1)
        
        # Barra de color superior
        tk.Frame(card, bg=color, height=4).pack(fill="x")
        
        # Contenido
        content = tk.Frame(card, bg=self.colors["card"])
        content.pack(fill="both", expand=True, padx=20, pady=20)
        
        tk.Label(
            content,
            text=title,
            font=("Segoe UI", 10),
            bg=self.colors["card"],
            fg=self.colors["text_light"]
        ).pack(anchor="w")
        
        value_label = tk.Label(
            content,
            text=value,
            font=("Segoe UI", 28, "bold"),
            bg=self.colors["card"],
            fg=self.colors["text"]
        )
        value_label.pack(anchor="w", pady=(5, 0))
        
        # Guardar referencia al label del valor
        card.value_label = value_label
        
        return card
    
    def create_patients_section(self):
        """Crea la sección de gestión de pacientes"""
        patients = tk.Frame(self.content_area, bg=self.colors["bg"])
        self.sections["patients"] = patients
        
        # Título
        tk.Label(
            patients,
            text="Gestión de Pacientes",
            font=("Segoe UI", 24, "bold"),
            bg=self.colors["bg"],
            fg=self.colors["text"]
        ).pack(anchor="w", pady=(0, 20))
        
        # Formulario de registro
        form_card = tk.Frame(patients, bg=self.colors["card"], relief="raised", bd=1)
        form_card.pack(fill="x", pady=(0, 20))
        
        tk.Label(
            form_card,
            text="Registrar Nuevo Paciente",
            font=("Segoe UI", 16, "bold"),
            bg=self.colors["card"],
            fg=self.colors["text"]
        ).pack(anchor="w", padx=30, pady=(20, 10))
        
        self.create_patient_form(form_card)
    
    def create_patient_form(self, parent):
        """Crea el formulario para registrar pacientes"""
        form_frame = tk.Frame(parent, bg=self.colors["card"])
        form_frame.pack(fill="x", padx=30, pady=(0, 20))
        
        # Grid para el formulario
        fields = [
            ("Nombre Completo:", "nombre"),
            ("Edad:", "edad"),
            ("Género:", "genero"),
            ("Síntomas:", "sintomas")
        ]
        
        self.entries = {}
        
        for i, (label_text, field_name) in enumerate(fields):
            # Label
            tk.Label(
                form_frame,
                text=label_text,
                font=("Segoe UI", 10),
                bg=self.colors["card"],
                fg=self.colors["text"]
            ).grid(row=i, column=0, sticky="w", pady=10, padx=(0, 20))
            
            # Entry o Combobox
            if field_name == "genero":
                entry = ttk.Combobox(
                    form_frame,
                    values=["Masculino", "Femenino", "Otro"],
                    font=("Segoe UI", 10),
                    state="readonly",
                    width=40
                )
                entry.set("Masculino")
            else:
                entry = tk.Entry(
                    form_frame,
                    font=("Segoe UI", 10),
                    bg="#f8f9fa",
                    relief="solid",
                    bd=1,
                    width=40
                )
            
            entry.grid(row=i, column=1, sticky="ew", pady=10)
            self.entries[field_name] = entry
        
        form_frame.columnconfigure(1, weight=1)
        
        # Botón de agregar
        btn_agregar = tk.Button(
            parent,
            text="Registrar Paciente",
            font=("Segoe UI", 11, "bold"),
            bg=self.colors["success"],
            fg="white",
            activebackground="#229954",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            command=self.agregar_paciente,
            padx=30,
            pady=12
        )
        btn_agregar.pack(pady=(0, 20), padx=30, anchor="e")
    
    def create_doctors_section(self):
        """Crea la sección de médicos activos"""
        doctors = tk.Frame(self.content_area, bg=self.colors["bg"])
        self.sections["doctors"] = doctors
        
        # Título
        tk.Label(
            doctors,
            text="Médicos Activos",
            font=("Segoe UI", 24, "bold"),
            bg=self.colors["bg"],
            fg=self.colors["text"]
        ).pack(anchor="w", pady=(0, 20))
        
        # Tarjeta de médicos
        doctors_card = tk.Frame(doctors, bg=self.colors["card"], relief="raised", bd=1)
        doctors_card.pack(fill="both", expand=True)
        
        tk.Label(
            doctors_card,
            text="Estado de los Médicos del Sistema",
            font=("Segoe UI", 14, "bold"),
            bg=self.colors["card"],
            fg=self.colors["text"]
        ).pack(anchor="w", padx=30, pady=20)
        
        # Lista de médicos
        self.doctors_frame = tk.Frame(doctors_card, bg=self.colors["card"])
        self.doctors_frame.pack(fill="both", expand=True, padx=30, pady=(0, 20))
    
    def create_statistics_section(self):
        """Crea la sección de estadísticas"""
        statistics = tk.Frame(self.content_area, bg=self.colors["bg"])
        self.sections["statistics"] = statistics
        
        # Título
        tk.Label(
            statistics,
            text="Estadísticas del Sistema",
            font=("Segoe UI", 24, "bold"),
            bg=self.colors["bg"],
            fg=self.colors["text"]
        ).pack(anchor="w", pady=(0, 20))
        
        # Tarjeta de estadísticas
        stats_card = tk.Frame(statistics, bg=self.colors["card"], relief="raised", bd=1)
        stats_card.pack(fill="both", expand=True)
        
        tk.Label(
            stats_card,
            text="Métricas en Tiempo Real",
            font=("Segoe UI", 14, "bold"),
            bg=self.colors["card"],
            fg=self.colors["text"]
        ).pack(anchor="w", padx=30, pady=20)
        
        # Contenido de estadísticas
        stats_content = tk.Frame(stats_card, bg=self.colors["card"])
        stats_content.pack(fill="both", expand=True, padx=30, pady=(0, 20))
        
        self.stat_labels = {}
        
        stats = [
            ("Total de Pacientes en Espera:", "pacientes_espera", "0"),
            ("Médicos Activos:", "medicos_activos", "0"),
            ("Capacidad del Buffer:", "capacidad", "0/0"),
            ("Tiempo de Actividad:", "uptime", "00:00:00")
        ]
        
        for i, (label_text, key, default) in enumerate(stats):
            frame = tk.Frame(stats_content, bg=self.colors["card"])
            frame.pack(fill="x", pady=15)
            
            tk.Label(
                frame,
                text=label_text,
                font=("Segoe UI", 12),
                bg=self.colors["card"],
                fg=self.colors["text"]
            ).pack(side="left")
            
            value_label = tk.Label(
                frame,
                text=default,
                font=("Segoe UI", 14, "bold"),
                bg=self.colors["card"],
                fg=self.colors["accent"]
            )
            value_label.pack(side="right")
            
            self.stat_labels[key] = value_label
    
    def agregar_paciente(self):
        """Agrega un paciente al buffer"""
        try:
            nombre = self.entries["nombre"].get().strip()
            edad = self.entries["edad"].get().strip()
            genero = self.entries["genero"].get()
            sintomas = self.entries["sintomas"].get().strip()
            
            if not all([nombre, edad, sintomas]):
                messagebox.showwarning(
                    "Campos incompletos",
                    "Por favor, completa todos los campos"
                )
                return
            
            edad = int(edad)
            
            # Crear objeto paciente
            from models.paciente import Paciente
            paciente = Paciente(nombre, edad, genero, sintomas)
            
            # Agregar al buffer
            exito = self.buffer.agregar_paciente(paciente)
            
            if exito:
                messagebox.showinfo(
                    "Registro Exitoso",
                    f"Paciente {nombre} registrado correctamente"
                )
                # Limpiar campos
                self.entries["nombre"].delete(0, tk.END)
                self.entries["edad"].delete(0, tk.END)
                self.entries["sintomas"].delete(0, tk.END)
            else:
                messagebox.showerror(
                    "Buffer Lleno",
                    "No se puede agregar el paciente. Sala de espera llena."
                )
        
        except ValueError:
            messagebox.showerror(
                "Error de Validación",
                "La edad debe ser un número válido"
            )
        except Exception as e:
            messagebox.showerror("Error", f"Error al agregar paciente: {e}")
    
    def update_stats(self):
        """Actualiza estadísticas en tiempo real"""
        if not self.root.winfo_exists():
            return
        
        try:
            # Obtener datos
            pacientes_espera = len(self.buffer)
            medicos_activos = sum(1 for c in self.consumidores if c.is_alive())
            capacidad_buffer = self.buffer.cola.maxsize
            
            # Actualizar tarjetas de métricas en dashboard
            if hasattr(self, 'metric_cards'):
                self.metric_cards["patients_waiting"].value_label.config(text=str(pacientes_espera))
                self.metric_cards["doctors_active"].value_label.config(text=str(medicos_activos))
                self.metric_cards["capacity"].value_label.config(text=f"{pacientes_espera}/{capacidad_buffer}")
                
                # Estado del sistema
                if pacientes_espera == capacidad_buffer:
                    status_text = "COMPLETO"
                    status_color = self.colors["danger"]
                elif pacientes_espera >= capacidad_buffer * 0.7:
                    status_text = "ALTO"
                    status_color = self.colors["warning"]
                else:
                    status_text = "NORMAL"
                    status_color = self.colors["success"]
                
                self.metric_cards["system_status"].value_label.config(
                    text=status_text,
                    fg=status_color
                )
            
            # Actualizar estadísticas en la sección de estadísticas
            if hasattr(self, 'stat_labels'):
                self.stat_labels["pacientes_espera"].config(text=str(pacientes_espera))
                self.stat_labels["medicos_activos"].config(text=str(medicos_activos))
                self.stat_labels["capacidad"].config(text=f"{pacientes_espera}/{capacidad_buffer}")
            
            # Actualizar lista de pacientes en dashboard
            if hasattr(self, 'dashboard_listbox'):
                self.dashboard_listbox.delete(0, tk.END)
                pacientes = self.buffer.obtener_lista_pacientes()
                
                if pacientes:
                    for i, p in enumerate(pacientes, 1):
                        self.dashboard_listbox.insert(
                            tk.END,
                            f"{i}. {p.nombre} | {p.edad} años | {p.genero} | {p.sintomas[:50]}..."
                        )
                else:
                    self.dashboard_listbox.insert(tk.END, "   --- No hay pacientes en espera ---")
            
            # Actualizar médicos en la sección de médicos
            self.update_doctors_display()
            
            # Actualizar hora en header
            now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            self.time_label.config(text=now)
        
        except Exception as e:
            print(f"Error actualizando stats: {e}")
        
        # Repetir cada segundo
        self.root.after(1000, self.update_stats)
    
    def update_doctors_display(self):
        """Actualiza la visualización de médicos"""
        if not hasattr(self, 'doctors_frame'):
            return
        
        # Limpiar frame
        for widget in self.doctors_frame.winfo_children():
            widget.destroy()
        
        # Crear tarjeta para cada médico
        for i, consumidor in enumerate(self.consumidores):
            doctor_card = tk.Frame(self.doctors_frame, bg="#f8f9fa", relief="raised", bd=1)
            doctor_card.pack(fill="x", pady=10)
            
            # Indicador de estado
            status_color = self.colors["success"] if consumidor.is_alive() else self.colors["danger"]
            status_text = "Activo" if consumidor.is_alive() else "Inactivo"
            
            tk.Frame(doctor_card, bg=status_color, height=4).pack(fill="x")
            
            content = tk.Frame(doctor_card, bg="#f8f9fa")
            content.pack(fill="x", padx=20, pady=15)
            
            tk.Label(
                content,
                text=f"Médico #{consumidor.id}",
                font=("Segoe UI", 12, "bold"),
                bg="#f8f9fa",
                fg=self.colors["text"]
            ).pack(side="left")
            
            tk.Label(
                content,
                text=status_text,
                font=("Segoe UI", 10, "bold"),
                bg="#f8f9fa",
                fg=status_color
            ).pack(side="right")
    
    def detener_sistema(self):
        """Detiene el sistema completo"""
        respuesta = messagebox.askyesno(
            "Confirmar Cierre",
            "¿Está seguro de detener el sistema?"
        )
        
        if respuesta:
            print("\n[SISTEMA] Deteniendo el sistema...")
            
            # Detener productor
            self.productor.detener()
            
            # Detener consumidores
            for c in self.consumidores:
                c.detener()
            
            # Esperar a que los hilos terminen (máximo 3 segundos)
            print("[SISTEMA] Esperando que los hilos terminen...")
            
            # Esperar al productor
            if self.productor.is_alive():
                self.productor.join(timeout=1)
            
            # Esperar a los consumidores
            for c in self.consumidores:
                if c.is_alive():
                    c.join(timeout=1)
            
            print("[SISTEMA] Todos los hilos detenidos.")
            messagebox.showinfo("Sistema Detenido", "El sistema se ha detenido correctamente")
            
            # Cerrar ventana
            self.root.after(100, self.root.destroy)
    
    def run(self):
        """Inicia la interfaz gráfica"""
        self.root.mainloop()

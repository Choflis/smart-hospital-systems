# ui/hospital_ui.py
"""
Interfaz Gráfica Moderna para Smart Hospital System
----------------------------------------------------
UI con diseño moderno tipo dashboard médico
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
        self.root.title("🏥 Smart Hospital System")
        self.root.geometry("1200x700")
        self.root.configure(bg="#f0f4f8")
        
        # Colores del tema médico
        self.colors = {
            "primary": "#2c3e50",
            "secondary": "#3498db",
            "success": "#27ae60",
            "danger": "#e74c3c",
            "warning": "#f39c12",
            "bg": "#f0f4f8",
            "card": "#ffffff",
            "text": "#2c3e50"
        }
        
        self.setup_ui()
        self.update_stats()
        
    def setup_ui(self):
        """Configura todos los componentes de la interfaz"""
        
        # === HEADER ===
        header = tk.Frame(self.root, bg=self.colors["primary"], height=80)
        header.pack(fill="x", side="top")
        
        title_label = tk.Label(
            header,
            text="🏥 SISTEMA HOSPITALARIO INTELIGENTE",
            font=("Segoe UI", 24, "bold"),
            bg=self.colors["primary"],
            fg="white"
        )
        title_label.pack(pady=20)
        
        # === CONTAINER PRINCIPAL ===
        main_container = tk.Frame(self.root, bg=self.colors["bg"])
        main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # === COLUMNA IZQUIERDA: Formulario ===
        left_panel = tk.Frame(main_container, bg=self.colors["bg"])
        left_panel.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        self.create_form_card(left_panel)
        self.create_stats_card(left_panel)
        
        # === COLUMNA DERECHA: Lista de pacientes ===
        right_panel = tk.Frame(main_container, bg=self.colors["bg"])
        right_panel.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        self.create_patients_list(right_panel)
        self.create_system_status(right_panel)
    
    def create_form_card(self, parent):
        """Tarjeta de formulario para agregar pacientes"""
        card = tk.Frame(parent, bg=self.colors["card"], relief="raised", bd=1)
        card.pack(fill="x", pady=(0, 20))
        
        # Título
        title_frame = tk.Frame(card, bg=self.colors["secondary"], height=40)
        title_frame.pack(fill="x")
        
        tk.Label(
            title_frame,
            text="➕ Registrar Nuevo Paciente",
            font=("Segoe UI", 14, "bold"),
            bg=self.colors["secondary"],
            fg="white"
        ).pack(pady=8)
        
        # Formulario
        form_frame = tk.Frame(card, bg=self.colors["card"])
        form_frame.pack(fill="x", padx=20, pady=20)
        
        # Campos
        fields = [
            ("Nombre Completo:", "nombre"),
            ("Edad:", "edad"),
            ("Género:", "genero"),
            ("Síntomas:", "sintomas")
        ]
        
        self.entries = {}
        
        for i, (label_text, field_name) in enumerate(fields):
            tk.Label(
                form_frame,
                text=label_text,
                font=("Segoe UI", 10, "bold"),
                bg=self.colors["card"],
                fg=self.colors["text"]
            ).grid(row=i, column=0, sticky="w", pady=8)
            
            if field_name == "genero":
                entry = ttk.Combobox(
                    form_frame,
                    values=["Masculino", "Femenino", "Otro"],
                    font=("Segoe UI", 10),
                    state="readonly"
                )
                entry.set("Masculino")
            else:
                entry = tk.Entry(
                    form_frame,
                    font=("Segoe UI", 10),
                    bg="#f8f9fa",
                    relief="solid",
                    bd=1
                )
            
            entry.grid(row=i, column=1, sticky="ew", pady=8, padx=(10, 0))
            self.entries[field_name] = entry
        
        form_frame.columnconfigure(1, weight=1)
        
        # Botón agregar
        btn_frame = tk.Frame(card, bg=self.colors["card"])
        btn_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        btn_agregar = tk.Button(
            btn_frame,
            text="✓ AGREGAR PACIENTE",
            font=("Segoe UI", 11, "bold"),
            bg=self.colors["success"],
            fg="white",
            relief="flat",
            cursor="hand2",
            command=self.agregar_paciente,
            padx=20,
            pady=10
        )
        btn_agregar.pack(fill="x")
    
    def create_stats_card(self, parent):
        """Tarjeta de estadísticas"""
        card = tk.Frame(parent, bg=self.colors["card"], relief="raised", bd=1)
        card.pack(fill="x", pady=(0, 20))
        
        # Título
        title_frame = tk.Frame(card, bg=self.colors["warning"], height=40)
        title_frame.pack(fill="x")
        
        tk.Label(
            title_frame,
            text="📊 Estadísticas en Tiempo Real",
            font=("Segoe UI", 14, "bold"),
            bg=self.colors["warning"],
            fg="white"
        ).pack(pady=8)
        
        # Contenido
        stats_frame = tk.Frame(card, bg=self.colors["card"])
        stats_frame.pack(fill="x", padx=20, pady=20)
        
        # Crear labels de estadísticas
        self.stat_labels = {}
        
        stats = [
            ("pacientes_espera", "Pacientes en Espera:", "0"),
            ("medicos_activos", "Médicos Activos:", "0"),
            ("capacidad", "Capacidad Buffer:", "0/0")
        ]
        
        for i, (key, label_text, default) in enumerate(stats):
            frame = tk.Frame(stats_frame, bg=self.colors["card"])
            frame.pack(fill="x", pady=5)
            
            tk.Label(
                frame,
                text=label_text,
                font=("Segoe UI", 10),
                bg=self.colors["card"],
                fg=self.colors["text"]
            ).pack(side="left")
            
            value_label = tk.Label(
                frame,
                text=default,
                font=("Segoe UI", 12, "bold"),
                bg=self.colors["card"],
                fg=self.colors["secondary"]
            )
            value_label.pack(side="right")
            
            self.stat_labels[key] = value_label
    
    def create_patients_list(self, parent):
        """Lista de pacientes en espera"""
        card = tk.Frame(parent, bg=self.colors["card"], relief="raised", bd=1)
        card.pack(fill="both", expand=True, pady=(0, 20))
        
        # Título
        title_frame = tk.Frame(card, bg=self.colors["primary"], height=40)
        title_frame.pack(fill="x")
        
        tk.Label(
            title_frame,
            text="👥 Pacientes en Sala de Espera",
            font=("Segoe UI", 14, "bold"),
            bg=self.colors["primary"],
            fg="white"
        ).pack(pady=8)
        
        # Lista con scrollbar
        list_frame = tk.Frame(card, bg=self.colors["card"])
        list_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side="right", fill="y")
        
        self.patients_listbox = tk.Listbox(
            list_frame,
            font=("Consolas", 10),
            bg="#f8f9fa",
            fg=self.colors["text"],
            relief="flat",
            yscrollcommand=scrollbar.set,
            selectmode="single"
        )
        self.patients_listbox.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.patients_listbox.yview)
    
    def create_system_status(self, parent):
        """Estado del sistema"""
        card = tk.Frame(parent, bg=self.colors["card"], relief="raised", bd=1)
        card.pack(fill="x")
        
        # Título
        title_frame = tk.Frame(card, bg=self.colors["danger"], height=40)
        title_frame.pack(fill="x")
        
        tk.Label(
            title_frame,
            text="⚙️ Estado del Sistema",
            font=("Segoe UI", 14, "bold"),
            bg=self.colors["danger"],
            fg="white"
        ).pack(pady=8)
        
        # Contenido
        status_frame = tk.Frame(card, bg=self.colors["card"])
        status_frame.pack(fill="x", padx=20, pady=20)
        
        self.status_label = tk.Label(
            status_frame,
            text="🟢 Sistema Operativo",
            font=("Segoe UI", 11, "bold"),
            bg=self.colors["card"],
            fg=self.colors["success"]
        )
        self.status_label.pack()
        
        self.time_label = tk.Label(
            status_frame,
            text="",
            font=("Segoe UI", 9),
            bg=self.colors["card"],
            fg=self.colors["text"]
        )
        self.time_label.pack(pady=5)
        
        # Botón detener
        btn_stop = tk.Button(
            status_frame,
            text="🛑 DETENER SISTEMA",
            font=("Segoe UI", 10, "bold"),
            bg=self.colors["danger"],
            fg="white",
            relief="flat",
            cursor="hand2",
            command=self.detener_sistema,
            padx=20,
            pady=8
        )
        btn_stop.pack(fill="x", pady=(10, 0))
    
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
                    "✓ Éxito",
                    f"Paciente {nombre} agregado correctamente"
                )
                # Limpiar campos
                self.entries["nombre"].delete(0, tk.END)
                self.entries["edad"].delete(0, tk.END)
                self.entries["sintomas"].delete(0, tk.END)
            else:
                messagebox.showerror(
                    "⚠️ Buffer lleno",
                    "No se puede agregar el paciente. Sala de espera llena."
                )
        
        except ValueError:
            messagebox.showerror(
                "❌ Error",
                "La edad debe ser un número válido"
            )
        except Exception as e:
            messagebox.showerror("❌ Error", f"Error al agregar paciente: {e}")
    
    def update_stats(self):
        """Actualiza estadísticas en tiempo real"""
        if not self.root.winfo_exists():
            return
        
        try:
            # Actualizar estadísticas
            pacientes_espera = len(self.buffer)
            medicos_activos = sum(1 for c in self.consumidores if c.is_alive())
            capacidad_buffer = self.buffer.cola.maxsize
            
            self.stat_labels["pacientes_espera"].config(text=str(pacientes_espera))
            self.stat_labels["medicos_activos"].config(text=str(medicos_activos))
            self.stat_labels["capacidad"].config(text=f"{pacientes_espera}/{capacidad_buffer}")
            
            # Actualizar lista de pacientes
            self.patients_listbox.delete(0, tk.END)
            pacientes = self.buffer.obtener_lista_pacientes()
            
            if pacientes:
                for i, p in enumerate(pacientes, 1):
                    self.patients_listbox.insert(
                        tk.END,
                        f"{i}. {p.nombre} | {p.edad}a | {p.sintomas[:40]}..."
                    )
            else:
                self.patients_listbox.insert(tk.END, "   --- Sin pacientes en espera ---")
            
            # Actualizar hora
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.time_label.config(text=f"Última actualización: {now}")
            
            # Cambiar color según capacidad
            if pacientes_espera == capacidad_buffer:
                self.stat_labels["capacidad"].config(fg=self.colors["danger"])
            elif pacientes_espera >= capacidad_buffer * 0.7:
                self.stat_labels["capacidad"].config(fg=self.colors["warning"])
            else:
                self.stat_labels["capacidad"].config(fg=self.colors["success"])
        
        except Exception as e:
            print(f"Error actualizando stats: {e}")
        
        # Repetir cada segundo
        self.root.after(1000, self.update_stats)
    
    def detener_sistema(self):
        """Detiene el sistema completo"""
        respuesta = messagebox.askyesno(
            "Confirmar",
            "¿Estás seguro de detener el sistema?"
        )
        
        if respuesta:
            self.status_label.config(
                text="🔴 Sistema Detenido",
                fg=self.colors["danger"]
            )
            
            # Detener hilos
            self.productor.detener()
            for c in self.consumidores:
                c.detener()
            
            messagebox.showinfo("Sistema Detenido", "El sistema se ha detenido correctamente")
            self.root.after(1000, self.root.destroy)
    
    def run(self):
        """Inicia la interfaz gráfica"""
        self.root.mainloop()

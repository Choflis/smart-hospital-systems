"""
Vista de Médicos - Lista de pacientes asignados por médico
"""

import tkinter as tk
from tkinter import ttk, messagebox


class MedicosView(tk.Frame):
    """Vista para que los médicos vean sus pacientes asignados"""
    
    def __init__(self, parent, hospital, colors):
        super().__init__(parent, bg=colors['secondary'])
        self.hospital = hospital
        self.colors = colors
        
        self._create_ui()
        self._load_medicos()
    
    def _create_ui(self):
        """Crear interfaz"""
        # Título
        title_frame = tk.Frame(self, bg=self.colors['bg_light'], pady=15)
        title_frame.pack(fill='x', pady=(0, 20))
        
        tk.Label(
            title_frame,
            text="👨‍⚕️ Gestión de Médicos y Pacientes Asignados",
            font=('Segoe UI', 22, 'bold'),
            bg=self.colors['bg_light'],
            fg=self.colors['text_dark']
        ).pack(side='left', padx=20)
        
        # Container principal
        main_container = tk.Frame(self, bg=self.colors['secondary'])
        main_container.pack(fill='both', expand=True, padx=10)
        
        # Panel izquierdo - Lista de médicos
        left_panel = tk.Frame(main_container, bg=self.colors['bg_light'], width=350)
        left_panel.pack(side='left', fill='y', padx=(0, 10))
        left_panel.pack_propagate(False)
        
        tk.Label(
            left_panel,
            text="Médicos Disponibles",
            font=('Segoe UI', 14, 'bold'),
            bg=self.colors['bg_light'],
            fg=self.colors['text_dark']
        ).pack(padx=20, pady=15)
        
        # Listbox de médicos
        self.medicos_listbox = tk.Listbox(
            left_panel,
            font=('Segoe UI', 11),
            bg='#F9FAFB',
            fg=self.colors['text_dark'],
            selectmode='single',
            relief='flat',
            highlightthickness=1,
            highlightbackground=self.colors['border'],
            highlightcolor=self.colors['primary']
        )
        self.medicos_listbox.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        self.medicos_listbox.bind('<<ListboxSelect>>', self._on_medico_select)
        
        # Panel derecho - Pacientes del médico seleccionado
        right_panel = tk.Frame(main_container, bg=self.colors['bg_light'])
        right_panel.pack(side='right', fill='both', expand=True)
        
        # Encabezado del panel derecho
        header_right = tk.Frame(right_panel, bg=self.colors['bg_light'])
        header_right.pack(fill='x', padx=20, pady=15)
        
        self.doctor_name_label = tk.Label(
            header_right,
            text="Seleccione un médico",
            font=('Segoe UI', 14, 'bold'),
            bg=self.colors['bg_light'],
            fg=self.colors['text_dark']
        )
        self.doctor_name_label.pack(side='left')
        
        self.patient_count_label = tk.Label(
            header_right,
            text="0 pacientes",
            font=('Segoe UI', 11),
            bg=self.colors['bg_light'],
            fg=self.colors['text_light']
        )
        self.patient_count_label.pack(side='right')
        
        # Tabla de pacientes
        table_frame = tk.Frame(right_panel, bg=self.colors['bg_light'])
        table_frame.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        
        # Crear Treeview
        columns = ('Nombre', 'Edad', 'Género', 'Síntomas', 'Fecha Ingreso')
        self.pacientes_tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show='headings',
            height=15
        )
        
        # Configurar columnas
        self.pacientes_tree.heading('Nombre', text='Nombre')
        self.pacientes_tree.heading('Edad', text='Edad')
        self.pacientes_tree.heading('Género', text='Género')
        self.pacientes_tree.heading('Síntomas', text='Síntomas')
        self.pacientes_tree.heading('Fecha Ingreso', text='Fecha Ingreso')
        
        self.pacientes_tree.column('Nombre', width=150)
        self.pacientes_tree.column('Edad', width=60, anchor='center')
        self.pacientes_tree.column('Género', width=80, anchor='center')
        self.pacientes_tree.column('Síntomas', width=200)
        self.pacientes_tree.column('Fecha Ingreso', width=120, anchor='center')
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient='vertical', command=self.pacientes_tree.yview)
        self.pacientes_tree.configure(yscrollcommand=scrollbar.set)
        
        self.pacientes_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Estilo para el Treeview
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Treeview',
                       background='#F9FAFB',
                       foreground=self.colors['text_dark'],
                       fieldbackground='#F9FAFB',
                       borderwidth=0)
        style.configure('Treeview.Heading',
                       background=self.colors['primary'],
                       foreground='white',
                       borderwidth=0)
        style.map('Treeview.Heading',
                 background=[('active', self.colors['primary_dark'])])
    
    def _load_medicos(self):
        """Cargar lista de médicos"""
        self.medicos_listbox.delete(0, tk.END)
        
        # Lista de médicos de ejemplo
        medicos = [
            "Dr. Juan Pérez - Cardiología",
            "Dra. María García - Pediatría",
            "Dr. Carlos López - Traumatología",
            "Dra. Ana Martínez - Neurología",
            "Dr. Luis Rodríguez - Medicina General"
        ]
        
        for medico in medicos:
            self.medicos_listbox.insert(tk.END, medico)
    
    def _on_medico_select(self, event):
        """Cuando se selecciona un médico"""
        selection = self.medicos_listbox.curselection()
        if not selection:
            return
        
        medico = self.medicos_listbox.get(selection[0])
        self.doctor_name_label.config(text=f"Pacientes de {medico.split(' - ')[0]}")
        
        # Cargar pacientes del médico
        self._load_pacientes(medico)
    
    def _load_pacientes(self, medico):
        """Cargar pacientes asignados al médico"""
        # Limpiar tabla
        for item in self.pacientes_tree.get_children():
            self.pacientes_tree.delete(item)
        
        # Datos de ejemplo
        pacientes_ejemplo = [
            ("Juan Rodríguez", "45", "M", "Dolor de pecho", "25/10/2025 14:30"),
            ("María López", "32", "F", "Fiebre alta", "25/10/2025 16:45"),
            ("Pedro Sánchez", "28", "M", "Fractura de brazo", "26/10/2025 09:15"),
        ]
        
        for paciente in pacientes_ejemplo:
            self.pacientes_tree.insert('', 'end', values=paciente)
        
        self.patient_count_label.config(text=f"{len(pacientes_ejemplo)} pacientes")
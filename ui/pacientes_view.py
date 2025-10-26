"""
Vista de Pacientes - Gestión completa de pacientes
"""

import tkinter as tk
from tkinter import ttk, messagebox


class PacientesView(tk.Frame):
    """Vista para gestión de pacientes"""
    
    def __init__(self, parent, hospital, colors):
        super().__init__(parent, bg=colors['secondary'])
        self.hospital = hospital
        self.colors = colors
        
        self._create_ui()
        self._load_pacientes()
    
    def _create_ui(self):
        """Crear interfaz"""
        # Título y barra de acciones
        title_frame = tk.Frame(self, bg=self.colors['bg_light'], pady=15)
        title_frame.pack(fill='x', pady=(0, 20))
        
        tk.Label(
            title_frame,
            text="🏥 Gestión de Pacientes",
            font=('Segoe UI', 22, 'bold'),
            bg=self.colors['bg_light'],
            fg=self.colors['text_dark']
        ).pack(side='left', padx=20)
        
        # Botones de acción
        btn_frame = tk.Frame(title_frame, bg=self.colors['bg_light'])
        btn_frame.pack(side='right', padx=20)
        
        self._create_action_button(
            btn_frame, "Nuevo Paciente", self.colors['success'], self._nuevo_paciente
        ).pack(side='left', padx=5)
        
        self._create_action_button(
            btn_frame, "Editar", self.colors['primary'], self._editar_paciente
        ).pack(side='left', padx=5)
        
        self._create_action_button(
            btn_frame, "Eliminar", self.colors['danger'], self._eliminar_paciente
        ).pack(side='left', padx=5)
        
        # Panel de búsqueda
        search_frame = tk.Frame(self, bg=self.colors['bg_light'])
        search_frame.pack(fill='x', padx=10, pady=(0, 10))
        
        tk.Label(
            search_frame,
            text="Buscar:",
            font=('Segoe UI', 11),
            bg=self.colors['bg_light'],
            fg=self.colors['text_dark']
        ).pack(side='left', padx=(20, 10), pady=10)
        
        self.search_var = tk.StringVar()
        self.search_var.trace('w', lambda *args: self._filtrar_pacientes())
        
        search_entry = tk.Entry(
            search_frame,
            textvariable=self.search_var,
            font=('Segoe UI', 11),
            relief='flat',
            bg='#F9FAFB',
            fg=self.colors['text_dark'],
            width=40
        )
        search_entry.pack(side='left', padx=(0, 20), pady=10, ipady=5)
        
        # Tabla de pacientes
        table_frame = tk.Frame(self, bg=self.colors['bg_light'])
        table_frame.pack(fill='both', expand=True, padx=10, pady=(0, 10))
        
        # Crear Treeview
        columns = ('ID', 'Nombre', 'Edad', 'Género', 'Síntomas', 'Médico', 'Fecha', 'Estado')
        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show='headings',
            selectmode='browse'
        )
        
        # Configurar columnas
        column_config = {
            'ID': (50, 'center'),
            'Nombre': (150, 'w'),
            'Edad': (60, 'center'),
            'Género': (80, 'center'),
            'Síntomas': (200, 'w'),
            'Médico': (150, 'w'),
            'Fecha': (120, 'center'),
            'Estado': (100, 'center')
        }
        
        for col, (width, anchor) in column_config.items():
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width, anchor=anchor)
        
        # Scrollbars
        vsb = ttk.Scrollbar(table_frame, orient='vertical', command=self.tree.yview)
        hsb = ttk.Scrollbar(table_frame, orient='horizontal', command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        self.tree.grid(row=0, column=0, sticky='nsew', padx=20, pady=20)
        vsb.grid(row=0, column=1, sticky='ns', pady=20)
        hsb.grid(row=1, column=0, sticky='ew', padx=20)
        
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)
        
        # Doble click para ver detalles
        self.tree.bind('<Double-Button-1>', self._ver_detalles)
        
        # Estilo
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Treeview',
                       background='#F9FAFB',
                       foreground=self.colors['text_dark'],
                       fieldbackground='#F9FAFB',
                       borderwidth=0,
                       rowheight=30)
        style.configure('Treeview.Heading',
                       background=self.colors['primary'],
                       foreground='white',
                       borderwidth=0,
                       font=('Segoe UI', 10, 'bold'))
        style.map('Treeview',
                 background=[('selected', self.colors['primary'])],
                 foreground=[('selected', 'white')])
    
    def _create_action_button(self, parent, text, color, command):
        """Crear botón de acción"""
        btn = tk.Button(
            parent,
            text=text,
            command=command,
            font=('Segoe UI', 10, 'bold'),
            bg=color,
            fg='white',
            activebackground=color,
            activeforeground='white',
            relief='flat',
            cursor='hand2',
            padx=15,
            pady=8
        )
        return btn
    
    def _load_pacientes(self):
        """Cargar pacientes"""
        # Limpiar
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Datos de ejemplo
        pacientes = [
            ("001", "Juan Pérez", "45", "M", "Dolor de pecho", "Dr. Juan Pérez", "25/10/2025", "En tratamiento"),
            ("002", "María García", "32", "F", "Fiebre alta", "Dra. María García", "25/10/2025", "Estable"),
            ("003", "Carlos López", "28", "M", "Fractura brazo", "Dr. Carlos López", "26/10/2025", "Cirugía"),
            ("004", "Ana Martínez", "55", "F", "Diabetes", "Dra. Ana Martínez", "24/10/2025", "Control"),
            ("005", "Luis Rodríguez", "38", "M", "Gripe", "Dr. Luis Rodríguez", "26/10/2025", "Recuperación"),
        ]
        
        for paciente in pacientes:
            self.tree.insert('', 'end', values=paciente)
    
    def _filtrar_pacientes(self):
        """Filtrar pacientes por búsqueda"""
        search_text = self.search_var.get().lower()
        
        # Limpiar
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Recargar filtrado (aquí conectar con datos reales)
        self._load_pacientes()
    
    def _nuevo_paciente(self):
        """Agregar nuevo paciente"""
        # TODO: Abrir formulario de nuevo paciente
        messagebox.showinfo("Nuevo Paciente", "Funcionalidad en desarrollo")
    
    def _editar_paciente(self):
        """Editar paciente seleccionado"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Editar", "Seleccione un paciente")
            return
        
        # TODO: Abrir formulario de edición
        messagebox.showinfo("Editar Paciente", "Funcionalidad en desarrollo")
    
    def _eliminar_paciente(self):
        """Eliminar paciente seleccionado"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Eliminar", "Seleccione un paciente")
            return
        
        item = self.tree.item(selection[0])
        nombre = item['values'][1]
        
        if messagebox.askyesno("Confirmar", f"¿Eliminar a {nombre}?"):
            self.tree.delete(selection[0])
            messagebox.showinfo("Éxito", "Paciente eliminado")
    
    def _ver_detalles(self, event):
        """Ver detalles del paciente"""
        selection = self.tree.selection()
        if not selection:
            return
        
        item = self.tree.item(selection[0])
        # TODO: Mostrar ventana con detalles completos
        messagebox.showinfo("Detalles", f"Paciente: {item['values'][1]}")
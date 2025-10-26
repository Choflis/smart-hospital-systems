"""
Ventana Principal del Sistema Hospitalario
Diseño moderno con menú lateral profesional
"""

import tkinter as tk
from tkinter import ttk
from .dashboard import DashboardView
from .medicos_view import MedicosView
from .pacientes_view import PacientesView
from .recursos_view import RecursosView


class MainWindow(tk.Tk):
    """Ventana principal con diseño moderno y menú lateral"""
    
    # Paleta de colores profesional
    COLORS = {
        'primary': '#2563EB',      # Azul médico
        'primary_dark': '#1E40AF',  # Azul oscuro
        'secondary': '#F3F4F6',     # Gris claro
        'bg_light': '#FFFFFF',      # Blanco
        'bg_dark': '#1F2937',       # Gris oscuro
        'text_dark': '#111827',     # Texto oscuro
        'text_light': '#6B7280',    # Texto claro
        'success': '#10B981',       # Verde
        'warning': '#F59E0B',       # Naranja
        'danger': '#EF4444',        # Rojo
        'border': '#E5E7EB'         # Borde gris
    }
    
    def __init__(self, hospital):
        super().__init__()
        self.hospital = hospital
        self.current_view = None
        
        # Configuración de la ventana
        self.title("Smart Hospital Management System")
        self.geometry("1400x800")
        self.configure(bg=self.COLORS['bg_light'])
        
        # Maximizar ventana (Windows)
        try:
            self.state('zoomed')
        except:
            pass
        
        # Crear interfaz
        self._create_ui()
        
        # Mostrar dashboard por defecto
        self.show_dashboard()
    
    def _create_ui(self):
        """Crear la interfaz completa"""
        # Container principal
        main_container = tk.Frame(self, bg=self.COLORS['bg_light'])
        main_container.pack(fill='both', expand=True)
        
        # Menú lateral (Sidebar)
        self.sidebar = self._create_sidebar(main_container)
        self.sidebar.pack(side='left', fill='y')
        
        # Área de contenido
        self.content_area = tk.Frame(
            main_container, 
            bg=self.COLORS['secondary'],
            padx=20,
            pady=20
        )
        self.content_area.pack(side='right', fill='both', expand=True)
    
    def _create_sidebar(self, parent):
        """Crear el menú lateral profesional"""
        sidebar = tk.Frame(
            parent,
            bg=self.COLORS['primary_dark'],
            width=250
        )
        
        # Logo/Título
        header = tk.Frame(sidebar, bg=self.COLORS['primary_dark'], height=80)
        header.pack(fill='x', pady=(0, 20))
        header.pack_propagate(False)
        
        tk.Label(
            header,
            text="Smart Hospital",
            font=('Segoe UI', 18, 'bold'),
            bg=self.COLORS['primary_dark'],
            fg='white',
            pady=20
        ).pack()
        
        # Separador
        tk.Frame(sidebar, bg=self.COLORS['primary'], height=2).pack(fill='x')
        
        # Botones del menú
        menu_items = [
            ('Dashboard', self.show_dashboard, '📊'),
            ('Médicos', self.show_medicos, '👨‍⚕️'),
            ('Pacientes', self.show_pacientes, '🏥'),
            ('UCI/Recursos', self.show_recursos, '🛏️'),
        ]
        
        self.menu_buttons = {}
        for text, command, icon in menu_items:
            btn = self._create_menu_button(sidebar, text, command, icon)
            btn.pack(fill='x', padx=10, pady=5)
            self.menu_buttons[text] = btn
        
        # Espaciador
        tk.Frame(sidebar, bg=self.COLORS['primary_dark']).pack(fill='both', expand=True)
        
        # Botón de salir
        exit_btn = tk.Button(
            sidebar,
            text="Salir",
            command=self.quit,
            font=('Segoe UI', 11),
            bg='#991B1B',
            fg='white',
            activebackground='#7F1D1D',
            activeforeground='white',
            relief='flat',
            cursor='hand2',
            padx=20,
            pady=12
        )
        exit_btn.pack(fill='x', padx=10, pady=10, side='bottom')
        
        return sidebar
    
    def _create_menu_button(self, parent, text, command, icon):
        """Crear botón del menú lateral"""
        btn = tk.Button(
            parent,
            text=f"  {icon}  {text}",
            command=lambda: self._on_menu_click(text, command),
            font=('Segoe UI', 11),
            bg=self.COLORS['primary_dark'],
            fg='white',
            activebackground=self.COLORS['primary'],
            activeforeground='white',
            relief='flat',
            cursor='hand2',
            anchor='w',
            padx=20,
            pady=12
        )
        
        # Efectos hover
        btn.bind('<Enter>', lambda e: btn.config(bg=self.COLORS['primary']))
        btn.bind('<Leave>', lambda e: self._reset_button_color(btn, text))
        
        return btn
    
    def _on_menu_click(self, text, command):
        """Manejar clic en menú"""
        # Resetear todos los botones
        for btn_text, btn in self.menu_buttons.items():
            if btn_text == text:
                btn.config(bg=self.COLORS['primary'])
            else:
                btn.config(bg=self.COLORS['primary_dark'])
        
        # Ejecutar comando
        command()
    
    def _reset_button_color(self, btn, text):
        """Resetear color del botón según si está activo"""
        is_active = (
            (text == 'Dashboard' and isinstance(self.current_view, DashboardView)) or
            (text == 'Médicos' and isinstance(self.current_view, MedicosView)) or
            (text == 'Pacientes' and isinstance(self.current_view, PacientesView)) or
            (text == 'UCI/Recursos' and isinstance(self.current_view, RecursosView))
        )
        
        if is_active:
            btn.config(bg=self.COLORS['primary'])
        else:
            btn.config(bg=self.COLORS['primary_dark'])
    
    def _clear_content(self):
        """Limpiar el área de contenido"""
        for widget in self.content_area.winfo_children():
            widget.destroy()
    
    def show_dashboard(self):
        """Mostrar dashboard"""
        self._clear_content()
        self.current_view = DashboardView(self.content_area, self.hospital, self.COLORS)
        self.current_view.pack(fill='both', expand=True)
    
    def show_medicos(self):
        """Mostrar vista de médicos"""
        self._clear_content()
        self.current_view = MedicosView(self.content_area, self.hospital, self.COLORS)
        self.current_view.pack(fill='both', expand=True)
    
    def show_pacientes(self):
        """Mostrar vista de pacientes"""
        self._clear_content()
        self.current_view = PacientesView(self.content_area, self.hospital, self.COLORS)
        self.current_view.pack(fill='both', expand=True)
    
    def show_recursos(self):
        """Mostrar vista de recursos"""
        self._clear_content()
        self.current_view = RecursosView(self.content_area, self.hospital, self.COLORS)
        self.current_view.pack(fill='both', expand=True)
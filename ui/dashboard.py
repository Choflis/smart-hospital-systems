"""
Dashboard - Vista principal con estadísticas
"""

import tkinter as tk
from tkinter import ttk
from datetime import datetime


class DashboardView(tk.Frame):
    """Dashboard con tarjetas de estadísticas"""
    
    def __init__(self, parent, hospital, colors):
        super().__init__(parent, bg=colors['secondary'])
        self.hospital = hospital
        self.colors = colors
        
        self._create_ui()
        self._load_data()
    
    def _create_ui(self):
        """Crear interfaz del dashboard"""
        # Título
        title_frame = tk.Frame(self, bg=self.colors['bg_light'], pady=15)
        title_frame.pack(fill='x', pady=(0, 20))
        
        tk.Label(
            title_frame,
            text="Dashboard del Sistema",
            font=('Segoe UI', 22, 'bold'),
            bg=self.colors['bg_light'],
            fg=self.colors['text_dark']
        ).pack(side='left', padx=20)
        
        # Fecha y hora
        self.time_label = tk.Label(
            title_frame,
            text=datetime.now().strftime("%d/%m/%Y %H:%M"),
            font=('Segoe UI', 11),
            bg=self.colors['bg_light'],
            fg=self.colors['text_light']
        )
        self.time_label.pack(side='right', padx=20)
        
        # Actualizar hora cada segundo
        self._update_time()
        
        # Grid de tarjetas
        cards_container = tk.Frame(self, bg=self.colors['secondary'])
        cards_container.pack(fill='both', expand=True, padx=10)
        
        # Primera fila de tarjetas
        row1 = tk.Frame(cards_container, bg=self.colors['secondary'])
        row1.pack(fill='x', pady=10)
        
        self.card_pacientes = self._create_stat_card(
            row1, "Total Pacientes", "0", self.colors['primary'], "👥"
        )
        self.card_pacientes.pack(side='left', fill='both', expand=True, padx=10)
        
        self.card_uci = self._create_stat_card(
            row1, "Camas UCI", "0/10", self.colors['danger'], "🛏️"
        )
        self.card_uci.pack(side='left', fill='both', expand=True, padx=10)
        
        self.card_quirofano = self._create_stat_card(
            row1, "Quirófanos", "0/5", self.colors['warning'], "🏥"
        )
        self.card_quirofano.pack(side='left', fill='both', expand=True, padx=10)
        
        self.card_farmacia = self._create_stat_card(
            row1, "Stock Farmacia", "0", self.colors['success'], "💊"
        )
        self.card_farmacia.pack(side='left', fill='both', expand=True, padx=10)
        
        # Segunda fila - Actividad reciente
        activity_frame = tk.Frame(self, bg=self.colors['bg_light'])
        activity_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        tk.Label(
            activity_frame,
            text="Actividad Reciente",
            font=('Segoe UI', 16, 'bold'),
            bg=self.colors['bg_light'],
            fg=self.colors['text_dark']
        ).pack(anchor='w', padx=20, pady=15)
        
        # Lista de actividad
        self.activity_text = tk.Text(
            activity_frame,
            height=10,
            font=('Consolas', 10),
            bg='#F9FAFB',
            fg=self.colors['text_dark'],
            relief='flat',
            padx=15,
            pady=10
        )
        self.activity_text.pack(fill='both', expand=True, padx=20, pady=(0, 20))
    
    def _create_stat_card(self, parent, title, value, color, icon):
        """Crear tarjeta de estadística"""
        card = tk.Frame(parent, bg=self.colors['bg_light'], relief='flat')
        card.pack_propagate(False)
        card.config(height=140)
        
        # Barra de color superior
        top_bar = tk.Frame(card, bg=color, height=4)
        top_bar.pack(fill='x')
        
        content = tk.Frame(card, bg=self.colors['bg_light'])
        content.pack(fill='both', expand=True, padx=20, pady=15)
        
        # Ícono y título
        header = tk.Frame(content, bg=self.colors['bg_light'])
        header.pack(fill='x')
        
        tk.Label(
            header,
            text=icon,
            font=('Segoe UI', 24),
            bg=self.colors['bg_light']
        ).pack(side='left')
        
        tk.Label(
            header,
            text=title,
            font=('Segoe UI', 11),
            bg=self.colors['bg_light'],
            fg=self.colors['text_light']
        ).pack(side='left', padx=10)
        
        # Valor
        value_label = tk.Label(
            content,
            text=value,
            font=('Segoe UI', 28, 'bold'),
            bg=self.colors['bg_light'],
            fg=color
        )
        value_label.pack(anchor='w', pady=(10, 0))
        
        # Guardar referencia al label del valor
        card.value_label = value_label
        
        return card
    
    def _update_time(self):
        """Actualizar reloj"""
        self.time_label.config(text=datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
        self.after(1000, self._update_time)
    
    def _load_data(self):
        """Cargar datos del hospital"""
        try:
            # Actualizar tarjetas
            # TODO: Conectar con datos reales del hospital
            self.card_pacientes.value_label.config(text="0")
            self.card_uci.value_label.config(text="0/10")
            self.card_quirofano.value_label.config(text="0/5")
            self.card_farmacia.value_label.config(text="100")
            
            # Actividad reciente
            self.activity_text.insert('1.0', "Sistema iniciado correctamente...\n")
            self.activity_text.insert('end', "Esperando eventos...\n")
            self.activity_text.config(state='disabled')
            
        except Exception as e:
            print(f"Error cargando datos: {e}")
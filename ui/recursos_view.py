"""
Vista de Recursos - UCI, Quirófanos y Farmacia
"""

import tkinter as tk
from tkinter import ttk, messagebox


class RecursosView(tk.Frame):
    """Vista para gestión de recursos hospitalarios"""
    
    def __init__(self, parent, hospital, colors):
        super().__init__(parent, bg=colors['secondary'])
        self.hospital = hospital
        self.colors = colors
        
        self._create_ui()
        self._load_recursos()
    
    def _create_ui(self):
        """Crear interfaz"""
        # Título
        title_frame = tk.Frame(self, bg=self.colors['bg_light'], pady=15)
        title_frame.pack(fill='x', pady=(0, 20))
        
        tk.Label(
            title_frame,
            text="🛏️ Gestión de Recursos Hospitalarios",
            font=('Segoe UI', 22, 'bold'),
            bg=self.colors['bg_light'],
            fg=self.colors['text_dark']
        ).pack(side='left', padx=20)
        
        # Notebook (pestañas)
        notebook = ttk.Notebook(self)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Estilo para las pestañas
        style = ttk.Style()
        style.configure('TNotebook', background=self.colors['secondary'], borderwidth=0)
        style.configure('TNotebook.Tab', 
                       padding=[20, 10],
                       font=('Segoe UI', 11, 'bold'))
        
        # Pestaña UCI
        uci_frame = self._create_uci_tab()
        notebook.add(uci_frame, text='🛏️  UCI')
        
        # Pestaña Quirófanos
        quirofano_frame = self._create_quirofano_tab()
        notebook.add(quirofano_frame, text='🏥  Quirófanos')
        
        # Pestaña Farmacia
        farmacia_frame = self._create_farmacia_tab()
        notebook.add(farmacia_frame, text='💊  Farmacia')
    
    def _create_uci_tab(self):
        """Crear pestaña de UCI"""
        frame = tk.Frame(self, bg=self.colors['bg_light'])
        
        # Título
        tk.Label(
            frame,
            text="Unidad de Cuidados Intensivos",
            font=('Segoe UI', 16, 'bold'),
            bg=self.colors['bg_light'],
            fg=self.colors['text_dark']
        ).pack(pady=20)
        
        # Estado de camas
        status_frame = tk.Frame(frame, bg=self.colors['bg_light'])
        status_frame.pack(pady=10)
        
        tk.Label(
            status_frame,
            text="Camas Disponibles: ",
            font=('Segoe UI', 12),
            bg=self.colors['bg_light']
        ).pack(side='left')
        
        self.uci_status = tk.Label(
            status_frame,
            text="10/10",
            font=('Segoe UI', 12, 'bold'),
            bg=self.colors['bg_light'],
            fg=self.colors['success']
        )
        self.uci_status.pack(side='left')
        
        # Grid de camas
        camas_frame = tk.Frame(frame, bg=self.colors['bg_light'])
        camas_frame.pack(fill='both', expand=True, padx=40, pady=20)
        
        self.camas_uci = []
        for i in range(10):
            cama_card = self._create_cama_card(camas_frame, f"Cama {i+1}", "Disponible")
            row = i // 5
            col = i % 5
            cama_card.grid(row=row, column=col, padx=10, pady=10)
            self.camas_uci.append(cama_card)
        
        return frame
    
    def _create_quirofano_tab(self):
        """Crear pestaña de quirófanos"""
        frame = tk.Frame(self, bg=self.colors['bg_light'])
        
        # Título
        tk.Label(
            frame,
            text="Quirófanos",
            font=('Segoe UI', 16, 'bold'),
            bg=self.colors['bg_light'],
            fg=self.colors['text_dark']
        ).pack(pady=20)
        
        # Estado
        status_frame = tk.Frame(frame, bg=self.colors['bg_light'])
        status_frame.pack(pady=10)
        
        tk.Label(
            status_frame,
            text="Quirófanos Disponibles: ",
            font=('Segoe UI', 12),
            bg=self.colors['bg_light']
        ).pack(side='left')
        
        self.quirofano_status = tk.Label(
            status_frame,
            text="5/5",
            font=('Segoe UI', 12, 'bold'),
            bg=self.colors['bg_light'],
            fg=self.colors['success']
        )
        self.quirofano_status.pack(side='left')
        
        # Grid de quirófanos
        quirofanos_frame = tk.Frame(frame, bg=self.colors['bg_light'])
        quirofanos_frame.pack(fill='both', expand=True, padx=40, pady=20)
        
        self.quirofanos = []
        for i in range(5):
            quirofano_card = self._create_quirofano_card(
                quirofanos_frame, 
                f"Quirófano {i+1}", 
                "Disponible"
            )
            quirofano_card.grid(row=i//3, column=i%3, padx=15, pady=15, sticky='ew')
            self.quirofanos.append(quirofano_card)
        
        return frame
    
    def _create_farmacia_tab(self):
        """Crear pestaña de farmacia"""
        frame = tk.Frame(self, bg=self.colors['bg_light'])
        
        # Título
        tk.Label(
            frame,
            text="Inventario de Farmacia",
            font=('Segoe UI', 16, 'bold'),
            bg=self.colors['bg_light'],
            fg=self.colors['text_dark']
        ).pack(pady=20)
        
        # Tabla de medicamentos
        table_frame = tk.Frame(frame, bg=self.colors['bg_light'])
        table_frame.pack(fill='both', expand=True, padx=40, pady=20)
        
        columns = ('Medicamento', 'Stock', 'Unidad', 'Estado')
        self.farmacia_tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show='headings',
            height=15
        )
        
        # Configurar columnas
        self.farmacia_tree.heading('Medicamento', text='Medicamento')
        self.farmacia_tree.heading('Stock', text='Stock')
        self.farmacia_tree.heading('Unidad', text='Unidad')
        self.farmacia_tree.heading('Estado', text='Estado')
        
        self.farmacia_tree.column('Medicamento', width=300)
        self.farmacia_tree.column('Stock', width=100, anchor='center')
        self.farmacia_tree.column('Unidad', width=100, anchor='center')
        self.farmacia_tree.column('Estado', width=150, anchor='center')
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient='vertical', command=self.farmacia_tree.yview)
        self.farmacia_tree.configure(yscrollcommand=scrollbar.set)
        
        self.farmacia_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Estilo
        style = ttk.Style()
        style.configure('Treeview',
                       background='#F9FAFB',
                       foreground=self.colors['text_dark'],
                       fieldbackground='#F9FAFB',
                       rowheight=30)
        style.configure('Treeview.Heading',
                       background=self.colors['primary'],
                       foreground='white',
                       font=('Segoe UI', 10, 'bold'))
        
        return frame
    
    def _create_cama_card(self, parent, nombre, estado):
        """Crear tarjeta de cama"""
        color = self.colors['success'] if estado == "Disponible" else self.colors['danger']
        
        card = tk.Frame(parent, bg='white', relief='solid', borderwidth=1, width=180, height=100)
        card.pack_propagate(False)
        
        tk.Label(
            card,
            text=nombre,
            font=('Segoe UI', 11, 'bold'),
            bg='white',
            fg=self.colors['text_dark']
        ).pack(pady=(10, 5))
        
        estado_label = tk.Label(
            card,
            text=estado,
            font=('Segoe UI', 10),
            bg='white',
            fg=color
        )
        estado_label.pack()
        
        card.status_label = estado_label
        return card
    
    def _create_quirofano_card(self, parent, nombre, estado):
        """Crear tarjeta de quirófano"""
        color = self.colors['success'] if estado == "Disponible" else self.colors['warning']
        
        card = tk.Frame(parent, bg='white', relief='solid', borderwidth=1, height=120)
        card.pack_propagate(False)
        
        tk.Label(
            card,
            text=nombre,
            font=('Segoe UI', 12, 'bold'),
            bg='white',
            fg=self.colors['text_dark']
        ).pack(pady=(15, 10))
        
        estado_label = tk.Label(
            card,
            text=estado,
            font=('Segoe UI', 11),
            bg='white',
            fg=color
        )
        estado_label.pack()
        
        card.status_label = estado_label
        return card
    
    def _load_recursos(self):
        """Cargar datos de recursos"""
        # Cargar medicamentos de ejemplo
        medicamentos = [
            ("Paracetamol 500mg", "1500", "Tabletas", "Stock Normal"),
            ("Ibuprofeno 400mg", "800", "Tabletas", "Stock Normal"),
            ("Amoxicilina 500mg", "50", "Cápsulas", "Stock Bajo"),
            ("Insulina", "200", "Viales", "Stock Normal"),
            ("Suero Fisiológico", "300", "Bolsas", "Stock Normal"),
        ]
        
        for med in medicamentos:
            self.farmacia_tree.insert('', 'end', values=med)
            # Colorear según stock
            if "Bajo" in med[3]:
                self.farmacia_tree.tag_configure('bajo', foreground=self.colors['danger'])
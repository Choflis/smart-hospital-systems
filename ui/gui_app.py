#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Interfaz Gráfica (GUI) del Sistema Hospitalario
================================================

Dos ventanas:
1. Panel de Control - Estadísticas y controles
2. Visualización de Flujo - Animación del proceso

Autor: Equipo de Desarrollo
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
from datetime import datetime


class PanelControl(tk.Toplevel):
    """Ventana 1: Panel de Control Principal"""
    
    def __init__(self, parent, hospital):
        super().__init__(parent)
        self.hospital = hospital
        self.title("🏥 Sistema Hospitalario - Panel de Control")
        self.geometry("600x700")
        self.configure(bg="#f0f0f0")
        
        # No cerrar toda la app al cerrar esta ventana
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        self._crear_widgets()
        self._actualizar_loop()
    
    def _crear_widgets(self):
        """Crear todos los widgets de la ventana"""
        
        # ===== TÍTULO =====
        frame_titulo = tk.Frame(self, bg="#2c3e50", height=60)
        frame_titulo.pack(fill=tk.X, pady=(0, 10))
        frame_titulo.pack_propagate(False)
        
        tk.Label(
            frame_titulo,
            text="🏥 SISTEMA HOSPITALARIO",
            font=("Arial", 18, "bold"),
            fg="white",
            bg="#2c3e50"
        ).pack(pady=15)
        
        # ===== BOTONES DE CONTROL =====
        frame_botones = tk.Frame(self, bg="#f0f0f0")
        frame_botones.pack(pady=10)
        
        self.btn_iniciar = tk.Button(
            frame_botones,
            text="▶️ INICIAR",
            font=("Arial", 12, "bold"),
            bg="#27ae60",
            fg="white",
            width=12,
            height=2,
            command=self._iniciar_sistema,
            cursor="hand2"
        )
        self.btn_iniciar.grid(row=0, column=0, padx=5)
        
        self.btn_pausar = tk.Button(
            frame_botones,
            text="⏸️ PAUSAR",
            font=("Arial", 12, "bold"),
            bg="#f39c12",
            fg="white",
            width=12,
            height=2,
            command=self._pausar_sistema,
            state=tk.DISABLED,
            cursor="hand2"
        )
        self.btn_pausar.grid(row=0, column=1, padx=5)
        
        self.btn_detener = tk.Button(
            frame_botones,
            text="⏹️ DETENER",
            font=("Arial", 12, "bold"),
            bg="#e74c3c",
            fg="white",
            width=12,
            height=2,
            command=self._detener_sistema,
            state=tk.DISABLED,
            cursor="hand2"
        )
        self.btn_detener.grid(row=0, column=2, padx=5)
        
        # ===== BUFFER DE PACIENTES =====
        frame_buffer = tk.LabelFrame(
            self,
            text="📦 BUFFER DE PACIENTES",
            font=("Arial", 12, "bold"),
            bg="#f0f0f0",
            fg="#2c3e50",
            padx=10,
            pady=10
        )
        frame_buffer.pack(fill=tk.X, padx=20, pady=10)
        
        self.canvas_buffer = tk.Canvas(
            frame_buffer,
            width=550,
            height=100,
            bg="white",
            highlightthickness=1,
            highlightbackground="#bdc3c7"
        )
        self.canvas_buffer.pack()
        
        # ===== ESTADÍSTICAS =====
        frame_stats = tk.LabelFrame(
            self,
            text="📊 ESTADÍSTICAS",
            font=("Arial", 12, "bold"),
            bg="#f0f0f0",
            fg="#2c3e50",
            padx=10,
            pady=10
        )
        frame_stats.pack(fill=tk.X, padx=20, pady=10)
        
        self.label_generados = tk.Label(
            frame_stats,
            text="● Pacientes Generados: 0",
            font=("Arial", 11),
            bg="#f0f0f0",
            anchor="w"
        )
        self.label_generados.pack(fill=tk.X, pady=2)
        
        self.label_atendidos = tk.Label(
            frame_stats,
            text="● Pacientes Atendidos: 0",
            font=("Arial", 11),
            bg="#f0f0f0",
            anchor="w"
        )
        self.label_atendidos.pack(fill=tk.X, pady=2)
        
        self.label_buffer = tk.Label(
            frame_stats,
            text="● En Buffer: 0 / 5",
            font=("Arial", 11),
            bg="#f0f0f0",
            anchor="w"
        )
        self.label_buffer.pack(fill=tk.X, pady=2)
        
        self.label_expedientes = tk.Label(
            frame_stats,
            text="● Expedientes Registrados: 0",
            font=("Arial", 11),
            bg="#f0f0f0",
            anchor="w"
        )
        self.label_expedientes.pack(fill=tk.X, pady=2)
        
        # ===== PRODUCTORES =====
        frame_productores = tk.LabelFrame(
            self,
            text="👥 PRODUCTORES",
            font=("Arial", 12, "bold"),
            bg="#f0f0f0",
            fg="#2c3e50",
            padx=10,
            pady=10
        )
        frame_productores.pack(fill=tk.X, padx=20, pady=10)
        
        self.label_productores = tk.Label(
            frame_productores,
            text="🟢 Productor-1: 0 generados\n🟢 Productor-2: 0 generados",
            font=("Arial", 10),
            bg="#f0f0f0",
            anchor="w",
            justify=tk.LEFT
        )
        self.label_productores.pack(fill=tk.X)
        
        # ===== MÉDICOS =====
        frame_medicos = tk.LabelFrame(
            self,
            text="🩺 MÉDICOS",
            font=("Arial", 12, "bold"),
            bg="#f0f0f0",
            fg="#2c3e50",
            padx=10,
            pady=10
        )
        frame_medicos.pack(fill=tk.X, padx=20, pady=10)
        
        self.label_medicos = tk.Label(
            frame_medicos,
            text="🟢 Dr. García: 0 atendidos\n🟢 Dra. Martínez: 0 atendidos\n🟢 Dr. López: 0 atendidos",
            font=("Arial", 10),
            bg="#f0f0f0",
            anchor="w",
            justify=tk.LEFT
        )
        self.label_medicos.pack(fill=tk.X)
        
        # ===== LOG DE EVENTOS =====
        frame_log = tk.LabelFrame(
            self,
            text="📋 LOG DE EVENTOS",
            font=("Arial", 12, "bold"),
            bg="#f0f0f0",
            fg="#2c3e50",
            padx=10,
            pady=10
        )
        frame_log.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Scrollbar para el log
        scrollbar = tk.Scrollbar(frame_log)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.text_log = tk.Text(
            frame_log,
            height=8,
            font=("Courier", 9),
            bg="#ecf0f1",
            fg="#2c3e50",
            yscrollcommand=scrollbar.set,
            wrap=tk.WORD
        )
        self.text_log.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.text_log.yview)
        
        self._agregar_log("Sistema iniciado. Esperando comandos...")
    
    def _dibujar_buffer(self):
        """Dibujar la visualización del buffer"""
        self.canvas_buffer.delete("all")
        
        stats = self.hospital.get_estadisticas()
        capacidad = self.hospital.capacidad_buffer
        ocupados = stats['buffer_ocupado']
        
        # Título
        self.canvas_buffer.create_text(
            275, 15,
            text=f"Buffer: {ocupados} / {capacidad}",
            font=("Arial", 12, "bold"),
            fill="#2c3e50"
        )
        
        # Dibujar slots del buffer
        ancho_slot = 80
        alto_slot = 60
        espacio = 10
        inicio_x = 50
        inicio_y = 35
        
        for i in range(capacidad):
            x = inicio_x + i * (ancho_slot + espacio)
            
            # Color según ocupación
            if i < ocupados:
                color = "#3498db"  # Azul - ocupado
                texto = "👤"
            else:
                color = "#ecf0f1"  # Gris claro - vacío
                texto = ""
            
            # Dibujar rectángulo
            self.canvas_buffer.create_rectangle(
                x, inicio_y,
                x + ancho_slot, inicio_y + alto_slot,
                fill=color,
                outline="#95a5a6",
                width=2
            )
            
            # Dibujar emoji o número
            if texto:
                self.canvas_buffer.create_text(
                    x + ancho_slot // 2,
                    inicio_y + alto_slot // 2,
                    text=texto,
                    font=("Arial", 24),
                    fill="white"
                )
    
    def _actualizar_loop(self):
        """Actualizar la interfaz periódicamente"""
        if not self.winfo_exists():
            return
        
        stats = self.hospital.get_estadisticas()
        
        # Actualizar estadísticas
        self.label_generados.config(
            text=f"● Pacientes Generados: {stats['pacientes_generados']}"
        )
        self.label_atendidos.config(
            text=f"● Pacientes Atendidos: {stats['pacientes_atendidos']}"
        )
        self.label_buffer.config(
            text=f"● En Buffer: {stats['buffer_ocupado']} / {self.hospital.capacidad_buffer}"
        )
        self.label_expedientes.config(
            text=f"● Expedientes Registrados: {stats['expedientes']['total']}"
        )
        
        # Actualizar buffer visual
        self._dibujar_buffer()
        
        # Programar siguiente actualización
        self.after(500, self._actualizar_loop)
    
    def _iniciar_sistema(self):
        """Iniciar el sistema hospitalario"""
        self.hospital.iniciar()
        self.btn_iniciar.config(state=tk.DISABLED)
        self.btn_pausar.config(state=tk.NORMAL)
        self.btn_detener.config(state=tk.NORMAL)
        self._agregar_log("✅ Sistema iniciado correctamente")
    
    def _pausar_sistema(self):
        """Pausar el sistema"""
        self._agregar_log("⏸️ Sistema pausado (funcionalidad pendiente)")
        messagebox.showinfo("Pausar", "Funcionalidad de pausa en desarrollo")
    
    def _detener_sistema(self):
        """Detener el sistema"""
        respuesta = messagebox.askyesno(
            "Detener Sistema",
            "¿Estás seguro de detener el sistema?\n\nSe perderán todos los procesos activos."
        )
        
        if respuesta:
            self.hospital.detener()
            self.btn_iniciar.config(state=tk.NORMAL)
            self.btn_pausar.config(state=tk.DISABLED)
            self.btn_detener.config(state=tk.DISABLED)
            self._agregar_log("🛑 Sistema detenido")
    
    def _agregar_log(self, mensaje):
        """Agregar mensaje al log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.text_log.insert(tk.END, f"[{timestamp}] {mensaje}\n")
        self.text_log.see(tk.END)  # Scroll automático
    
    def on_closing(self):
        """Manejar cierre de ventana"""
        self.withdraw()  # Ocultar en lugar de cerrar


class VisualizacionFlujo(tk.Toplevel):
    """Ventana 2: Visualización del Flujo de Datos"""
    
    def __init__(self, parent, hospital):
        super().__init__(parent)
        self.hospital = hospital
        self.title("📊 Sistema Hospitalario - Visualización de Flujo")
        self.geometry("900x600")
        self.configure(bg="#ecf0f1")
        
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        self._crear_widgets()
        self._animar_loop()
    
    def _crear_widgets(self):
        """Crear widgets de visualización"""
        
        # Título
        frame_titulo = tk.Frame(self, bg="#34495e", height=50)
        frame_titulo.pack(fill=tk.X)
        frame_titulo.pack_propagate(False)
        
        tk.Label(
            frame_titulo,
            text="📊 VISUALIZACIÓN DEL FLUJO DE CONCURRENCIA",
            font=("Arial", 16, "bold"),
            fg="white",
            bg="#34495e"
        ).pack(pady=12)
        
        # Canvas para dibujar el flujo
        self.canvas = tk.Canvas(
            self,
            bg="white",
            highlightthickness=0
        )
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Animaciones
        self.particulas = []  # Pacientes moviéndose
    
    def _dibujar_flujo(self):
        """Dibujar el diagrama de flujo"""
        self.canvas.delete("all")
        
        # Dimensiones
        ancho = self.canvas.winfo_width()
        alto = self.canvas.winfo_height()
        
        if ancho <= 1 or alto <= 1:
            return
        
        # Posiciones
        x_productores = 100
        x_buffer = ancho // 2
        x_medicos = ancho - 150
        y_centro = alto // 2
        
        # ===== PRODUCTORES =====
        self.canvas.create_rectangle(
            x_productores - 60, y_centro - 80,
            x_productores + 60, y_centro + 80,
            fill="#3498db",
            outline="#2980b9",
            width=3
        )
        self.canvas.create_text(
            x_productores, y_centro - 50,
            text="👥",
            font=("Arial", 32),
            fill="white"
        )
        self.canvas.create_text(
            x_productores, y_centro + 10,
            text="PRODUCTORES",
            font=("Arial", 11, "bold"),
            fill="white"
        )
        self.canvas.create_text(
            x_productores, y_centro + 40,
            text="Generan\nPacientes",
            font=("Arial", 9),
            fill="white"
        )
        
        # ===== FLECHA 1: Productores → Buffer =====
        self._dibujar_flecha(x_productores + 60, y_centro, x_buffer - 80, y_centro, "#27ae60")
        
        # ===== BUFFER =====
        self.canvas.create_rectangle(
            x_buffer - 80, y_centro - 100,
            x_buffer + 80, y_centro + 100,
            fill="#f39c12",
            outline="#e67e22",
            width=3
        )
        self.canvas.create_text(
            x_buffer, y_centro - 60,
            text="📦",
            font=("Arial", 32),
            fill="white"
        )
        self.canvas.create_text(
            x_buffer, y_centro - 10,
            text="BUFFER",
            font=("Arial", 11, "bold"),
            fill="white"
        )
        
        stats = self.hospital.get_estadisticas()
        self.canvas.create_text(
            x_buffer, y_centro + 20,
            text=f"{stats['buffer_ocupado']} / {self.hospital.capacidad_buffer}",
            font=("Arial", 14, "bold"),
            fill="white"
        )
        self.canvas.create_text(
            x_buffer, y_centro + 50,
            text="Cola de\nEspera",
            font=("Arial", 9),
            fill="white"
        )
        
        # ===== FLECHA 2: Buffer → Médicos =====
        self._dibujar_flecha(x_buffer + 80, y_centro, x_medicos - 60, y_centro, "#27ae60")
        
        # ===== MÉDICOS =====
        self.canvas.create_rectangle(
            x_medicos - 60, y_centro - 80,
            x_medicos + 60, y_centro + 80,
            fill="#e74c3c",
            outline="#c0392b",
            width=3
        )
        self.canvas.create_text(
            x_medicos, y_centro - 50,
            text="🩺",
            font=("Arial", 32),
            fill="white"
        )
        self.canvas.create_text(
            x_medicos, y_centro + 10,
            text="MÉDICOS",
            font=("Arial", 11, "bold"),
            fill="white"
        )
        self.canvas.create_text(
            x_medicos, y_centro + 40,
            text="Atienden\nPacientes",
            font=("Arial", 9),
            fill="white"
        )
        
        # ===== EXPEDIENTES (abajo) =====
        y_expedientes = alto - 100
        self.canvas.create_rectangle(
            x_buffer - 100, y_expedientes - 40,
            x_buffer + 100, y_expedientes + 40,
            fill="#9b59b6",
            outline="#8e44ad",
            width=3
        )
        self.canvas.create_text(
            x_buffer, y_expedientes - 10,
            text="📄 EXPEDIENTES",
            font=("Arial", 11, "bold"),
            fill="white"
        )
        self.canvas.create_text(
            x_buffer, y_expedientes + 15,
            text=f"Total: {stats['expedientes']['total']}",
            font=("Arial", 10),
            fill="white"
        )
        
        # Flecha: Médicos → Expedientes
        self._dibujar_flecha(
            x_medicos, y_centro + 80,
            x_buffer, y_expedientes - 40,
            "#9b59b6",
            curva=True
        )
        
        # ===== LEYENDA =====
        y_leyenda = 30
        self.canvas.create_text(
            20, y_leyenda,
            text="🔄 Flujo: Productores → Buffer → Médicos → Expedientes",
            font=("Arial", 10, "italic"),
            fill="#7f8c8d",
            anchor="w"
        )
    
    def _dibujar_flecha(self, x1, y1, x2, y2, color, curva=False):
        """Dibujar flecha animada"""
        if curva:
            # Flecha curva (para médicos → expedientes)
            puntos = [
                x1, y1,
                x1 + 50, y1 + 30,
                x2, y2
            ]
            self.canvas.create_line(
                puntos,
                arrow=tk.LAST,
                fill=color,
                width=3,
                smooth=True,
                arrowshape=(12, 15, 5)
            )
        else:
            # Flecha recta
            self.canvas.create_line(
                x1, y1, x2, y2,
                arrow=tk.LAST,
                fill=color,
                width=4,
                arrowshape=(15, 18, 6)
            )
            
            # Texto en la flecha
            x_medio = (x1 + x2) / 2
            y_medio = (y1 + y2) / 2
            self.canvas.create_text(
                x_medio, y_medio - 15,
                text="→",
                font=("Arial", 16),
                fill=color
            )
    
    def _animar_loop(self):
        """Loop de animación"""
        if not self.winfo_exists():
            return
        
        self._dibujar_flujo()
        
        # Redibujar cada 1 segundo
        self.after(1000, self._animar_loop)
    
    def on_closing(self):
        """Manejar cierre de ventana"""
        self.withdraw()


class GUIApp:
    """Aplicación principal con múltiples ventanas"""
    
    def __init__(self, hospital):
        self.hospital = hospital
        self.root = tk.Tk()
        self.root.withdraw()  # Ocultar ventana principal
        
        # Crear ventanas
        self.panel_control = PanelControl(self.root, hospital)
        self.visualizacion = VisualizacionFlujo(self.root, hospital)
        
        # Configurar cierre de aplicación
        self.root.protocol("WM_DELETE_WINDOW", self.cerrar_aplicacion)
    
    def ejecutar(self):
        """Iniciar la aplicación"""
        self.root.mainloop()
    
    def cerrar_aplicacion(self):
        """Cerrar toda la aplicación"""
        respuesta = messagebox.askyesno(
            "Salir",
            "¿Deseas cerrar el sistema hospitalario?"
        )
        
        if respuesta:
            self.hospital.detener()
            self.root.quit()
            self.root.destroy()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Launcher para abrir múltiples ventanas del sistema hospitalario
================================================================

Este script permite abrir múltiples ventanas de panel_hospital y registro_paciente
desde un solo proceso, compartiendo la misma aplicación Tkinter.

Uso:
    python launcher.py
"""

import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import sys
import os

# Agregar directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ui.panel_hospital import PanelHospital
from ui.registro_paciente import RegistroPaciente


class LauncherApp:
    """Aplicación launcher para abrir múltiples ventanas"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🏥 Sistema Hospitalario - Launcher")
        self.root.geometry("600x400")
        self.root.configure(bg="#ecf0f1")
        
        self.ventanas_panel = []
        self.ventanas_registro = []
        
        self._crear_interfaz()
        
        # Verificar si el servidor está corriendo
        self._verificar_servidor()
    
    def _crear_interfaz(self):
        """Crear la interfaz del launcher"""
        
        # Header
        frame_header = tk.Frame(self.root, bg="#2c3e50", height=80)
        frame_header.pack(fill=tk.X)
        frame_header.pack_propagate(False)
        
        tk.Label(
            frame_header,
            text="🏥 SISTEMA HOSPITALARIO",
            font=("Arial", 20, "bold"),
            fg="white",
            bg="#2c3e50"
        ).pack(pady=25)
        
        # Body
        frame_body = tk.Frame(self.root, bg="#ecf0f1", padx=30, pady=20)
        frame_body.pack(fill=tk.BOTH, expand=True)
        
        # Estado del servidor
        self.label_estado = tk.Label(
            frame_body,
            text="⏳ Verificando servidor...",
            font=("Arial", 11),
            bg="#ecf0f1",
            fg="#7f8c8d"
        )
        self.label_estado.pack(pady=10)
        
        # Separador
        ttk.Separator(frame_body, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=20)
        
        # Botón: Panel Hospital
        tk.Button(
            frame_body,
            text="📊 Abrir Panel del Hospital",
            font=("Arial", 12, "bold"),
            bg="#3498db",
            fg="white",
            width=30,
            height=2,
            cursor="hand2",
            command=self.abrir_panel_hospital
        ).pack(pady=10)
        
        # Botón: Registro Paciente
        tk.Button(
            frame_body,
            text="📋 Abrir Registro de Pacientes",
            font=("Arial", 12, "bold"),
            bg="#27ae60",
            fg="white",
            width=30,
            height=2,
            cursor="hand2",
            command=self.abrir_registro_paciente
        ).pack(pady=10)
        
        # Separador
        ttk.Separator(frame_body, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=20)
        
        # Info
        tk.Label(
            frame_body,
            text="💡 Puedes abrir múltiples ventanas de cada tipo",
            font=("Arial", 9, "italic"),
            bg="#ecf0f1",
            fg="#7f8c8d"
        ).pack()
        
        # Footer
        frame_footer = tk.Frame(self.root, bg="#34495e", height=40)
        frame_footer.pack(fill=tk.X, side=tk.BOTTOM)
        frame_footer.pack_propagate(False)
        
        tk.Label(
            frame_footer,
            text="Sistema Hospitalario - Proyecto de Sistemas Operativos",
            font=("Arial", 9),
            fg="white",
            bg="#34495e"
        ).pack(pady=10)
    
    def _verificar_servidor(self):
        """Verificar si el servidor está corriendo"""
        import socket
        
        def verificar():
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(1)
                s.connect(('localhost', 5555))
                s.close()
                self.label_estado.config(
                    text="🟢 Servidor activo (puerto 5555)",
                    fg="#27ae60"
                )
            except:
                self.label_estado.config(
                    text="🔴 Servidor no disponible (modo demo)",
                    fg="#e74c3c"
                )
        
        self.root.after(100, verificar)
    
    def abrir_panel_hospital(self):
        """Abrir una nueva ventana de panel hospital"""
        try:
            ventana = PanelHospital(self.root)
            self.ventanas_panel.append(ventana)
            print(f"✅ Panel Hospital abierto ({len(self.ventanas_panel)} ventanas)")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir el panel:\n{e}")
    
    def abrir_registro_paciente(self):
        """Abrir una nueva ventana de registro"""
        try:
            ventana = RegistroPaciente(self.root)
            self.ventanas_registro.append(ventana)
            print(f"✅ Registro abierto ({len(self.ventanas_registro)} ventanas)")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir el registro:\n{e}")
    
    def ejecutar(self):
        """Ejecutar la aplicación"""
        self.root.mainloop()


def main():
    """Función principal"""
    print("=" * 60)
    print("🏥 LAUNCHER DEL SISTEMA HOSPITALARIO")
    print("=" * 60)
    print()
    print("💡 Este launcher permite abrir múltiples ventanas")
    print("   desde un solo proceso.")
    print()
    print("📋 Opciones:")
    print("   - Abrir Panel del Hospital")
    print("   - Abrir Registro de Pacientes")
    print()
    print("🌐 Si el servidor (servidor.py) está corriendo,")
    print("   las ventanas se conectarán automáticamente.")
    print()
    print("=" * 60)
    print()
    
    try:
        app = LauncherApp()
        app.ejecutar()
    except KeyboardInterrupt:
        print("\n⏸️  Launcher cerrado")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

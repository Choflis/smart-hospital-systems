#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ventana de Registro de Pacientes
=================================

Interfaz gráfica para registrar nuevos pacientes en el sistema hospitalario.
Puede ejecutarse de forma independiente:
    python ui/registro_paciente.py

Si el sistema principal está activo, se conecta y registra pacientes reales.
Si no, muestra la interfaz sin conexión funcional.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import threading
import socket
import json
import sys
import os

# Agregar directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class RegistroPaciente(tk.Toplevel):
    """Ventana de Registro de Pacientes"""
    
    def __init__(self, parent=None, host='localhost', port=5555):
        """
        Inicializar registro de pacientes
        
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
        
        # Si es standalone, configurar cierre
        if self._is_standalone:
            self.protocol("WM_DELETE_WINDOW", self._on_closing_standalone)
        
        self.host = host
        self.port = port
        self.socket = None
        self.conectado = False
        
        # Configuración de la ventana
        self.title("🏥 Registro de Pacientes")
        self.geometry("500x650")
        self.configure(bg="#ecf0f1")
        self.resizable(False, False)
        
        # Variables del formulario
        self.var_nombre = tk.StringVar()
        self.var_apellidos = tk.StringVar()
        self.var_dni = tk.StringVar()
        self.var_telefono = tk.StringVar()
        self.var_edad = tk.StringVar()
        self.var_genero = tk.StringVar(value="Masculino")
        self.var_sintomas = tk.StringVar()
        self.var_doctor = tk.StringVar()
        
        # Contador de pacientes registrados
        self.pacientes_registrados = 0
        
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
                self.after(0, lambda: self._actualizar_estado_conexion(True))
                
                # Solicitar lista de médicos
                self._enviar_comando({'comando': 'obtener_medicos'})
                
                # Iniciar thread para recibir respuestas
                thread = threading.Thread(target=self._recibir_respuestas, daemon=True)
                thread.start()
                
            except Exception as e:
                self.conectado = False
                self.after(0, lambda: self._actualizar_estado_conexion(False))
                self.after(0, self._cargar_doctores)
        
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
            return False
    
    def _recibir_respuestas(self):
        """Recibe respuestas del servidor"""
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
                        self._procesar_respuesta(mensaje)
            
            except socket.timeout:
                continue
            except Exception as e:
                if self.conectado:
                    self.conectado = False
                    self.after(0, lambda: self._actualizar_estado_conexion(False))
                break
    
    def _procesar_respuesta(self, respuesta):
        """Procesa una respuesta del servidor"""
        tipo = respuesta.get('tipo')
        
        if tipo == 'medicos':
            # Lista de médicos recibida
            medicos = [m['nombre'] for m in respuesta.get('medicos', [])]
            self.after(0, lambda: self._actualizar_lista_medicos(medicos))
        
        elif tipo == 'confirmacion':
            # Confirmación de registro
            estado = respuesta.get('estado')
            if estado == 'ok':
                self.after(0, lambda: self._confirmar_registro())
    
    def _actualizar_estado_conexion(self, conectado):
        """Actualiza el indicador de estado de conexión"""
        if hasattr(self, 'label_estado'):
            if conectado:
                self.label_estado.config(
                    text="🟢 Conectado al sistema",
                    fg="#27ae60"
                )
            else:
                self.label_estado.config(
                    text="🔴 Sin conexión (modo demo)",
                    fg="#e74c3c"
                )
    
    def _actualizar_lista_medicos(self, medicos):
        """Actualiza la lista de médicos en el combobox"""
        if medicos:
            self.combo_doctor['values'] = medicos
            if len(medicos) > 0:
                self.combo_doctor.current(0)
    
    def _crear_interfaz(self):
        """Crear la interfaz de registro"""
        
        # ===== ENCABEZADO =====
        frame_header = tk.Frame(self, bg="#3498db", height=80)
        frame_header.pack(fill=tk.X)
        frame_header.pack_propagate(False)
        
        tk.Label(
            frame_header,
            text="📋 REGISTRO DE PACIENTES",
            font=("Arial", 20, "bold"),
            fg="white",
            bg="#3498db"
        ).pack(pady=25)
        
        # ===== INDICADOR DE ESTADO =====
        frame_estado = tk.Frame(self, bg="#ecf0f1", height=30)
        frame_estado.pack(fill=tk.X)
        
        self.label_estado = tk.Label(
            frame_estado,
            text="⏳ Conectando...",
            font=("Arial", 9, "italic"),
            fg="#7f8c8d",
            bg="#ecf0f1"
        )
        self.label_estado.pack(pady=5)
        
        # ===== FORMULARIO =====
        frame_form = tk.Frame(self, bg="#ecf0f1", padx=30, pady=20)
        frame_form.pack(fill=tk.BOTH, expand=True)
        
        # Nombre
        self._crear_campo(frame_form, "Nombre:", self.var_nombre, 0)
        
        # Apellidos
        self._crear_campo(frame_form, "Apellidos:", self.var_apellidos, 1)
        
        # DNI
        self._crear_campo(frame_form, "DNI:", self.var_dni, 2)
        
        # Teléfono
        self._crear_campo(frame_form, "Teléfono:", self.var_telefono, 3)
        
        # Edad
        self._crear_campo(frame_form, "Edad:", self.var_edad, 4)
        
        # Género
        tk.Label(
            frame_form,
            text="Género:",
            font=("Arial", 11, "bold"),
            bg="#ecf0f1",
            anchor="w"
        ).grid(row=5, column=0, sticky="w", pady=8)
        
        frame_genero = tk.Frame(frame_form, bg="#ecf0f1")
        frame_genero.grid(row=5, column=1, sticky="w", pady=8)
        
        tk.Radiobutton(
            frame_genero,
            text="Masculino",
            variable=self.var_genero,
            value="Masculino",
            font=("Arial", 10),
            bg="#ecf0f1"
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Radiobutton(
            frame_genero,
            text="Femenino",
            variable=self.var_genero,
            value="Femenino",
            font=("Arial", 10),
            bg="#ecf0f1"
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Radiobutton(
            frame_genero,
            text="Otro",
            variable=self.var_genero,
            value="Otro",
            font=("Arial", 10),
            bg="#ecf0f1"
        ).pack(side=tk.LEFT, padx=5)
        
        # Síntomas
        tk.Label(
            frame_form,
            text="Síntomas:",
            font=("Arial", 11, "bold"),
            bg="#ecf0f1",
            anchor="w"
        ).grid(row=6, column=0, sticky="nw", pady=8)
        
        text_sintomas = tk.Text(
            frame_form,
            height=4,
            width=30,
            font=("Arial", 10),
            wrap=tk.WORD,
            relief=tk.SOLID,
            borderwidth=1
        )
        text_sintomas.grid(row=6, column=1, sticky="ew", pady=8)
        self.text_sintomas = text_sintomas
        
        # Doctor asignado
        tk.Label(
            frame_form,
            text="Doctor:",
            font=("Arial", 11, "bold"),
            bg="#ecf0f1",
            anchor="w"
        ).grid(row=7, column=0, sticky="w", pady=8)
        
        self.combo_doctor = ttk.Combobox(
            frame_form,
            textvariable=self.var_doctor,
            font=("Arial", 10),
            state="readonly",
            width=28
        )
        self.combo_doctor.grid(row=7, column=1, sticky="ew", pady=8)
        
        # Configurar grid
        frame_form.columnconfigure(1, weight=1)
        
        # ===== BOTONES =====
        frame_botones = tk.Frame(self, bg="#ecf0f1", pady=20)
        frame_botones.pack(fill=tk.X)
        
        tk.Button(
            frame_botones,
            text="✅ REGISTRAR PACIENTE",
            font=("Arial", 12, "bold"),
            bg="#27ae60",
            fg="white",
            width=20,
            height=2,
            cursor="hand2",
            command=self._registrar_paciente
        ).pack(side=tk.LEFT, padx=20)
        
        tk.Button(
            frame_botones,
            text="🔄 LIMPIAR FORMULARIO",
            font=("Arial", 12, "bold"),
            bg="#e67e22",
            fg="white",
            width=20,
            height=2,
            cursor="hand2",
            command=self._limpiar_formulario
        ).pack(side=tk.RIGHT, padx=20)
        
        # ===== PIE DE PÁGINA =====
        frame_footer = tk.Frame(self, bg="#34495e", height=40)
        frame_footer.pack(fill=tk.X, side=tk.BOTTOM)
        frame_footer.pack_propagate(False)
        
        self.label_contador = tk.Label(
            frame_footer,
            text="Pacientes registrados: 0",
            font=("Arial", 10),
            fg="white",
            bg="#34495e"
        )
        self.label_contador.pack(pady=10)
    
    def _crear_campo(self, parent, texto, variable, fila):
        """Crear un campo de entrada estándar"""
        tk.Label(
            parent,
            text=texto,
            font=("Arial", 11, "bold"),
            bg="#ecf0f1",
            anchor="w"
        ).grid(row=fila, column=0, sticky="w", pady=8)
        
        entry = tk.Entry(
            parent,
            textvariable=variable,
            font=("Arial", 10),
            width=30,
            relief=tk.SOLID,
            borderwidth=1
        )
        entry.grid(row=fila, column=1, sticky="ew", pady=8)
        
        return entry
    
    def _cargar_doctores(self):
        """Cargar lista de doctores disponibles (modo demo)"""
        # Doctores por defecto para modo demo/independiente
        doctores = [
            "Dr. García",
            "Dra. Martínez",
            "Dr. López",
            "Dra. Rodríguez",
            "Dr. Sánchez"
        ]
        
        self.combo_doctor['values'] = doctores
        if doctores:
            self.combo_doctor.current(0)
    
    def _validar_formulario(self):
        """Validar que todos los campos estén completos"""
        if not self.var_nombre.get().strip():
            messagebox.showerror("Error", "Por favor ingrese el nombre")
            return False
        
        if not self.var_apellidos.get().strip():
            messagebox.showerror("Error", "Por favor ingrese los apellidos")
            return False
        
        if not self.var_dni.get().strip():
            messagebox.showerror("Error", "Por favor ingrese el DNI")
            return False
        
        if not self.var_telefono.get().strip():
            messagebox.showerror("Error", "Por favor ingrese el teléfono")
            return False
        
        if not self.var_edad.get().strip():
            messagebox.showerror("Error", "Por favor ingrese la edad")
            return False
        
        try:
            edad = int(self.var_edad.get())
            if edad < 0 or edad > 150:
                messagebox.showerror("Error", "Edad inválida")
                return False
        except ValueError:
            messagebox.showerror("Error", "La edad debe ser un número")
            return False
        
        sintomas = self.text_sintomas.get("1.0", tk.END).strip()
        if not sintomas:
            messagebox.showerror("Error", "Por favor ingrese los síntomas")
            return False
        
        if not self.var_doctor.get():
            messagebox.showerror("Error", "Por favor seleccione un doctor")
            return False
        
        return True
    
    def _registrar_paciente(self):
        """Registrar el paciente en el sistema"""
        if not self._validar_formulario():
            return
        
        # Obtener datos del formulario
        nombre_completo = f"{self.var_nombre.get()} {self.var_apellidos.get()}"
        dni = self.var_dni.get()
        telefono = self.var_telefono.get()
        edad = int(self.var_edad.get())
        genero = self.var_genero.get()
        sintomas = self.text_sintomas.get("1.0", tk.END).strip()
        doctor = self.var_doctor.get()
        
        # Crear diccionario de paciente
        paciente_data = {
            'id': int(datetime.now().timestamp() * 1000) % 1000000,
            'nombre': nombre_completo,
            'dni': dni,
            'telefono': telefono,
            'edad': edad,
            'genero': genero,
            'sintomas': sintomas,
            'doctor_asignado': doctor,
            'fecha_registro': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'estado': 'En espera'
        }
        
        # Imprimir en consola
        print("\n" + "="*60)
        print("✅ NUEVO PACIENTE REGISTRADO")
        print("="*60)
        print(f"ID: {paciente_data['id']}")
        print(f"Nombre: {paciente_data['nombre']}")
        print(f"DNI: {paciente_data['dni']}")
        print(f"Teléfono: {paciente_data['telefono']}")
        print(f"Edad: {paciente_data['edad']} años")
        print(f"Género: {paciente_data['genero']}")
        print(f"Síntomas: {paciente_data['sintomas']}")
        print(f"Doctor asignado: {paciente_data['doctor_asignado']}")
        print(f"Fecha de registro: {paciente_data['fecha_registro']}")
        print("="*60 + "\n")
        
        # Si está conectado, enviar al servidor
        if self.conectado:
            comando = {
                'comando': 'registrar_paciente',
                'datos': paciente_data
            }
            if self._enviar_comando(comando):
                # El servidor confirmará el registro
                pass
            else:
                # Conexión perdida, mostrar en modo demo
                self._mostrar_confirmacion_demo(nombre_completo, doctor)
        else:
            # Modo demo
            self._mostrar_confirmacion_demo(nombre_completo, doctor)
        
        # Incrementar contador
        self.pacientes_registrados += 1
        self.label_contador.config(text=f"Pacientes registrados: {self.pacientes_registrados}")
        
        # Limpiar formulario
        self._limpiar_formulario()
    
    def _confirmar_registro(self):
        """Confirmación de registro desde el servidor"""
        messagebox.showinfo(
            "Éxito",
            "Paciente registrado correctamente en el sistema"
        )
    
    def _mostrar_confirmacion_demo(self, nombre, doctor):
        """Muestra confirmación en modo demo"""
        messagebox.showinfo(
            "Modo Demo",
            f"Paciente {nombre} registrado (modo demo)\n"
            f"Asignado a: {doctor}\n\n"
            f"Para conexión real, inicie el sistema principal:\n"
            f"python main.py"
        )
    
    def _limpiar_formulario(self):
        """Limpiar todos los campos del formulario"""
        self.var_nombre.set("")
        self.var_apellidos.set("")
        self.var_dni.set("")
        self.var_telefono.set("")
        self.var_edad.set("")
        self.var_genero.set("Masculino")
        self.text_sintomas.delete("1.0", tk.END)
        if self.combo_doctor['values']:
            self.combo_doctor.current(0)
    
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
    """Ejecutar ventana de registro de forma independiente"""
    print("=" * 60)
    print("🏥 REGISTRO DE PACIENTES")
    print("=" * 60)
    print("\n💡 Esta ventana se conecta al sistema hospitalario")
    print("   Si el sistema no está activo, funcionará en modo demo")
    print("\n📋 Para iniciar el servidor:")
    print("   python servidor.py")
    print("\n💡 Para abrir múltiples ventanas:")
    print("   python launcher.py")
    print("\n=" * 60 + "\n")
    
    app = RegistroPaciente()
    app.mainloop()


if __name__ == "__main__":
    main()

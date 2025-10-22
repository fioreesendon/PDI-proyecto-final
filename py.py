import tkinter as tk
from tkinter import messagebox
import win32serviceutil
import psutil
import time

def obtener_servicios():
    """Obtiene todos los servicios y su estado (activo/deshabilitado)."""
    servicios = []
    for servicio in psutil.win_service_iter():
        estado = "Habilitado" if servicio.status() == psutil.STATUS_RUNNING else "Deshabilitado"
        # Simulamos el fabricante con el nombre del servicio
        fabricante = servicio.as_dict().get('name', 'Desconocido')
        servicios.append((servicio.name(), estado, fabricante))
    return servicios

def cambiar_estado(servicio, nuevo_estado):
    """Cambia el estado del servicio a habilitado o deshabilitado."""
    try:
        if nuevo_estado == 'Habilitar':
            win32serviceutil.StartService(servicio)
            time.sleep(1)  # Pausa para asegurar que el estado cambie
        else:
            win32serviceutil.StopService(servicio)
            time.sleep(1)
        
        # Retornamos el nuevo estado
        estado_actual = "Habilitado" if nuevo_estado == 'Habilitar' else "Deshabilitado"
        return estado_actual
    except Exception as e:
        messagebox.showerror("Error", f"Error al cambiar el estado del servicio: {e}")
        return None

def actualizar_estado(servicio, nuevo_estado):
    """Actualiza el estado visual de la interfaz."""
    for idx, (chk, estado, label_estado) in enumerate(checkbuttons):
        if chk.cget("text").startswith(servicio):
            # Cambia el texto del checkbutton para reflejar el nuevo estado
            estado_texto = f"{servicio} ({nuevo_estado})"
            chk.config(text=estado_texto)
            label_estado.config(text=nuevo_estado)

def on_toggle_check(servicio, var, label_estado):
    """Se ejecuta cuando se cambia el estado del Checkbutton."""
    nuevo_estado = 'Habilitar' if var.get() == 1 else 'Deshabilitar'
    estado_actual = cambiar_estado(servicio, nuevo_estado)
    if estado_actual:
        # Actualiza el estado visual en tiempo real
        actualizar_estado(servicio, estado_actual)

# Crear la ventana principal
root = tk.Tk()
root.title("Gestor de Servicios")
root.geometry("600x400")

# Obtener la lista de servicios
servicios = obtener_servicios()

# Crear un contenedor de tabla para mostrar los servicios y sus estados
frame_servicios = tk.Frame(root)
frame_servicios.pack(padx=10, pady=10)

# Crear la cabecera de la tabla
label_servicio = tk.Label(frame_servicios, text="Servicio", width=30, anchor="w", font=("Arial", 10, "bold"))
label_estado = tk.Label(frame_servicios, text="Estado", width=15, anchor="w", font=("Arial", 10, "bold"))
label_fabricante = tk.Label(frame_servicios, text="Fabricante", width=20, anchor="w", font=("Arial", 10, "bold"))

label_servicio.grid(row=0, column=0, padx=5, pady=5)
label_estado.grid(row=0, column=1, padx=5, pady=5)
label_fabricante.grid(row=0, column=2, padx=5, pady=5)

# Lista para almacenar los checkbuttons, estados y etiquetas de estado
checkbuttons = []

# Crear los checkbuttons para los servicios
for idx, (servicio, estado, fabricante) in enumerate(servicios):
    var = tk.IntVar(value=1 if estado == "Habilitado" else 0)
    
    # Creamos el Checkbutton
    chk = tk.Checkbutton(frame_servicios, text=f"{servicio} ({estado})", variable=var, anchor="w", width=30,
                         command=lambda s=servicio, v=var, l=label_estado: on_toggle_check(s, v, l))
    chk.grid(row=idx + 1, column=0, padx=5, pady=5, sticky="w")
    
    # Creamos una etiqueta para mostrar el estado
    label_estado = tk.Label(frame_servicios, text=estado, width=15, anchor="w")
    label_estado.grid(row=idx + 1, column=1, padx=5, pady=5)
    
    # Creamos una etiqueta para mostrar el fabricante
    label_fab = tk.Label(frame_servicios, text=fabricante, width=20, anchor="w")
    label_fab.grid(row=idx + 1, column=2, padx=5, pady=5)
    
    # Guardamos el checkbutton, estado y label de estado en la lista
    checkbuttons.append((chk, estado, label_estado))

# Ejecutar la aplicación
root.mainloop()
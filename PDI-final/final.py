import tkinter as tk
from tkinter import messagebox
import win32serviceutil
import psutil
import time

def obtener_servicios():
    """Obtiene todos los servicios y su estado."""
    servicios = []
    for servicio in psutil.win_service_iter():
        try:
            s = servicio.as_dict()

            nombre = s.get("name", servicio.name())
            estado = "Habilitado" if servicio.status() == psutil.STATUS_RUNNING else "Deshabilitado"
            fabricante = s.get("display_name", "Desconocido")

            servicios.append((nombre, estado, fabricante))

        except Exception:
            continue
    return servicios

def cambiar_estado(servicio, nuevo_estado):
    try:
        if nuevo_estado == 'Habilitar':
            win32serviceutil.StartService(servicio)
            time.sleep(1)
        else:
            win32serviceutil.StopService(servicio)
            time.sleep(1)

        return "Habilitado" if nuevo_estado == 'Habilitar' else "Deshabilitado"
    except Exception as e:
        messagebox.showerror("Error", f"Error al cambiar el estado del servicio:\n{e}")
        return None

def actualizar_estado(servicio, nuevo_estado):
    for chk, _, estado_label in checkbuttons:
        if chk.cget("text").startswith(servicio):
            chk.config(text=f"{servicio} ({nuevo_estado})")
            estado_label.config(text=nuevo_estado)

def on_toggle_check(servicio, var, label_estado):
    nuevo_estado = 'Habilitar' if var.get() == 1 else 'Deshabilitar'
    estado_actual = cambiar_estado(servicio, nuevo_estado)
    if estado_actual:
        actualizar_estado(servicio, estado_actual)

# ---------------- INTERFAZ ----------------

root = tk.Tk()
root.title("Gestor de Servicios")
root.geometry("650x500")

# Frame contenedor con scrollbar
contenedor = tk.Frame(root)
contenedor.pack(fill="both", expand=True)

canvas = tk.Canvas(contenedor)
canvas.pack(side="left", fill="both", expand=True)

scrollbar = tk.Scrollbar(contenedor, orient="vertical", command=canvas.yview)
scrollbar.pack(side="right", fill="y")

canvas.configure(yscrollcommand=scrollbar.set)
canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

frame_servicios = tk.Frame(canvas)
canvas.create_window((0, 0), window=frame_servicios, anchor="nw")

# Encabezados
tk.Label(frame_servicios, text="Servicio", width=30, anchor="w", font=("Arial", 10, "bold")).grid(row=0, column=0, padx=5, pady=5)
tk.Label(frame_servicios, text="Estado", width=15, anchor="w", font=("Arial", 10, "bold")).grid(row=0, column=1, padx=5, pady=5)
tk.Label(frame_servicios, text="Fabricante", width=20, anchor="w", font=("Arial", 10, "bold")).grid(row=0, column=2, padx=5, pady=5)

servicios = obtener_servicios()
checkbuttons = []

for idx, (servicio, estado, fabricante) in enumerate(servicios):
    var = tk.IntVar(value=1 if estado == "Habilitado" else 0)

    chk = tk.Checkbutton(frame_servicios, text=f"{servicio} ({estado})", variable=var, anchor="w", width=30,
                         command=lambda s=servicio, v=var: on_toggle_check(s, v, None))
    chk.grid(row=idx + 1, column=0, padx=5, pady=2, sticky="w")

    estado_label = tk.Label(frame_servicios, text=estado, width=15, anchor="w")
    estado_label.grid(row=idx + 1, column=1, padx=5, pady=2)

    tk.Label(frame_servicios, text=fabricante, width=20, anchor="w").grid(row=idx + 1, column=2, padx=5, pady=2)

    checkbuttons.append((chk, estado, estado_label))

root.mainloop()
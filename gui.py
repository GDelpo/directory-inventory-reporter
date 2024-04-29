from main import main
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox


def elegir_ruta():
    ruta = filedialog.askdirectory()
    if ruta:
        ruta_elegida.set(f"Ruta elegida: {ruta}")
        btn_lanzar_informe.config(state=tk.NORMAL)

def lanzar_informe():
    ruta_seleccionada = ruta_elegida.get()
    # Elimina el texto "Ruta elegida: " al principio de la cadena
    ruta_seleccionada = ruta_seleccionada.replace("Ruta elegida: ", "")
    if ruta_seleccionada:
        main(ruta_seleccionada)  # Llama a la función con la ruta seleccionada
        messagebox.showinfo("Info", "Se finalizó el proceso con éxito")
        ruta_elegida.set(None)  # Limpia la variable para futuros usos
        ruta_elegida.set("Ruta elegida: ")
        btn_lanzar_informe.config(state=tk.DISABLED)
    else:
        # Manejo de error si no se ha seleccionado una ruta
        messagebox.showerror("Error", "Primero, elija una ruta.")

if __name__ == "__main__":
    
    app = tk.Tk()
    app.title("Seleccionar Directorio")

    ruta_elegida = tk.StringVar()
    ruta_elegida.set("Ruta elegida: ")

    label_ruta = tk.Label(app, textvariable=ruta_elegida)
    label_ruta.pack(pady=10)

    btn_elegir_ruta = tk.Button(app, text="Elegir Ruta", command=elegir_ruta)
    btn_elegir_ruta.pack()

    btn_lanzar_informe = tk.Button(app, text="Lanzar Informe", state=tk.DISABLED, command=lanzar_informe)
    btn_lanzar_informe.pack(pady=10)

    app.mainloop()
    

import tkinter as tk
from tkinter import messagebox
class Participante:
    def __init__(self, nombre, institucion):
        self.nombre = nombre
        self.institucion = institucion

    def mostrar_info(self):
        return f"{self.nombre} - {self.institucion}"


class BandaEscolar(Participante):
    CATEGORIAS_VALIDAS = ["Primaria", "Basico", "Diversificado"]
    CRITERIOS = ["ritmo (1 a 10)", "uniformidad(1 a 10)", "coreografía(1 a 10)", "alineación(1 a 10)", "puntualidad(1 a 10)"]

    def __init__(self, nombre, institucion, categoria):
        super().__init__(nombre, institucion)
        self._categoria = None
        self._puntajes = {}
        self.set_categoria(categoria)

    def set_categoria(self, categoria):
        if categoria not in BandaEscolar.CATEGORIAS_VALIDAS:
            raise ValueError(f"Categoría inválida: {categoria}")
        self._categoria = categoria

    def registrar_puntajes(self, puntajes: dict):
        if set(puntajes.keys()) != set(BandaEscolar.CRITERIOS):
            raise ValueError("Faltan o sobran criterios de evaluación.")
        for c, v in puntajes.items():
            if not (0 <= v <= 10):
                raise ValueError(f"Puntaje inválido en {c}: {v}")
        self._puntajes = puntajes

    @property
    def total(self):
        return sum(self._puntajes.values()) if self._puntajes else 0

    def mostrar_info(self):
        info = super().mostrar_info() + f" | Categoría: {self._categoria}"
        if self._puntajes:
            info += f" | Total: {self.total}"
        return info


class Concurso:
    def __init__(self, nombre, fecha):
        self.nombre = nombre
        self.fecha = fecha
        self._bandas = []

    def inscribir_banda(self, banda: BandaEscolar):
        if any(b.nombre == banda.nombre for b in self._bandas):
            raise ValueError(f"La banda '{banda.nombre}' ya está inscrita.")
        self._bandas.append(banda)

    def registrar_evaluacion(self, nombre_banda, puntajes):
        for banda in self._bandas:
            if banda.nombre == nombre_banda:
                banda.registrar_puntajes(puntajes)
                return
        raise ValueError(f"No existe una banda llamada {nombre_banda}")

    def listar_bandas(self):
        return [b.mostrar_info() for b in self._bandas]

    def ranking(self):
        return sorted(
            self._bandas,
            key=lambda b: b.total,
            reverse=True
        )
class ConcursoBandasApp:
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("Concurso de Bandas - Quetzaltenango")
        self.ventana.geometry("500x300")

        # Crear concurso
        self.concurso = Concurso("Concurso de Bandas - 14 de Septiembre", "2025-09-14")

        self.menu()

        tk.Label(
            self.ventana,
            text="Sistema de Inscripción y Evaluación de Bandas Escolares\nConcurso 14 de Septiembre - Quetzaltenango",
            font=("Arial", 12, "bold"),
            justify="center"
        ).pack(pady=50)

        self.ventana.mainloop()

    def menu(self):
        barra = tk.Menu(self.ventana)
        opciones = tk.Menu(barra, tearoff=0)
        opciones.add_command(label="Inscribir Banda", command=self.inscribir_banda)
        opciones.add_command(label="Registrar Evaluación", command=self.registrar_evaluacion)
        opciones.add_command(label="Listar Bandas", command=self.listar_bandas)
        opciones.add_command(label="Ver Ranking", command=self.ver_ranking)
        opciones.add_separator()
        opciones.add_command(label="Salir", command=self.ventana.quit)
        barra.add_cascade(label="Opciones", menu=opciones)
        self.ventana.config(menu=barra)
    def inscribir_banda(self):
        ventana = tk.Toplevel(self.ventana)
        ventana.title("Inscribir Banda")

        tk.Label(ventana, text="Nombre de la Banda").grid(row=0, column=0)
        tk.Label(ventana, text="Institución").grid(row=1, column=0)
        tk.Label(ventana, text="Categoría").grid(row=2, column=0, pady = 5, sticky="W")

        nombre_entry = tk.Entry(ventana)
        inst_entry = tk.Entry(ventana)

        nombre_entry.grid(row=0, column=1)
        inst_entry.grid(row=1, column=1)
        categoria_var = tk.StringVar(ventana)
        categoria_var.set(BandaEscolar.CATEGORIAS_VALIDAS[0])
        menu = tk.OptionMenu(ventana,categoria_var, *BandaEscolar.CATEGORIAS_VALIDAS)
        menu.grid(row=2, column=1, padx = 10, pady = 5)

        def guardar():
            try:
                banda = BandaEscolar(nombre_entry.get(), inst_entry.get(), categoria_var.get())
                self.concurso.inscribir_banda(banda)
                messagebox.showinfo("Éxito", f"Banda '{banda.nombre}' inscrita correctamente.")
                ventana.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        tk.Button(ventana, text="Guardar", command=guardar).grid(row=3, column=0, columnspan=2)

    def registrar_evaluacion(self):
        ventana = tk.Toplevel(self.ventana)
        ventana.title("Registrar Evaluación")

        tk.Label(ventana, text="Nombre de la Banda").grid(row=0, column=0)
        nombre_entry = tk.Entry(ventana)
        nombre_entry.grid(row=0, column=1)

        entradas = {}
        for i, crit in enumerate(BandaEscolar.CRITERIOS, start=1):
            tk.Label(ventana, text=crit.capitalize()).grid(row=i, column=0)
            ent = tk.Entry(ventana)
            ent.grid(row=i, column=1)
            entradas[crit] = ent

        def guardar():
            try:
                puntajes = {c: int(e.get()) for c, e in entradas.items()}
                self.concurso.registrar_evaluacion(nombre_entry.get(), puntajes)
                messagebox.showinfo("Éxito", "Evaluación registrada correctamente.")
                ventana.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        tk.Button(ventana, text="Guardar", command=guardar).grid(row=6, column=0, columnspan=2)

    def listar_bandas(self):
        ventana = tk.Toplevel(self.ventana)
        ventana.title("Listado de Bandas")
        text = tk.Text(ventana, width=60, height=15)
        text.pack()
        for info in self.concurso.listar_bandas():
            text.insert(tk.END, info + "\n")

    def ver_ranking(self):
        ventana = tk.Toplevel(self.ventana)
        ventana.title("Ranking Final")
        text = tk.Text(ventana, width=60, height=15)
        text.pack()
        for i, banda in enumerate(self.concurso.ranking(), 1):
            text.insert(tk.END, f"{i}. {banda.nombre} - {banda.institucion} | "
                                f"{banda._categoria} | Total: {banda.total}\n")


if __name__ == "__main__":
    ConcursoBandasApp()

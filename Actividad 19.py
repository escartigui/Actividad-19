import tkinter as tk
from tkinter import messagebox


class Participante:
    def __init__(self, nombre, institucion):
        self.nombre = nombre
        self.institucion = institucion
    def mostrarparticipantes(self):
        return f"Nombre:{self.nombre}, Institucion:{self.institucion},"
class BandaEscolar(Participante):
    categoriasvalidas = ["Primaria", "Basico", "Diversificado"]
    def __init__(self,nombre,institucion, categoria):
        super().__init__(nombre, institucion)
        self.categoria = None
        self.set_categoria(categoria)
    def set_categoria(self,categoria):
        if categoria not in BandaEscolar.categoriasvalidas:
            raise ValueError(f"Categoria invalida: {categoria}")
        self.categoria = categoria
class Criterios(BandaEscolar):
    criterios = ["ritmo","uniformidad","coreografia","alineacion","puntualidad"]
    def __init__(self,nombre,institucion, categoria):
        super().__init__(nombre, institucion,categoria)
        self.puntajes = {}
    def registro_puntajes(self,puntajes:dict):
        if set(puntajes.keys()) != set(self.criterios):
            raise ValueError(f"Verifica los criterios")
        for criterio, valor in puntajes.items():
            if not(0 <= valor <= 10):
                raise ValueError(f"Valor invalido: {valor}")
        self.puntajes = puntajes
    def total(self):
        return sum(self.puntajes.values()) if self.puntajes else 0
    def promedio(self):
        return self.total()/len(self.puntajes) if self.puntajes else 0
    def mostrarpuntajes(self):
        info = super().mostrarparticipantes() + f"|categoria: {self.categoria}"
        if self.puntajes:
            info += f"| Total: {self.total()}"
        return info
class Concurso:
    def __init__(self,nombre,fecha):
        self.nombre = nombre
        self.fecha = fecha
        self.bandas = []
    def inscribir_banda(self, banda:BandaEscolar):
        if any(b.nombre == banda.nombre for b in self.bandas):
            raise ValueError("La banda ya existe")
        self.bandas.append(banda)
    def registrar_evaluacion(self,nombre_banda, puntajes):
        for banda in self.bandas:
            if banda.nombre == nombre_banda:
                banda.registrar_puntajes(puntajes)
                return
        raise ValueError(f"No existe la banda {nombre_banda}")
    def listar_bandas(self):
        print(f"Listado de bandas")
        for banda in self.bandas:
            print(banda.mostrarpuntajes())
    def ranking(self):
        ordenados = sorted(self.bandas, key = lambda b: (b.total, b.promedio), reverse = True)
        print("\n Ranking Final")
        for i,banda in enumerate(ordenados,1):
            print(f"{i}.{banda.nombre}, {banda.institucion}, {banda.categoria}, Total: {banda.total}")


class ConcursoBandasApp:
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("Concurso de Bandas - Quetzaltenango")
        self.ventana.geometry("500x300")

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
        tk.Label(ventana, text = "Nombre de la banda").grid(row = 0, column = 0)
        tk.Label(ventana, text = "institucion").grid(row = 1, column = 0)
        tk.Label(ventana, text = "Categoria").grid(row = 2, column = 0)
        nombre_entrada = tk.Entry(ventana)
        inst_entrada = tk.Entry(ventana)
        cat_entry = tk.Entry(ventana)
        nombre_entrada.grid(row = 0, column = 1)
        inst_entrada.grid(row = 1, column = 1)
        cat_entry.grid(row = 2, column = 1)
        def guardar():
            try:
                banda = BandaEscolar(nombre_entrada.get(), inst_entrada.get(), cat_entry.get())
                messagebox.showinfo("Se inscribio correctamente")
                ventana.destroy()
            except Exception as e:
                messagebox.showerror("Error",str(e))
        tk.Button(ventana, text = "Guardar", command = guardar).grid(row = 6, column = 0,columnspan = 2)

    def registrar_evaluacion(self):
        ventana = tk.Toplevel(self.ventana)
        tk.Toplevel(self.ventana).title("Registrar Evaluación")
        tk.Label(ventana, text = "Nombre de la banda").grid(row = 0, column = 0)
        nombre_entrada = tk.Entry(ventana)
        nombre_entrada.grid(row = 0, column = 1)
        entradas = {}
        for i, crit in enumerate(Criterios, start=1):
            tk.Label(ventana, text = crit.capitalize().grid(row = i, column = 0))
            ent = tk.Entry(ventana)
            ent.grid(row = i, column = 1)
            entradas[crit] = ent
        def guardar():
            try:
                puntajes = {c:int(e.get())for c,e in entradas.items()}
                self.concurso.registrar_evaluacion(nombre_entrada.get(), puntajes)
                messagebox.showinfo("Se registrado correctamente")
                ventana.destroy()
            except Exception as e:
                messagebox.showerror("Error",str(e))
        tk.Button(ventana, text = "Guardar", command = guardar).grid(row = 6, column = 0,columnspan = 2)

    def listar_bandas(self):
        ventana = tk.Toplevel(self.ventana)
        tk.Toplevel(self.ventana).title("Listado de Bandas")
        text = tk.Text(ventana, width = 60, height = 15)
        text.pack()
        for info in self.concurso.listar_bandas():
            text.insert(tk.END, info + "\n")

    def ver_ranking(self):
        ventana = tk.Toplevel(self.ventana)
        tk.Toplevel(self.ventana).title("Ranking Final")
        text = tk.Text(ventana , width = 60, height = 15)
        text.pack()
        for i, band in enumerate(self.concurso.ranking(),1):
            text.insert(tk.END, f"{i}.{band.nombre}, {band.institucion}, {band.categoria}, TOTAL: {band.total}")


if __name__ == "__main__":
    ConcursoBandasApp()

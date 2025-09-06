import tkinter as tk

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
        self.nombre

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
        tk.Toplevel(self.ventana).title("Inscribir Banda")

    def registrar_evaluacion(self):
        print("Se abrió la ventana: Registrar Evaluación")
        tk.Toplevel(self.ventana).title("Registrar Evaluación")

    def listar_bandas(self):
        print("Se abrió la ventana: Listado de Bandas")
        tk.Toplevel(self.ventana).title("Listado de Bandas")

    def ver_ranking(self):
        print("Se abrió la ventana: Ranking Final")
        tk.Toplevel(self.ventana).title("Ranking Final")


if __name__ == "__main__":
    ConcursoBandasApp()

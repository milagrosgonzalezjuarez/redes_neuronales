"""EJERCICIO 2: SISTEMA EXPERTO MÉDICO (EJERCICIO CON PYCHARM-MEJORADO)"""

import collections
import collections.abc
import inspect

# Compatibilidad con dependencias antiguas de experta.
for nombre in ("Mapping", "Callable", "Iterable", "Iterator", "Hashable", "Sequence"):
    if not hasattr(collections, nombre):
        setattr(collections, nombre, getattr(collections.abc, nombre))
if not hasattr(inspect, "getargspec"):
    ArgSpec = collections.namedtuple("ArgSpec", "args varargs keywords defaults")
    def getargspec_compatible(func):
        datos = inspect.getfullargspec(func)
        return ArgSpec(datos.args, datos.varargs, datos.varkw, datos.defaults)
    inspect.getargspec = getargspec_compatible

from experta import KnowledgeEngine, Fact, Rule

SINTOMAS = {
    "1": ("fiebre", "Fiebre"),
    "2": ("tos", "Tos"),
    "3": ("dificultad_respiratoria", "Dificultad para respirar"),
    "4": ("dolor_muscular", "Dolor muscular"),
    "5": ("cansancio", "Cansancio"),
    "6": ("dolor_de_cabeza", "Dolor de cabeza"),
    "7": ("nauseas", "Náuseas"),
    "8": ("congestion_nasal", "Congestión nasal"),
}

class DiagnosticoMedico(KnowledgeEngine):
    def __init__(self):
        super().__init__()
        self.coincidencias = []

    @Rule(Fact(sintoma="fiebre"), Fact(sintoma="tos"), Fact(sintoma="dificultad_respiratoria"))
    def cuadro_respiratorio(self):
        self.coincidencias.append(
            "Cuadro respiratorio: se identificó fiebre, tos y "
            "dificultad respiratoria. Requiere evaluación médica."
        )

    @Rule(Fact(sintoma="fiebre"), Fact(sintoma="dolor_muscular"), Fact(sintoma="cansancio"))
    def cuadro_gripal(self):
        self.coincidencias.append(
            "Cuadro tipo gripal: se identificó fiebre, dolor muscular "
            "y cansancio. Estos síntomas pueden presentarse en "
            "infecciones virales como la influenza."
        )

    @Rule(Fact(sintoma="dolor_de_cabeza"), Fact(sintoma="fiebre"), Fact(sintoma="nauseas"))
    def cuadro_febril(self):
        self.coincidencias.append(
            "Cuadro febril: se identificó dolor de cabeza, fiebre "
            "y náuseas. Estos síntomas pueden tener distintas causas "
            "y requieren valoración médica."
        )

    @Rule(Fact(sintoma="congestion_nasal"), Fact(sintoma="tos"))
    def sintomas_vias_superiores(self):
        self.coincidencias.append(
            "Síntomas respiratorios: se identificó congestión nasal "
            "y tos. Pueden estar relacionados con un resfriado "
            "u otras afecciones respiratorias."
        )

    @Rule(Fact(sintoma="cansancio"), Fact(sintoma="dolor_de_cabeza"))
    def sintomas_generales(self):
        self.coincidencias.append(
            "Malestar general: se identificó cansancio y dolor "
            "de cabeza. Estos síntomas pueden relacionarse "
            "con diferentes condiciones."
        )

    @Rule(Fact(sintoma="fiebre"))
    def aviso_fiebre(self):
        self.coincidencias.append(
            "Presencia de fiebre: se registró fiebre entre los "
            "síntomas seleccionados. Es importante controlar "
            "su evolución y consultar cuando corresponda."
        )


def elegir_sintomas():
    print("\n=== SISTEMA EXPERTO MÉDICO (EJERCICIO EDUCATIVO) ===")
    print("Elegí los números de los síntomas separados por comas:")

    for numero, (_, etiqueta) in SINTOMAS.items():
        print(f"  {numero}. {etiqueta}")

    while True:
        entrada = input("\nSíntomas (ejemplo: 1,2,3): ").strip()
        numeros = [parte.strip() for parte in entrada.split(",")]

        if numeros and all(n in SINTOMAS for n in numeros):
            return {SINTOMAS[n][0] for n in numeros}

        print("Entrada inválida. Usá números del 1 al 8 separados por comas.")


def main():
    while True:
        sintomas = elegir_sintomas()

        motor = DiagnosticoMedico()
        motor.reset()

        for sintoma in sorted(sintomas):
            motor.declare(Fact(sintoma=sintoma))

        motor.run()

        print("\n--- RESULTADOS DEL ANÁLISIS ---")

        if motor.coincidencias:
            for i, coincidencia in enumerate(sorted(motor.coincidencias), 1):
                print(f"\n{i}. {coincidencia}")
        else:
            print("No se encontraron coincidencias con los síntomas seleccionados.")

        if "dificultad_respiratoria" in sintomas:
            print(
                "\nIMPORTANTE: la dificultad para respirar "
                "requiere atención médica urgente."
            )

        if input("\n¿Probar otra combinación? (s/n): ").strip().lower() != "s":
            print("Fin del programa.")
            break


if __name__ == "__main__":
    main()
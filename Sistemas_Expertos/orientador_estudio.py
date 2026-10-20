"""Segundo ejemplo de sistema experto: sugerencias de estudio."""
import collections
import collections.abc
import inspect
for nombre in ('Mapping', 'Callable', 'Iterable', 'Iterator', 'Hashable', 'Sequence'):
    if not hasattr(collections, nombre):
        setattr(collections, nombre, getattr(collections.abc, nombre))
if not hasattr(inspect, 'getargspec'):
    ArgSpec = collections.namedtuple('ArgSpec', 'args varargs keywords defaults')
    def getargspec_compatible(func):
        s = inspect.getfullargspec(func)
        return ArgSpec(s.args, s.varargs, s.varkw, s.defaults)
    inspect.getargspec = getargspec_compatible
import tkinter as tk
from tkinter import ttk
from experta import Fact, KnowledgeEngine, Rule

class PerfilEstudio(Fact):
    pass

class OrientadorEstudio(KnowledgeEngine):
    def __init__(self):
        super().__init__()
        self.consejo = 'Sin recomendacion'

    @Rule(PerfilEstudio(tiempo='corto', internet='si'))
    def r1(self): self.consejo = 'Microlecciones online y ejercicios de 15 minutos.'

    @Rule(PerfilEstudio(tiempo='corto', internet='no'))
    def r2(self): self.consejo = 'Fichas impresas y repasos breves sin conexion.'

    @Rule(PerfilEstudio(tiempo='largo', internet='si'))
    def r3(self): self.consejo = 'Curso online con proyectos y practica guiada.'

    @Rule(PerfilEstudio(tiempo='largo', internet='no'))
    def r4(self): self.consejo = 'Lectura de apuntes y resolucion de ejercicios extensos.'

def ejecutar():
    motor = OrientadorEstudio()
    motor.reset()
    motor.declare(PerfilEstudio(tiempo=tiempo.get(), internet=internet.get()))
    motor.run()
    salida.set(motor.consejo)

app = tk.Tk()
app.title('Orientador de estudio | Sistema experto')
app.geometry('440x320')
app.configure(bg='#F6F5F1')
tiempo = tk.StringVar(value='corto')
internet = tk.StringVar(value='si')
salida = tk.StringVar(value='Selecciona las opciones y consulta.')
ttk.Label(app, text='Orientador de estudio', font=('Arial', 17, 'bold')).pack(pady=14)
ttk.Label(app, text='Tiempo disponible').pack(anchor='w', padx=25)
for texto, valor in [('Menos de 30 minutos', 'corto'), ('30 minutos o mas', 'largo')]:
    ttk.Radiobutton(app, text=texto, variable=tiempo, value=valor).pack(anchor='w', padx=25)
ttk.Label(app, text='¿Tenes acceso a internet?').pack(anchor='w', padx=25, pady=(12, 0))
for texto, valor in [('Si', 'si'), ('No', 'no')]:
    ttk.Radiobutton(app, text=texto, variable=internet, value=valor).pack(anchor='w', padx=25)
ttk.Button(app, text='Obtener consejo', command=ejecutar).pack(pady=13)
ttk.Label(app, textvariable=salida, wraplength=380, font=('Arial', 10, 'bold')).pack(padx=20)
app.mainloop()

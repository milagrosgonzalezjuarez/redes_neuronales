"""Trabajo practico: sistema experto de recomendacion de mascotas (18 reglas)."""
import collections
import collections.abc
import inspect

# Compatibilidad para dependencias antiguas de experta.
for nombre in ('Mapping', 'MutableMapping', 'Callable', 'Iterable', 'Iterator', 'Hashable', 'Sequence'):
    if not hasattr(collections, nombre):
        setattr(collections, nombre, getattr(collections.abc, nombre))
if not hasattr(inspect, 'getargspec'):
    ArgSpec = collections.namedtuple('ArgSpec', 'args varargs keywords defaults')
    def getargspec_compatible(func):
        spec = inspect.getfullargspec(func)
        return ArgSpec(spec.args, spec.varargs, spec.varkw, spec.defaults)
    inspect.getargspec = getargspec_compatible

import tkinter as tk
from tkinter import ttk
from experta import Fact, KnowledgeEngine, Rule


class Preferencias(Fact):
    """Hecho que contiene actividad, espacio y experiencia."""
    pass


class RecomendadorMascotas(KnowledgeEngine):
    def __init__(self):
        super().__init__()
        self.recomendacion = 'No se encontro una recomendacion.'
        self.motivo = 'Revisa tus preferencias.'

    def elegir(self, mascota, motivo):
        self.recomendacion = mascota
        self.motivo = motivo

    # ACTIVIDAD ALTA: 6 combinaciones
    @Rule(Preferencias(actividad='alta', espacio='grande', experiencia='alta'))
    def regla_01(self):
        self.elegir('Perro mestizo deportivo adulto', 'Puede acompañar rutinas activas; conviene evaluar su temperamento individual.')

    @Rule(Preferencias(actividad='alta', espacio='grande', experiencia='media'))
    def regla_02(self):
        self.elegir('Perro mediano jugueton', 'Disfruta de paseos y juegos; necesita educacion positiva y tiempo diario.')

    @Rule(Preferencias(actividad='alta', espacio='grande', experiencia='baja'))
    def regla_03(self):
        self.elegir('Perro adulto sociable de refugio', 'Un refugio puede orientar sobre un animal activo y apto para principiantes.')

    @Rule(Preferencias(actividad='alta', espacio='pequeño', experiencia='alta'))
    def regla_04(self):
        self.elegir('Perro pequeño atletico', 'El tamaño del hogar no reemplaza los paseos ni la estimulacion diaria.')

    @Rule(Preferencias(actividad='alta', espacio='pequeño', experiencia='media'))
    def regla_05(self):
        self.elegir('Perro adulto pequeño y energico', 'Puede adaptarse a un departamento con ejercicio y enriquecimiento.')

    @Rule(Preferencias(actividad='alta', espacio='pequeño', experiencia='baja'))
    def regla_06(self):
        self.elegir('Gato joven sociable', 'Puede disfrutar del juego activo dentro de casa; requiere rascadores y lugares altos.')

    # ACTIVIDAD MEDIA: 6 combinaciones
    @Rule(Preferencias(actividad='media', espacio='grande', experiencia='alta'))
    def regla_07(self):
        self.elegir('Perro adulto de energia moderada', 'Permite combinar paseos regulares con momentos de descanso.')

    @Rule(Preferencias(actividad='media', espacio='grande', experiencia='media'))
    def regla_08(self):
        self.elegir('Perro mestizo mediano equilibrado', 'Puede disfrutar del jardin y de caminatas cotidianas supervisadas.')

    @Rule(Preferencias(actividad='media', espacio='grande', experiencia='baja'))
    def regla_09(self):
        self.elegir('Gato adulto acostumbrado a personas', 'Su personalidad conocida puede facilitar la adaptacion de un primer tutor.')

    @Rule(Preferencias(actividad='media', espacio='pequeño', experiencia='alta'))
    def regla_10(self):
        self.elegir('Gato adulto curioso', 'Se beneficia de juegos interactivos y un ambiente interior enriquecido.')

    @Rule(Preferencias(actividad='media', espacio='pequeño', experiencia='media'))
    def regla_11(self):
        self.elegir('Perro adulto pequeño de energia media', 'Requiere paseos, vinculo social y una rutina consistente.')

    @Rule(Preferencias(actividad='media', espacio='pequeño', experiencia='baja'))
    def regla_12(self):
        self.elegir('Gato adulto tranquilo y jugueton', 'Puede ser una opcion para comenzar, con atencion veterinaria y juego diario.')

    # ACTIVIDAD BAJA: 6 combinaciones
    @Rule(Preferencias(actividad='baja', espacio='grande', experiencia='alta'))
    def regla_13(self):
        self.elegir('Perro senior de temperamento sereno', 'Puede preferir paseos suaves; sus cuidados de salud deben evaluarse.')

    @Rule(Preferencias(actividad='baja', espacio='grande', experiencia='media'))
    def regla_14(self):
        self.elegir('Gato adulto calmado', 'Un hogar espacioso puede ofrecerle zonas de descanso y exploracion.')

    @Rule(Preferencias(actividad='baja', espacio='grande', experiencia='baja'))
    def regla_15(self):
        self.elegir('Gato senior sociable', 'Conviene conocer sus necesidades de salud y dedicarle atencion diaria.')

    @Rule(Preferencias(actividad='baja', espacio='pequeño', experiencia='alta'))
    def regla_16(self):
        self.elegir('Gato senior de interior', 'Un ambiente tranquilo puede ser apropiado con enriquecimiento y controles.')

    @Rule(Preferencias(actividad='baja', espacio='pequeño', experiencia='media'))
    def regla_17(self):
        self.elegir('Gato adulto de caracter relajado', 'Necesita juego, rascadores y cuidados aunque tenga baja energia.')

    @Rule(Preferencias(actividad='baja', espacio='pequeño', experiencia='baja'))
    def regla_18(self):
        self.elegir('Gato adulto tranquilo de refugio', 'El personal puede ayudarte a elegir un caracter compatible con tu rutina.')


def recomendar():
    motor = RecomendadorMascotas()
    motor.reset()
    motor.declare(Preferencias(actividad=actividad_var.get(),
                              espacio=espacio_var.get(),
                              experiencia=experiencia_var.get()))
    motor.run()
    titulo_resultado.config(text=motor.recomendacion)
    detalle_resultado.config(text=motor.motivo)


def limpiar():
    actividad_var.set('media')
    espacio_var.set('pequeño')
    experiencia_var.set('baja')
    titulo_resultado.config(text='Tu recomendacion aparecera aqui')
    detalle_resultado.config(text='Elegi tus preferencias y presiona Recomendar.')


ventana = tk.Tk()
ventana.title('Huella Ideal | Sistema experto')
ventana.geometry('680x720')
ventana.minsize(580, 660)
ventana.configure(bg='#F6F5F1')

estilo = ttk.Style(ventana)
estilo.theme_use('clam')
estilo.configure('Panel.TLabelframe', background='#FFFFFF', bordercolor='#D7E3DD', relief='solid')
estilo.configure('Panel.TLabelframe.Label', background='#F6F5F1', foreground='#24544B', font=('Arial', 11, 'bold'))
estilo.configure('Opcion.TRadiobutton', background='#FFFFFF', foreground='#263C37', font=('Arial', 10), padding=5)
estilo.configure('Accion.TButton', font=('Arial', 11, 'bold'), padding=11, background='#246C5B', foreground='white')
estilo.map('Accion.TButton', background=[('active', '#174E42')])
estilo.configure('Secundario.TButton', font=('Arial', 10), padding=10)

actividad_var = tk.StringVar(value='media')
espacio_var = tk.StringVar(value='pequeño')
experiencia_var = tk.StringVar(value='baja')

contenedor = tk.Frame(ventana, bg='#F6F5F1', padx=26, pady=20)
contenedor.pack(fill='both', expand=True)
tk.Label(contenedor, text='HUELLA IDEAL', bg='#F6F5F1', fg='#246C5B', font=('Arial', 12, 'bold')).pack(anchor='w')
tk.Label(contenedor, text='Encontra una mascota compatible', bg='#F6F5F1', fg='#20332E', font=('Arial', 19, 'bold')).pack(anchor='w', pady=(4, 5))
tk.Label(contenedor, text='Responde tres preguntas y conoce una sugerencia orientativa.', bg='#F6F5F1', fg='#53655E', font=('Arial', 10)).pack(anchor='w', pady=(0, 13))

def grupo(titulo, variable, opciones):
    panel = ttk.LabelFrame(contenedor, text=titulo, style='Panel.TLabelframe', padding=9)
    panel.pack(fill='x', pady=6)
    for etiqueta, valor in opciones:
        ttk.Radiobutton(panel, text=etiqueta, variable=variable, value=valor, style='Opcion.TRadiobutton').pack(anchor='w')

grupo('01  Actividad que podes ofrecer', actividad_var, [('Alta - paseos largos y juegos', 'alta'), ('Media - paseos y juego moderado', 'media'), ('Baja - rutina tranquila', 'baja')])
grupo('02  Espacio disponible', espacio_var, [('Grande - casa amplia o patio', 'grande'), ('Pequeño - departamento o casa compacta', 'pequeño')])
grupo('03  Experiencia previa', experiencia_var, [('Alta - mucha experiencia', 'alta'), ('Media - alguna experiencia', 'media'), ('Baja - primera mascota', 'baja')])

botones = tk.Frame(contenedor, bg='#F6F5F1')
botones.pack(fill='x', pady=(14, 9))
ttk.Button(botones, text='Ver recomendacion', command=recomendar, style='Accion.TButton').pack(side='left', padx=(0, 10))
ttk.Button(botones, text='Reiniciar', command=limpiar, style='Secundario.TButton').pack(side='left')

resultado_panel = tk.Frame(contenedor, bg='#E4F1EB', padx=16, pady=12)
resultado_panel.pack(fill='x', pady=(5, 8))
tk.Label(resultado_panel, text='RESULTADO', bg='#E4F1EB', fg='#246C5B', font=('Arial', 9, 'bold')).pack(anchor='w')
titulo_resultado = tk.Label(resultado_panel, text='Tu recomendacion aparecera aqui', bg='#E4F1EB', fg='#1E3D33', font=('Arial', 13, 'bold'), wraplength=560, justify='left')
titulo_resultado.pack(anchor='w', pady=(5, 4))
detalle_resultado = tk.Label(resultado_panel, text='Elegi tus preferencias y presiona Recomendar.', bg='#E4F1EB', fg='#37584D', font=('Arial', 10), wraplength=560, justify='left')
detalle_resultado.pack(anchor='w')
tk.Label(contenedor, text='Orientacion educativa: cada animal necesita tiempo, recursos y cuidados veterinarios.', bg='#F6F5F1', fg='#61716A', font=('Arial', 9), wraplength=600).pack(anchor='w', pady=(5, 0))
ventana.mainloop()

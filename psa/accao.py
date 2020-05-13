# uncompyle6 version 3.6.6
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\sp1\Documents\proj19\ia1\proj\src\lib_psa\psa\accao.py
# Compiled at: 2016-01-28 09:49:00
# Size of source mod 2**32: 1974 bytes
"""
Acções do actuador
@author: Luís Morgado
"""

class Accao:
    """Acção geral para execução através do actuador"""
    __module__ = __name__
    __qualname__ = 'Accao'

    def __init__(self, ang=0, vel=1, ang_abs=True):
        """Iniciar acção
        @param ang: ângulo
        @param vel: velocidade linear
        @param pegar: pegar alvo (sim/não)
        @param ang_abs: ângulo absoluto (sim/não)"""
        self.ang = ang
        self.vel = vel
        self.ang_abs = ang_abs


class Avancar(Accao):
    """Acção avançar"""
    __module__ = __name__
    __qualname__ = 'Avancar'

    def __init__(self, ang=0, vel=1, pegar=True, ang_abs=True):
        """Iniciar acção
        @param ang: ângulo
        @param vel: velocidade linear
        @param pegar: pegar alvo (sim/não)
        @param ang_abs: ângulo absoluto (sim/não)"""
        Accao.__init__(self, ang, vel, ang_abs)
        self.pegar = pegar
        self.mag = 1

    def vector(self):
        return (
         self.mag, self.ang)

    def __repr__(self):
        return 'Avancar' + str((self.vel, self.ang))


class Rodar(Accao):
    """Acção rodar"""
    __module__ = __name__
    __qualname__ = 'Rodar'

    def __init__(self, ang=0):
        """Iniciar acção
        @param ang: ângulo"""
        Accao.__init__(self, ang)


class Pegar(Accao):
    """Acção pegar alvo"""
    __module__ = __name__
    __qualname__ = 'Pegar'

    def __init__(self, ang=0):
        """Iniciar acção
        @param ang: ângulo"""
        Accao.__init__(self, ang, ang_abs=False)


class Largar(Accao):
    """Acção largar alvo"""
    __module__ = __name__
    __qualname__ = 'Largar'

    def __init__(self, ang=0):
        """Iniciar acção
        @param ang: ângulo"""
        Accao.__init__(self, ang, ang_abs=False)


class Mover(Accao):
    """Acção mover numa direcção (relativa por omissão)
    com velocidade fixa de 1 passo/ciclo e pegar automático"""
    __module__ = __name__
    __qualname__ = 'Mover'

    def __init__(self, ang=0, ang_abs=False):
        """Iniciar acção
        @param ang: ângulo"""
        Accao.__init__(self, ang, 1, ang_abs)
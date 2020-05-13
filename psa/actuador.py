# uncompyle6 version 3.6.6
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\sp1\Documents\proj19\ia1\proj\src\lib_psa\psa\actuador.py
# Compiled at: 2019-01-04 20:18:24
# Size of source mod 2**32: 5372 bytes
"""
Actuador
@author: Lu�s Morgado
"""
import math
from math import pi
from .util import dirdisc, intdir
from .accao import Avancar, Rodar, Pegar, Largar, Mover
from .ambiente import DPASSO
ESQ = pi / 4
DIR = -pi / 4
FRT = 0
FRENTE = 0
RPASSO = math.pi / 4
AVANCAR = 'avancar()'
PEGAR = 'pegar()'
LARGAR = 'largar()'
RODAR = lambda ang: 'rodar(%f)' % ang
ORIENTAR = lambda ang: 'orientar(%f)' % ang
MOVER = lambda ang: 'mover(%f)' % ang
MOVER_AV = lambda ang: 'mover(%f, False)' % ang

class Actuador:
    """Actuador para acção no ambiente"""
    __module__ = __name__
    __qualname__ = 'Actuador'

    def __init__(self, amb):
        """Iniciar actuador
        @param amb: ambiente"""
        self.amb = amb
        self.accao = None

    def avancar(self, dpasso=1, cont=False):
        """Avançar agente um passo de translação"""
        self.amb.avancar(True, dpasso, cont)

    def rodar(self, ang):
        """Rodar agente num ângulo de rotação relativo
        @param ang: ângulo relativo no intervalo [-pi/4, pi/4]"""
        return self.amb.rodar(ang)

    def orientar(self, ang):
        """Orientar agente numa direcção absoluta
        @param ang: direcção absoluta [radianos]"""
        self.amb.orientar(ang)

    def pegar(self, dpasso=1, cont=False):
        """Avançar e pegar alvo"""
        self.amb.pegar(dpasso, cont)

    def largar(self):
        """Largar carga"""
        self.amb.largar()

    def mover(self, ang, pegar=True):
        """Mover numa direcção absoluta, pegando alvo se existir"""
        self.orientar(ang)
        if pegar:
            self.pegar()
        else:
            self.avancar()

    def actuar(self, accao, avmod=False, ang_abs=False, pegar=True):
        """Executar acção geral
        @param accao: acção a executar
        @param avmod: avanço proporcional ao módulo do vector de acção
        @param ang_abs: ângulo absoluto (sim/não)
        @param pegar: pegar alvo automaticamente (sim/não)"""
        self.accao = accao
        if isinstance(accao, Avancar):
            accao_temp = accao
            ang_abs = accao.ang_abs
            mag = accao_temp.vel
            ang = accao_temp.ang if avmod else dirdisc(accao_temp.ang)
            accao = (mag, ang)
            pegar = accao_temp.pegar
        else:
            if isinstance(accao, Rodar):
                self.rodar(accao.ang)
                return
            if isinstance(accao, Pegar):
                self.pegar(0, avmod)
                return
        if isinstance(accao, Pegar):
            self.pegar(0, avmod)
            return
        elif isinstance(accao, Mover):
            if accao.ang_abs:
                self.orientar(accao.ang)
            else:
                self.amb.rodar(accao.ang)
            self.pegar((accao.vel), cont=avmod)
            return
        elif isinstance(accao, tuple):
            if len(accao) == 2:
                mod, ang = accao
                if ang_abs:
                    self.orientar(ang)
                else:
                    self.amb.rodar(ang)
                if mod > 0:
                    if pegar:
                        self.pegar(mod, cont=avmod)
                    else:
                        self.avancar(mod, cont=avmod)
            else:
                inten, rot, tipoac = accao
                self.rodar(rot)
                if tipoac != RODAR:
                    exec('self.' + tipoac)
        else:
            exec('self.' + accao)

    def dirmov(self):
        """Direcções possíveis de movimento [radianos]"""
        return [ang for ang in self.amb.gerardir()]

    def numac(self):
        """Número de acções executadas"""
        return self.amb.numac()

    def dist(self):
        """distância percorrida"""
        return self.amb.distag()


class ActuadorCont(Actuador):
    """Actuador contínuo"""
    __module__ = __name__
    __qualname__ = 'ActuadorCont'

    def rodar(self, ang):
        """Rodar agente num ângulo de rotação relativo
        @param ang: ângulo relativo [radianos]"""
        return self.amb.rodar(ang)
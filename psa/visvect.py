# uncompyle6 version 3.6.6
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\sp1\Documents\proj19\ia1\proj\src\lib_psa\psa\visvect.py
# Compiled at: 2019-01-04 20:26:04
# Size of source mod 2**32: 2312 bytes
"""
Visualizador de vectores de campo
@author: Luís Morgado
"""
import pygame
from math import pi
from .util import linhasvect
from .accao import Accao
COR_DIRAG = (0, 204, 51)
RVCAMPO = (875, 510, 90, 90)
PVCAMPO = (919, 554)
DVCAMPO = 45
LVCAMPO = 2

class VisVectCampo:
    """Visualizador de vectores de campo"""
    __module__ = __name__
    __qualname__ = 'VisVectCampo'

    def __init__(self, mod, svis, imgvcampo):
        """Iniciar visualizador"""
        self.mod = mod
        self.svis = svis
        self.imgvcampo = imgvcampo

    def limpar(self):
        """Limpar visualizador"""
        self.svis.blit(self.imgvcampo, RVCAMPO)

    def vector(self, vpol, cor, linha=LVCAMPO, dir_ref=True):
        """Visualizar vector relativo"""
        mod, ang = vpol
        if dir_ref:
            dirag = self.mod.ambiente.dirag()
        else:
            dirag = 0
        self.vectorabs((mod, dirag + ang), cor, linha=LVCAMPO)

    def vectorabs(self, vpol, cor, linha=LVCAMPO):
        """Visualizar vector absoluto"""
        mod, ang = vpol
        x, y = PVCAMPO
        dim = mod * DVCAMPO
        if dim > DVCAMPO:
            dim = DVCAMPO
        if dim < 0:
            dim = 0
        dim -= 1
        linhas = linhasvect((x, y), dim, ang, 0.17 * pi, 0.3)
        for posini, posfin in linhas:
            pygame.draw.line(self.svis, cor, posini, posfin, linha)

    def accoesestado(self, s, accoes, q, vnorm=100):
        """Visualizar acções de estado
        @param s: estado
        @param accoes: acções
        @param q: Q(s,a)
        @param param: valor de normalização"""
        for a in accoes:
            aval = 255 * q.get((s, a), 0.0) / vnorm
            if aval > 0:
                cor = (
                 0, min(aval, 255), 0)
            elif aval < 0:
                cor = (
                 min(-aval, 255), 0, 0)
            else:
                continue
            if isinstance(a, Accao):
                a = a.ang
            self.vectorabs((1, a), cor)
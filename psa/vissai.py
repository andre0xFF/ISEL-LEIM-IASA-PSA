# uncompyle6 version 3.6.6
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\sp1\Documents\proj19\ia1\proj\src\lib_psa\psa\vissai.py
# Compiled at: 2019-01-04 20:31:31
# Size of source mod 2**32: 2343 bytes
"""
Plataforma de Simulação de Agentes
@author: Luís Morgado
"""
import pygame
from .visualizsai import VisualizadorSAI

class SimulVisSAI:

    def __init__(self, fps, mod, cfa):
        pygame.init()
        self.visamb = VisualizadorSAI()
        self.visper = VisualizadorSAI()
        self.vismod = VisualizadorSAI()
        self.visvec = VisualizadorSAI()

    def terminarvis(self):
        pass

    def actvis(self):
        pass

    def obterelemgraf(self):
        pass

    def actinfo(self):
        pass

    def iniciarvis(self):
        pass

    def altcfa(self, cfa):
        pass

    def estado(self, pausa):
        pass

    def infosimul(self, texto, rect, ajustepos=False, corfundo=0, fonte=None, cor=0):
        pass

    def info(self, texto):
        pass

    def cursor(self, pos):
        pass

    def posdirag(self):
        pass

    def actuador(self):
        pass

    def sonar(self, rot, dist, dmax):
        pass

    def passo(self):
        pass

    def tempoexec(self):
        pass

    def temposimul(self):
        pass

    def ambiente(self):
        pass

    def agente(self):
        pass

    def infosens(self, vis_pot=False):
        pass

    def posvirt(self, pos, rect):
        """ Converter posição em pixeis em posição virtual"""
        xp, yp = pos
        xi, yi, larg, alt = rect
        escala = larg / float(self.mod.ambiente.dimx)
        x = int((xp - xi) / escala)
        y = int((yp - yi) / escala)
        return (
         x, y)

    def comutarfs(self, fs):
        pass
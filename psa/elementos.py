# uncompyle6 version 3.6.6
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\sp1\Documents\proj19\ia1\proj\src\lib_psa\psa\elementos.py
# Compiled at: 2013-12-20 16:32:00
# Size of source mod 2**32: 2707 bytes
"""
Definição de elementos do ambiente
@author: Luís Morgado
"""
from random import random
AGENTE = 'agente'
ALVO = 'alvo'
OBST = 'obst'
BASE = 'base'
VAZIO = 'vazio'

class Elemento(object):

    def __init__(self, pos, tipo, din=0):
        self.pos = pos
        self.posant = pos
        self.tipo = tipo
        self.din = din
        self.tvida = float('+inf')
        self.alterado = True

    def evoluir(self, dt=1):
        pass

    def mover(self, pos):
        self.posant = self.pos
        self.pos = pos


class Agente(Elemento):

    def __init__(self, pos, vtrans, vrot):
        super(Agente, self).__init__(pos, 'agente')
        self.dir = 0
        self.col = False
        self._carga = False
        self._ncarga = 0
        self.vtrans = vtrans
        self.vrot = vrot
        self.varang = None

    def ncarga(self):
        return self._ncarga

    def carga(self):
        return self._carga

    def pegar(self):
        self._ncarga += 1
        self._carga = True

    def largar(self):
        self._ncarga -= 1
        if self._ncarga < 0:
            self._ncarga = 0


class Alvo(Elemento):

    def __init__(self, pos, din=0):
        super(Alvo, self).__init__(pos, 'alvo', din)
        if din > 0:
            dinbase = 50.0 / din
            tgestbase = 10.0 / din
            self.tmgest = 1 + int(random() * tgestbase)
            self.tmvida = 2 + int(dinbase + random() * dinbase)
            self.tgest = self.tmgest
            self.tvida = 1 + int(random() * dinbase)

    def evoluir(self, dt=1):
        if self.din > 0:
            if self.tvida > 0:
                self.tvida -= dt
                if self.tvida < 0:
                    self.tvida = 0
            else:
                self.tgest -= dt
                if self.tgest < 0:
                    self.tgest = self.tmgest
                    self.tvida = self.tmvida


class Base(Elemento):

    def __init__(self, pos, din=0):
        super(Base, self).__init__(pos, 'base', din)
        self.carga = False

    def preencher(self):
        self.carga = True
        self.tipo = 'base_preenchida'


class Obstaculo(Elemento):

    def __init__(self, pos, din=0):
        super(Obstaculo, self).__init__(pos, 'obst', din)


class Vazio(Elemento):

    def __init__(self, pos=None):
        super(Vazio, self).__init__(pos, 'vazio')
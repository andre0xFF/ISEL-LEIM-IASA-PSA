# uncompyle6 version 3.6.6
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\sp1\Documents\proj19\ia1\proj\src\lib_psa\psa\sensorpotencial.py
# Compiled at: 2019-01-04 20:23:44
# Size of source mod 2**32: 5537 bytes
"""
Sensor de colisão
@author: Luís Morgado
"""
import psa
from .sensor import Sensor
from .sensorglobal import SensorGlobal
from .sensorloc import SensorLoc
from .util import movpospol, dist

class SensorPotencial(Sensor):
    """Sensor de potencial"""
    __module__ = __name__
    __qualname__ = 'SensorPotencial'

    def __init__(self, amb, rot=0, gama_alvo=0.9, gama_obst=0.01, vis=False):
        """
        @param rot: Rotação [Radianos]
        @param gama_alvo: Factor de decaimento de intensidade de campo de alvos
        @param gama_obst: Factor de decaimento de intensidade de campo de obst.
        @param vis: Visualização activa (Sim/Não)"""
        super(SensorPotencial, self).__init__(amb)
        self.rot = rot
        self.gama_alvo = gama_alvo
        self.gama_obst = gama_obst
        self.vis = vis
        self.sensor_glob = SensorGlobal(amb)
        self.sensor_loc = SensorLoc(amb)
        self.pos_alvo_prox = []
        self.dist_alvo = float('inf')
        self.pos_obst_prox = []
        self.dist_obst = 1.5

    def def_dist_obst(dist_obst):
        self.dist_obst = dist_obst

    def detectar(self):
        """Detectar potencial
        @return: (potencial de alvo, potencial de obstáculo)"""
        pos, rot = self.sensor_loc.detectar()
        pos_frt = movpospol(pos, (0.01, rot + self.rot))
        if self.rot == 0:
            self.detectar_elem_prox(pos)
        if self.vis:
            if not psa.vmax():
                self.mostrar_pot(pos_frt)
        pot_alvo = self.detectar_pot_prox(pos_frt, 'alvo', self.gama_alvo)
        pot_obst = self.detectar_pot(pos_frt, 'obst', self.gama_obst)
        return (
         pot_alvo, pot_obst)

    def detectar_pot_pos(self):
        """Detectar potencial na posição do agente
        @return: (potencial de alvo, potencial de obstáculo)"""
        pos, _ = self.sensor_loc.detectar()
        pot_alvo = self.detectar_pot_prox(pos, 'alvo', self.gama_alvo)
        pot_obst = self.detectar_pot(pos, 'obst', self.gama_obst)
        return (
         pot_alvo, pot_obst)

    def detectar_pot(self, pos_sens, tipo_elem, gama):
        per_glob = self.sensor_glob.detectar()
        pot_sens = 0
        for pos_elem, elem in per_glob.items():
            if elem == tipo_elem:
                pot_sens += self.potencial(pos_sens, pos_elem, elem, gama)

        return pot_sens

    def detectar_pot_prox(self, pos_sens, tipo_elem, gama):
        per_glob = self.sensor_glob.detectar()
        dist_min = float('inf')
        pos_min = None
        elem_min = None
        for pos_elem, elem in per_glob.items():
            if elem == tipo_elem:
                dist_elem = dist(pos_sens, pos_elem)
                if dist_elem < dist_min:
                    dist_min = dist_elem
                    pos_min = pos_elem
                    elem_min = elem

        if pos_min is not None:
            pot_sens = self.potencial(pos_sens, pos_min, elem_min, gama)
        else:
            pot_sens = 0
        return pot_sens

    def potencial(self, pos_sens, pos_elem, elem, gama):
        dist_elem = dist(pos_sens, pos_elem)
        return gama ** dist_elem

    def detectar_elem_prox(self, pos_sens):
        per_glob = self.sensor_glob.detectar()
        self.dist_alvo = float('inf')
        self.pos_alvo_prox = []
        self.pos_obst_prox = []
        for pos_elem, elem in per_glob.items():
            dist_elem = dist(pos_sens, pos_elem)
            if elem == 'alvo':
                if dist_elem < self.dist_alvo:
                    self.dist_alvo = dist_elem
                    self.pos_alvo_prox = [pos_elem]
            if elem == 'obst' and dist_elem <= self.dist_obst:
                self.pos_obst_prox.append(pos_elem)

    def mostrar_pot(self, pos_frt=None):
        campo_pot = {}
        for x in range(self.amb.dimx):
            for y in range(self.amb.dimy):
                pot_alvo = self.detectar_pot_prox((x, y), 'alvo', self.gama_alvo)
                pot_obst = self.detectar_pot((x, y), 'obst', self.gama_obst)
                campo_pot[(x, y)] = pot_alvo - pot_obst

        psa.visper = psa.vis(0)
        psa.visper.campo(campo_pot)
        if pos_frt:
            psa.visper.marcar([pos_frt], 0, linha=1)
        if self.pos_alvo_prox:
            psa.visper.marcar((self.pos_alvo_prox), linha=1, margem=(-1), cor=(255,
                                                                               255,
                                                                               255))
        if self.pos_obst_prox:
            psa.visper.marcar((self.pos_obst_prox), linha=1, margem=(-1), cor=(200,
                                                                               200,
                                                                               200))
# uncompyle6 version 3.6.6
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\sp1\Documents\proj19\ia1\proj\src\lib_psa\psa\sensormultiplo.py
# Compiled at: 2019-01-04 20:24:30
# Size of source mod 2**32: 6981 bytes
"""
Sensor múltiplo
@author: Luís Morgado
"""
from math import pi
from .util import difpospol, fint, DPI, normang, dist, dirint, dirdisc, dirmov
from .ambiente import posint
from .detestim import *
from .actuador import ESQ, DIR, FRT

class PerDir:

    def __init__(self):
        self.contacto = None
        self.distancia = None
        self.alvo = None
        self.obstaculo = None
        self.pot_alvo = None
        self.pot_obst = None
        self.potencial = None
        self.sonar = None
        self.imagem = None


class Percepcao:

    def __init__(self):
        self.sens = {}
        self.posicao = None
        self.orientacao = None
        self.elementos = None
        self.imagem = None
        self.carga = None
        self.colisao = None
        self.periferia = None
        self.dir_accao = None
        self.dist_mov = None
        self.custo_mov = None
        self.per_dir = {ESQ: PerDir(), 
         FRT: PerDir(), 
         DIR: PerDir()}

    def __getitem__(self, idx):
        return self.per_dir.get(idx)


class SensorMultiplo:
    """Sensor múltiplo"""
    __module__ = __name__
    __qualname__ = 'SensorMultiplo'

    def __init__(self, agente):
        self.agente = agente
        self.per = None
        self.accoes = dirmov()

    def detectar(self):
        """Detectar informação sensorial - Abstracto"""
        per = Percepcao()
        per.sens = {'localiz':self.agente.sensorloc.detectar(), 
         'global':self.agente.sensorglob.detectar(), 
         'carga':self.agente.sensorcarga.detectar(), 
         'ncarga':self.agente.sensorcarga.detectar_ncarga(), 
         'colisao':self.agente.sensorcolis.detectar(), 
         'periferia':self.agente.sensorperif.detectar(), 
         'potesq':self.agente.sensorpotesq.detectar(), 
         'potfrt':self.agente.sensorpotfrt.detectar(), 
         'potdir':self.agente.sensorpotdir.detectar(), 
         'sonaresq':self.agente.sonaresq.detectar(), 
         'imagesq':self.agente.sonaresq.obterimag(), 
         'sonarfrt':self.agente.sonarfrt.detectar(), 
         'imagfrt':self.agente.sonarfrt.obterimag(), 
         'sonardir':self.agente.sonardir.detectar(), 
         'imagdir':self.agente.sonardir.obterimag()}
        per.accao = self.agente.actuador.accao
        per.posicao = posicao(per)
        per.orientacao = dirdisc(orientacao(per))
        per.elementos = elementos(per)
        per.imagem = self.agente.sensorglob.detectarimg()
        per.carga = carga(per)
        per.ncarga = ncarga(per)
        per.colisao = colisao(per)
        per.periferia = periferia(per)
        per.dir_accao = dirint(per.orientacao)
        per.dist_mov = dist(self.per.posicao, per.posicao) if self.per else 0
        per.custo_mov = per.dist_mov if per.dist_mov != 0 else 1
        per.pos_alvo_prox = self.agente.sensorpotfrt.pos_alvo_prox
        per.pos_obst_prox = self.agente.sensorpotfrt.pos_obst_prox
        per.alvo_prox = [difpospol(elem, per.posicao) for elem in per.pos_alvo_prox]
        per.obst_prox = [difpospol(elem, per.posicao) for elem in per.pos_obst_prox]
        per.alvo = self.agente.amb.alvo
        per.pos_abs = posint(per.posicao)
        per.per_dir[ESQ].alvo = alvo_canal(per, 'esq')
        per.per_dir[FRT].alvo = alvo(per)
        per.per_dir[DIR].alvo = alvo_canal(per, 'dir')
        per.per_dir[ESQ].obstaculo = obstaculo_canal(per, 'esq')
        per.per_dir[FRT].obstaculo = obstaculo(per)
        per.per_dir[DIR].obstaculo = obstaculo_canal(per, 'dir')
        per.per_dir[ESQ].contacto = contacto_canal(per, 'esq')
        per.per_dir[FRT].contacto = contacto(per)
        per.per_dir[DIR].contacto = contacto_canal(per, 'dir')
        per.per_dir[ESQ].pot_alvo = pot_alvo(per, 'esq')
        per.per_dir[FRT].pot_alvo = pot_alvo(per, 'frt')
        per.per_dir[DIR].pot_alvo = pot_alvo(per, 'dir')
        per.per_dir[ESQ].pot_obst = pot_obst(per, 'esq')
        per.per_dir[FRT].pot_obst = pot_obst(per, 'frt')
        per.per_dir[DIR].pot_obst = pot_obst(per, 'dir')
        per.per_dir[ESQ].potencial = potencial(per, 'esq')
        per.per_dir[FRT].potencial = potencial(per, 'frt')
        per.per_dir[DIR].potencial = potencial(per, 'dir')
        if self.per:
            pot_alvo_pos, pot_obst_pos = self.agente.sensorpotfrt.detectar_pot_pos()
            per.potencial = pot_alvo_pos - pot_obst_pos
            per.dif_pot = per.potencial - self.per.potencial
        else:
            per.potencial = 0
            per.dif_pot = 0
        per.per_dir[ESQ].sonar = sonar(per, 'esq')
        per.per_dir[FRT].sonar = sonar(per, 'frt')
        per.per_dir[DIR].sonar = sonar(per, 'dir')
        per.per_dir[ESQ].distancia = sonar(per, 'esq')[1]
        per.per_dir[FRT].distancia = sonar(per, 'frt')[1]
        per.per_dir[DIR].distancia = sonar(per, 'dir')[1]
        per.per_dir[ESQ].imagem = per.sens['imagesq']
        per.per_dir[FRT].imagem = per.sens['imagfrt']
        per.per_dir[DIR].imagem = per.sens['imagdir']
        self.per = per
        return per
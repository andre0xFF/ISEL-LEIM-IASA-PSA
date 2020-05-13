# uncompyle6 version 3.6.6
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\sp1\Documents\proj19\ia1\proj\src\lib_psa\psa\detestim.py
# Compiled at: 2019-01-04 20:24:41
# Size of source mod 2**32: 1225 bytes
"""
Detecção de estímulos sensoriais
@author: Luís Morgado
"""
from .actuador import DPASSO

def contacto(per):
    return contacto_canal(per, 'frt')


def contacto_canal(per, canal_sens):
    return per.sens[('sonar' + canal_sens)][1] <= DPASSO


def alvo(per):
    return alvo_canal(per, 'frt')


def alvo_canal(per, canal_sens):
    return per.sens[('sonar' + canal_sens)][0] == 'alvo'


def obstaculo(per):
    return obstaculo_canal(per, 'frt')


def obstaculo_canal(per, canal_sens):
    return per.sens[('sonar' + canal_sens)][0] == 'obst'


def pot_alvo(per, canal_sens):
    return per.sens[('pot' + canal_sens)][0]


def pot_obst(per, canal_sens):
    return per.sens[('pot' + canal_sens)][1]


def potencial(per, canal_sens):
    return pot_alvo(per, canal_sens) - pot_obst(per, canal_sens)


def posicao(per):
    return per.sens['localiz'][0]


def orientacao(per):
    return per.sens['localiz'][1]


def elementos(per):
    return per.sens['global']


def carga(per):
    return per.sens['carga']


def ncarga(per):
    return per.sens['ncarga']


def colisao(per):
    return per.sens['colisao']


def periferia(per):
    return per.sens['periferia']


def sonar(per, canal_sens):
    return per.sens[('sonar' + canal_sens)]
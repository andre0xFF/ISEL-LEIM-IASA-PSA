# uncompyle6 version 3.6.6
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\sp1\Documents\proj19\ia1\proj\src\lib_psa\psa\sensor.py
# Compiled at: 2019-01-04 20:22:58
# Size of source mod 2**32: 826 bytes
"""
Definição geral de sensor
@author: Lu�s Morgado
"""
import psa
from .elementos import AGENTE, ALVO, OBST, BASE, VAZIO
AMARELO = AGENTE
VERDE = ALVO
CINZENTO = OBST
VERDE_BRANCO = BASE
BRANCO = VAZIO

class Sensor(object):
    """Sensor geral para detec��o de informa��o sensorial"""
    __module__ = __name__
    __qualname__ = 'Sensor'

    def __init__(self, amb=None):
        if amb:
            self.amb = amb
        else:
            self.amb = psa.ambiente()

    def detectar(self):
        """Detectar informa��o sensorial - Abstracto"""
        raise NotImplementedError
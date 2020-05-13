# uncompyle6 version 3.6.6
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\sp1\Documents\proj19\ia1\proj\src\lib_psa\psa\sensorloc.py
# Compiled at: 2019-01-04 20:23:08
# Size of source mod 2**32: 600 bytes
"""
Sensor de localização
@author: Luís Morgado
"""
from .sensor import Sensor

class SensorLoc(Sensor):
    """Sensor de localização"""
    __module__ = __name__
    __qualname__ = 'SensorLoc'

    def detectar(self):
        """Detectar posição e direcção absoluta do agente
        @return: (posição, direcção absoluta)"""
        return (
         self.amb.posag(), self.amb.dirag())

    def detectarpos(self):
        """Detectar posição"""
        return self.amb.posag()

    def detectardir(self):
        """Detectar direcção absoluta do agente"""
        return self.amb.dirag()
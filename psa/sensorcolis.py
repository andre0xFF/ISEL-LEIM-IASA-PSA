# uncompyle6 version 3.6.6
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\sp1\Documents\proj19\ia1\proj\src\lib_psa\psa\sensorcolis.py
# Compiled at: 2019-01-04 20:23:56
# Size of source mod 2**32: 293 bytes
"""
Sensor de colisão
@author: Luís Morgado
"""
from .sensor import Sensor

class SensorColisao(Sensor):
    """Sensor de colisão"""
    __module__ = __name__
    __qualname__ = 'SensorColisao'

    def detectar(self):
        """Obter indicação de colisão (sim/não)"""
        return self.amb.colisag()
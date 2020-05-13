# uncompyle6 version 3.6.6
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\sp1\Documents\proj19\ia1\proj\src\lib_psa\psa\sensorcarga.py
# Compiled at: 2019-01-04 20:23:17
# Size of source mod 2**32: 424 bytes
"""
Sensor de carga
@author: Luís Morgado
"""
from .sensor import Sensor

class SensorCarga(Sensor):
    """Sensor de carga"""
    __module__ = __name__
    __qualname__ = 'SensorCarga'

    def detectar(self):
        """Obter informação se o agente tem em carga"""
        return self.amb.cargaagt()

    def detectar_ncarga(self):
        """Obter número de alvos que o agente tem em carga"""
        return self.amb.ncargaagt()
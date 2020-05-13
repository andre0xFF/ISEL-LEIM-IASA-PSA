# uncompyle6 version 3.6.6
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\sp1\Documents\proj19\ia1\proj\src\lib_psa\psa\sensorperif.py
# Compiled at: 2019-01-04 20:24:13
# Size of source mod 2**32: 753 bytes
"""
Sensor de periferia
@author: Luís Morgado
"""
from .util import mover
from .sensor import Sensor
from .elementos import Vazio

class SensorPerif(Sensor):
    """Sensor de detecção global (panorâmica)"""
    __module__ = __name__
    __qualname__ = 'SensorPerif'

    def detectar(self):
        """Detectar objectos na periferia do agente
        @return: dicionário de associações posição:objecto"""
        elementos = []
        pos_ag = self.amb.posag()
        for ang in self.amb.gerardir():
            pos_elem = mover(pos_ag, ang)
            elem = self.amb.obterelempos(pos_elem)
            if elem is None:
                elem = Vazio(pos_elem)
            elementos.append((pos_elem, elem.tipo, ang))

        return elementos
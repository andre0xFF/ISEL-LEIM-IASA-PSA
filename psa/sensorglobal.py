# uncompyle6 version 3.6.6
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\sp1\Documents\proj19\ia1\proj\src\lib_psa\psa\sensorglobal.py
# Compiled at: 2019-01-04 20:23:26
# Size of source mod 2**32: 1101 bytes
"""
Sensor global
@author: Luís Morgado
"""
from .sensor import Sensor

class SensorGlobal(Sensor):
    """Sensor de detecção global (panorâmica)"""
    __module__ = __name__
    __qualname__ = 'SensorGlobal'

    def detectar(self):
        """Detectar objectos do ambiente
        @return: dicionário de associações posição:objecto"""
        return self.amb.obterelem()

    def detectarimg(self):
        """Detectar imagem do ambiente, incluindo posições vazias
        @return: dicionário de associações posição:objecto"""
        return self.amb.obterimagem()

    def detectardif(self):
        """Detectar diferencialmente objectos do ambiente
        @return: dicionário de associações posição:objecto"""
        return self.amb.obterelemdif()

    def detectarpos(self):
        """Detectar posições do ambiente
        @return: conjunto de posições"""
        return self.amb.gerarpos()

    def detectardim(self):
        """Detectar dimensões ambiente
        @return: (dimx, dimy)"""
        return (
         self.amb.dimx, self.amb.dimy)
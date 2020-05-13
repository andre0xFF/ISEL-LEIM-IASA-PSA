# uncompyle6 version 3.6.6
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\sp1\Documents\proj19\ia1\proj\src\lib_psa\psa\sonar.py
# Compiled at: 2019-01-04 20:22:30
# Size of source mod 2**32: 1095 bytes
"""
Sonar
@author: Luís Morgado
"""
from .sensor import Sensor

class Sonar(Sensor):
    """Sonar móvel (permite rotação)"""
    __module__ = __name__
    __qualname__ = 'Sonar'

    def detectar(self, rot):
        """Detectar objectos numa determinada direcção
        @param rot: ângulo relativo de rotação
        @return: (objecto, distância, rotação)"""
        elem, dist, rot = self.amb.obterisens(rot)
        return (
         elem.tipo, dist, rot)

    def obterimag(self):
        """Obter imagem após detectar
        @return: imagem do ambiente { pos:elem }"""
        return self.amb.obterimagsens()


class SonarFixo(Sonar):
    """Sonar fixo numa direcção relativa"""
    __module__ = __name__
    __qualname__ = 'SonarFixo'

    def __init__(self, amb, ang):
        super(SonarFixo, self).__init__(amb)
        self.ang = ang

    def detectar(self):
        return super(SonarFixo, self).detectar(self.ang)
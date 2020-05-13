# uncompyle6 version 3.6.6
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\sp1\Documents\proj19\ia1\proj\src\lib_psa\psa\agente.py
# Compiled at: 2019-01-04 20:22:17
# Size of source mod 2**32: 4089 bytes
"""
Agente
@author: Luís Morgado
"""
import copy
from math import pi
import psa
from .actuador import ESQ, DIR, FRENTE
import psa.sonar as sonar
import psa.sensorloc as sensorloc
import psa.sensorcarga as sensorcarga
import psa.sensorglobal as sensorglobal
import psa.sensorpotencial as sensorpotencial
import psa.sensorcolis as sensorcolis
import psa.sensorperif as sensorperif
import psa.actuador as actuador
import psa.sensormultiplo as sensormultiplo

def criar_sensores(obj, amb):
    """Criar sensores do agente"""
    obj.sensorloc = sensorloc.SensorLoc(amb)
    obj.sonar = sonar.Sonar(amb)
    obj.sonaresq = sonar.SonarFixo(amb, ESQ)
    obj.sonardir = sonar.SonarFixo(amb, DIR)
    obj.sonarfrt = sonar.SonarFixo(amb, FRENTE)
    obj.sensorcarga = sensorcarga.SensorCarga(amb)
    obj.sensorglob = sensorglobal.SensorGlobal(amb)
    obj.sensorcolis = sensorcolis.SensorColisao(amb)
    obj.sensorperif = sensorperif.SensorPerif(amb)
    obj.sensorpotesq = sensorpotencial.SensorPotencial(amb, pi / 4)
    obj.sensorpotfrt = sensorpotencial.SensorPotencial(amb, 0)
    obj.sensorpotdir = sensorpotencial.SensorPotencial(amb, -pi / 4)
    obj.sensores = sensormultiplo.SensorMultiplo(obj)
    obj.sensor_multiplo = obj.sensores


def criar_actuadores(obj, amb):
    """Criar actuadores do agente"""
    obj.actuador = actuador.Actuador(amb)
    obj.actcont = actuador.ActuadorCont(amb)


class Agente(object):
    """Definição geral de agente"""
    __module__ = __name__
    __qualname__ = 'Agente'

    def __init__(self):
        self.actuador = None
        self.sensor_multiplo = None

    def iniciaramb(self, amb):
        """Iniciar associação ao ambiente
        @param amb: ambiente"""
        self.amb = amb
        criar_sensores(self, amb)
        criar_actuadores(self, amb)

    def iniciar(self):
        """Iniciar execução do agente"""
        if hasattr(self, '_controlo'):
            self.iniciar_controlo()

    def reiniciar(self):
        """Reiniciar execução do agente"""
        self.actuador.accao = None

    def iniciar_controlo(self):
        """Iniciar controlo do agente, se existir"""
        if hasattr(self, 'controlo_inicial'):
            self._controlo = copy.deepcopy(self.controlo_inicial)
        else:
            self.controlo_inicial = copy.deepcopy(self._controlo)

    def executar(self):
        """Executar passo de processamento interno"""
        pass


class Percepcao:
    """Processo de percepção"""
    __module__ = __name__
    __qualname__ = 'Percepcao'

    def __init__(self):
        criar_sensores(self, psa.ambiente())

    def percepcionar(self):
        """percepcionar ambiente"""
        return self.sensores.detectar()


class Actuacao:
    """Processo de actuação"""
    __module__ = __name__
    __qualname__ = 'Actuacao'

    def __init__(self):
        """Iniciar associação ao ambiente"""
        amb = psa.ambiente()
        criar_actuadores(self, psa.ambiente())

    def actuar(self, accao):
        """Realizar acção"""
        if accao:
            self.actuador.actuar(accao)
# uncompyle6 version 3.6.6
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\sp1\Documents\proj19\ia1\proj\src\lib_psa\psa\__init__.py
# Compiled at: 2019-01-04 21:18:14
# Size of source mod 2**32: 15266 bytes
"""
Plataforma de Simulação de Agentes
@author: Luís Morgado
"""
import time, sys
from math import pi
from .util import dist
from .vissim import SimulVis
from .vissai import SimulVisSAI
from .ctl import SimulCtl, TERMINAR
from .ambiente import Ambiente
from .elementos import *
__all__ = [
 'iniciar', 'executar', 'reiniciar', 'terminar', 'passo',
 'tempopasso', 'tempoexec', 'temposimul', 'info', 'pausa', 'actvis',
 'espera', 'ambiente', 'dirmov', 'infopee', 'infodelib', 'infoexec', 'VisPEE',
 'repamb', 'custoaccao', 'vis']

class SimulMod:

    def __init__(self, agente, famb, perexec, dinamb, pvm, fpe, detalhe, reiniciar, nepisod):
        self.agente = agente
        self.defamb = open(famb).readlines()
        self.perexec = perexec
        self.dinamb = dinamb
        self.pvm = pvm
        self.fpe = fpe
        self.reiniciar = reiniciar
        if nepisod == 0:
            self.vmax = False
        else:
            self.vmax = True
        self.vtrans = 1.0 / perexec
        self.vrot = pi / 4 / perexec
        self.ambiente = Ambiente(self.defamb, self.dinamb, self.vtrans, self.vrot, self.pvm, detalhe)
        self.iniciaramb()
        self.iniciarag()
        self.iniciartemp()

    def iniciaramb(self):
        self.ambiente.iniciar()
        if self.agente:
            if hasattr(self.agente, 'iniciaramb'):
                self.agente.iniciaramb(self.ambiente)

    def iniciarag(self, agente=None):
        if agente:
            self.agente = agente
            self.agente.iniciaramb(self.ambiente)
        if self.agente:
            self.agente.iniciar()

    def iniciartemp(self):
        self.tini = time.time()
        self.tant = self.tini
        self.tsim = 0.0
        self.texec = 0.0
        self.tpasso = 0.0
        self.passo = 0


class Simulador:

    def __init__(self, agente, defamb, pausa, perexec, dinamb, fps, pvm, cfa, fpe, detalhe, reiniciar, nepisod):
        self.mod = SimulMod(agente, defamb, perexec, dinamb, pvm, fpe, detalhe, reiniciar, nepisod)
        if nepisod == 0:
            self.vis = SimulVis(fps, self.mod, cfa)
        else:
            self.vis = SimulVisSAI(fps, self.mod, cfa)
        self.ctl = SimulCtl(self.mod, self.vis, pausa)
        self.nepisod = nepisod
        self.episod = 0
        self.passos = 0
        self.passos_ep_act = 0
        self.passos_episod = []
        self.ncol = 0
        self.ncol_ep_act = 0
        self.ncol_episod = []

    def executar(self):
        while not self.ctl.estadofinal():
            terminar = self.executar_passo()
            if terminar:
                break

        self.vis.terminarvis()
        print('PSA: Terminar')

    def executar_passo(self):
        terminar = False
        self.passos += 1
        self.passos_ep_act += 1
        self.ctl.processar()
        self.vis.actvis()
        if self.mod.agente.sensor_multiplo.per is not None:
            if self.mod.agente.sensor_multiplo.per.colisao:
                self.ncol += 1
                self.ncol_ep_act += 1
        elif self.mod.reiniciar:
            if self.mod.agente.sensor_multiplo.per.alvo:
                self.ncol_episod.append(self.ncol_ep_act)
                self.ncol_ep_act = 0
                self.episod += 1
                self.passos_episod.append(self.passos_ep_act)
                self.passos_ep_act = 0
                if self.nepisod == 0 or self.episod < self.nepisod:
                    reiniciar()
                else:
                    terminar = True
        return terminar


osim = None
visamb = None
visper = None
vismod = None
visvec = None

def iniciar_osim(agente, defamb, pausa, perexec, dinamb, fps, pvm, cfa, fpe, detalhe, reiniciar, nepisod):
    """Iniciar objecto simulador e visualizadores"""
    global osim
    global visamb
    global vismod
    global visper
    global visvec
    if dinamb <= 1:
        dinamb = dinamb * 100.0
    osim = Simulador(agente, defamb, pausa, perexec, dinamb, fps, pvm, cfa, fpe, detalhe, reiniciar, nepisod)
    visamb = osim.vis.visamb
    visper = osim.vis.visper
    vismod = osim.vis.vismod
    visvec = osim.vis.visvec


def iniciar(defamb, pausa=False, perexec=0.05, dinamb=0, fps=50, pvm=0, cfa=(0, 0, 0), fpe=10, detalhe=1, reiniciar=False, nepisod=0):
    """Iniciar PSA    
        @param defamb: ficheiro de definição do ambiente        
        @param pausa: pausa activa (sim/não)        
        @param perexec: período de execução [s]        
        @param dinamb: dinamismo do ambiente [%] (0 - ambiente estático)        
        @param fps: ritmo de actualização da visualização [fps]
        @param pvm: probabilidade de variação de movimento [0,1]
        @param cfa: Cor de fundo do ambiente (R,G,B)
        @param fpe: factor de período de execução
        @param detalhe: nível de detalhe do ambiente
        @param reiniciar: reiniciar quando o agente atinge um alvo
        @param nepisod: Número de episódios a executar
    """
    iniciar_osim(None, defamb, pausa, perexec, dinamb, fps, pvm, cfa, fpe, detalhe, reiniciar, nepisod)
    osim.vis.actvis()
    print('PSA: Iniciar')


def executar(agente, defamb=None, pausa=False, perexec=0.05, dinamb=0, fps=50, pvm=0, cfa=(255, 255, 255), fpe=10, detalhe=1):
    """Executar simulação    
        @param agente: agente a executar        
        @param defamb: ficheiro de definição do ambiente        
        @param pausa: pausa activa (sim/não)        
        @param perexec: período de execução [s]        
        @param dinamb: dinamismo do ambiente [%] (0 - ambiente estático)        
        @param fps: ritmo de actualização da visualização [fps]
        @param pvm: probabilidade de variação de movimento [0,1]
        @param fpe: factor de período de execução
        @param detalhe: nível de detalhe do ambiente
    """
    if not osim:
        iniciar_osim(agente, defamb, pausa, perexec, dinamb, fps, pvm, cfa, fpe, detalhe)
    else:
        osim.mod.iniciarag(agente)
        osim.vis.actinfo()
        osim.vis.altcfa(cfa)
    print('PSA: Executar')
    osim.executar()


def reiniciar():
    """Reiniciar evolução do ambiente"""
    if osim:
        print('PSA: Reiniciar')
        osim.mod.ambiente.iniciar()
        osim.mod.agente.reiniciar()


def pausa():
    """Activar pausa de execução"""
    if osim.mod.agente:
        osim.ctl.activarpausa()
    else:
        espera()


def espera():
    """Espera de tecla"""
    while True:
        eventos = osim.ctl.eventosiu()
        if eventos:
            if TERMINAR in eventos:
                osim.ctl.processarevento(TERMINAR)
                break
            else:
                break
        osim.vis.actvis()


def actvis():
    """Actualizar visualização"""
    if osim:
        osim.vis.actvis()


def terminar():
    """Terminar execução"""
    if osim:
        osim.vis.terminarvis()
        print('PSA: Terminar (Pausa)')
    else:
        print('PSA: Terminar (Pausa, OSIM=NDEF)')


def passo():
    """Obter passo de execução"""
    return osim.mod.passo


def tempopasso():
    """Obter duração do último passo de execução"""
    return osim.mod.tpasso


def tempoexec():
    """Obter tempo decorrido desde o início do actual passo de execução"""
    return osim.mod.texec


def temposimul():
    """Obter tempo decorrido desde o início da simulação"""
    return osim.mod.tsim


def ambiente():
    """Obter ambiente
    @return: ambiente"""
    if osim is None:
        raise Exception('PSA: Simulador não iniciado')
    return osim.mod.ambiente


def dirmov(n=8):
    """Obter direcções de movimento
    @param n: número de direcções
    @return: lista de ângulos [rad]"""
    return ambiente().gerardir(n)


def vis(nvis):
    """Obter visualizador
    @param nvis: número do visualizador
    @return: visualizador"""
    if nvis == 0:
        return visper
    if nvis == 1:
        return vismod
    if nvis == 2:
        return visvec
    if nvis == 3:
        return visamb
    return


def info(texto):
    """Apresentar informação
    @param texto: texto a apresentar
    """
    osim.vis.info(texto)


def infopee(mecproc, no, objectivo=None):
    """Apresentar informação de procura
    @param mecproc: mecanismo de procura
    @param no: nó expandido
    @param objectivo: objectivo da procura
    """
    vismod.limpar()
    if hasattr(mecproc, 'gerados'):
        vismod.gerados(mecproc.gerados)
    vismod.abertos(mecproc.abertos)
    info('PROF: %d, CUSTO: %.3f' % (no.prof, no.g))
    vismod.rect(no.estado, 0, (255, 0, 0), 1)
    solparcial = mecproc.gerarsolucao(no)
    if solparcial:
        vismod.solucao(solparcial)
    if objectivo:
        if hasattr(objectivo, 'estadofinal'):
            vismod.rect(objectivo.estadofinal, 1, (255, 0, 0), 1)
    actvis()


def infodelib(posag, elemamb, posobj=None, plano=None):
    """Apresentar informação deliberativa
    @param posag: posição do agente
    @param elemamb: elementos do ambiente
    @param posobj: posição objectivo
    @param plano: plano de acção
    """
    vismod.limpar()
    vismod.elementos(elemamb)
    if posobj:
        vismod.rect(posobj)
    if plano:
        vismod.plano(posag, plano)


class VisPEE:
    """Visualizador de Procura em Espaços de Estados"""
    __module__ = __name__
    __qualname__ = 'VisPEE'

    def __init__(self, vis=None):
        if vis:
            self.vis = vis
        else:
            self.vis = vismod

    def mostrar(self, no, estados=None, fronteira=None):
        """Apresentar informação de procura
        @param no: nó expandido
        @param estados: estados explorados
        @param fronteira: fronteira de exploração
        """
        visualizar_procura(no, estados, fronteira)

    def solucao(self, sol):
        """Apresentar solução
        @param sol: solução
        """
        visualizar_solucao(sol)


def visualizar_procura(no=None, estados=None, fronteira=None, solucao=None, estado=None):
    """Visualização de Procura em Espaços de Estados   
    @param no: nó expandido
    @param estados: estados explorados
    @param fronteira: fronteira de exploração
    @param solucao: solução resultante da procura
    @param estado: estado actual do agente
    """
    vismod.limpar()
    if estados:
        vismod.gerados(estados)
    else:
        if fronteira:
            if hasattr(fronteira, 'memoria'):
                vismod.abertos(fronteira.memoria)
            else:
                vismod.abertos(fronteira)
        elif no is None:
            estado_actual = estado
        else:
            estado_actual = no.estado
        if estado_actual is not None:
            vismod.rect(estado_actual, 0, (255, 0, 0), 1)
        if solucao is None:
            if no:
                sol = no.percurso()
            else:
                sol = None
        else:
            sol = [(no.estado, no.operador) for no in solucao[1:]]
    if sol:
        vismod.percurso(sol)
    actvis()


def visualizar_solucao(sol):
    vismod.percurso(sol)
    actvis()


from .memrel import MemRel

def repamb():
    """Obter representação do ambiente"""
    rep = MemRel(ambiente().obterimagem().iteritems())
    rep.ins(osim.mod.ambiente.elemag.pos, 'agente')
    return rep


def custoaccao():
    """Obter custo da última acção executada"""
    if osim is None:
        raise Exception('PSA: Simulador não iniciado')
    return dist(osim.mod.ambiente.pos_mov, osim.mod.ambiente.nova_pos_mov)


def infoexec():
    """Obter informação de execução
    @return: {'agente': nome do agente,
              'episodios': número de episódios,
              'passos': número de passos total,
              'passos_episod': lista com número de passos por episódio}"""
    nome_agente = str(osim.mod.agente.__class__.__name__)
    info_exec = {'agente':nome_agente,  'episodios':osim.episod, 
     'passos':osim.passos, 
     'passos_episodio':osim.passos_episod, 
     'colisoes':osim.ncol, 
     'colisoes_episodio':osim.ncol_episod}
    return info_exec
# uncompyle6 version 3.6.6
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\sp1\Documents\proj19\ia1\proj\src\lib_psa\psa\ctl.py
# Compiled at: 2019-01-04 20:35:11
# Size of source mod 2**32: 6813 bytes
"""
Plataforma de Simulação de Agentes
@author: Luís Morgado
"""
import pygame, time
EVOLUIR = 'EVOLUIR'
TERMINAR = 'TERMINAR'
ESPAUSA = 'ESPAUSA'
PASSO = 'PASSO'
INICIAR = 'INICIAR'
REINICIAR = 'REINICIAR'
VMAX = 'VMAX'
TECLA = 'TECLA'
ALVOINI = 'ALVOINI'
ESEXEC = 'ESEXEC'
ESPAUSA = 'ESPAUSA'
ESFIM = 'ESFIM'

class SimulCtl:

    def __init__(self, mod, vis, pausa):
        self.mod = mod
        self.vis = vis
        self.fullscreen = False
        self.vis_pot = False
        if pausa:
            self.estado = ESPAUSA
        else:
            self.estado = ESEXEC
        self.vis.estado(pausa)
        self.vis.ambiente()
        self.vis.infosens()

    def processar(self):
        self.evoltemp()
        self.vis.temposimul()
        eventos = self.eventostemp() + self.eventosiu()
        for evento in eventos:
            self.processarevento(evento)

    def processarevento(self, evento):
        if evento == EVOLUIR:
            if self.estado == ESEXEC:
                self.evoluirsimul()
        elif evento == ESPAUSA:
            if self.estado == ESEXEC:
                self.mod.vmax = False
                self.vis.estado(True)
                self.estado = ESPAUSA
            else:
                self.vis.estado(False)
                self.estado = ESEXEC
        elif evento == PASSO:
            if self.estado == ESPAUSA:
                self.evoluirsimul()
        elif evento == VMAX:
            self.mod.vmax = not self.mod.vmax
        elif evento == INICIAR:
            self.iniciarsimul()
            self.evoluirsimul()
        elif evento == REINICIAR:
            self.iniciarsimul(False)
            self.evoluirsimul()
        elif evento == ALVOINI:
            self.mod.alvo_ini = True
        elif evento == TERMINAR:
            self.estado = ESFIM

    def iniciarsimul(self, iniciar_agente=True):
        self.mod.iniciaramb()
        if iniciar_agente:
            self.mod.iniciarag()
        else:
            self.vis.ambiente()
            self.vis.infosens()
            if iniciar_agente:
                print('PSA: Iniciar')
            else:
                print('PSA: Reiniciar')

    def evoluirsimul(self):
        if self.mod.vmax:
            texec_agente = self.mod.texec
        else:
            texec_agente = self.mod.texec - self.mod.perexec
        passosevol = int(texec_agente / self.mod.perexec * self.mod.fpe)
        if passosevol < 1 or self.estado == ESPAUSA:
            passosevol = 1
        self.mod.ambiente.evoluir(passosevol)
        self.vis.ambiente()
        if not self.mod.vmax:
            self.vis.infosens(self.vis_pot)
        self.vis.agente()
        self.vis.actvis()
        self.mod.ambiente.accoes = []
        self.mod.agente.executar()
        self.evoluirpasso()

    def evoluirpasso(self):
        self.mod.passo += 1
        self.evoltemp()
        self.vis.tempoexec()
        self.evoltemppasso()
        self.vis.passo()

    def estadofinal(self):
        """ Indicação de estado final """
        return self.estado == ESFIM

    def pausa(self):
        """ Indicação de pausa """
        return self.estado == ESPAUSA

    def activarpausa(self):
        self.estado = ESPAUSA

    def eventostemp(self):
        """ Gerar eventos temporais """
        if self.mod.vmax:
            eventos = [
             EVOLUIR]
        else:
            eventos = []
            nevolamb = int(self.mod.texec / self.mod.perexec)
            if nevolamb > 0:
                eventos.append(EVOLUIR)
        return eventos

    def eventosiu(self):
        """ Gerar eventos de interface de utilização """
        eventos = []
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                eventos.append(TERMINAR)
            else:
                if evento.type == pygame.KEYDOWN:
                    if evento.unicode in ('t', 'T'):
                        eventos.append(TERMINAR)
                    elif evento.unicode in ('p', 'P'):
                        eventos.append(ESPAUSA)
                    elif evento.unicode in ('e', 'E'):
                        eventos.append(PASSO)
                    elif evento.unicode in ('i', 'I'):
                        eventos.append(INICIAR)
                    elif evento.unicode in ('r', 'R'):
                        eventos.append(REINICIAR)
                    elif evento.unicode in ('v', 'V'):
                        eventos.append(VMAX)
                    elif evento.unicode in ('f', 'F'):
                        self.fullscreen = self.vis.comutarfs(self.fullscreen)
                    elif evento.unicode in ('c', 'C'):
                        self.vis_pot = not self.vis_pot
                    elif evento.unicode in ('a', 'A'):
                        eventos.append(ALVOINI)
                    else:
                        eventos.append(TECLA)

        return eventos

    def evoltemp(self):
        """ Evoluir temporização """
        tact = time.time()
        self.mod.tsim = tact - self.mod.tini
        self.mod.texec = tact - self.mod.tant

    def evoltemppasso(self):
        """ Evoluir temporização do passo de execução """
        self.mod.tpasso = self.mod.texec
        self.mod.tant = time.time()
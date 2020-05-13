# uncompyle6 version 3.6.6
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\sp1\Documents\proj19\ia1\proj\src\lib_psa\psa\vissim.py
# Compiled at: 2019-01-04 20:13:31
# Size of source mod 2**32: 12291 bytes
"""
Plataforma de Simulação de Agentes
@author: Luís Morgado
"""
import pygame, os
from datetime import datetime
from .versao import __version__
from .util import fint, incpos
import psa.elementos as elementos
from .visualizador import Visualizador
from .agente import ESQ, DIR, FRENTE
from .visvect import VisVectCampo
POS_INI_X = 10
POS_INI_Y = 40
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
AMARELO = (255, 255, 0)
VERMELHO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)
COR_FUNDO_BASE = (0, 0, 0)
COR_VIS_ACTIVO = BRANCO
COR_VIS_INACTIVO = PRETO
COR_LSONAR = (100, 100, 0)
COR_BASE = (51, 51, 51)
COR_DIRAG = (0, 204, 51)
COR_INFO = (27, 27, 27)
IMG_BASE = '/img/base.png'
IMG_EXEC = '/img/exec.png'
IMG_PAUSA = '/img/pausa.png'
IMG_PDIRAG = '/img/pdirag.png'
IMG_VCAMPO = '/img/vcampo.png'
FONTE1 = '/fnt/DejaVuSans.ttf'
DFONTE1 = 14
FONTE2 = '/fnt/LCDN.TTF'
DFONTE2 = 17
DFONTE3 = 12
RAMB = (0, 60, 560, 560)
RPER = (565, 60, 280, 280)
RMOD = (565, 341, 280, 280)
RESTADO = (0, 30, 105, 30)
RFPS = (110, 33, 30, 23)
RDINAMB = (165, 33, 63, 23)
RELEMAMB = (255, 33, 63, 23)
RPASSO = (365, 33, 71, 23)
RPEREXEC = (460, 33, 43, 23)
RTEXEC = (560, 33, 43, 23)
RTSIM = (712, 33, 100, 23)
RMODAG = (820, 36, 167, 21)
RPDIRAG = (873, 83, 94, 94)
RCARGA = (918, 193, 47, 21)
RVTRANS = (929, 212, 22, 21)
RVROT = (907, 231, 43, 21)
RACT = (860, 290, 122, 60)
RLACT = (860, 290, 122, 20)
RSONAR1 = (885, 405, 70, 10)
RSONAR2 = (885, 425, 70, 10)
RSONAR3 = (885, 445, 70, 10)
RSONDIST1 = (960, 401, 26, 20)
RSONDIST2 = (960, 422, 26, 20)
RSONDIST3 = (960, 442, 26, 20)
RINFO = (59, 633, 871, 21)
RCURSOR = (932, 631, 51, 21)
PPDIRAG = (889, 135, 66, 16)
PDIRAG = (921, 131)
DDIRAG = 44
LDIRAG = 3
DYACT = 20

class SimulVis:

    def __init__(self, fps, mod, cfa):
        pygame.init()
        self.fps = fps
        self.mod = mod
        self.cfa = cfa
        self.fs_comut = False
        self.clock = pygame.time.Clock()
        self.obterelemgraf()
        self.iniciarvis()

    def terminarvis(self):
        pygame.quit()

    def actvis(self):
        self.svis.blit(self.visamb.svis, self.rectamb)
        self.svis.blit(self.visper.svis, self.rectper)
        self.svis.blit(self.vismod.svis, self.rectmod)
        pygame.display.flip()
        if not self.mod.vmax:
            self.clock.tick(self.fps)

    def obterelemgraf(self):
        """" Iniciar elementos gráficos (fontes e imagens) """
        psapath = os.path.dirname(__file__)
        self.imgbase = pygame.image.load(psapath + IMG_BASE)
        self.imgexec = pygame.image.load(psapath + IMG_EXEC)
        self.imgpausa = pygame.image.load(psapath + IMG_PAUSA)
        self.imgpdirag = pygame.image.load(psapath + IMG_PDIRAG)
        self.imgvcampo = pygame.image.load(psapath + IMG_VCAMPO)
        self.fonte1 = pygame.font.Font(psapath + FONTE1, DFONTE1)
        self.fonte2 = pygame.font.Font(psapath + FONTE2, DFONTE2)
        self.fonte3 = pygame.font.Font(psapath + FONTE2, DFONTE3)

    def actinfo(self):
        self.infosimul(str(self.fps), RFPS)
        self.infosimul(str(self.mod.dinamb), RDINAMB)
        self.infosimul(str(self.mod.ambiente.obternumelem()), RELEMAMB)
        self.infosimul('%.3f' % self.mod.perexec, RPEREXEC)
        self.infosimul((str(self.mod.agente.__class__.__name__)), RMODAG, fonte=(self.fonte1))
        self.info('')
        self.cursor(None)
        self.agente()
        self.ambiente()
        self.infosens()
        self.passo()
        self.tempoexec()
        self.temposimul()

    def iniciarvis(self):
        pygame.display.set_caption('PSA v' + __version__)
        os.environ['SDL_VIDEO_WINDOW_POS'] = str(POS_INI_X) + ',' + str(POS_INI_Y)
        dimx, dimy = self.imgbase.get_size()
        self.svis = pygame.display.set_mode([dimx, dimy])
        self.svis.blit(self.imgbase, self.svis.get_rect())
        largbase = self.mod.ambiente.dimx
        self.rectamb, self.visamb = criarvis(RAMB, largbase, self.cfa)
        self.rectper, self.visper = criarvis(RPER, largbase, PRETO)
        self.rectmod, self.vismod = criarvis(RMOD, largbase, PRETO)
        self.visvec = VisVectCampo(self.mod, self.svis, self.imgvcampo)
        self.actinfo()

    def altcfa(self, cfa):
        self.cfa = cfa
        largbase = self.mod.ambiente.dimx
        self.rectamb, self.visamb = criarvis(RAMB, largbase, self.cfa)
        self.actvis()

    def estado(self, pausa):
        if pausa:
            img = self.imgpausa
        else:
            img = self.imgexec
        self.svis.blit(img, RESTADO)

    def infosimul(self, texto, rect, ajustepos=False, corfundo=COR_BASE, fonte=None, cor=BRANCO):
        if not fonte:
            fonte = self.fonte2
        vistexto(self.svis, fonte, rect, texto, cor, corfundo, ajustepos)

    def info(self, texto):
        self.infosimul(texto, RINFO, False, COR_INFO, self.fonte1)

    def cursor(self, pos):
        if pos:
            self.infosimul('(%d,%d)' % pos, RCURSOR, False, COR_INFO)
        else:
            self.infosimul('', RCURSOR, False, COR_INFO)

    def posdirag(self):
        self.svis.blit(self.imgpdirag, RPDIRAG)
        px, py = self.mod.ambiente.posag()
        dirag = self.mod.ambiente.dirag()
        pdirtxt = '(%.1f,%.1f) : %.1f' % (px, py, dirag)
        self.infosimul(pdirtxt, PPDIRAG, fonte=(self.fonte3))
        x, y = PDIRAG
        dx, dy = incpos(DDIRAG, self.mod.ambiente.dirag())
        pygame.draw.line(self.svis, COR_DIRAG, (x, y), (x + dx, y + dy), LDIRAG)

    def actuador(self):
        self.infosimul('', RACT, False, COR_INFO)
        x, y, larg, alt = RLACT
        dy = 0
        for accao in self.mod.ambiente.accoes:
            self.infosimul(str(accao), (x, y + dy, larg, alt), False, COR_INFO, self.fonte1)
            dy += DYACT

    def sonar(self, rot, dist, dmax):
        dnorm = dist / float(dmax)
        if rot == ESQ:
            rect = RSONAR1
            posdist = RSONDIST1
        elif rot == FRENTE:
            rect = RSONAR2
            posdist = RSONDIST2
        elif rot == DIR:
            rect = RSONAR3
            posdist = RSONDIST3
        pygame.draw.rect(self.svis, COR_BASE, rect, 0)
        x, y, larg, alt = rect
        pygame.draw.rect(self.svis, COR_DIRAG, (x, y, larg * dnorm, alt), 0)
        self.infosimul('%.0f' % dist, posdist)

    def passo(self):
        self.infosimul(str(self.mod.passo), RPASSO)

    def tempoexec(self):
        self.infosimul('%.3f' % self.mod.texec, RTEXEC)

    def temposimul(self):
        self.infosimul(tempotexto(self.mod.tsim), RTSIM)

    def ambiente(self):
        self.infosimul(str(self.mod.ambiente.obternumelem()), RELEMAMB)
        self.visamb.limpar()
        for elem in self.mod.ambiente.elementos.values():
            viselem(self.visamb, elem, self.fs_comut)

        viselem(self.visamb, self.mod.ambiente.elemag)
        self.fs_comut = False

    def agente(self):
        self.posdirag()
        self.infosimul('%2d' % self.mod.ambiente.cargaag(), RCARGA)
        self.infosimul('%.0f' % self.mod.ambiente.vtransag(), RVTRANS)
        self.infosimul('%.3f' % self.mod.ambiente.vrotag(), RVROT)
        self.actuador()
        self.visvec.limpar()
        self.mod.ambiente.iniciarevol()

    def infosens(self, vis_pot=False):
        elemag = self.mod.ambiente.elemag
        if vis_pot:
            self.mod.agente.sensorpotfrt.mostrar_pot()
        else:
            self.visper.limpar()
            dmax = self.mod.ambiente.dmax()
            for rot in [ESQ, FRENTE, DIR]:
                elem, dist, rot = self.mod.ambiente.obterisens(rot)
                if dist >= 0:
                    self.visper.linha(centrar(elemag.pos), centrar(elem.pos), COR_LSONAR)
                    self.sonar(rot, dist, dmax)
                viselem(self.visper, elem)

        viselem(self.visper, elemag)

    def posvirt(self, pos, rect):
        """ Converter posição em pixeis em posição virtual"""
        xp, yp = pos
        xi, yi, larg, alt = rect
        escala = larg / float(self.mod.ambiente.dimx)
        x = int((xp - xi) / escala)
        y = int((yp - yi) / escala)
        return (
         x, y)

    def comutarfs(self, fs):
        self.fs_comut = True
        fs = not fs
        if fs:
            pygame.display.set_mode(self.imgbase.get_size(), pygame.FULLSCREEN)
        else:
            pygame.display.set_mode(self.imgbase.get_size())
        self.svis.blit(self.imgbase, self.svis.get_rect())
        self.actinfo()
        return fs


def viselem(vis, elem, fs_comut=False):
    if isinstance(elem, elementos.Agente):
        vis.agente(elem.pos, elem.dir, elem.col, elem.carga(), elem.varang)
        elem.varang = None
    elif (elem.alterado or fs_comut) and isinstance(elem, elementos.Obstaculo):
        vis.obstaculo(elem.pos)
    elif isinstance(elem, elementos.Alvo):
        vis.alvo(elem.pos)
    elif isinstance(elem, elementos.Base):
        vis.base(elem.pos, elem.carga)
    elif isinstance(elem, elementos.Vazio):
        vis.vazio(elem.pos)


def vistexto(svis, fonte, rect, texto, cor=BRANCO, corfundo=COR_FUNDO_BASE, ajustepos=False):
    svis.fill(corfundo, rect)
    imgtexto = fonte.render(texto, True, cor)
    largtexto = imgtexto.get_rect()[2]
    x, y, larg, alt = rect
    if ajustepos:
        dx = larg - largtexto
        larg = largtexto
    else:
        dx = 0
    svis.blit(imgtexto, (x + dx, y, larg, alt))


def vismovag(svis, elemag):
    svis.visvazio(elemag.pos)
    svis.visvazio(elemag.posant)
    viselem(svis, elemag)


def criarvis(rectbase, dimvirt, corfundo):
    x, y, larg, alt = rectbase
    escala = larg / float(dimvirt)
    escvis = int(escala)
    margem = fint(0.5 * (escala - escvis) * dimvirt)
    x += margem
    y += margem
    larg = alt = escvis * dimvirt
    rectvis = (x, y, larg, alt)
    svis = pygame.Surface((larg, alt))
    return (
     rectvis, Visualizador(svis, escvis, corfundo))


def tempotexto(tempo):
    t = datetime.fromtimestamp(tempo)
    return '%02d:%02d:%02d:%02d' % (t.hour, t.minute, t.second, t.microsecond / 10000)


def centrar(pos):
    x, y = pos
    return (
     x + 0.5, y + 0.5)
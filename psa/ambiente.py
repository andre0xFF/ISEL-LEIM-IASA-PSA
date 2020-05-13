# uncompyle6 version 3.6.6
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\sp1\Documents\proj19\ia1\proj\src\lib_psa\psa\ambiente.py
# Compiled at: 2018-01-26 17:34:22
# Size of source mod 2**32: 14414 bytes
"""
Plataforma de Simulação de Agentes
@author: Luís Morgado
"""
import itertools
from math import sqrt, pi
from random import random
from copy import copy
import psa.util as util
import psa.elementos as elementos
from .util import posint
SQRT2 = sqrt(2)
DPASSO = SQRT2

class Ambiente:
    """ Gestão do ambiente """
    __module__ = __name__
    __qualname__ = 'Ambiente'

    def __init__(self, defamb, dinamb, vtrans, vrot, pvm, detalhe):
        self.defamb = defamb
        self.dinamb = dinamb
        self.vtrans = vtrans
        self.vrot = vrot
        self.pvm = pvm
        self.detalhe = detalhe
        self.imagem_sens = []
        self.iniciar()

    def iniciar(self):
        self.iniciarelem(self.defamb, self.vtrans, self.vrot, self.dinamb)
        self.elemgest = []
        self.numaccoes = 0
        self.distagente = 0
        self.alterado = True
        self.pos_mov = self.elemag.pos
        self.nova_pos_mov = self.elemag.pos
        self.alvo = False
        self.dir_accao = self.elemag.dir
        self.iniciarevol()

    def iniciarevol(self):
        self.isens = []
        self.accoes = []

    def evoluir(self, passosevol):
        self.elemag.evoluir()
        elemrem = {}
        elemins = {}
        if self.dinamb > 0:
            for elem in self.elementos.values():
                elem.evoluir(passosevol)
                if elem.tvida == 0:
                    self.elemgest.append(elem)
                    self.remelemex(elem, elemrem)

            if self.elemgest:
                for ielem, elem in enumerate(self.elemgest):
                    elem.evoluir(passosevol)
                    if elem.tvida > 0:
                        x = random() * (self.dimx - 1)
                        y = random() * (self.dimy - 1)
                        novapos = posint((x, y))
                    if not self.elementos.get(novapos):
                        if elemins.get(novapos):
                            for posalt in self.area:
                                if not self.elementos.get(posalt):
                                    novapos = elemins.get(novapos) or posalt
                                    break

                        if self.elementos.get(novapos) or elemins.get(novapos) or util.dist(self.elemag.pos, novapos) > 1:
                            elem.pos = novapos
                            elem.alterado = True
                            self.inselemex(elem, elemins)
                            self.elemgest.pop(ielem)

            self.actelem(elemrem, elemins)
            self.alterado = True
            alvos = [e for _, e in self.elementos.items() if e.tipo == 'alvo']
        res = self.alterado
        self.alterado = False
        return res

    def posag(self):
        return self.elemag.pos

    def dirag(self):
        return self.elemag.dir

    def cargaag(self):
        return self.elemag.ncarga()

    def cargaagt(self):
        carga = self.elemag.carga()
        self.elemag._carga = False
        return carga

    def ncargaagt(self):
        return self.elemag.ncarga()

    def colisag(self):
        return self.elemag.col

    def vtransag(self):
        return self.elemag.vtrans

    def vrotag(self):
        return self.elemag.vrot

    def distag(self):
        """Distância percorrida pelo agente"""
        return self.distagente

    def numac(self):
        """Número de acções realizadas pelo agente"""
        return self.numaccoes

    def obterimagsens(self):
        return self.imagem_sens

    def obterisens(self, rot):
        self.imagem_sens = []
        posper = posag = self.elemag.pos
        dpasso = 1
        incpos = util.incpos(dpasso, self.elemag.dir + rot)
        isens = None
        while isens is None:
            self.posperant = posint(posper)
            posper = util.movpos(posper, incpos)
            if self.posval(posint(posper)):
                elem = self.obterelempos(posper)
                if elem is not None:
                    dist = util.dist(posag, posint(posper))
                    isens = (
                     elem, dist, rot)
                    break
                else:
                    self.imagem_sens.append((posint(posper), elementos.VAZIO))
            else:
                dist = util.dist(posag, posint(posper))
                elem = elementos.Obstaculo(posper)
                isens = (elem, dist, rot)
                break

        if isens:
            self.isens.append(isens)
            self.imagem_sens.append((posint(posper), isens[0].tipo))
        self.posper = posper
        return isens

    def regaccao(self, accao):
        self.accoes.append(accao)
        self.numaccoes += 1

    def rodar(self, rot):
        varang = 0
        if self.pvm:
            if random() < self.pvm:
                varang = pi / 4
                self.elemag.varang = varang
            elif random() < self.pvm:
                varang = -pi / 4
                self.elemag.varang = varang
            else:
                self.elemag.varang = None
        self.regaccao('rodar(%.3f)' % rot)
        if varang:
            self.regaccao('var: %+.3f' % varang)
        self.elemag.dir = util.normang(self.elemag.dir + rot + varang)
        self.elemag.col = False

    def orientar(self, ang):
        varang = 0
        if self.pvm:
            if random() < self.pvm:
                varang = pi / 4
                self.elemag.varang = varang
            elif random() < self.pvm:
                varang = -pi / 4
                self.elemag.varang = varang
            else:
                self.elemag.varang = None
        self.regaccao('orientar(%.3f)' % ang)
        if varang:
            self.regaccao('var: %+.3f' % varang)
        self.elemag.dir = util.normang(ang + varang)
        self.elemag.col = False

    def avancar(self, regaccao=True, dpasso=1, cont=False):
        if regaccao:
            self.regaccao('avancar(%.3f)' % dpasso)
        novapos = self.novaposag(dpasso, cont)
        self.pos_mov = posint(self.elemag.pos)
        self.nova_pos_mov = posint(novapos)
        self.dir_accao = self.elemag.dir
        self.elemag.col = True
        elempos = None
        if dpasso > 1:
            dist_col = self.detectar_colisao(novapos)
            if dist_col is not None:
                novapos = self.posperant
                elempos = self.obterelempos(novapos)
                self.moverag(novapos)
                self.distagente += dist_col
            else:
                elempos = self.obterelempos(novapos)
                self.moverag(novapos)
                self.elemag.col = False
        elif self.posval(posint(novapos)):
            elempos = self.obterelempos(novapos)
            if elempos is None or isinstance(elempos, elementos.Alvo) or isinstance(elempos, elementos.Base):
                self.elemag.col = False
                self.moverag(novapos)
                self.distagente += dpasso
                self.alvo = isinstance(elempos, elementos.Alvo)
        return (
         novapos, elempos)

    def detectar_colisao(self, novapos):
        elem, _, _ = self.obterisens(0)
        if elem.tipo == 'obst':
            dist_posperant = util.dist(self.elemag.pos, self.posperant)
            dist_novapos = util.dist(self.elemag.pos, novapos)
            if dist_posperant < dist_novapos:
                return dist_posperant

    def _pegaralvo(self, elem):
        self.elemag.pegar()
        self.elemag.col = False
        self.remelem(elem)
        self.alterado = True

    def pegar(self, dpasso=1, cont=False):
        self.regaccao('pegar')
        elem = self.obterelempos(self.elemag.pos)
        if isinstance(elem, elementos.Alvo):
            self._pegaralvo(elem)
        else:
            _, elem = self.avancar(False, dpasso, cont)
            if elem is not None:
                if isinstance(elem, elementos.Alvo):
                    self._pegaralvo(elem)
                    if not cont:
                        self.moverag(elem.pos)

    def _largaralvo(self, elem):
        self.elemag.largar()
        self.elemag.col = False
        elem.preencher()
        self.alterado = True

    def largar(self):
        self.regaccao('largar')
        elem = self.obterelempos(self.elemag.pos)
        if isinstance(elem, elementos.Base):
            if self.elemag.ncarga() > 0:
                self._largaralvo(elem)
            else:
                self.elemag.col = True
        else:
            _, elem = self.avancar(False)
            if elem is not None:
                if isinstance(elem, elementos.Base):
                    if not elem.carga:
                        if self.elemag.carga():
                            self._largaralvo(elem)

    def obterimagem(self):
        """Obter imagem do ambiente, incluindo posições vazias"""
        imagem = self.area.copy()
        for pos, elem in iter(self.elementos.items()):
            imagem[pos] = elem.tipo

        return imagem

    def obterelem(self):
        """Obter todos os elementos"""
        return dict([(pos, elem.tipo) for pos, elem in self.elementos.items()])

    def obterelempos(self, pos):
        """Obter elemento de uma posição"""
        x, y = pos
        posdisc = (util.fint(x), util.fint(y))
        return self.elementos.get(posdisc)

    def obterelemdif(self):
        """Obter elementos em que houve alteração"""
        elemdif = dict([(pos, elem.tipo) for pos, elem in self.elemdif.items()])
        self.elemdif = {}
        return elemdif

    def obternumelem(self):
        """Obter número de elementos no ambiente"""
        return len(self.elementos)

    def remelem(self, elem):
        """Sinalizar elemento do ambiente para remoção"""
        pos = elem.pos
        self.elemdif[pos] = elem
        del self.elementos[pos]

    def inselem(self, elem):
        """Inserir elemento no ambiente"""
        self.elementos[elem.pos] = elem
        self.elemdif[elem.pos] = elem

    def remelemex(self, elem, elemrem):
        """Sinalizar elemento do ambiente para remoção"""
        pos = elem.pos
        self.elemdif[pos] = elem
        elemrem[pos] = elem

    def inselemex(self, elem, elemins):
        """Inserir elemento no ambiente"""
        elemins[elem.pos] = elem
        self.elemdif[elem.pos] = elem

    def actelem(self, elemrem, elemins):
        """Actualizar elemento do ambiente"""
        for pos in elemrem:
            del self.elementos[pos]

        for pos, elem in elemins.items():
            self.elementos[pos] = elem

    def iniciarelem(self, defamb, vtrans, vrot, dinamb):
        """Iniciar elementos do ambiente"""
        self.area = {}
        self.elementos = {}
        self.elemag = None
        dimamb = None
        y = 0
        for linha in defamb:
            if dimamb is None:
                dimamb = len(linha) - 1
            x = 0
            for c in linha:
                if c not in ('\n', '\r'):
                    pos = (
                     x, y)
                    x += 1
                    self.area[pos] = elementos.VAZIO
                    if c == '@':
                        elem = elementos.Agente(pos, vtrans, vrot)
                        self.elemag = elem
                        continue
                    elif c == 'A':
                        elem = elementos.Alvo(pos, dinamb)
                    elif c == 'B':
                        elem = elementos.Base(pos, dinamb)
                    elif c == 'O':
                        elem = elementos.Obstaculo(pos, dinamb)
                    else:
                        continue
                    self.elementos[pos] = elem

            y += 1

        self.dimx = dimamb
        self.dimy = dimamb
        if self.detalhe > 1:
            x, y = self.elemag.pos
            self.elemag.pos = (x * self.detalhe, y * self.detalhe)
            elementos_det = {}
            area_det = {}
            for x, y in self.area:
                elem = self.elementos.get((x, y))
                for xi in range(self.detalhe):
                    for yi in range(self.detalhe):
                        x_det = int(x * self.detalhe + xi)
                        y_det = int(y * self.detalhe + yi)
                        pos_det = (x_det, y_det)
                        area_det[pos_det] = elementos.VAZIO
                        if elem and elem.tipo == 'obst':
                            elem_det = copy(elem)
                            elem_det.pos = pos_det
                            elementos_det[pos_det] = elem_det

                if elem and elem.tipo in ('alvo', 'base'):
                    pos_det = (
                     x * self.detalhe, y * self.detalhe)
                    elem.pos = pos_det
                    elementos_det[pos_det] = elem

            self.area = area_det
            self.elementos = elementos_det
            self.dimx *= self.detalhe
            self.dimy *= self.detalhe
        for x in range(-1, self.dimx + 1):
            pos = (x, -1)
            self.elementos[pos] = elementos.Obstaculo(pos)
            pos = (x, self.dimy)
            self.elementos[pos] = elementos.Obstaculo(pos)

        for y in range(self.dimy):
            pos = (
             -1, y)
            self.elementos[pos] = elementos.Obstaculo(pos)
            pos = (self.dimx, y)
            self.elementos[pos] = elementos.Obstaculo(pos)

        self.elemdif = self.elementos.copy()

    def moverag(self, novapos):
        """Mover agente no ambiente"""
        self.elemag.mover(novapos)

    def novaposag(self, dpasso, cont):
        """Gerar nova posição do agente
                @param dpasso: distância de passo de avanço"""
        if cont:
            incpos = util.incpos(dpasso, self.elemag.dir)
        else:
            incpos = util.incposint(dpasso, self.elemag.dir)
        novapos = util.movpos(self.elemag.pos, incpos)
        return novapos

    def dmax(self):
        """Dimensão máxima do ambiente"""
        return SQRT2 * self.dimx

    def posval(self, pos):
        """Verificação de posição válida (interior ao ambiente)"""
        return util.interior(pos, (0, 0, self.dimx, self.dimy))

    def gerarpos(self):
        """ Gerar todas as posições do ambiente """
        xcoord = range(self.dimx)
        ycoord = range(self.dimy)
        return list(itertools.product(xcoord, ycoord))

    def gerardir(self, n=8):
        """ Gerar direcções em passos de pi/(n/2) """
        return util.dirmov(n)
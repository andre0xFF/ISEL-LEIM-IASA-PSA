# uncompyle6 version 3.6.6
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\sp1\Documents\proj19\ia1\proj\src\lib_psa\psa\visualizador.py
# Compiled at: 2019-01-04 20:44:08
# Size of source mod 2**32: 17955 bytes
"""
Visualizador de ambiente
@author: Luís Morgado
"""
import math, pygame, pygame.gfxdraw, colorsys
from .util import fint, linhasvect, incposint, movpos, argmax, intdir, difpospol
from .accao import Accao
COR_AGENTE = (255, 220, 0)
COR_AGLINHA = (0, 0, 0)
COR_ALVO = (0, 250, 0)
COR_BASE = (0, 250, 0)
COR_OBST = (150, 150, 150)
COR_COLIS = (255, 0, 0)

class Visualizador:

    def __init__(self, svis, escala, corfundo):
        """Iniciar visualizador"""
        self.svis = svis
        self.escala = escala
        self.corfundo = corfundo
        self.nivel_detalhe = 1
        self.limpar()

    def obter_escala(self):
        """Obter escala de visualização
        @return: escala (dimensão de visualização)"""
        return self.escala

    def obter_detalhe(self):
        """Obter nível de detalhe
        @return: nível de detalhe"""
        return self.nivel_detalhe

    def definir_detalhe(self, nivel_detalhe):
        """Definir nível de detalhe
        @param nivel_detalhe: nível de detalhe"""
        self.nivel_detalhe = nivel_detalhe
        self.escala /= float(nivel_detalhe)

    def limpar(self):
        """Limpar visualizador"""
        self.svis.fill(self.corfundo)

    def agente(self, pos, ang=None, col=False, carga=False, varang=None):
        """Visualizar agente"""
        r = int(0.5 * self.escala)
        x, y = self.pvpix(pos)
        x0 = x + r
        y0 = y + r
        if col:
            cor = COR_COLIS
        else:
            cor = COR_AGENTE
        pygame.gfxdraw.filled_circle(self.svis, x0, y0, r, cor)
        pygame.gfxdraw.aacircle(self.svis, x0, y0, r, cor)
        if ang is not None:
            dx = +(r - 1) * math.cos(ang)
            dy = -(r - 1) * math.sin(ang)
            x1 = fint(x + r + dx)
            y1 = fint(y + r + dy)
            pygame.draw.line(self.svis, COR_AGLINHA, (x0, y0), (x1, y1))
        if carga:
            self.rect(pos, int(0.3 * self.escala), COR_ALVO, 0)
        if varang is not None:
            vang = ang + varang
            self.vector(pos, 2, vang, cor=(255, 0, 0), linha=2)

    def alvo(self, pos):
        """Visualizar alvo"""
        self.rect(pos, 2, COR_ALVO, 0)

    def base(self, pos, carga=False):
        """Visualizar base"""
        self.rect(pos, 2, COR_BASE, 1)
        if carga:
            dim = fint(self.escala * 0.3)
            if dim < 1:
                dim = 1
            self.rect(pos, dim, COR_BASE, 0)

    def obstaculo(self, pos):
        """Visualizar obstáculo"""
        self.rect(pos, 0, COR_OBST, 0)

    def vazio(self, pos):
        """Visualizar vazio"""
        self.rect(pos, 0, self.corfundo, 0)

    def rect(self, pos, margem=0, cor=(255, 0, 0), linha=1):
        """Visualizar rectângulo
        @param pos: posição do ambiente
        @param margem: margem em pixeis
        @param cor: cor RGB
        @param linha: espessura de linha (0 - preencher)"""
        x, y = self.pvpix(pos)
        spx = margem
        spy = margem
        rect = pygame.Rect(x + spx, y + spy, self.escala - spx * 2, self.escala - spy * 2)
        pygame.draw.rect(self.svis, cor, rect, linha)

    def rectx(self, rect, cor=(255, 0, 0), linha=1):
        """Visualizar rectângulo auxiliar
        @param rect: (x, y, dimx, dimy)
        @param cor: cor RGB
        @param linha: espessura de linha (0 - preencher)"""
        rx, ry, rdx, rdy = rect
        x, y = self.pvpix((rx, ry))
        dimx, dimy = self.pvpix((rdx, rdy))
        rect = pygame.Rect(x, y, dimx, dimy)
        pygame.draw.rect(self.svis, cor, rect, linha)

    def circx(self, pos, raio, cor=(255, 255, 255), linha=1):
        """Visualizar círculo
        @param pos: posição do ambiente
        @param margem: margem em pixeis
        @param cor: cor RGB
        @param linha: espessura de linha (0 - preencher)"""
        x, y = self.pvpix(pos)
        dcentro = fint(0.5 * self.escala)
        x0 = x + dcentro
        y0 = y + dcentro
        r = raio * self.escala
        if linha == 0:
            pygame.gfxdraw.filled_circle(self.svis, x0, y0, r, cor)
        pygame.gfxdraw.aacircle(self.svis, x0, y0, r, cor)

    def circ(self, pos, margem, cor, linha=1, pos_int=False):
        """Visualizar círculo
        @param pos: posição do ambiente
        @param margem: margem em pixeis
        @param cor: cor RGB
        @param linha: espessura de linha (0 - preencher)"""
        x, y = self.pvpix(pos)
        dcentro = fint(0.5 * self.escala)
        x0 = x + dcentro
        y0 = y + dcentro
        r = fint(0.5 * self.escala - margem)
        if linha == 0:
            pygame.gfxdraw.filled_circle(self.svis, x0, y0, r, cor)
        pygame.gfxdraw.aacircle(self.svis, x0, y0, r, cor)

    def linha(self, pos_i, pos_f, cor, linha=1, pos_int=False):
        """Visualizar linha"""
        xi, yi = pos_i
        xf, yf = pos_f
        if pos_int:
            posini = (
             xi + 0.5, yi + 0.5)
            posfin = (xf + 0.5, yf + 0.5)
        else:
            posini = (
             xi, yi)
            posfin = (xf, yf)
            pini = self.pvpix(posini)
            pfin = self.pvpix(posfin)
            pygame.draw.line(self.svis, cor, pini, pfin, linha)

    def vector(self, pos, mod, ang, cor=(255, 255, 255), linha=1, seta=True):
        """Visualizar vector """
        x, y = self.pvpix(pos)
        dim = fint(0.5 * mod * self.escala)
        xi = x + self.escala / 2
        yi = y + self.escala / 2
        linhas = linhasvect((xi, yi), dim, ang, 0.17 * math.pi, 0.5)
        if seta:
            for posini, posfin in linhas:
                pygame.draw.line(self.svis, cor, posini, posfin, linha)

        else:
            posini, posfin = linhas[0]
            pygame.draw.line(self.svis, cor, posini, posfin, linha)

    def elemento(self, pos, obj):
        """Visualizar elemento numa posição"""
        if not isinstance(obj, str):
            obj = obj.tipo
        elif obj == 'agente':
            self.agente(pos)
        elif obj == 'alvo':
            self.alvo(pos)
        elif obj == 'obst':
            self.obstaculo(pos)
        elif obj == 'base':
            self.base(pos)
        elif obj == 'vazio':
            self.vazio(pos)

    def elementos(self, poselem):
        """Visualizar elementos num conjunto de posições
        @param poselem: dicionário com associações posição:elemento"""
        for pos in poselem:
            obj = poselem[pos]
            self.elemento(pos, obj)

    def campo(self, campo, escala=None):
        """Visualizar campo de potencial
        @param campo: dicionário com associações posição:valor
        @param escala: (mínimo, máximo)"""
        if escala:
            vmin, vmax = escala
        else:
            vmax = float('-inf')
            vmin = float('+inf')
            for val in campo.values():
                if val > vmax:
                    vmax = val
                if val < vmin:
                    vmin = val

        vmaxnorm = max(vmax, -vmin)
        for pos, val in campo.items():
            if val > 0:
                vnorm = val / vmax
            elif val < 0:
                vnorm = val / vmin
            else:
                vnorm = 0
            if val == 0:
                cor = (0, 0, 0)
            elif val > 0:
                cor = (
                 0, vnorm * 255, 0)
            elif val < 0:
                cor = (
                 vnorm * 255, 0, 0)
            self.rect(pos, 0, cor, 0)

    def campoabs(self, campo, escala, normalizar=False):
        """Visualizar campo de potencial
        @param campo: dicionário com associações posição:valor
        @param escala: escala de visualização
        @param normalizar: normalizar valores"""
        for pos, val in campo.iteritems():
            if normalizar:
                vnorm = val / max(campo.values())
            else:
                vnorm = val * escala
            if vnorm > 1:
                vnorm = 1
            r, g, b = colorsys.hsv_to_rgb(0.5 - vnorm * 0.5, 1, 1)
            self.rect(pos, 0, (r * 255, g * 255, b * 255, 0), 0)

    def gradiente(self, grad):
        """Visualizar gradiente descrito por vectores polares
        @param grad: dicionário com associações posição:(módulo, ângulo)"""
        for pos, (mod, ang) in grad.iteritems():
            self.vector(pos, mod, ang, (255, 255, 0))

    def politica(self, pol):
        """Visualizar política
        @param pol: dicionário com associações posição:operador"""
        for pos, oper in pol.items():
            if hasattr(oper, 'ang'):
                if callable(getattr(oper, 'ang')):
                    ang = oper.ang()
                else:
                    ang = oper.ang
            elif hasattr(oper, 'accao'):
                ang = oper.accao.ang
            else:
                ang = oper
            self.vector(pos, 1, ang, (255, 255, 0))

    def trajecto(self, posini, seqvect):
        """Visualizar sequência de vectores
        @param posini: posição inicial
        @param seqvect: sequência de vectores polares (módulo, ângulo)"""
        pos = posini
        for mod, ang in seqvect:
            self.vector(pos, mod, ang, (255, 255, 0))
            pos = movpos(pos, incposint(mod, ang))

    def plano(self, posini, plano):
        """Visualizar trajecto
        @param posini: posição inicial
        @param plano: sequência de operadores com atributo ang"""
        if plano:
            if hasattr(plano[0], 'ang'):
                if callable(getattr(plano[0], 'ang')):
                    trajecto = [(1, oper.ang()) for oper in plano]
                else:
                    trajecto = [(1, oper.ang) for oper in plano]
            elif hasattr(plano[0], 'accao'):
                oper = getattr(plano[0], 'accao')
                if isinstance(oper, int) or isinstance(oper, float):
                    trajecto = [(1, oper.accao) for oper in plano]
                else:
                    trajecto = [(1, oper.accao.ang) for oper in plano]
            elif hasattr(plano[0], 'direccao'):
                trajecto = [(1, oper.direccao) for oper in plano]
            else:
                trajecto = [(1, ang) for ang in plano]
            self.trajecto(posini, trajecto)

    def accaovalor(self, q, accoes):
        """Visualizar função acção-valor Q(s,a)
        @param q: função acção-valor
        @param accoes: acções definidas"""
        qpos = set([pos for pos, _ in q])
        fval = {}
        for pos in qpos:
            accao = self._Visualizador__maxaccao(pos, q, accoes)
            fval[pos] = self._Visualizador__valor(q, (pos, accao), 0.0)

        self.campo(fval)
        for pos in qpos:
            accao = self._Visualizador__maxaccao(pos, q, accoes)
            self.vector(pos, 1, accao)

        self.marcar(qpos, 1, linha=1)

    def aprendref(self, mec_aprend, vnorm=100, vmin=70, campo=False, fval=None, seta_max=True, ndef=False, ndir=8):
        """Visualizar aprendizagem por reforço
        @param mec_aprend: mecanismo de aprendizagem por reforço"""
        q = mec_aprend._mem_aprend.memoria
        if hasattr(mec_aprend._sel_accao, '_accoes'):
            accoes = mec_aprend._sel_accao._accoes
        else:
            accoes = mec_aprend._sel_accao.accoes
        self.accaovalordir(q, accoes, vnorm, vmin, campo, fval, seta_max, ndef, ndir)

    def accaovalordir(self, q, accoes, vnorm=100, vmin=70, campo=False, fval=None, seta_max=True, ndef=False, ndir=8):
        """Visualizar função acção-valor Q(s,a)
        @param q: função acção-valor
        @param accoes: acções definidas"""
        qpos = set([pos for pos, _ in q])
        if campo:
            fval = {}
            for pos in qpos:
                accao = self._Visualizador__maxaccao(pos, q, accoes)
                fval[pos] = self._Visualizador__valor(q, (pos, accao), 0.0)

            self.campo(fval)
        for pos in qpos:
            if type(accoes) is not list:
                accoes_pos = accoes.get(pos, [])
            else:
                accoes_pos = accoes
            maxaccao = self._Visualizador__maxaccao(pos, q, accoes_pos)
            for accao in accoes_pos:
                qval = q.get((pos, accao))
                if qval is not None:
                    aval = 255 * self._Visualizador__valor(q, (pos, accao), 0.0) / vnorm
                    if aval != 0:
                        if abs(aval) < vmin:
                            if aval > 0:
                                aval = vmin
                            else:
                                aval = -vmin
                        else:
                            if aval > 0:
                                cor = (
                                 0, min(aval, 255), 0)
                            elif aval < 0:
                                cor = (
                                 min(-aval, 255), 0, 0)
                            else:
                                cor = (0, 0, 0)
                            if accao == maxaccao:
                                seta = True
                            else:
                                seta = False
                    elif ndef:
                        cor = (0, 0, 200)
                        seta = False
                    else:
                        cor = (0, 0, 0)
                        seta = False
                    if type(accao) is int:
                        accao = intdir(accao, ndir)
                    elif isinstance(accao, Accao):
                        accao = accao.ang
                    elif type(accao) is tuple:
                        if accao == pos:
                            self.rect(pos, margem=3, cor=cor)
                            accao = None
                        else:
                            _, accao = difpospol(accao, pos)
                    if accao is not None:
                        self.vector(pos, 1, accao, cor, 3, seta)

        self.marcar(qpos, 1, linha=1)

    def __maxaccao(self, s, q, accoes):
        amax = None
        qmax = float('-inf')
        for a in accoes:
            qa = self._Visualizador__valor(q, (s, a), 0.0)
            if qa > qmax:
                qmax = qa
                amax = a

        return amax

    def __valor(self, q, k, v_ini):
        return q.get(k, v_ini)

    def marcar(self, conjpos, margem=2, cor=(255, 255, 0), linha=0):
        """Marcar posições
        @param conjpos: conjunto de posições
        @param margem: margem em pixeis
        @param cor: cor RGB
        @param linha: espessura de linha (0 - preencher)"""
        for pos in conjpos:
            self.rect(pos, margem, cor, linha)

    def gerados(self, estados):
        """Visualizar nós gerados
        @param estados: dicionário com estados gerados """
        for pos in estados:
            no = estados[pos]
            cor = (0, 100, 255)
            self.rect(pos, 2, cor, 0)

    def abertos(self, abertos):
        """Visualizar nós abertos
        @param abertos: nós abertos"""
        if abertos:
            if isinstance(abertos[0], tuple):
                estados = [no.estado for valor, no in abertos]
            else:
                estados = [no.estado for no in abertos]
            self.marcar(estados, 2, (255, 255, 255), 1)

    def solucao(self, solucao):
        """Visualizar solução
        @param solucao: lista de nós solução da procura"""
        noinicial = solucao[0]
        if len(solucao) > 1 and isinstance(solucao[1].operador, tuple):
            trajecto = [(1, no.operador[1]) for no in solucao[1:]]
        else:
            trajecto = [(1, no.operador.ang) for no in solucao[1:]]
        self.trajecto(noinicial.estado, trajecto)

    def percurso(self, perc):
        """Visualizar percurso
        @param perc: lista de pares (estado, operador)"""
        if perc:
            if isinstance(perc[0], tuple):
                trajecto = [(1, operador.ang) for estado, operador in perc]
                pos_ini = perc[0][0]
            else:
                if perc[0].operador is None:
                    inicio = 1
                else:
                    inicio = 0
                trajecto = [(1, no.operador.ang) for no in perc[inicio:]]
                pos_ini = perc[0].estado
            self.trajecto(pos_ini, trajecto)

    def repamb(self, memrel):
        """Visualizar representação do ambiente
        @param memrel: memória relacional (MemRel) com representação do ambiente"""
        self.limpar()
        self.elementos(memrel.mem)

    def accoesestado(self, s, accoes, q, vnorm=100):
        """Visualizar acções de estado
        @param s: estado
        @param accoes: acções
        @param q: Q(s,a)
        @param param: valor de normalização"""
        raise NotImplementedError

    def pvpix(self, pos_v):
        """ Converter posição virtual em pixeis """
        xv, yv = pos_v
        x = fint(xv * self.escala)
        y = fint(yv * self.escala)
        return (
         x, y)
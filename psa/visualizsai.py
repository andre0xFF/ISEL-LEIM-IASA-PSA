# uncompyle6 version 3.6.6
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\sp1\Documents\proj19\ia1\proj\src\lib_psa\psa\visualizsai.py
# Compiled at: 2019-01-04 20:34:13
# Size of source mod 2**32: 6951 bytes
"""
Visualizador de ambiente sem actualização de imagem (SAI)
@author: Luís Morgado
"""

class VisualizadorSAI:

    def __init__(self):
        """Iniciar visualizador"""
        self.svis = None
        self.escala = 1
        self.corfundo = 0
        self.nivel_detalhe = 1

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
        pass

    def agente(self, pos, ang=None, col=False, carga=False, varang=None):
        """Visualizar agente"""
        pass

    def alvo(self, pos):
        """Visualizar alvo"""
        pass

    def base(self, pos, carga=False):
        """Visualizar base"""
        pass

    def obstaculo(self, pos):
        """Visualizar obstáculo"""
        pass

    def vazio(self, pos):
        """Visualizar vazio"""
        pass

    def rect(self, pos, margem=0, cor=(255, 0, 0), linha=1):
        """Visualizar rectângulo
        @param pos: posição do ambiente
        @param margem: margem em pixeis
        @param cor: cor RGB
        @param linha: espessura de linha (0 - preencher)"""
        pass

    def rectx(self, rect, cor=(255, 0, 0), linha=1):
        """Visualizar rectângulo auxiliar
        @param rect: (x, y, dimx, dimy)
        @param cor: cor RGB
        @param linha: espessura de linha (0 - preencher)"""
        pass

    def circ(self, pos, margem, cor, linha=1, pos_int=False):
        """Visualizar círculo
        @param pos: posição do ambiente
        @param margem: margem em pixeis
        @param cor: cor RGB
        @param linha: espessura de linha (0 - preencher)"""
        pass

    def linha(self, pos_i, pos_f, cor, linha=1, pos_int=False):
        """Visualizar linha"""
        pass

    def vector(self, pos, mod, ang, cor=(255, 255, 255), linha=1, seta=True):
        """Visualizar vector """
        pass

    def elemento(self, pos, obj):
        """Visualizar elemento numa posição"""
        pass

    def elementos(self, poselem):
        """Visualizar elementos num conjunto de posições
        @param poselem: dicionário com associações posição:elemento"""
        pass

    def campo(self, campo, escala=None):
        """Visualizar campo de potencial
        @param campo: dicionário com associações posição:valor
        @param escala: (mínimo, máximo)"""
        pass

    def campoabs(self, campo, escala, normalizar=False):
        """Visualizar campo de potencial
        @param campo: dicionário com associações posição:valor
        @param escala: escala de visualização
        @param normalizar: normalizar valores"""
        pass

    def gradiente(self, grad):
        """Visualizar gradiente descrito por vectores polares
        @param grad: dicionário com associações posição:(módulo, ângulo)"""
        for pos, (mod, ang) in grad.iteritems():
            self.vector(pos, mod, ang, (255, 255, 0))

    def politica(self, pol):
        """Visualizar política
        @param pol: dicionário com associações posição:operador"""
        pass

    def trajecto(self, posini, seqvect):
        """Visualizar sequência de vectores
        @param posini: posição inicial
        @param seqvect: sequência de vectores polares (módulo, ângulo)"""
        pass

    def plano(self, posini, plano):
        """Visualizar trajecto
        @param posini: posição inicial
        @param plano: sequência de operadores com atributo ang"""
        pass

    def accaovalor(self, q, accoes):
        """Visualizar função acção-valor Q(s,a)
        @param q: função acção-valor
        @param accoes: acções definidas"""
        pass

    def aprendref(self, mec_aprend, vnorm=100, vmin=70, campo=False, fval=None, seta_max=True, ndef=False, ndir=8):
        """Visualizar aprendizagem por reforço
                @param mec_aprend: mecanismo de aprendizagem por reforço"""
        pass

    def accaovalordir(self, q, accoes, vnorm=100, vmin=70, campo=False, fval=None, seta_max=True, ndef=False, ndir=8):
        """Visualizar função acção-valor Q(s,a)
        @param q: função acção-valor
        @param accoes: acções definidas"""
        pass

    def marcar(self, conjpos, margem=2, cor=(255, 255, 0), linha=0):
        """Marcar posições
        @param conjpos: conjunto de posições
        @param margem: margem em pixeis
        @param cor: cor RGB
        @param linha: espessura de linha (0 - preencher)"""
        pass

    def gerados(self, estados):
        """Visualizar nós gerados
        @param estados: dicionário com estados gerados """
        pass

    def abertos(self, abertos):
        """Visualizar nós abertos
        @param abertos: nós abertos"""
        pass

    def solucao(self, solucao):
        """Visualizar solução
        @param solucao: lista de nós solução da procura"""
        pass

    def percurso(self, perc):
        """Visualizar percurso
        @param perc: lista de pares (estado, operador)"""
        pass

    def repamb(self, memrel):
        """Visualizar representação do ambiente
        @param memrel: memória relacional (MemRel) com representação do ambiente"""
        pass

    def accoesestado(self, s, accoes, q, vnorm=100):
        """Visualizar acções de estado
        @param s: estado
        @param accoes: acções
        @param q: Q(s,a)
        @param param: valor de normalização"""
        pass

    def vector(self, vpol, cor, linha=1, dir_ref=True):
        """Visualizar vector relativo"""
        pass

    def vectorabs(self, vpol, cor, linha=1):
        """Visualizar vector absoluto"""
        pass

    def pvpix(self, pos_v):
        """ Converter posição virtual em pixeis """
        xv, yv = pos_v
        x = fint(xv * self.escala)
        y = fint(yv * self.escala)
        return (
         x, y)
# uncompyle6 version 3.6.6
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\sp1\Documents\proj19\ia1\proj\src\lib_psa\psa\util.py
# Compiled at: 2019-01-04 19:46:38
# Size of source mod 2**32: 8999 bytes
"""
Funções utilitárias
@author: Luís Morgado
"""
import math, cmath

def argmin(args, func):
    """Determinar argumento que minimiza uma função
        @param args: domínio dos argumentos
        @param func: função
        @return: argumento que minimiza função"""
    return min(map(lambda arg: (func(arg), arg), args))[1]


def argmax(args, func):
    """Determinar argumento que maximiza uma função
        @param args: domínio dos argumentos
        @param func: função
        @return: argumento que maximiza função"""
    return max(map(lambda arg: (func(arg), arg), args))[1]


def fint(val):
    """Conversão de float para int com arredondamento"""
    return int(round(val))


def posint(pos):
    """Posição em valores inteiros"""
    x, y = pos
    return (
     fint(x), fint(y))


def posdisc(pos, detalhe=1):
    """Posição abstracta
        @param detalhe: detalhe de abstracção"""
    x, y = pos
    return (
     valordisc(x, detalhe), valordisc(y, detalhe))


def valordisc(val, detalhe=1):
    """Valor abstracto
        @param detalhe: detalhe de abstracção"""
    return fint(val / detalhe) * detalhe


def incpos(avanco, orient):
    """Gerar incremento de posição (dx,dy)"""
    dx = avanco * math.cos(orient)
    dy = -avanco * math.sin(orient)
    return (
     dx, dy)


def incposint(avanco, orient):
    """Gerar incremento de posição (dx,dy) com valores inteiros"""
    dx, dy = incpos(avanco, orient)
    return (
     fint(dx), fint(dy))


def movpos(pos, dpos):
    """Mover posição com incremento (dx,dy)"""
    x, y = pos
    dx, dy = dpos
    return (
     x + dx, y + dy)


def movpospol(pos, pol):
    """Mover posição com incremento polar (avanco, orient)"""
    x, y = pos
    avanco, orient = pol
    dx, dy = incpos(avanco, orient)
    return (
     x + dx, y + dy)


def mover(pos, ang, dist=1):
    """Mover posição num determinado ângulo e distância"""
    inc_pos = incposint(dist, ang)
    return movpos(pos, inc_pos)


def difpos(pos_a, pos_b):
    """Diferença entre posições"""
    xa, ya = pos_a
    xb, yb = pos_b
    return (
     xa - xb, ya - yb)


def difpospol(posini, posfin, dirbase=0):
    """Diferença entre posições na forma de vector polar
        @param posini: posição inicial
        @param posfin: posição final
        @param dirbase: direcção base de referência
        @return: Vector diferença no formato (módulo, ângulo)"""
    vdif = difpos(posini, posfin)
    mod, ang = cartpol(vdif)
    return (
     mod, ang - dirbase)


def dist(posini, posfin):
    """Distância entre posições"""
    dx, dy = difpos(posini, posfin)
    return math.sqrt(dx ** 2 + dy ** 2)


def interior(pos, rect):
    """Indica se uma posição é interior a uma região definida pela posição inicial 
        e dimensão"""
    x, y = pos
    xini, yini, dimx, dimy = rect
    xmax = xini + dimx
    ymax = yini + dimy
    return x >= xini and x < xmax and y >= yini and y < ymax


def somavect(conjvpol):
    """Soma de um conjunto de vectores polares
        @param conjvpol: conjunto de vectores polares no formato (módulo, ângulo)
        @return: Vector soma no formato (módulo, ângulo)"""
    vsoma = sum([cmath.rect(m, d) for m, d in conjvpol])
    return (
     abs(vsoma), cmath.phase(vsoma))


def cartpol(pos):
    """Converter coordenadas cartesianas em polares"""
    x, y = pos
    return cmath.polar(complex(x, -y))


def posarea(pos):
    """Gerar todas as posições da área que inclui as posições em pos"""
    pos_area = []
    if pos:
        xmin, ymin = min(pos)
        xmax, ymax = max(pos)
        for x in range(xmin, xmax + 1):
            for y in range(ymin, ymax + 1):
                pos_area.append((x, y))

    return pos_area


def magdist(dist, dist_max):
    """Gerar magnitude inversamente proporcional à distância
        @param dist: distância
        @param dist_max: distância máxima
        @return: magnitude"""
    if dist < dist_max:
        mag = (dist_max - dist) / dist_max
    else:
        mag = 0
    return mag


DPI = 2 * math.pi

def normang(ang):
    """ Normalizar ângulo no intervalo [0, 2*pi] """
    if ang >= DPI:
        ang -= DPI
    if ang < 0:
        ang = DPI + ang
    return ang


def normang2(ang):
    """
        Normalizar ângulo no intervalo [-pi, pi]
        """
    ang_norm = normang(ang)
    if ang_norm < math.pi:
        return ang_norm
    return ang_norm - 2 * math.pi


def dirmov(n=8):
    """ Gerar direcções em passos de pi/(n/2) """
    return [idir * DPI / n for idir in range(n)]


def dirdisc(ang, n=8):
    """ Direcção discreta"""
    return normang(fint(n * ang / DPI) * DPI / n)


def dirint(ang, n=8):
    """ Representação da direcção em formato inteiro """
    return int(n * normang(ang) / DPI)


def intdir(ang_int, n=8):
    """ Conversão de direcção em formato inteiro para ângulo"""
    return ang_int * DPI / n


def linhasvect(pos_i, mod, ang, beta, fseta):
    """Gerar linha de um vector"""
    xi, yi = pos_i
    dx, dy = incpos(mod, ang)
    xf = xi + dx
    yf = yi + dy
    gama = ang + math.pi
    gama1 = gama + beta
    gama2 = gama - beta
    nmod = fseta * mod
    dx1, dy1 = incpos(nmod, gama1)
    dx2, dy2 = incpos(nmod, gama2)
    linha1 = ((xi, yi), (xf, yf))
    linha2 = ((xf, yf), (xf + dx1, yf + dy1))
    linha3 = ((xf, yf), (xf + dx2, yf + dy2))
    return [
     linha1, linha2, linha3]


DM = 0.5
DP = 0.5
DC = DP + DM
ANG_POS = dirmov(4)
DOM_POS = {ANG_POS[0]: ((DC, DP), (DC, -DP)), 
 ANG_POS[1]: ((DP, -DC), (-DP, -DC)), 
 ANG_POS[2]: ((-DC, -DP), (-DC, DP)), 
 ANG_POS[3]: ((-DP, DC), (DP, DC))}
DIST_DIR = math.sqrt(2) / 2

def dominio_angular(a):
    """Gerar domínio angular para uma acção sob a forma de ângulo
        @param a: acção (ângulo)
        @return: domínio angular [ang+, ang-]"""
    DANG = math.pi / 8
    return [
     normang2(a + DANG), normang2(a - DANG)]


def ajustar_dominio_angular(ang, dom_ang):
    """Ajustar ângulo a domínio angular
        @param ang: ângulo
        @param dom_ang: domínio angular
        @return: ângulo ajustado"""
    ang_aux = normang2(ang)
    ang_esq = normang2(dom_ang[0])
    ang_dir = normang2(dom_ang[1])
    if ang_aux < ang_esq:
        if ang_aux > ang_dir:
            return ang
    if abs(ang_aux - ang_esq) < abs(ang_aux - ang_dir):
        return dom_ang[0]
    return dom_ang[1]


def ajustar_ang_dom(ang, ang_ref, pos_ref, pos):
    """Ajustar ângulo a domínio
        @param ang: ângulo a ajustar
        @param ang_ref: ângulo de referência (central) do domínio
        @param pos_ref: posição de referência (centro da posição discreta)
        @param pos: posição contínua para ajuste do ângulo
        @return: ângulo ajustado
        """
    if ang_ref in ANG_POS:
        (dxd, dyd), (dxe, dye) = DOM_POS[ang_ref]
        sx, sy = pos_ref
        _, ang_esq = difpospol((sx + dxe, sy + dye), pos)
        _, ang_dir = difpospol((sx + dxd, sy + dyd), pos)
        dom_ang = [ang_esq, ang_dir]
        return ajustar_dominio_angular(ang, dom_ang)
    return ang_ref


def angrelpos(ang, pos_base, pos):
    """Retornar ângulo relativo a posição referente a posição discreta
        @param ang: ângulo em relação a pos_base
        @param pos_base: posição base
        @param pos: posição inicial do ângulo relativo
        @return: ângulo ajustado à posição em função dos limites da posição discreta
        """
    pos_dir = movpospol(pos_base, (DIST_DIR, ang))
    _, ang_dir = difpospol(pos_dir, pos)
    return ang_dir


def restringir_ang(ang, restricoes, pos_abs, pos):
    """Restringir ângulo de acordo com restrições (ângulos de referência)
    @param ang: ângulo a restringir
    @param restricoes: restrições (ângulos de referência)
    @param pos_abs: posição abstracta
    @param pos: posição contínua
    @return: ângulo restricto a ângulo de referência mais próximo"""
    ang_max = None
    corr_max = -float('inf')
    for ang_restr in restricoes:
        correlacao = math.cos(ang - ang_restr)
        if correlacao > corr_max:
            ang_max = ang_restr
            corr_max = correlacao

    if ang_max is not None:
        return angrelpos(ang_max, pos_abs, pos)
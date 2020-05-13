# uncompyle6 version 3.6.6
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\sp1\Documents\proj19\ia1\proj\src\lib_psa\psa\memrel.py
# Compiled at: 2013-11-08 11:07:00
# Size of source mod 2**32: 4201 bytes
"""
Memória relacional 
@author: Luís Morgado
"""

class MemRel:

    def __init__(self, tuplos=[]):
        self.mem = dict(tuplos)

    def __str__(self):
        return str(self.mem)

    def ins(self, chave, valor):
        """Inserir relação (chave, valor)"""
        self.mem[chave] = valor

    def sel(self, criterio=None, valor=True):
        """Obter item por criterio (chave ou valor)
        @param criterio: critério de selecção
        @param valor: selecção por valor Sim/Não"""
        if criterio:
            val_mem = self.mem.get(criterio)
            if val_mem is None and valor:
                tuplos = self.sel_valor(criterio)
                if tuplos:
                    return tuplos[0][0]
            else:
                return val_mem
        else:
            return self.sel_chaves()

    def sel_tuplos(self, criterio=None):
        """Obter as associações por criterio (chave ou valor)"""
        if criterio:
            tuplos_chave = self.sel_chave(criterio)
            tuplos_valor = self.sel_valor(criterio)
            return tuplos_chave + tuplos_valor
        return self.mem.items()

    def sel_chaves(self):
        """Obter todas as chaves"""
        return self.mem.keys()

    def sel_chave(self, chave):
        """Obter as associações que satisfazem uma chave"""
        valor = self.mem.get(chave)
        if valor is None:
            return []
        return [
         (
          chave, valor)]

    def sel_valor(self, valor):
        """Obter as associações que satisfazem um valor"""
        return [(k, v) for k, v in self.mem.iteritems() if v == valor]

    def act(self, chave, valor):
        """Actualizar associação se chave existir. Retorna True/False"""
        if self.mem.get(chave) is not None:
            self.mem[chave] = valor
            return True
        return False

    def act_tuplos(self, tuplos):
        """Actualizar memória com conjunto de tuplos, alterando e eliminado"""
        tuplos_dif = self.dif(tuplos)
        self.mem = dict(tuplos)
        return tuplos_dif

    def rem(self, criterio):
        """Remover associações que satisfazem chave e/ou valor.
        Retorna lista de tuplos removidos"""
        tuplos = self.sel_tuplos(criterio)
        if tuplos:
            for chave, valor in tuplos:
                if self.mem.has_key(chave):
                    del self.mem[chave]

            return tuplos

    def dim(self):
        """Obter número de tuplos em memória"""
        return len(self.mem)

    def dif(self, tuplos):
        """Obter diferença entre tuplos em memória e conjunto de tuplos"""
        return list(set(self.mem.iteritems()) ^ set(tuplos))

    def abstrair(self, resolucao):
        mem_abs = {}
        for x, y in self.mem:
            x_abs = int(x / resolucao)
            y_abs = int(y / resolucao)
            elem_abs = mem_abs.get((x_abs, y_abs))
            if elem_abs != 'obst' and elem_abs != 'alvo':
                mem_abs[(x_abs, y_abs)] = self.mem[(x, y)]

        return MemRel(mem_abs.items())

    def abstrair_info(self, resolucao):
        mem_abs = {}
        for x, y in self.mem:
            x_abs = int(x / resolucao)
            y_abs = int(y / resolucao)
            n_alvo = 0
            n_obst = 0
            elem = self.mem[(x, y)]
            if elem == 'alvo':
                n_alvo = 1
            if elem == 'obst':
                n_obst = 1
            n_alvos, n_obsts = mem_abs.get((x_abs, y_abs), (0, 0))
            n_alvos += n_alvo
            n_obsts += n_obst
            mem_abs[(x_abs, y_abs)] = (n_alvos, n_obsts)

        return mem_abs
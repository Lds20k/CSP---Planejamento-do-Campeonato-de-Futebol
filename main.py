from array import array
from itertools import permutations, product
from random import shuffle
from typing import Counter
from satisfacao_restricoes import Restricao, SatisfacaoRestricoes

# class NaoPodeJogarContraSi(Restricao):
#     def __init__(self, partida):
#         super().__init__([partida])

#     def esta_satisfeita(self, atribuicao: dict):
#         for it in atribuicao:
#             if atribuicao[it][0] == atribuicao[it][1]:
#                 return False
#         return True

# class TodosJogamContraTodos(Restricao):
#     def __init__(self, time, partidas_existentes):
#         super().__init__([time])
#         self.partidas_existentes = partidas_existentes

#     def esta_satisfeita(self, atribuicao: dict):
#         for it in atribuicao:
#             if(atribuicao[it] in self.partidas_existentes):
#                 return False
#         return True

class NaoPodeJogarMaisDeUmaVez(Restricao):
    def __init__(self, time):
        super().__init__([time])

    def esta_satisfeita(self, atribuicao: dict):
        times = []
        for it in list(atribuicao.values()):
            times.extend(list([it[0], it[1]]))

        return len(set(times)) == len(times)

class SoPodeUmClassico(Restricao):
    def __init__(self, time, classicos):
        super().__init__([time])
        self.classicos = classicos

    def esta_satisfeita(self, atribuicao: dict):
        i = 0
        for it in atribuicao.values():
            if(it in self.classicos):
                i += 1
                if i > 1:
                    return False
        return True

class SoPodeJogarUmaPartidaNaCidade(Restricao):
    def __init__(self, partida):
        super().__init__([partida])
        self.partida = partida

    def esta_satisfeita(self, atribuicao: dict):
        cidades = list(atribuicao.values())
        return len(set(cidades)) == len(cidades)

class CidadeDoTimeOuAdversarioOuQualquerOutra(Restricao):
    def __init__(self, partida):
        super().__init__([partida])
        self.partida = partida

    def esta_satisfeita(self, atribuicao: dict):
        if list(atribuicao.values())[-1] != times_cidades[list(atribuicao.keys())[-1][0]]:
            return False

        return True

maiores_times_cidades = {
    "SE Escondidos": "Escondidos",
    "Porto FC": "Porto",
    "SE Leoes": "Leao",
    "Guardioes FC": "Guardiao",
    "Ferroviaria EC": "Porto"
}

times_cidades = {
    "Campos FC": "Campos",
    "Guardioes FC": "Guardiao",
    "CA Protetores": "Guardiao",
    "SE Leoes": "Leao",
    "Simba EC": "Leao",
    "SE Granada": "Granada",
    "CA Lagos": "Lagos",
    "Solaris EC": "Ponte-do-Sol",
    "Porto FC": "Porto",
    "Ferroviaria EC": "Porto",
    "Portuarios AA": "Porto",
    "CA Azedos": "Limoes",
    "SE Escondidos": "Escondidos",
    "Secretos FC": "Escondidos"
}

def gerar_rodada(partidas, classicos):
    qtd_partida = int(len(times_cidades)/2)
    variaveis = list(range(1, qtd_partida+1))

    dominios = {}
    for variavel in variaveis:
        dominios[variavel] = partidas.copy()
    
    problema = SatisfacaoRestricoes(variaveis, dominios)

    for partida in variaveis:
        # Um time não pode jogar contra sí
        #problema.adicionar_restricao(NaoPodeJogarContraSi(partida))

        # Todos os times devem jogar todas as rodadas uns contra os outros em jogos de turno e returno
        #problema.adicionar_restricao(TodosJogamContraTodos(partida, partidas_existentes))

        # Um time não pode jogar mais de uma vez por rodada
        problema.adicionar_restricao(NaoPodeJogarMaisDeUmaVez(partida))

        # Clássicos (qualquer jogos entre os 5 maiores times) não podem acontecer na mesma rodada por competição com a TV
        problema.adicionar_restricao(SoPodeUmClassico(partida, classicos))

        # So pode jogar Uma partida na cidade
        # problema.adicionar_restricao(SoPodeJogarUmaPartidaNaCidade(partida))

    resposta = problema.busca_backtracking()
    if resposta is None:
        print("Nenhuma resposta encontrada")
    return resposta

def associar_cidade(partidas: dict):
    variaveis = partidas.copy().values()

    dominios = {}
    for variavel in variaveis:
        dominios[variavel] = list(set(times_cidades.copy().values()))
    
    problema = SatisfacaoRestricoes(variaveis, dominios)

    for partida in variaveis:
        # So pode jogar Uma partida na cidade
        problema.adicionar_restricao(SoPodeJogarUmaPartidaNaCidade(partida))

        # Cidade do time OU adversario OU qualquer outra
        problema.adicionar_restricao(CidadeDoTimeOuAdversarioOuQualquerOutra(partida))

    resposta = problema.busca_backtracking()
    if resposta is None:
        print("Nenhuma resposta encontrada")
    return resposta

def gerar_partidas(times_cidades: dict):
    partidas = list(permutations(times_cidades.keys(), 2))
    return partidas

if __name__ == "__main__":
    classicos = gerar_partidas(maiores_times_cidades)
    partidas = gerar_partidas(times_cidades)
    rodadas = []

    print("Gerando rodadas...")
    partidas_aux = partidas.copy()
    shuffle(partidas_aux)
    while len(rodadas) < int(len(times_cidades) - 1) * 2:
        rodada = gerar_rodada(partidas_aux, classicos)
        if rodada == None:
            partidas_aux = partidas
            shuffle(partidas_aux)
        else:
            for partida in rodada:
                partidas_aux.remove(rodada[partida])
            rodadas.append(rodada)
    
    rodada_cidade = []
    for i in rodadas:
        rodada = associar_cidade(i)
        rodada_cidade.append(rodada)
    
    print("{")
    for rodada in rodadas:
        print("  [")
        for partida in rodada:
            print(f"    {partida}: {rodada[partida]},")
        print("  ],")
    print("}")
    
    
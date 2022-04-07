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

class NaoUsarRodadaSemResposta(Restricao):
    def __init__(self, time, sem_resposta):
        super().__init__([time])
        self.sem_resposta = sem_resposta

    def esta_satisfeita(self, atribuicao: dict):
        return not Counter(atribuicao) in self.sem_resposta

class SoPodeJogarUmaPartidaNaCidade(Restricao):
    def __init__(self, partida):
        super().__init__([partida])
        self.partida = partida

    def esta_satisfeita(self, atribuicao: dict):
        cidades = []
        for it in list(atribuicao.values()):
            cidades.extend(list([it[2]]))
        
        return len(set(cidades)) == len(cidades)

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

def gerar_rodada(partidas, classicos, sem_resposta: list):
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

        if len(sem_resposta):
            # Não pode usar rodada sem resposta
            problema.adicionar_restricao(NaoUsarRodadaSemResposta(partida, sem_resposta))

        # So pode jogar Uma partida na cidade
        # problema.adicionar_restricao(SoPodeJogarUmaPartidaNaCidade(partida))

    resposta = problema.busca_backtracking()
    if resposta is None:
        print("Nenhuma resposta encontrada")
    else:
        print("Resposta encontrada")
    return resposta

def associar_cidade(partidas):
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
    else:
        print("Resposta encontrada")
    return resposta

def gerar_partidas(times_cidades: dict):
    partidas = list(permutations(times_cidades.keys(), 2))
    # times_partidas_cidades = dict()
    # times_partidas = list(permutations(times_cidades.keys(), 2))
    # for partida in times_partidas:
    #     times_partidas_cidades[partida] = times_cidades[partida[0]]
    #     partidas.append(times_partidas_cidades)
    return partidas

if __name__ == "__main__":
    classicos = gerar_partidas(maiores_times_cidades)
    partidas = gerar_partidas(times_cidades)
    rodadas = []

    print("Gerando rodadas...")
    shuffle(partidas)
    sem_final_definido = []
    while len(rodadas) < int(len(times_cidades) - 1) * 2:
        rodada = gerar_rodada(partidas, classicos, sem_final_definido)
        if rodada == None:
            rodada_removida = rodadas.pop()
            sem_final_definido.append(Counter(rodada_removida))
            for partida in rodada_removida.values():
                partidas.append(partida)
            exit()
        else:
            sem_final_definido.clear()
            for partida in rodada:
                partidas.remove(rodada[partida])
            rodadas.append(rodada)
    
    for i in rodadas:
        rodada = associar_cidade(partidas)
        for partida in rodada:
            partidas.remove(rodada[partida])
        rodadas.append(rodada)
    
    print("{")
    for rodada in rodadas:
        print("  [")
        for partida in rodada:
            print(f"    {partida}: {rodada[partida]},")
        print("  ],")
    print("}")
    
    
from itertools import permutations
from random import shuffle
from satisfacao_restricoes import Restricao, SatisfacaoRestricoes

class NaoPodeJogarMaisDeUmaVez(Restricao):
    def __init__(self, time):
        super().__init__([time])

    def esta_satisfeita(self, atribuicao: dict):
        times = []
        for it in list(atribuicao.values()):
            times.extend(list([it[0], it[1]]))

        return len(set(times)) == len(times)

class NaoPodeJogosNaMesmaCidade(Restricao):
    def __init__(self, time):
        super().__init__([time])

    def esta_satisfeita(self, atribuicao: dict):
        cidade_casa = {}
        for it in list(atribuicao.values()):
            time_1 = it[0]
            cidade_time_1 = times_cidades[time_1]
            if cidade_casa.get(cidade_time_1) != None:
                return False
            cidade_casa[cidade_time_1] = time_1

        return True

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

maiores_times_cidades = {
    "SE Escondidos": "Escondidos",
    "Porto FC": "Porto",
    "SE Leoes": "Leao",
    "Guardioes FC": "Guardiao",
    "Ferroviaria EC": "Campos"
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
    "Ferroviaria EC": "Campos",
    "Portuarios AA": "Porto",
    "CA Azedos": "Limoes",
    "SE Escondidos": "Escondidos",
    "Secretos FC": "Escondidos"
}

def gerar_rodada(partidas, classicos):
    qtd_partida = int(len(times_cidades)/2)
    variaveis = list(range(1, qtd_partida + 1))

    dominios = {}
    for variavel in variaveis:
        dominios[variavel] = partidas.copy()
    
    problema = SatisfacaoRestricoes(variaveis, dominios)

    for partida in variaveis:
        # Um time não pode jogar mais de uma vez por rodada
        problema.adicionar_restricao(NaoPodeJogarMaisDeUmaVez(partida))

        # Clássicos (qualquer jogos entre os 5 maiores times) não podem acontecer na mesma rodada por competição com a TV
        problema.adicionar_restricao(SoPodeUmClassico(partida, classicos))

        # nao poderá ter duas partidas com time 1 na mesma cidade na mesma rodada
        problema.adicionar_restricao(NaoPodeJogosNaMesmaCidade(partida))

    resposta = problema.busca_backtracking()
    # if resposta is None:
        # print("Nenhuma resposta encontrada")
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
    
    print()
    i = 1
    for rodada in rodadas:
        print(f"  Rodada {i}")
        for partida in rodada:
            print(f"    {partida} - {rodada[partida][0]} X {rodada[partida][1]} - {times_cidades[rodada[partida][0]]}")
        print()
        i += 1
    print()
    
    
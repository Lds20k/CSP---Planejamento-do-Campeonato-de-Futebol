from array import array
from itertools import product
from random import shuffle
from satisfacao_restricoes import Restricao, SatisfacaoRestricoes

class NaoPodeJogarContraSi(Restricao):
    def __init__(self, partida):
        super().__init__([partida])

    def esta_satisfeita(self, atribuicao: dict):
        for it in atribuicao:
            if atribuicao[it][0] == atribuicao[it][1]:
                return False
        return True

class NaoPodeJogarMaisDeUmaVez(Restricao):
    def __init__(self, time):
        super().__init__([time])

    def esta_satisfeita(self, atribuicao: dict):
        times = []
        for it in list(atribuicao.values()):
            times.extend(list(it))
        
        return len(set(times)) == len(times)

class TodosJogamContraTodos(Restricao):
    def __init__(self, time, partidas_existentes):
        super().__init__([time])
        self.partidas_existentes = partidas_existentes

    def esta_satisfeita(self, atribuicao: dict):
        for it in atribuicao:
            if(atribuicao[it] in self.partidas_existentes):
                return False
        return True

class SoPodeUmClassico(Restricao):
    def __init__(self, time, classicos):
        super().__init__([time])
        self.classicos = classicos

    def esta_satisfeita(self, atribuicao: dict):
        i = 0
        for it in atribuicao:
            if(atribuicao[it] in self.classicos):
                i += 1
                if i > 1:
                    return False
        return True

class SoPodeJogarUmaPartidaNaCidade(Restricao):
    def __init__(self, partida):
        super().__init__([partida])
        self.partida = partida

    def esta_satisfeita(self, atribuicao: dict):
        return len(set(atribuicao.values())) == len(atribuicao.values())

maiores_time = [
    "SE Escondidos",
    "Porto FC",
    "SE Leões",
    "Guardiões FC",
    "Ferroviária EC"
]

times = [
    "Campos FC",
    "Guardioes FC",
    "CA Protetores",
    "SE Leoes",
    "Simba EC",
    "SE Granada",
    "CA Lagos",
    "Solaris EC",
    "Porto FC",
    "Ferroviaria EC",
    "Portuarios AA",
    "CA Azedos",
    "SE Escondidos",
    "Secretos FC"
]

time_cidade = {
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

def gerar_classicos():
    classicos = []
    for time in maiores_time:
        m_time = maiores_time.copy()
        m_time.remove(time)

        partida = list(product(*[[time], m_time]))
        classicos = classicos + partida

    return classicos


# def gerar_partida(times, classicos, partidas_existentes):
#     qtd_partida = int(len(times)/2)
#     variaveis = times[:qtd_partida].copy()

#     dominios = {}
#     for variavel in variaveis:
#         dominios[variavel] = times.copy()
    
#     problema = SatisfacaoRestricoes(variaveis, dominios)

#     for time in variaveis:
#         # Um time não pode jogar contra sí
#         problema.adicionar_restricao(NaoPodeJogarContraSi(time))

#         # Todos os times devem jogar todas as rodadas uns contra os outros em jogos de turno e returno
#         problema.adicionar_restricao(TodosJogamContraTodos(time, partidas_existentes))

#         # Um time não pode jogar mais de uma vez por rodada
#         problema.adicionar_restricao(NaoPodeJogarMaisDeUmaVez(time))

#         # Clássicos (qualquer jogos entre os 5 maiores times) não podem acontecer na mesma rodada por competição com a TV
#         problema.adicionar_restricao(SoPodeUmClassico(time, classicos))

#     resposta = problema.busca_backtracking()
#     if resposta is None:
#         print("Nenhuma resposta encontrada")
#     return resposta

def gerar_rodada(partidas, classicos):
    qtd_partida = int(len(times)/2)
    variaveis = list(range(1, qtd_partida+1))

    dominios = {}
    for variavel in variaveis:
        dominios[variavel] = partidas.copy()
    
    problema = SatisfacaoRestricoes(variaveis, dominios)

    for partida in variaveis:
        # Um time não pode jogar contra sí
        problema.adicionar_restricao(NaoPodeJogarContraSi(partida))

        # Todos os times devem jogar todas as rodadas uns contra os outros em jogos de turno e returno
        #problema.adicionar_restricao(TodosJogamContraTodos(partida, partidas_existentes))

        # Um time não pode jogar mais de uma vez por rodada
        problema.adicionar_restricao(NaoPodeJogarMaisDeUmaVez(partida))

        # Clássicos (qualquer jogos entre os 5 maiores times) não podem acontecer na mesma rodada por competição com a TV
        problema.adicionar_restricao(SoPodeUmClassico(partida, classicos))

    resposta = problema.busca_backtracking()
    if resposta is None:
        print("Nenhuma resposta encontrada")
    return resposta
    
if __name__ == "__main__":
    classicos = gerar_classicos()
    rodadas = []
    partidas_existentes = []

    # partidas = []
    # for time in time_cidade:
    #     partidas = partidas + list(tuple(product([time], times)))
    
    todas_partidas = []
    for time in time_cidade:
        partidas = list(tuple(product([time], times)))
        partida_cidade = []
        for partida in partidas:
            partida_temp = tuple(list(list(partida) + [time_cidade[time]]))
            partida_cidade.extend([partida_temp])
        todas_partidas = partida_cidade + todas_partidas

    print("Gerando rodadas...")
    #shuffle(todas_partidas)    
    for i in range(int(len(times)-1)*2):
        rodada = gerar_rodada(todas_partidas, classicos)
        for partida in rodada:
            todas_partidas.remove(rodada[partida])
        rodadas.append(rodada)
    
    print("{")
    for rodada in rodadas:
        print("  [")
        for partida in rodada:
            print(f"    {partida}: {rodada[partida]},")
        print("  ],")
    print("}")
    #partidas_cidades = gerar_partidas_em_cidades(partidas)
    
    
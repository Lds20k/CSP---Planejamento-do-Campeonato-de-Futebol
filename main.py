from array import array
from itertools import product
from random import shuffle
from satisfacao_restricoes import Restricao, SatisfacaoRestricoes

class NaoPodeJogarContraSi(Restricao):
    def __init__(self, time):
        super().__init__([time])
        self.time = time

    def esta_satisfeita(self, atribuicao: dict):
        if self.time in atribuicao:
            return self.time != atribuicao[self.time]
        return True

class NaoPodeJogarMaisDeUmaVez(Restricao):
    def __init__(self, time):
        super().__init__([time])

    def esta_satisfeita(self, atribuicao: dict):            
        return len(atribuicao.values()) == len(set(atribuicao.values()))

class SoPodeUmClassico(Restricao):
    def __init__(self, time, classicos):
        super().__init__([time])
        self.classicos = classicos

    def esta_satisfeita(self, atribuicao: dict):
        i = 0
        for it in atribuicao:
            if(tuple([it, atribuicao[it]]) in self.classicos):
                i += 1
                if i > 1:
                    return False
        return True

class Jogos(Restricao):
    def __init__(self, time, classicos):
        super().__init__([time])
        self.classicos = classicos

    def esta_satisfeita(self, atribuicao: dict):
        i = 0
        for it in atribuicao:
            if(tuple([it, atribuicao[it]]) in self.classicos):
                i += 1
                if i > 1:
                    return False
        return True

maiores_time = [
    "SE Escondidos",
    "Porto FC",
    "SE Leões",
    "Guardiões FC",
    "Ferroviária EC"
]

times = [
    "Campos FC",
    "Guardiões FC",
    "CA Protetores",
    "SE Leões",
    "Simba EC",
    "SE Granada",
    "CA Lagos",
    "Solaris EC",
    "Porto FC",
    "Ferroviária EC",
    "Portuários AA",
    "CA Azedos",
    "SE Escondidos",
    "Secretos FC"
]

cidades = [
    "Campos",
    "Guardião",
    "Leão",
    "Granada",
    "Lagos",
    "Ponte-do-Sol",
    "Porto",
    "Limões",
    "Escondidos"
]

def gerar_classicos():
    classicos = []
    for time in maiores_time:
        m_time = maiores_time.copy()
        m_time.remove(time)

        partida = list(product(*[[time], m_time]))
        classicos = classicos + partida

    return classicos


def gerar_partidas(classicos):
    # Todos os times devem jogar todas as rodadas uns contra os outros em jogos de turno e returno
    times_div = times.copy()
    shuffle(times_div)
    variaveis = times_div[:int(len(times_div)/2)].copy()

    dominios = {}
    for variavel in variaveis:
        dominios[variavel] = times_div[int(len(times_div)/2):].copy()
    
    problema = SatisfacaoRestricoes(variaveis, dominios)

    for time in variaveis:
        # Um time não pode jogar contra sí
        problema.adicionar_restricao(NaoPodeJogarContraSi(time))

        # Um time não pode jogar mais de uma vez por rodada
        problema.adicionar_restricao(NaoPodeJogarMaisDeUmaVez(time))

        # Clássicos (qualquer jogos entre os 5 maiores times) não podem acontecer na mesma rodada por competição com a TV
        problema.adicionar_restricao(SoPodeUmClassico(time, classicos))

    resposta = problema.busca_backtracking()
    if resposta is None:
        print("Nenhuma resposta encontrada")
        return gerar_partidas()
    else:
        print(resposta)
    
    return resposta

def gerar_partidas_em_cidades(partidas: array):
    cidades_div = times.copy()
    shuffle(cidades_div)
    qtd_cidades = int(len(cidades_div) - (len(times)/2 - len(cidades_div)))
    variaveis = cidades_div[:qtd_cidades].copy()

    dominios = {}
    for variavel in variaveis:
        dominios[variavel] = partidas
    
if __name__ == "__main__":
    classicos = gerar_classicos()
    partidas = []
    for i in range(10):
        partidas.append(gerar_partidas(classicos))
    partidas_cidades = gerar_partidas_em_cidades(partidas)
    
    
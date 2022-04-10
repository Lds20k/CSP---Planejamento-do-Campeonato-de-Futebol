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
    
class UmJogoPorRodada(Restricao):
    def __init__(self, partidasTime, rodada):
        super().__init__(partidasTime)
        self.partidasTime = partidasTime
        self.rodada = rodada

    def esta_satisfeita(self, atribuicao: dict):
        for partida in self.partidasTime:
            if partida in atribuicao and atribuicao[partida] == self.rodada:
                return False 
        return True

class NaoPodeNaMesmaRodada(Restricao):
    def __init__(self, partida1, partida2):
        super().__init__([partida1, partida2])
        self.partida1 = partida1
        self.partida2 = partida2

    def esta_satisfeita(self, atribuicao: dict):
        if self.partida1 in atribuicao and self.partida2 in atribuicao:
            return atribuicao[self.partida1] != atribuicao[self.partida2]
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

time_cidade = {
    "Campos FC" : "Campos", 
    "Guardiões FC" : "Guardião",
    "CA Protetores" : "Guardião",
    "SE Leões" : "Leão",
    "Simba EC" : "Leão",
    "SE Granada" : "Granada",
    "CA Lagos" : "Lagos",
    "Solaris EC" : "Ponte-do-Sol",
    "Porto FC" : "Porto",
    "Ferroviária EC" : "Campos",
    "Portuários AA" : "Porto",
    "CA Azedos" : "Limões",
    "SE Escondidos" : "Escondidos",
    "Secretos FC" : "Escondidos"
}


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

def gerar_partidas_possiveis():
    partidas = []
    for time1 in times:
        for time2 in times:
            if time1 != time2:
                cidade_time_casa = time_cidade[time1]
                tupla_partidas = tuple((time1, time2, cidade_time_casa))
                partidas.append(tupla_partidas)
    return partidas

def nao_pode_na_mesma_rodada(partida1, partida2, listaPartidasRestricoes):
    TIME_1 = 0
    TIME_2 = 1
    CIDADE = 2

    # if (partida1[TIME_1] == partida2[TIME_1] or partida1[TIME_1] == partida2[TIME_2] or partida1[TIME_2] == partida2[TIME_2]):
    #     return True
    
    # if (partida1[CIDADE] == partida2[CIDADE]):
    #     return True

    # if (partida1[TIME_1] in maiores_time and partida1[TIME_2] in maiores_time and partida2[TIME_1] in maiores_time and partida2[TIME_2] in maiores_time):
    #         return True

    return False

if __name__ == "__main__":
    qntdJogosUmaRodadas = (int)(len(times) / 2)
    qntdRodadasCmapeonato = (int)( ( (len(times) - 1) * len(times) ) / qntdJogosUmaRodadas )
    variaveis = gerar_partidas_possiveis()
    rodadas = []
    
    for i in range(1, (qntdRodadasCmapeonato + 1)):
        rodadas.append(i)
    
    dominios = {}

    for variavel in variaveis:
        dominios[variavel] = rodadas.copy()

    problema = SatisfacaoRestricoes(variaveis, dominios, True)
    
    contN = 0
    contF = 0
    listaPartidasRestricoes = []
    # Todos os times devem jogar todas as rodadas uns contra os outros em jogos de turno e returno
    for variavel1 in variaveis:
        for variavel2 in variaveis:
            CONJUNTO_PARTIDA = tuple((variavel1, variavel2))
            if variavel1 != variavel2 and CONJUNTO_PARTIDA not in listaPartidasRestricoes and nao_pode_na_mesma_rodada(variavel1, variavel2, listaPartidasRestricoes):
                contF += 1
                listaPartidasRestricoes.append(tuple((variavel2, variavel1)))
                problema.adicionar_restricao(NaoPodeNaMesmaRodada(variavel1, variavel2))
            else:
                contN += 1      
    print(contN)
    print(contF)
    print(contF + contN)

    resposta = problema.busca_backtracking()
    if resposta is None:
        print("Nenhuma resposta encontrada")
    else:
        faltam_partidas = False
        tabela = []
        for i in range(qntdRodadasCmapeonato):
            tabela.append("Rodada " + (str)(i + 1))
        for partida in variaveis:
            if partida in resposta:
                rodada = resposta[partida]
                tabela[rodada - 1] +=  '\n' + (str)(partida[0]) + " x " + (str)(partida[1]) + ' - ' + (str)(partida[2])
            else:
                faltam_partidas = True
        for rodada in tabela:
            print(rodada + '\n\n')
        if faltam_partidas:
            print("Faltam partidas")
    
    
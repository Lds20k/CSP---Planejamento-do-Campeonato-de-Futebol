from satisfacao_restricoes import Restricao, RestricaoDominio, SatisfacaoRestricoes
from random import shuffle

equipes = {
  "Campos FC": {"cidade": "Campos", "torcedores": 23},
  "Guardiões FC": {"cidade": "Guardião", "torcedores": 40},
  "CA Protetores": {"cidade": "Guardião", "torcedores": 20},
  "SE Leões": {"cidade": "Leão", "torcedores": 40},
  "Simba FC": {"cidade": "Leão", "torcedores": 15},
  "SE Granada": {"cidade": "Granada", "torcedores": 10},
  "CA Lagos": {"cidade": "Lagos", "torcedores": 20},
  "Solaris RC": {"cidade": "Ponte-do-Sol", "torcedores": 30},
  "Porto EC": {"cidade": "Porto", "torcedores": 45},
  "Ferroviária EC": {"cidade": "Campos", "torcedores": 38},
  "Portuários AA": {"cidade": "Porto", "torcedores": 12},
  "CA Azedos": {"cidade": "Limões", "torcedores": 18},
  "SE Escondidos": {"cidade": "Escondidos", "torcedores": 50},
  "Secretos FC": {"cidade": "Escondidos", "torcedores": 25},
}

RODADAS = (len(equipes)-1) * 2
JOGOS = int(len(equipes)/2)

# gera combinação de todos os jogos
combinacao_de_todos_jogos = tuple((l1, l2) for l2 in equipes.keys() for l1 in equipes.keys())

# remove jogos com o mesmo time
combinacao_de_todos_jogos = list(filter(lambda x: (x[0] != x[1]), combinacao_de_todos_jogos))

# Dica 1: Fazer Restrições Genéricas
class NaoPodePatidaMesmaCidadeNaRodada(Restricao):
  def __init__(self, jogos_rodada):
    super().__init__(jogos_rodada)
    self.jogos_rodada = jogos_rodada

  # atribuicao = {"variavel1": "valor1", "variavel2": "valor2", ...}
  def esta_satisfeita(self, atribuicao):
    cidades = []
    for jogo in self.jogos_rodada:
        if jogo in atribuicao:
            if equipes[atribuicao[jogo][0]]["cidade"] in cidades:
                return False
            cidades.append(equipes[atribuicao[jogo][0]]["cidade"])
    return True

class TemQueTerCidadeNaRodada(Restricao):
  def __init__(self, jogo, cidade):
    super().__init__(jogo)
    self.jogo = jogo
    self.cidade = cidade

  # atribuicao = {"variavel1": "valor1", "variavel2": "valor2", ...}
  def esta_satisfeita(self, atribuicao):
    if jogo in atribuicao and equipes[atribuicao[jogo][0]]["cidade"] == self.cidade:
        return True
    return False

class RestringeDominiosCidade(RestricaoDominio):
    def __init__(self, variaveis):
        super().__init__()
        self.variaveis = variaveis
    def reduzir_dominio(self, dominios, atribuicao, valores_atribuidos):
      for key in variaveis:
        if key in atribuicao:
          for valor_atribuido in valores_atribuidos:
            dominio_filtrado = list(filter(lambda x: (equipes[x[0]]["cidade"] != equipes[valor_atribuido[0]]["cidade"]), dominios[key]))
            dominios[key] = dominio_filtrado
      return dominios

class RestringeDominiosMesmoTime(RestricaoDominio):
    def __init__(self, variaveis):
        super().__init__()
        self.variaveis = variaveis
    def reduzir_dominio(self, dominios, atribuicao, valores_atribuidos):
      for key in variaveis:
        if key in atribuicao:
          for valor_atribuido in valores_atribuidos:
            dominio_filtrado = list(filter(lambda x: ( x[0] != valor_atribuido[0] and x[0] != valor_atribuido[1] and x[1] != valor_atribuido[0] and x[1] != valor_atribuido[1]), dominios[key]))
            dominios[key] = dominio_filtrado
      return dominios      

def gerar_maiores_times(qntd_maiores_times):
    times_ordenados = list({k: v for k, v in sorted(equipes.items(), key=lambda item: item[1]["torcedores"], reverse=True)}.keys())
    maiores_times = [ times_ordenados[i] for i in range(qntd_maiores_times) ]
    return maiores_times

def gerar_dominio_com_classicos(qntd_maiores_times):
    maiores_times = gerar_maiores_times(qntd_maiores_times)
    dominio_maiores_times = list(filter(lambda x: (x[0] in maiores_times and x[1] in maiores_times), combinacao_de_todos_jogos))
    shuffle(dominio_maiores_times)
    return dominio_maiores_times

def gerar_dominio_sem_classico(dominio_com_classicos):
    dominio_sem_classicos = list(filter(lambda x: (x not in dominio_com_classicos), combinacao_de_todos_jogos))
    shuffle(dominio_sem_classicos)
    return dominio_sem_classicos

if __name__ == "__main__":
    variaveis = []
    dominios = {}
    dominio_com_classicos = gerar_dominio_com_classicos(5)
    dominio_sem_classicos = gerar_dominio_sem_classico(dominio_com_classicos)

    for i in range(RODADAS): # rodadas
      for j in range(JOGOS): # jogos
        # Variável RnJm, tal que n é o número da rodada e m é o jogo da rodada
        variavel = "R" + str(i) + "J" + str(j)
        variaveis.append(variavel)
        # primeiro jogo da rodada sera um classico (ate quando houver partidas de classico)
        if i < len(dominio_com_classicos) and j == 0:
            dominios[variavel] = dominio_com_classicos    
        else:
            dominios[variavel] = dominio_sem_classicos

  
    # for variavel in variaveis:
        # o domínio são as combinações de todos os possívels jogos
    
    problema = SatisfacaoRestricoes(variaveis, dominios)
    rodadas = []
    for i in range(RODADAS): # rodadas
        jogos_rodada = []
        for j in range(JOGOS): # jogos
            jogos_rodada.append("R" + str(i) + "J" + str(j))
        rodadas.append(jogos_rodada)
    


    for jogos_rodada in rodadas:
        problema.adicionar_restricao_dominio(RestringeDominiosMesmoTime(jogos_rodada))
        problema.adicionar_restricao_dominio(RestringeDominiosCidade(jogos_rodada))
    
    resposta = problema.busca_backtracking()
    if resposta is None:
      print("Nenhuma resposta encontrada")
    else:
      for i in range(RODADAS): # rodadas
        print("\n---------- Rodada " + str(i+1) + " ----------\n")
        for j in range(JOGOS): # jogos
          jogo = resposta["R" + str(i) + "J" + str(j)]
          print("Jogo " + str(j+1) + ": " + jogo[0] + " x " + jogo[1] + "\tCidade: " + equipes[jogo[0]]["cidade"])
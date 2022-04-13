from satisfacao_restricoes import Restricao, RestricaoDominio, SatisfacaoRestricoes
from random import shuffle
# se escondidos 50
# porto 45
# leoes 40
# guardioes 40
# ferroviaria 38
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

TURNOS = 2
RODADAS = (len(equipes)-1) * TURNOS
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
    def reduzir_dominio(self, dominios, atribuicao):
        ultima_atribuida = list(atribuicao.keys())[-1]
        if ultima_atribuida not in self.variaveis:
            return dominios

        cidades_atribuidas = []
        for key in self.variaveis:
            if atribuicao.get(key) != None:
                partida = atribuicao[key]
                if equipes[partida[0]]["cidade"] not in cidades_atribuidas:
                    cidades_atribuidas.append(equipes[partida[0]]["cidade"])
                for key in self.variaveis:
                    dominio_filtrado = list(filter(lambda partida: (equipes[partida[0]]["cidade"] not in cidades_atribuidas), dominios[key]))
                    dominios[key] = dominio_filtrado
        return dominios

class RestringeDominiosMesmoTime(RestricaoDominio):
    def __init__(self, variaveis):
        super().__init__()
        self.variaveis = variaveis
    def reduzir_dominio(self, dominios, atribuicao):
        ultima_atribuida = list(atribuicao.keys())[-1]
        if ultima_atribuida not in self.variaveis:
            return dominios
        
        times_atribuidos = []
        for key in self.variaveis:
            if atribuicao.get(key) != None:
                partida = atribuicao[key]
                if partida[0] not in times_atribuidos:
                    times_atribuidos.append(partida[0])
                if partida[1] not in times_atribuidos:
                    times_atribuidos.append(partida[1])
                for key in self.variaveis:
                    dominio_filtrado = list(filter(lambda partida: (partida[0] not in times_atribuidos and partida[1] not in times_atribuidos), dominios[key]))
                    dominios[key] = dominio_filtrado
        return dominios     

def gerar_maiores_times(qntd_maiores_times):
    times_ordenados = list({k: v for k, v in sorted(equipes.items(), key=lambda item: item[1]["torcedores"], reverse=True)}.keys())
    maiores_times = times_ordenados[0:qntd_maiores_times]
    return maiores_times

def gerar_jogos_classicos(qntd_maiores_times):
    maiores_times = gerar_maiores_times(qntd_maiores_times)
    dominio_maiores_times = list(filter(lambda x: (x[0] in maiores_times and x[1] in maiores_times), combinacao_de_todos_jogos))
    shuffle(dominio_maiores_times)
    return dominio_maiores_times

# gera dominio de cidades que obrigatoriamente aparecerao em todas rodadas
def gerar_jogos_separados_cidades_exclusivas():
  
  cidades_ocorrencias = {}
  for caracteristica in equipes.values():
    cidade = caracteristica["cidade"]
    if cidades_ocorrencias.get(cidade) != None:
      cidades_ocorrencias[cidade] += 1
    else:
      cidades_ocorrencias[cidade] = 1
  
  cidades_restricao_rodadas = []
  for cidade, ocorrencias in cidades_ocorrencias.items():
    if ocorrencias > 2:
      print("Não é possível respeitar a condição de uma unica cidade na rodada")
      return None
    if ocorrencias == 2:
      cidades_restricao_rodadas.append(cidade)
  shuffle(cidades_restricao_rodadas)
  
  jogos_sem_restricao_cidade_todas_rodadas = []
  cidade_jogos = {}
  for jogo in combinacao_de_todos_jogos:
    cidade = equipes[jogo[0]]["cidade"]
    if cidade in cidades_restricao_rodadas:
      if cidade_jogos.get(cidade) != None:
        cidade_jogos[cidade].append(jogo)
      else:
        cidade_jogos[cidade] = [jogo]
    else:
      jogos_sem_restricao_cidade_todas_rodadas.append(jogo)

  return jogos_sem_restricao_cidade_todas_rodadas, list(cidade_jogos.values())

def definir_prioridade(jogos, prioridade):
  times_ordenados_por_prioridade = list(sorted(jogos, key=lambda jogo: jogo in prioridade, reverse=True))
  return times_ordenados_por_prioridade
  
if __name__ == "__main__":
    variaveis = []
    dominios = {}
    jogos_classicos = gerar_jogos_classicos(5)
    jogos_sem_restricao_cidade_todas_rodadas, jogos_restricao_cidade_todas_rodadas = gerar_jogos_separados_cidades_exclusivas()

    qntd_restricoes_cidades = len(jogos_restricao_cidade_todas_rodadas)

    for i in range(RODADAS): # rodadas
      for j in range(JOGOS): # jogos
        # Variável RnJm, tal que n é o número da rodada e m é o jogo da rodada
        variavel = "R" + str(i) + "J" + str(j)
        variaveis.append(variavel)
        if j < qntd_restricoes_cidades:
          shuffle(jogos_restricao_cidade_todas_rodadas[j])
          definir_prioridade(jogos_restricao_cidade_todas_rodadas[j], jogos_classicos)
          dominios[variavel] = jogos_restricao_cidade_todas_rodadas[j]
        else:
          shuffle(jogos_sem_restricao_cidade_todas_rodadas)
          definir_prioridade(jogos_sem_restricao_cidade_todas_rodadas, jogos_classicos)
          dominios[variavel] = jogos_sem_restricao_cidade_todas_rodadas

    
    problema = SatisfacaoRestricoes(variaveis, dominios)
    rodadas = []
    for i in range(RODADAS): # rodadas
        jogos_rodada = []
        for j in range(JOGOS): # jogos
            jogos_rodada.append("R" + str(i) + "J" + str(j))
        rodadas.append(jogos_rodada)
    

    # problema.adicionar_restricao_dominio(RestringeDominiosMesmoTime(""))

    # for jogos_rodada in rodadas:
        # problema.adicionar_restricao_dominio(RestringeDominiosMesmoTime(jogos_rodada))
        # problema.adicionar_restricao_dominio(RestringeDominiosCidade(jogos_rodada))
    
    resposta = problema.busca_backtracking()
    if resposta is None:
      print("Nenhuma resposta encontrada")
    else:
      for i in range(RODADAS): # rodadas
        print("\n---------- Rodada " + str(i+1) + " ----------\n")
        for j in range(JOGOS): # jogos
          jogo = resposta["R" + str(i) + "J" + str(j)]
          print("Jogo " + str(j+1) + ": " + jogo[0] + " x " + jogo[1] + "\tCidade: " + equipes[jogo[0]]["cidade"])
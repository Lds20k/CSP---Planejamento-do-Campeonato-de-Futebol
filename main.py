from satisfacao_restricoes import FiltroDominio, Restricao, SatisfacaoRestricoes
from random import seed, shuffle
import re
import time
from itertools import cycle

# maiores times
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
USAR_ULTIMA_SEED = False

# gera combinação de todos os jogos
combinacao_de_todos_jogos = tuple((l1, l2) for l2 in equipes.keys() for l1 in equipes.keys())

# remove jogos com o mesmo time
combinacao_de_todos_jogos = list(filter(lambda x: (x[0] != x[1]), combinacao_de_todos_jogos))
class NaoPodePatidaMesmaCidadeNaRodada(Restricao):
  def __init__(self, variaveis, qntd_restricoes_cidades):
    super().__init__(variaveis)
    self.qntd_restricoes_cidades = qntd_restricoes_cidades

  # atribuicao = {"variavel1": "valor1", "variavel2": "valor2", ...}
  def esta_satisfeita(self, atribuicao):
    ultimo_variavel_atribuido = list(atribuicao)[-1]
    ultima_partida_atribuida =  atribuicao[ultimo_variavel_atribuido]
    numeros_variavel = re.findall('\d\d?', ultimo_variavel_atribuido)
    rodada = int(numeros_variavel[0])
    num_jogo = int(numeros_variavel[1])
    cidades = []
    for jogo in range(JOGOS):
      variavel = 'R' + str(rodada) + 'J' + str(jogo)
      if atribuicao.get(variavel) != None:
        time1 = atribuicao[variavel][0]
        if equipes[time1]["cidade"] not in cidades:
          cidades.append(equipes[time1]["cidade"])
        else:
          return False
    return True
class NaoPodeTimeNaMesmaRodada(Restricao):
  def __init__(self, variaveis):
    super().__init__(variaveis)

  # atribuicao = {"variavel1": "valor1", "variavel2": "valor2", ...}
  def esta_satisfeita(self, atribuicao):
    ultimo_variavel_atribuido = list(atribuicao)[-1]
    ultima_partida_atribuida =  atribuicao[ultimo_variavel_atribuido]
    numeros_variavel = re.findall('\d\d?', ultimo_variavel_atribuido)
    rodada = int(numeros_variavel[0])
    num_jogo = int(numeros_variavel[1])
    times = []
    for jogo in range(JOGOS):
      variavel = 'R' + str(rodada) + 'J' + str(jogo)
      if atribuicao.get(variavel) != None:
        if atribuicao[variavel][0] not in times and atribuicao[variavel][1] not in times:
          time1= atribuicao[variavel][0]
          times.append(time1)
          time2= atribuicao[variavel][1]
          times.append(time2)
        else:
          return False
    return True

class NaoPodeClassicoNaMesmaRodada(Restricao):
  def __init__(self, variaveis, classicos):
    super().__init__(variaveis)
    self.classicos = classicos
  # atribuicao = {"variavel1": "valor1", "variavel2": "valor2", ...}
  def esta_satisfeita(self, atribuicao):
    ultimo_variavel_atribuido = list(atribuicao)[-1]
    ultima_partida_atribuida =  atribuicao[ultimo_variavel_atribuido]
    numeros_variavel = re.findall('\d\d?', ultimo_variavel_atribuido)
    rodada = int(numeros_variavel[0])
    num_jogo = int(numeros_variavel[1])
    tem_classico = False
    for jogo in range(JOGOS):
      variavel = 'R' + str(rodada) + 'J' + str(jogo)
      if atribuicao.get(variavel) != None:
        if atribuicao[variavel] in self.classicos and tem_classico == False:
          tem_classico = True
        elif atribuicao[variavel] in self.classicos:
          return False
    return True

class RestringeDominiosClassicos(FiltroDominio):
    def __init__(self, classicos):
        super().__init__()
        self.qntd_restricoes_cidades = qntd_restricoes_cidades
    def reduzir_dominio(self, dominios, atribuicao):

      ultimo_variavel_atribuido = list(atribuicao)[-1]
      ultima_partida_atribuida =  atribuicao[ultimo_variavel_atribuido]
      numeros_variavel = re.findall('\d\d?', ultimo_variavel_atribuido)
      rodada = int(numeros_variavel[0])
      num_jogo = int(numeros_variavel[1])
      
      tem_classico = False
      variaveis_nao_atribuidas = []
      for jogo in range(JOGOS):
        variavel = 'R' + str(rodada) + 'J' + str(jogo)
        if atribuicao.get(variavel) != None:
          if atribuicao[variavel] in jogos_classicos:
            if tem_classico == False:
              tem_classico = True
        else:
          variaveis_nao_atribuidas.append(variavel)
      for variavel in variaveis_nao_atribuidas:
        if tem_classico:
          dominio_filtrado = list(filter(lambda x: (x not in jogos_classicos), dominios[variavel]))
          dominios[variavel] = dominio_filtrado
      return dominios
class RestringeDominiosCidade(FiltroDominio):
    def __init__(self, qntd_restricoes_cidades):
        super().__init__()
        self.qntd_restricoes_cidades = qntd_restricoes_cidades
    def reduzir_dominio(self, dominios, atribuicao):
      ultimo_variavel_atribuido = list(atribuicao)[-1]
      ultima_partida_atribuida =  atribuicao[ultimo_variavel_atribuido]
      numeros_variavel = re.findall('\d\d?', ultimo_variavel_atribuido)
      rodada = int(numeros_variavel[0])
      num_jogo = int(numeros_variavel[1])

      if num_jogo < self.qntd_restricoes_cidades:
        return dominios

      cidades = []
      variaveis_nao_atribuidas = []
      for jogo in range(JOGOS):
        variavel = 'R' + str(rodada) + 'J' + str(jogo)
        if atribuicao.get(variavel) != None:
          time1= atribuicao[variavel][0]
          cidades.append(equipes[time1]["cidade"])
        else:
          variaveis_nao_atribuidas.append(variavel)
      for variavel in variaveis_nao_atribuidas:
        dominio_filtrado = list(filter(lambda x: (x not in cidades), dominios[variavel]))
        dominios[variavel] = dominio_filtrado
      return dominios

class RestringeDominiosMesmoTime(FiltroDominio):
    def __init__(self):
        super().__init__()
    def reduzir_dominio(self, dominios, atribuicao):
      ultimo_variavel_atribuido = list(atribuicao)[-1]
      ultima_partida_atribuida =  atribuicao[ultimo_variavel_atribuido]
      numeros_variavel = re.findall('\d\d?', ultimo_variavel_atribuido)
      rodada = int(numeros_variavel[0])
      num_jogo = int(numeros_variavel[1])
      times = []
      variaveis_nao_atribuidas = []
      
      for jogo in range(JOGOS):
        variavel = 'R' + str(rodada) + 'J' + str(jogo)
        if atribuicao.get(variavel) != None:
          time1= atribuicao[variavel][0]
          times.append(time1)
          time2= atribuicao[variavel][1]
          times.append(time2)
        else:
          variaveis_nao_atribuidas.append(variavel)

      for variavel in variaveis_nao_atribuidas:
        dominio_filtrado = list(filter(lambda x: (x[0] not in times and x[1] not in times), dominios[variavel]))
        dominios[variavel] = dominio_filtrado
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
  aux_par = None
  pares_cidades_ocorrencia_unica = []
  for caracteristica in equipes.values():
    cidade = caracteristica["cidade"]
    if cidades_ocorrencias.get(cidade) != None:
      cidades_ocorrencias[cidade] += 1
    else:
      cidades_ocorrencias[cidade] = 1
  
  cidades_restricao_rodadas = []
  par_cidades = []
  for cidade, ocorrencias in cidades_ocorrencias.items():
    if ocorrencias > 2:
      print(f'Não é possível respeitar a condição de uma unica cidade na rodada.')
      print(f'Há {ocorrencias} ocorrências na cidade {cidade} totalizando {int(ocorrencias * (RODADAS / TURNOS))} partidas nesse estádio.')
      print(f'Porém só tem {RODADAS} rodadas no campeonato.')
      return None, None
    if ocorrencias == 2:
      cidades_restricao_rodadas.append(cidade)
    if ocorrencias == 1:
      if aux_par != None:
        par = [aux_par, cidade]
        par_cidades.append(par)
        aux_par = None
      else:
        aux_par = cidade
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
      for i in range(len(par_cidades)):
        if cidade == par_cidades[i][0] or cidade == par_cidades[i][1]:
          if len(jogos_sem_restricao_cidade_todas_rodadas) > i:
            jogos = jogos_sem_restricao_cidade_todas_rodadas[i].copy()
            jogos.append(jogo)
            jogos_sem_restricao_cidade_todas_rodadas[i] = jogos
          else:
            jogos_sem_restricao_cidade_todas_rodadas.append([jogo])

  return jogos_sem_restricao_cidade_todas_rodadas, list(cidade_jogos.values())

def definir_prioridade(jogos, prioridade):
  times_ordenados_por_prioridade = list(sorted(jogos, key=lambda jogo: jogo in prioridade, reverse=True))
  return times_ordenados_por_prioridade

if __name__ == "__main__":
    start_time = time.time()
    linhas = ''
    seed_number = ''
    if USAR_ULTIMA_SEED:
      with open('static.txt', encoding='utf-8') as file:
        linhas = file.read().split('\n')
      seed_number = float(linhas[0].split(' ')[1])
    else:
      seed_number = start_time

    seed(seed_number)
    
    variaveis = []
    dominios = {}
    jogos_classicos = gerar_jogos_classicos(5)
    jogos_sem_restricao_cidade_todas_rodadas, jogos_restricao_cidade_todas_rodadas = gerar_jogos_separados_cidades_exclusivas()
    
    if jogos_sem_restricao_cidade_todas_rodadas != None and jogos_restricao_cidade_todas_rodadas != None:
      qntd_restricoes_cidades = len(jogos_restricao_cidade_todas_rodadas)

      for i in range(RODADAS): # rodadas
        for j in range(JOGOS): # jogos
          # Variável RnJm, tal que n é o número da rodada e m é o jogo da rodada
          variavel = "R" + str(i) + "J" + str(j)
          variaveis.append(variavel)
          if j < qntd_restricoes_cidades:
            dominio = jogos_restricao_cidade_todas_rodadas[j].copy()
            shuffle(dominio)
            dominio = definir_prioridade(dominio, jogos_classicos)
            dominios[variavel] = dominio
          else:
            index = j - qntd_restricoes_cidades
            dominio = jogos_sem_restricao_cidade_todas_rodadas[index].copy()
            
            shuffle(dominio)
            dominio = definir_prioridade(dominio, jogos_classicos)
            dominios[variavel] = dominio

      problema = SatisfacaoRestricoes(variaveis, dominios)
      rodadas = []
      for i in range(RODADAS): # rodadas
          jogos_rodada = []
          for j in range(JOGOS): # jogos
              jogos_rodada.append("R" + str(i) + "J" + str(j))
          rodadas.append(jogos_rodada)

      # nao repete cidade 
      problema.adicionar_restricao(NaoPodePatidaMesmaCidadeNaRodada(variaveis, qntd_restricoes_cidades))
      problema.adicionar_restricao_dominio(RestringeDominiosCidade(qntd_restricoes_cidades))
      
      # nao repete classico
      problema.adicionar_restricao(NaoPodeClassicoNaMesmaRodada(variaveis, jogos_classicos))
      problema.adicionar_restricao_dominio(RestringeDominiosClassicos(jogos_classicos))


      # nao repete time na rodada
      problema.adicionar_restricao(NaoPodeTimeNaMesmaRodada(variaveis))
      problema.adicionar_restricao_dominio(RestringeDominiosMesmoTime())
      
      print("Contruindo tabela...")
      resposta = problema.busca_backtracking()

      respota_str = "TABELA DE JOGOS\n\n"
      if resposta is None:
        respota_str = "Nenhuma resposta encontrada\n"
      else:
        for i in range(RODADAS): # rodadas
          respota_str += "---------- Rodada " + str(i+1) + " ----------\n"
          for j in range(JOGOS): # jogos
            jogo = resposta["R" + str(i) + "J" + str(j)]
            respota_str += "Jogo " + str(j+1) + ": " + jogo[0] + " x " + jogo[1] + "\tCidade: " + equipes[jogo[0]]["cidade"] + '\n'
            if j == (JOGOS - 1):
              respota_str += '\n'
      with open('table.txt', 'w', encoding='utf-8') as file:
        file.write(respota_str)

      tempo_duracao =  time.strftime("%H hora(s) e %M minuto(s) e %S segundo(s)", time.gmtime(time.time()-start_time))
      new_static = "Seed: " + str(seed_number) + "\nDemorou: " + tempo_duracao
      with open('static.txt', 'w', encoding='utf-8') as file:
        file.write(new_static)
      
      print("Demorou: ",tempo_duracao,end='\n')

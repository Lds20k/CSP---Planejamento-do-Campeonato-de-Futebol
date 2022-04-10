class Restricao():
    def __init__(self, variaveis):
        self.variaveis = variaveis

    def esta_satisfeita(self, atribuicao):
      return True

class SatisfacaoRestricoes():
  def __init__(self, variaveis, dominios, deve_performar):
    self.variaveis = variaveis # Variáveis para serem restringidas
    self.dominios = dominios # Domínio de cada variável
    self.restricoes = {}
    self.rodadas = self.dominios[variaveis[0]].copy()
    self.deve_performar = deve_performar
    for variavel in self.variaveis:
        self.restricoes[variavel] = []
        if variavel not in self.dominios:
            raise LookupError("Cada variávei precisa de um domínio")

  def adicionar_restricao(self, restricao):
    for variavel in restricao.variaveis:
      if variavel not in self.variaveis:
        raise LookupError("Variável não definida previamente")
      else:
        self.restricoes[variavel].append(restricao)

  def esta_consistente(self, variavel, atribuicao):
    for restricoes in self.restricoes[variavel]:
      if not restricoes.esta_satisfeita(atribuicao):
        return False
    return True
  
  def reduzir_dominio(self, atribuicao, variavel_atribuida):
    # ultima_atribuida = list(atribuicao.keys())
    # dominio_atribuido = atribuicao[variavel_atribuida]
    # time1 = ultima_atribuida[0]
    # time2 = ultima_atribuida[1]
    # cidade = ultima_atribuida[2]
    count = 0
    for partida in self.dominios.keys():
      # or time2 == partida[0] or time2 == partida[1]
      # cidade == partida[2]
      # or time1 == partida[1] or time2 == partida[0] or time2 == partida[1]
      # or partida_atribuicao[1] == partida[1] or partida_atribuicao[0] == partida[1] or partida_atribuicao[1] == partida[0]
      # partida1[TIME_1] == partida2[TIME_1] or partida1[TIME_1] == partida2[TIME_2] or partida1[TIME_2] == partida2[TIME_2]
      rodadas = self.rodadas.copy()
      for partida_atribuicao in atribuicao.keys():
        #  or partida_atribuicao[2] == partida[2]
        if (partida_atribuicao[0] == partida[0] or partida_atribuicao[0] == partida[1] or partida_atribuicao[1] == partida[0] or partida_atribuicao[1] == partida[1]) and atribuicao[partida_atribuicao] in rodadas:
          rodadas.remove(atribuicao[partida_atribuicao])
      # if partida not in atribuicao:
      self.dominios[partida] = rodadas
      # count += 1
      # print(count)
      # for partida in partidas:
      #   # ira remover todas partias com o time1 atribuido
      #   if partida[0] != ultima_atribuida[0] and partida[0] != ultima_atribuida[1] and partida[1] != ultima_atribuida[0] and partida[1] != ultima_atribuida[1]:
      #     dominio_filtrado.append(partida)
      #   # atribui a nova array de dominios filtrado
      #   for variavel in self.variaveis:
      #     self.dominios[variavel] = dominio_filtrado
        


  def busca_backtracking(self, atribuicao = {}):
    # retorna sucesso quando todas as variáveis forem atribuídas
    if len(atribuicao) == len(self.variaveis):
      return atribuicao

    # pega todas as variáveis que ainda não foram atribuídas
    variaveis_nao_atribuida  = [v for v in self.variaveis if v not in atribuicao]
    # pega primeira variável não atribuída
    variavel_menos_dominios = None
    menor_dominio = len(self.rodadas) + 1

    for variavel in variaveis_nao_atribuida:
      if len(self.dominios[variavel]) < menor_dominio:
        variavel_menos_dominios = variavel
        menor_dominio = len(self.dominios[variavel])
    if menor_dominio == 0:
      print("Erro")
      return atribuicao
    for valor in self.dominios[variavel_menos_dominios]:
      atribuicao_local = atribuicao.copy()
      atribuicao_local[variavel_menos_dominios] = valor
      # estamos consistentes, seguir recursão
      if self.esta_consistente(variavel_menos_dominios, atribuicao_local):
        self.reduzir_dominio(atribuicao_local, variavel_menos_dominios)
        resultado  = self.busca_backtracking(atribuicao_local)
        # para o backtracking se não encontra todos os resultados
        if resultado is not None:
          return resultado
    return None
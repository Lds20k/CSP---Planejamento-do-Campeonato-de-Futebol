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

    for partida in self.dominios:
      # or time2 == partida[0] or time2 == partida[1]
      # cidade == partida[2]
      # or time1 == partida[1] or time2 == partida[0] or time2 == partida[1]
      rodadas = self.rodadas.copy()
      for partida_atribuicao in atribuicao.keys():
        if (partida_atribuicao[2] == partida[2] or partida_atribuicao[0] == partida[1]) and atribuicao[partida_atribuicao] in rodadas:
          rodadas.remove(atribuicao[partida_atribuicao])
      self.dominios[partida] = rodadas
    #   for partida in partidas:
    #     # ira remover todas partias com o time1 atribuido
    #     if partida[0] != ultima_atribuida[0] and partida[0] != ultima_atribuida[1] and partida[1] != ultima_atribuida[0] and partida[1] != ultima_atribuida[1]:
    #       dominio_filtrado.append(partida)
    #     # atribui a nova array de dominios filtrado
    #     for variavel in self.variaveis:
    #       self.dominios[variavel] = dominio_filtrado
        


  def busca_backtracking(self, atribuicao = {}):
    # retorna sucesso quando todas as variáveis forem atribuídas
    if len(atribuicao) == len(self.variaveis):
      return atribuicao

    # pega todas as variáveis que ainda não foram atribuídas
    variaveis_nao_atribuida  = [v for v in self.variaveis if v not in atribuicao]
    # pega primeira variável não atribuída
    primeira_variavel = variaveis_nao_atribuida[0]
    for valor in self.dominios[primeira_variavel]:
      atribuicao_local = atribuicao.copy()
      atribuicao_local[primeira_variavel] = valor
      # estamos consistentes, seguir recursão
      if self.esta_consistente(primeira_variavel, atribuicao_local):
        self.reduzir_dominio(atribuicao_local, primeira_variavel)
        resultado  = self.busca_backtracking(atribuicao_local)
        # para o backtracking se não encontra todos os resultados
        if resultado is not None:
          return resultado
    return None
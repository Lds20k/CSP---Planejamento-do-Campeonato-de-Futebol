class Restricao():
    def __init__(self, variaveis):
        self.variaveis = variaveis

    def esta_satisfeita(self, atribuicao):
      return True

class SatisfacaoRestricoes():
  def __init__(self, variaveis, dominios):
    self.variaveis = variaveis # Variáveis para serem restringidas
    self.dominios = dominios # Domínio de cada variável
    self.partidas = dominios[1].copy()
    self.restricoes = {}
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
  
  def reduzir_dominio(self, atribuicao, variavel):
    partida = atribuicao[variavel]
    dominio_filtrado = []
    primeira_variavel = self.variaveis[0]
    if len(atribuicao) < (len(self.variaveis)/2):
      partidas = self.dominios[primeira_variavel].copy()
      partidas_atribuiddas = []
      for p in atribuicao.values():
        partidas_atribuiddas.append(p)
      for p in partidas:
        if p != partida and p[0] != partida[0]:
          dominio_filtrado.append(p)
      for variavel in self.variaveis:
        self.dominios[variavel] = dominio_filtrado
      


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
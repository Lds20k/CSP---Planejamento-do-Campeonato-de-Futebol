# Irá declarar as restrições de cada variavel
class Restricao():
  def __init__(self, variaveis):
      self.variaveis = variaveis

  def esta_satisfeita(self, atribuicao):
    return True

# Irá declarar os filtros de dominios (Forward Checking)
class FiltroDominio():
  def reduzir_dominio(self, dominios, valores_atribuidos):
    return dominios

# Irá rodar o backtracking
class SatisfacaoRestricoes():
  def __init__(self, variaveis, dominios):
    self.variaveis = variaveis # Variáveis para serem restringidas
    self.dominios = dominios # Domínio de cada variável
    self.dominios_copia = dominios.copy() # uma copia para filtrar os dominios
    self.restricoes = {}
    self.filtro_dominio = []

    for variavel in self.variaveis:
        self.restricoes[variavel] = []
        if variavel not in self.dominios:
            raise LookupError("Cada variávei precisa de um domínio")

  # adiciona a restricao na lista de restrições
  def adicionar_restricao(self, restricao):
    for variavel in restricao.variaveis:
      if variavel not in self.variaveis:
        raise LookupError("Variável não definida previamente")
      else:
        self.restricoes[variavel].append(restricao)
  # verifica se a atribuicao é valida rodando todas as restricoes
  def esta_consistente(self, variavel, atribuicao):
    for restricoes in self.restricoes[variavel]:
      if not restricoes.esta_satisfeita(atribuicao):
        return False
    return True

  # adiciona um filtro a lista de filtros de dominio
  def adicionar_filtro_dominio(self, adicionar_filtro_dominio):
      self.filtro_dominio.append(adicionar_filtro_dominio)

  # reduz o dominio nao deixando repetir partida e depois rodando os filtros que se criar
  def reduzir_dominio(self, atribuicao: dict):
    # nao irá deixar repetir partidas
    valores_atribuidos = list(atribuicao.values())
    for key in dict(self.dominios_copia).keys():
      dominio_filtrado = list(filter(lambda x: (x not in valores_atribuidos), self.dominios_copia[key]))
      self.dominios[key] = dominio_filtrado
    
    # vai rodar todos filtros de dominios personalizados
    for filtros_dominio in self.filtro_dominio:
      self.dominios = filtros_dominio.reduzir_dominio(self.dominios, atribuicao)

  # MRV (Most Remaining Values) - Escolhe a variavel nao atribuida que contém menor dominio
  def escolher_menor_dominio(self, variaveis_nao_atribuida):
    variavel_menor_dominio = variaveis_nao_atribuida[0]
    for variavel in variaveis_nao_atribuida:
      if len(self.dominios[variavel]) < len(self.dominios[variavel_menor_dominio]):
        variavel_menor_dominio = variavel
    return variavel_menor_dominio

  def busca_backtracking(self, atribuicao = {}):
    # retorna sucesso quando todas as variáveis forem atribuídas
    if len(atribuicao) == len(self.variaveis):
      return atribuicao

    # pega todas as variáveis que ainda não foram atribuídas
    variaveis_nao_atribuida  = [v for v in self.variaveis if v not in atribuicao]

    # pega a variável com menor dominio
    variavel_menor_dominio = self.escolher_menor_dominio(variaveis_nao_atribuida)

    # roda o loop do dominio da variavel escolhida
    for valor in self.dominios[variavel_menor_dominio]:
      atribuicao_local = atribuicao.copy()   
      atribuicao_local[variavel_menor_dominio] = valor

      # estamos consistentes, seguir recursão
      if self.esta_consistente(variavel_menor_dominio, atribuicao_local):
        # quando atribui um valor roda o filtro de dominio
        self.reduzir_dominio(atribuicao_local)
        # recursao para achar os proximos valores
        resultado = self.busca_backtracking(atribuicao_local)

        # para o backtracking se não encontra todos os resultados
        if resultado is not None:
          return resultado
    return None
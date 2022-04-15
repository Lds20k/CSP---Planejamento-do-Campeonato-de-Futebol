class Restricao():
  def __init__(self, variaveis):
      self.variaveis = variaveis

  def esta_satisfeita(self, atribuicao):
    return True

class FiltroDominio():
  def reduzir_dominio(self, dominios, valores_atribuidos):
    return dominios


class SatisfacaoRestricoes():
  def __init__(self, variaveis, dominios):
    self.variaveis = variaveis # Variáveis para serem restringidas
    self.dominios = dominios # Domínio de cada variável
    self.dominios_copia = dominios.copy()
    self.restricoes = {}
    self.restricoes_dominio = []

    for variavel in self.variaveis:
        self.restricoes[variavel] = []
        if variavel not in self.dominios:
            raise LookupError("Cada variávei precisa de um domínio")

  def adicionar_restricao_dominio(self, restricao_dominio):
    self.restricoes_dominio.append(restricao_dominio)

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
  
  # nao vai deixar repetir partida no campeonato e ira reduzir os dominios (otimização)
  def reduzir_dominio(self, atribuicao: dict):
    valores_atribuidos = list(atribuicao.values())
    for key in dict(self.dominios_copia).keys():
      dominio_filtrado = list(filter(lambda x: (x not in valores_atribuidos), self.dominios_copia[key]))
      self.dominios[key] = dominio_filtrado
    
    for filtros_dominio in self.restricoes_dominio:
      self.dominios = filtros_dominio.reduzir_dominio(self.dominios, atribuicao)

  def escolher_menor_dominio(self, variaveis_nao_atribuida):
    menor_tamanho_dominio = 182
    variavel_com_menor_dominio = ''
    for variavel, dominio in self.dominios.items():
      if variavel in variaveis_nao_atribuida and len(dominio) < menor_tamanho_dominio:
        menor_tamanho_dominio = len(dominio)
        variavel_com_menor_dominio = variavel
    return variavel_com_menor_dominio

  def busca_backtracking(self, atribuicao = {}):
    # retorna sucesso quando todas as variáveis forem atribuídas
    if len(atribuicao) == len(self.variaveis):
      return atribuicao

    # pega todas as variáveis que ainda não foram atribuídas
    variaveis_nao_atribuida  = [v for v in self.variaveis if v not in atribuicao]
    # print(len(atribuicao))
    # pega a variável com menor dominio
    variavel_menor_dominio = self.escolher_menor_dominio(variaveis_nao_atribuida)
    for valor in self.dominios[variavel_menor_dominio]:
      atribuicao_local = atribuicao.copy()   
      atribuicao_local[variavel_menor_dominio] = valor
      # estamos consistentes, seguir recursão
      if self.esta_consistente(variavel_menor_dominio, atribuicao_local):
        self.reduzir_dominio(atribuicao_local)
        resultado  = self.busca_backtracking(atribuicao_local)
        # para o backtracking se não encontra todos os resultados
        if resultado is not None:
          return resultado
    return None
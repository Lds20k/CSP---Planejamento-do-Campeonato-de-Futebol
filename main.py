from satisfacao_restricoes import Restricao, SatisfacaoRestricoes

equipe = {
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

RODADAS = (len(equipe)-1) * 2
JOGOS = int(len(equipe)/2)

# gera combinação de todos os jogos
combinacao_de_todos_jogos = tuple((l1, l2) for l2 in equipe.keys() for l1 in equipe.keys())

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
    for jogo in jogos_rodada:
        if atribuicao.get(jogo) != None and equipe[jogo[0]]["cidade"] in cidades:
            return False
        cidades.append(equipe[jogo[0]]["cidade"])
    return True

if __name__ == "__main__":
    variaveis = []
    for i in range(RODADAS): # rodadas
      for j in range(JOGOS): # jogos
        # Variável RnJm, tal que n é o número da rodada e m é o jogo da rodada
        variaveis.append("R" + str(i) + "J" + str(j))
      
    dominios = {}
    for variavel in variaveis:
        # o domínio são as combinações de todos os possívels jogos
        dominios[variavel] = combinacao_de_todos_jogos
    
    problema = SatisfacaoRestricoes(variaveis, dominios)
    aux = []
    for i in range(RODADAS): # rodadas
        jogos_rodada = []
        for j in range(JOGOS): # jogos
            jogos_rodada.append("R" + str(i) + "J" + str(j))
        problema.adicionar_restricao(NaoPodePatidaMesmaCidadeNaRodada(jogos_rodada))
    
    resposta = problema.busca_backtracking()
    if resposta is None:
      print("Nenhuma resposta encontrada")
    else:
      for i in range(RODADAS): # rodadas
        print("\n---------- Rodada " + str(i+1) + " ----------\n")
        for j in range(JOGOS): # jogos
          jogo = resposta["R" + str(i) + "J" + str(j)]
          print("Jogo " + str(j+1) + ": " + jogo[0] + " x " + jogo[1] + "\tCidade: " + equipe[jogo[0]]["cidade"])
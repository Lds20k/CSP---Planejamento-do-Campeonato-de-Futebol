from itertools import product
from satisfacao_restricoes import Restricao, SatisfacaoRestricoes

class AnimaisJaulasDiferentes(Restricao):
  def __init__(self, animal1, animal2):
    super().__init__([animal1, animal2])
    self.animal1 = animal1
    self.animal2 = animal2

  def esta_satisfeita(self, atribuicao):
    if self.animal1 in atribuicao and self.animal2 in atribuicao:
      return atribuicao[self.animal1] != atribuicao[self.animal2]
    return True


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

def gerar_dominio():
    partidas = []
    for time in times:
        times_copy = times.copy()
        times_copy.remove(time)
        time_array = [time]
        
        produto = [time_array, times_copy]
        partidas.extend(list(product(*produto)))
        
    return partidas

if __name__ == "__main__":
    variaveis = list(range(1, 14))
    
    dominios = {}
    # Dica: o domínio pode ser String, inteiro, Dicionário ou objetos
    for variavel in variaveis:
        dominios[variavel] = gerar_dominio()
        print(dominios)
    
    problema = SatisfacaoRestricoes(variaveis, dominios)

    # Leão e Tigre se odeiam e não querem ficar na mesma jaula
    problema.adicionar_restricao(AnimaisJaulasDiferentes("Leao", "Tigre"))

    resposta = problema.busca_backtracking()
    if resposta is None:
        print("Nenhuma resposta encontrada")
    else:
        print(resposta) 
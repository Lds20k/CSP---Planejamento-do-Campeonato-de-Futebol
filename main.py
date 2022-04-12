from itertools import permutations
import json
import sys
from satisfacao_restricoes import SatisfacaoRestricoes

maiores_times_cidades = {
    "SE Escondidos": "Escondidos",
    "Porto FC": "Porto",
    "SE Leoes": "Leao",
    "Guardioes FC": "Guardiao",
    "Ferroviaria EC": "Porto"
}

times_cidades = {
    "Campos FC": "Campos",
    "Guardioes FC": "Guardiao",
    "CA Protetores": "Guardiao",
    "SE Leoes": "Leao",
    "Simba EC": "Leao",
    "SE Granada": "Granada",
    "CA Lagos": "Lagos",
    "Solaris EC": "Ponte-do-Sol",
    "Porto FC": "Porto",
    "Ferroviaria EC": "Porto",
    "Portuarios AA": "Porto",
    "CA Azedos": "Limoes",
    "SE Escondidos": "Escondidos",
    "Secretos FC": "Escondidos"
}

def gerar_rodadas(rodadas_partidas, partidas):
    variaveis = rodadas_partidas
    dominios = {}
    for variavel in variaveis:
        dominios[variavel] = partidas.copy()
    
    problema = SatisfacaoRestricoes(variaveis, dominios)

    problema.restricoes()

    resposta = problema.busca_backtracking()
    if resposta is None:
        print("Nenhuma resposta encontrada")
    return resposta

def gerar_partidas(times_cidades: dict):
    partidas = list(permutations(times_cidades.keys(), 2))
    return partidas

def gerar_rodada_partida(qtd_partidas, qtd_rodadas):
    rodadas_partidas = []
    for i in range(1, qtd_rodadas + 1):
        for j in range(1, qtd_partidas + 1):
            rodadas_partidas.append(f"R{i}P{j}")
    return rodadas_partidas

if __name__ == "__main__":
    qtd_partidas = int(len(times_cidades) / 2)
    qtd_rodadas = (len(times_cidades) - 1) * 2

    classicos = gerar_partidas(maiores_times_cidades)
    partidas_permutadas = gerar_partidas(times_cidades)
    rodada_partida_permutadas = gerar_rodada_partida(qtd_partidas, qtd_rodadas)
    partidas = []
    for partida in partidas_permutadas:
        partidas.append(tuple([partida, partida in classicos]))

    print("Gerando rodadas...")
    rodadas = gerar_rodadas(rodada_partida_permutadas, partidas)
    
    original_stdout = sys.stdout
    with open('output.json', 'w') as f:
        sys.stdout = f
        print(json.dumps(rodadas, indent=4))
        sys.stdout = original_stdout
    
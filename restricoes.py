from satisfacao_restricoes import Restricao

class NaoPodeJogarMaisDeUmaVez(Restricao):
    def __init__(self, time):
        super().__init__([time])

    def esta_satisfeita(self, atribuicao: dict):
        times = []
        for it in list(atribuicao.values()):
            times.extend(list([it[0], it[1]]))

        return len(set(times)) == len(times)
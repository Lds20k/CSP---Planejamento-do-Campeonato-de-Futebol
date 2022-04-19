# CSP para campeonato de futebol
Constroí uma tabela de rodadas e jogos dentro do arquivo table.txt, para iniciar basta ter Python3 instalado e rodar no modo debug.

# O que é uma variável
A variavel é a combinação da partida com a rodada.
Exemplo: R0P0, R0P1, ..., R(i)P(j)

# Como se define o dominío do problema
O dominío é todos os jogos do campeonato (uma tupla com timeA  e timeB).

# Quais são as restrições do problema
## Restrições

- Todos os times devem jogar todas as rodadas uns contra os outros em jogos de turno e returno;

- Não pode ter repetição de jogos durante o campeonato;

- Um time não pode jogar mais de uma vez por rodada;

- O jogo ocorre na cidade do time mandante. Jogos diferentes na mesma cidade não podem ocorrer na mesma rodada porque os times usam o mesmo estádio;

- Clássicos (qualquer jogos entre os 5 maiores times) não podem acontecer na mesma rodada por competição com a TV;


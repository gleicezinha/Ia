import argparse
from aigyminsper.search.search_algorithms import BuscaLargura, AEstrela, BuscaProfundidadeIterativa, BuscaProfundidade, BuscaCustoUniforme
from aigyminsper.search.graph import State

class MyAgent(State):

    objetivo = [14, 18]

    def __init__(self, labirinto, pos_x, pos_y, op):
        super().__init__(op)
        self.labirinto = labirinto
        self.lin_max = len(self.labirinto) - 1
        self.col_max = len(self.labirinto[0]) - 1
        self.linha = pos_x
        self.coluna = pos_y

    def successors(self):
        successors = []
        # print(f"posição atual linha:{self.linha}, coluna:{self.coluna}")
        # print(self.labirinto[self.linha][self.coluna])
        if self.linha - 1 >= 0 and self.labirinto[self.linha - 1][self.coluna] != 0:
            new = [row.copy() for row in self.labirinto]
            successors.append(MyAgent(new, self.linha-1, self.coluna, 'cima'))

        if self.linha + 1 <= self.col_max and self.labirinto[self.linha + 1][self.coluna] != 0:
            new = [row.copy() for row in self.labirinto]
            successors.append(MyAgent(new, self.linha+1, self.coluna, 'baixo'))
            
        if self.coluna - 1 >= 0 and self.labirinto[self.linha][self.coluna - 1] != 0:
            new = [row.copy() for row in self.labirinto]
            successors.append(MyAgent(new, self.linha, self.coluna-1, 'esquerda'))

        if self.coluna + 1 <= self.lin_max and self.labirinto[self.linha][self.coluna + 1] != 0:
            new = [row.copy() for row in self.labirinto]
            successors.append(MyAgent(new, self.linha, self.coluna+1, 'direita'))

        # if self.labirinto[self.coluna][self.linha] == 0:
        #     new = self.labirinto.copy()
        #     new[self.coluna][self.linha] = 0
        #     successors.append(MyAgent(new, self.linha, self.coluna, 'visitado'))

        return successors

    def is_goal(self):
        return self.labirinto[self.linha][self.coluna] == self.objetivo[0] or self.labirinto[self.linha][self.coluna] == self.objetivo[1]

    def description(self):
        return "Percorrendo um labirinto de 7x7"

    def cost(self):
        if self.labirinto[self.linha][self.coluna] not in self.objetivo:
            return 2
        else:
            return 4

    #Heuristica
    def h(self):
        #Como não é possível definir dois valores para heuristica, temos que definir um objetivo unico, no caso 14
        return abs(self.linha - 1) + abs(self.coluna - 1)

    def env(self):
        return (self.linha, self.coluna)

def leituraDeArquivoTxT(nomeDoArquivo):
    matriz = list()
    with open(nomeDoArquivo, 'r') as arquivo:
        for linha in arquivo:         
            matriz.append(conversaoDeLista(linha.strip().split(',')))
    return matriz

def conversaoDeLista(lista):
    listaCorrigida = [int(i) if i.strip().isdigit() else 0 for i in lista]
    return listaCorrigida

def printarMatriz(matriz):
    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            print(f"{matriz[i][j]}\t", end=' ')
        print()

def main():
    print("oi")

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "nome_arquivo",
        type = str,
        help = "Caminho do arquivo txt para ser lido"
    )
    parser.add_argument(
        "origem_x",
        type = str,
        help = "Posição x da origem no labirinto"
    )
    parser.add_argument(
        "origem_y",
        type = str,
        help = "Posição y da origem no labirinto"
    )
    args = parser.parse_args()

    #Preparando Agente
    matriz = leituraDeArquivoTxT(args.nome_arquivo)
    pos_x = int(args.origem_x)
    pos_y = int(args.origem_y)
    printarMatriz(matriz)
    print(matriz[pos_x][pos_y]) 
    # print(matriz[2][1])
    # print(matriz[1][2])
    agente = MyAgent(matriz, pos_x, pos_y, '')
 
    #Implementando Buscas
    print("Busca Por Largura")
    bfs = BuscaLargura()
    resultado = bfs.search(agente)
    if resultado != None:
        print("Achei")
        print(resultado.show_path())
        # print(dir(resultado))
        print(f"Custo: {resultado.g}")
        # print(f"Heuristica: {resultado.h}")
        # print(f"Nó pai: {resultado.father_node}")
        # print(f"Agente: {resultado.state}")
        print(f"Profundidade: {resultado.depth}")
    else: 
        print('Não achou solução')

    #Busca por Profundidade
    print("Busca por Profundidade")
    dfs = BuscaProfundidade()
    # help(dfs)
    # print(dir(dfs))
    resultado = dfs.search(agente, m=20, pruning='general', trace=False) #Precisa ter o limite de profundidade e o pruning dita onde a busca deve ir ou não, se deve repetir ou não
    if resultado != None:
        print("Achei")
        print(resultado.show_path())
        # print(dir(resultado))
        print(f"Custo: {resultado.g}")
        # print(f"Heuristica: {resultado.h}")
        # print(f"Nó pai: {resultado.father_node}")
        # print(f"Agente: {resultado.state}")
        print(f"Profundidade: {resultado.depth}")
    else: 
        print('Não achou solução')

    #Busca por custo
    print("Busca Por Custo")
    ucs = BuscaCustoUniforme()
    resultado = ucs.search(agente)
    if resultado != None:
        print("Achei")
        print(resultado.show_path())
        # print(dir(resultado))
        print(f"Custo: {resultado.g}")
        # print(f"Heuristica: {resultado.h}")
        # print(f"Nó pai: {resultado.father_node}")
        # print(f"Agente: {resultado.state}")
        print(f"Profundidade: {resultado.depth}")
    else: 
        print('Não achou solução')

    #Busca AEstrela
    print("Busca AEstrela")
    aes = AEstrela()
    resultado = aes.search(agente, m=20, pruning='general', trace=False)
    if resultado != None:
        print("Achei")
        print(resultado.show_path())
        # print(dir(resultado))
        print(f"Custo: {resultado.g}")
        # print(f"Heuristica: {resultado.h}")
        # print(f"Nó pai: {resultado.father_node}")
        # print(f"Agente: {resultado.state}")
        print(f"Profundidade: {resultado.depth}")
    else: 
        print('Não achou solução')

if __name__ == '__main__':
    #Pra chamar o código, digitar no terminal: python labirintoCusto.py configuracao.txt 4 1 
    main()
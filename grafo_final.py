import os
from pyvis.network import Network
import networkx as nx
from networkx.algorithms.planarity import check_planarity
import csv

#função para verificar se o grafo é planar
def is_planar_advanced(grafo):
    if grafo.number_of_nodes() <= 20:
        # Função para verificar se um grafo contém K5 ou K3,3
        # Implementação ingênua para grafos pequenos

        # Verificar se contém K5 (grafo completo com 5 vértices)
        k5_vertices = set()
        for v in grafo.nodes():
            if grafo.degree(v) >= 5:
                k5_vertices.add(v)
                if len(k5_vertices) == 5:
                    return True  # Encontrou K5

        # Reinicializar para verificar K3,3 (grafo bipartido completo com 6 vértices)
        k5_vertices.clear()

        # Verificar se contém K3,3
        for v in grafo.nodes():
            if grafo.degree(v) >= 3:
                k5_vertices.add(v)
                if len(k5_vertices) == 3:
                    # Verificar bipartição
                    neighbors = set(grafo.neighbors(v))
                    if all(grafo.degree(u) >= 3 for u in neighbors):
                        return True  # Encontrou K3,3

        return False  # Não encontrou nenhum dos dois
    else:
        # Verifica a planaridade do grafo utilizando a biblioteca networkx
        # A função retorna uma tupla (boolean, subgrafo), onde o boolean indica se o grafo é planar
        # e o subgrafo é um planoembedding do grafo (usado para desenhar o grafo planar).
        # Aqui, pegamos apenas o boolean, indicando se o grafo é planar ou não.
        if not check_planarity(grafo)[0]:
            return False

    return True

#função para verificar se um grafo é uma árvore
def is_tree(grafo):
    # Verifica se o grafo é conexo usando a função is_connected do módulo networkx
    if not nx.is_connected(grafo):
        return False  # O grafo não é conexo, portanto, não é uma árvore

    # Inicializa um conjunto para rastrear nós visitados e uma fila para o algoritmo BFS
    visited = set()
    queue = [next(grafo.nodes)]  # Inicie o BFS a partir de um vértice qualquer

    while queue:
         # Pop o próximo nó da fila
        node = queue.pop(0)
        visited.add(node)

        # Itera sobre os vizinhos do nó atual
        for neighbor in grafo.neighbors(node):
            if neighbor not in visited:
                # Se o vizinho não foi visitado, adiciona à fila
                queue.append(neighbor)
            else:
                # Se o vizinho já foi visitado, encontrou um ciclo, portanto, não é uma árvore
                return False  # Encontrou um ciclo, portanto, não é uma árvore

    return len(visited) == len(grafo.nodes)  # Verifique se todos os nós foram visitados

#função para verificar o número cromático de um grafo
def calcular_numero_cromatico(grafo):
    if not grafo:
        return 0  # Grafo vazio tem número cromático zero

    vertices = list(grafo.nodes())
    coloracao = {}  # Mapeia vértices para suas cores atribuídas

    for vertice in vertices:
        vizinhos = set(coloracao.get(v, None) for v in grafo[vertice])
        cor = 0
        while cor in vizinhos:
            cor += 1
        coloracao[vertice] = cor

    numero_cromatico = max(coloracao.values()) + 1
    return numero_cromatico

#função para verificar se o grafo contém ciclos
def verifica_ciclo(grafo):
    # Conjunto para rastrear nós visitados durante a DFS
    visitados = set()
    # Conjunto para rastrear nós na pilha durante a DFS
    pilha = set()

    # Função de busca em profundidade recursiva
    def dfs(v):
        # Adiciona o nó ao conjunto de visitados e à pilha
        visitados.add(v)
        pilha.add(v)

        # Itera sobre os vizinhos do nó atual
        for vizinho in grafo.neighbors(v):
            if vizinho not in visitados:
                # Se o vizinho não foi visitado, realiza a DFS recursivamente
                if dfs(vizinho):
                    return True
            elif vizinho in pilha:
                # Se o vizinho já está na pilha, encontrou um ciclo
                return True
        # Remove o nó da pilha após explorar todos os vizinhos
        pilha.remove(v)
        # Indica que não foi encontrado ciclo a partir deste nó
        return False

    # Itera sobre todos os nós do grafo
    for node in grafo.nodes:
        # Se o nó não foi visitado, inicia a DFS a partir desse nó
        if node not in visitados:
            if dfs(node):
                # Se encontrou ciclo a partir deste nó, retorna True
                return True
    # Se nenhum ciclo foi encontrado em toda a busca, retorna False
    return False

# Função para verificar se um grafo é conexo
def verifica_conexo(grafo):
    if not grafo:
        return False  # Grafo vazio não é conexo

    visitados = set()
    queue = [next(iter(grafo))]  # Inicie o BFS a partir de um vértice qualquer

    while queue:
        node = queue.pop(0)
        visitados.add(node)

        for neighbor in grafo[node]:
            if neighbor not in visitados:
                queue.append(neighbor)

    return len(visitados) == len(grafo)

# Função para verificar se um grafo é bipartido
def is_bipartite(grafo):
    if not grafo:
        return False  # Grafo vazio não é bipartido

    color = {}
    queue = [next(iter(grafo))]  # Inicie o BFS a partir de um vértice qualquer
    color[queue[0]] = 0  # Atribua a cor 0 ao primeiro vértice

    while queue:
        node = queue.pop(0)

        for neighbor in grafo[node]:
            if neighbor not in color:
                color[neighbor] = 1 - color[node]
                queue.append(neighbor)
            elif color[neighbor] == color[node]:
                return False  # Dois vértices adjacentes têm a mesma cor, não é bipartido

    return True


# Função para verificar se um grafo é completo
def is_completo(grafo):
    # Verifica todos os pares de vértices
    vertices = grafo.nodes()
    for u in vertices:
        for v in vertices:
            # Se u e v são diferentes e não existe uma aresta entre eles, o grafo não é completo
            if u != v and not grafo.has_edge(u, v):
                return False
    # Se nenhum par de vértices não tiver uma aresta, o grafo é completo
    return True

# Função para verificar se um grafo é euleriano
def is_eulerian(grafo):
    # Verifica se o grafo é conexo
    if not verifica_conexo(grafo):
        # Se não for conexo, não pode ser euleriano
        return False

    # Verifica se todos os vértices têm grau par
    for node in grafo.nodes():
        if grafo.degree(node) % 2 != 0:
            # Se algum vértice tiver grau ímpar, o grafo não é euleriano
            return False

    # Se todos os vértices tiverem grau par, o grafo é euleriano
    return True

#função para verificar se um grafo é uma árvore
def is_tree(grafo):
    # Verifica se o grafo é conexo
    if not verifica_conexo(grafo):
        return False  # O grafo não é conexo, portanto, não é uma árvore

    # Conjunto para rastrear nós visitados durante o BFS
    visited = set()
    # Lista para armazenar os nós do grafo
    nodes = list(grafo.nodes())  # Converte a visualização dos nós em uma lista
    # Fila para o algoritmo BFS, iniciando a partir do primeiro vértice da lista
    queue = [(nodes[0], None)]  

    while queue:
        # Pop o próximo nó e seu pai da fila
        node, parent = queue.pop(0)
        # Adiciona o nó ao conjunto de visitados
        visited.add(node)

        # Itera sobre os vizinhos do nó atual
        for neighbor in grafo.neighbors(node):
            if neighbor != parent:
                # Se o vizinho não é o pai do nó atual
                if neighbor in visited:
                    return False  # Encontrou um ciclo, portanto, não é uma árvore
                # Adiciona o vizinho à fila junto com o nó atual como pai
                queue.append((neighbor, node))

    return len(visited) == len(nodes)  # Verifique se todos os nós foram visitados

#função para verificar se o grafo contém um caminhop hamiltoniano
def is_hamiltonian(grafo):
    def hamiltonian_ciclo_util(v, visitados, caminho):
        # Marca o vértice como visitado e adiciona ao caminho
        visitados[v] = True
        caminho.append(v)

        if len(caminho) == grafo.number_of_nodes():
            # Verifica se o último vértice no caminho tem uma aresta para o primeiro vértice
            if grafo.has_edge(caminho[-1], caminho[0]):
                return True
            else:
                return False

        # Explora todos os vizinhos não visitados do vértice atual
        for vizinho in grafo.neighbors(v):
            if not visitados[vizinho]:
                if hamiltonian_ciclo_util(vizinho, visitados, caminho):
                    return True

        # Se o vértice atual não levar a uma solução, retroceda
        visitados[v] = False
        caminho.pop()
        return False

    # Inicializa a lista de vértices visitados como False
    visitados = {v: False for v in grafo.nodes}

    # Inicializa o caminho como uma lista vazia
    caminho = []

    # Começa a verificação do ciclo Hamiltoniano a partir do primeiro vértice
    for v in grafo.nodes:
        if hamiltonian_ciclo_util(v, visitados, caminho):
            return True

    # Se nenhum ciclo Hamiltoniano for encontrado
    return False

#função para visualizar diferentes propriedades de um grafo
def visualizar_propriedades(grafo):
    
    # Verifica se o grafo é válido (não nulo e contém nós)
    if grafo is None or not grafo.nodes:
        print("Não há um grafo aberto ou criado. Por favor, crie um grafo ou abra um existente.")
        return criar_grafo()
    
    # Loop principal para exibir opções de propriedades do grafo
    while True:
        print("\nOpções de Propriedades do Grafo:")
        print("1.  Grau do Grafo")
        print("2.  Número cromático")
        print("3.  Grafo Cíclico")
        print("4.  Grafo Conexo")
        print("5.  Grafo Bipartido")
        print("6.  Grafo Completo")
        print("7.  Grafo Euleriano")
        print("8.  Grafo Hamiltoniano")
        print("9.  Grafo Árvore")
        print("10. Grafo planar")
        print("11. Voltar")

        # Solicita ao usuário que escolha uma opção
        opcao = input("Escolha uma opção para visualizar a propriedade do grafo: ")

        # Verifica a opção escolhida e exibe a propriedade correspondente
        if opcao == "1":
            # Função para verificar o grau do vértice
            if grafo.number_of_nodes() == 0:
                print("O grafo está vazio.")
            else:
                grau_Max = max(dict(grafo.degree()).values())
                grau_Min = min(dict(grafo.degree()).values())
                print(f"O grau máximo do meu grafo é: {grau_Max}")
                print(f"O grau mínimo do meu grafo é: {grau_Min}")
        
        elif opcao == '2':
            # Calcula e exibe o número cromático do grafo
            numero_cromatico = calcular_numero_cromatico(grafo)
            print(f"Número cromático do grafo: {numero_cromatico}")
        
        elif opcao == '3':
            # Verifica e exibe se o grafo contém ciclos
            if verifica_ciclo(grafo):
                print("O grafo contém ciclos")
            else:
                print("O grafo não contém ciclos")
        
        elif opcao == '4':
            # Verifica e exibe se o grafo é conexo
            if verifica_conexo(grafo):
                print("O grafo é conexo")
            else:
                print("O grafo não é conexo")
        
        elif opcao == '5':
            # Verifica e exibe se o grafo é bipartido
            if is_bipartite(grafo):
                print("O grafo é bipartido.")
            else:
                print("O grafo não é bipartido.")
                
        elif opcao == '6':
            # Verifica e exibe se o grafo é completo
            if is_completo(grafo):
                print("O grafo é completo.")
            else:
                print("O grafo não é completo.")
        
        elif opcao == '7':
            # Verifica e exibe se o grafo é euleriano
            if is_eulerian(grafo):
                print("O grafo é Euleriano.")
            else:
                print("O grafo não é Euleriano.")
        
        elif opcao == '8':
            # Verifica e exibe se o grafo é hamiltoniano
            if is_hamiltonian(grafo):
                print("O grafo é Hamiltoniano.")
            else:
                print("O grafo não é Hamiltoniano.")

        elif opcao == '9':
            # Verifica e exibe se o grafo é uma árvore
            if is_tree(grafo):
                print("O grafo é uma árvore")
            else:
                print("O Grafo não é uma árvore")
        
        elif opcao == '10':
            # Verifica e exibe se o grafo é planar
            if check_planarity(grafo)[0]:
                print("O grafo é planar.")
            else:
                print("O grafo não é planar.")

        elif opcao == '11':
            # Sai do loop e retorna ao menu principal
            break
        else:
            print("Opção inválida. Tente novamente.")

# Função para abrir um arquivo existente e criar um grafo a partir dele
def abrir_arquivo_existente():
    while True:
        # Solicita ao usuário o nome do arquivo existente
        arquivo = input("Digite o nome do arquivo existente: ")
        # Verifica se o arquivo existe
        if os.path.exists(arquivo):
            if arquivo.endswith('.csv'):
                grafo = nx.Graph()
                try:
                    # Abre o arquivo CSV e lê as arestas
                    with open(arquivo, 'r', newline='') as file:
                        # Cria um objeto leitor CSV associado ao arquivo aberto
                        reader = csv.reader(file)
                        # Itera sobre cada linha no arquivo
                        for row in reader:
                            # Verifica se a linha tem pelo menos dois elementos, representando uma aresta no grafo
                            if len(row) >= 2:
                                # Atribui os dois primeiros elementos da linha às variáveis origem e destino
                                origem, destino = row[0], row[1]
                                # Obtém o terceiro elemento da linha como o peso da aresta, convertendo-o para um inteiro
                                # Assume peso 1 se o terceiro elemento não existir (aresta sem peso especificado)
                                peso = int(row[2]) if len(row) > 2 else 1  
                                # Adiciona a aresta ao grafo, especificando origem, destino e peso
                                grafo.add_edge(origem, destino, weight=peso)
                    print("Arquivo aberto e grafo carregado.")
                    return grafo
                except Exception as e:
                    print(f"Erro ao abrir o arquivo CSV: {e}")
            # Se o arquivo for do tipo TXT      
            elif arquivo.endswith('.txt'):
                grafo = nx.Graph()
                try:
                    # Abre o arquivo de texto e lê as arestas
                    with open(arquivo, 'r') as file:
                        lines = file.readlines()
                        for line in lines:
                            parts = line.strip().split()
                            if len(parts) >= 2:
                                origem, destino = parts[0], parts[1]
                                peso = int(parts[2]) if len(parts) > 2 else 1  # Assume peso 1 se não especificado
                                grafo.add_edge(origem, destino, weight=peso)
                    print("Arquivo aberto e grafo carregado.")
                    return grafo
                except Exception as e:
                    print(f"Erro ao abrir o arquivo de texto: {e}")

            else:
                print("Formato de arquivo não suportado.")
        else:
            print("Arquivo não encontrado. Verifique o caminho e nome do arquivo.")

def salvar_grafo(grafo):
    while True:
        #Exibe opções para salvar o grafo
        print("\nOpções para salvar o grafo:")
        print("1. Salvar em CSV")
        print("2. Salvar em TXT")
        print("3. Voltar")

        #Solicita a escolha da opção ao usuário
        opcao = input("Escolha uma opção para salvar o grafo: ")

        if opcao == "1":
            # Solicita o nome do arquivo CSV para salvar o grafo
            arquivo_csv = input("Digite o nome do arquivo CSV para salvar: ")
            # Verifica se o nome do arquivo tem a extensão correta
            if arquivo_csv.endswith('.csv'):
                # Lógica para salvar o grafo em um arquivo CSV
                with open(arquivo_csv, 'w', newline='') as file:
                    writer = csv.writer(file)
                    for origem, destino, peso in grafo.edges(data='weight', default=1):
                        writer.writerow([origem, destino, peso])
                print(f"Grafo salvo no arquivo CSV: {arquivo_csv}")
            else:
                print("Formato de arquivo não é CSV.")
        
        elif opcao == "2":
            #Solicita o nome do arquivo TXT para salvar o grafo
            arquivo_txt = input("Digite o nome do arquivo TXT para salvar: ")
            # Verifica se o nome do arquivo tem a extensão correta
            if arquivo_txt.endswith('.txt'):
                # Lógica para salvar o grafo em um arquivo de texto
                with open(arquivo_txt, 'w') as file:
                    # Itera sobre as arestas do grafo, obtendo origem, destino e peso (ou assumindo peso 1 se não especificado)
                    for origem, destino, peso in grafo.edges(data='weight', default=1):
                        # Escreve a representação da aresta no arquivo TXT, seguida por uma quebra de linha
                        file.write(f"{origem} {destino} {peso}\n")
                # Exibe mensagem indicando que o grafo foi salvo no arquivo TXT com o nome fornecido
                print(f"Grafo salvo no arquivo TXT: {arquivo_txt}")
            else:
                print("Formato de arquivo não é TXT.")
        
        elif opcao == "3":
            return criar_grafo()
        else:
            print("Opção inválida. Tente novamente.")

def criar_grafo():
    # Exibe mensagem de boas-vindas ao programa de criação e visualização de grafos
    print("Bem-vindo ao programa de criação e visualização de grafos!")

    # Inicialize o grafo vazio não direcionado
    grafo = nx.Graph()

    while True:
        # Exibe o menu de opções
        print("\nMenu:")
        print("1. Criar Grafo")
        print("2. Mostrar Grafo")
        print("3. Visualizar propriedades do grafo")
        print("4. Abrir arquivo existente")
        print("5. Salvar grafo")
        print("6. Sair")

        # Solicita ao usuário que escolha uma opção
        escolha = input("Escolha uma opção: ")

        if escolha == "1":
            while True:
                # Solicita a entrada do usuário para vértices de origem e destino, permitindo a adição de arestas
                origem = input("Digite o vértice de origem (ou 'fim' para encerrar): ")
                if origem.lower() == 'fim':
                    break
                elif not origem:
                    print("Um vértice não pode estar em branco. Por favor, digite novamente.")
                    continue  # Solicita novamente o vértice de origem

                destino = input("Digite o vértice de destino (ou 'fim' para encerrar): ")
                if destino.lower() == 'fim':
                    break
                elif not destino:
                    print("Um vértice não pode estar em branco. Por favor, digite novamente.")
                    continue  # Solicita novamente o vértice de destino

                # Adiciona uma aresta ao grafo        
                grafo.add_edge(origem, destino)
                print(f"Aresta adicionada: {origem} -> {destino}")

        elif escolha == "2":
            # Visualiza o grafo criado e o salva em um arquivo HTML
            nt = Network('1080px', '920px', directed=False)
            nt.from_nx(grafo)
            nt.write_html('G_pontes.html')
            print("Grafo visualizado em 'G_pontes.html'")

        elif escolha == "3":
            # Chama a função para visualizar as propriedades do grafo
            visualizar_propriedades(grafo)

        elif escolha == "4":
            # Chama a função para abrir um arquivo existente e carregar o grafo
            grafo_aberto = abrir_arquivo_existente()
            if grafo_aberto:
                grafo = grafo_aberto
                continue  # Volta ao menu principal com o novo grafo

        elif escolha == "5":
            # Chama a função para salvar o grafo
            salvar_grafo(grafo)
            break

        elif escolha == "6":
            # Encerra o programa
            # Sair
            break

        else:
            print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    # Inicia a execução do programa ao chamar a função criar_grafo()
    criar_grafo()
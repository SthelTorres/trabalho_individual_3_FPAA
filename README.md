# trabalho_individual_3_FPAA

# Caminho Hamiltoniano 

## Introdução
Este programa implementa uma busca por **Caminho Hamiltoniano** em grafos dirigidos ou não-dirigidos, utilizando **backtracking**.  
Um Caminho Hamiltoniano é uma sequência de vértices que visita cada vértice exatamente uma vez.

O algoritmo suporta:
- Grafos não-dirigidos e dirigidos.
- Definição opcional de um vértice inicial.
- Listagem de apenas um caminho ou de todos os caminhos Hamiltonianos possíveis.

---

## Formato do Arquivo de Entrada
O grafo deve ser descrito em um arquivo `.txt` no seguinte formato:

- Linha opcional: `DIRECTED=0` (não-dirigido) ou `DIRECTED=1` (dirigido).  
- Linha opcional: `V= v1 v2 v3 ...` para declarar todos os vértices (inclui isolados).  
- Linhas seguintes: arestas no formato `u v` (uma por linha).  
- Linhas em branco ou iniciadas com `#` são ignoradas.  

### Exemplo (`grafo.txt`)
```txt
DIRECTED=0
V= A B C D
A B
B C
C D
A D
```


---

## Como Executar
```bash
python main.py --input grafo.txt
```
Executa o programa com o grafo informado. Tenta encontrar um Caminho Hamiltoniano em qualquer vértice inicial.
```bash
python main.py --input grafo.txt --start A
```
Define explicitamente que o Caminho Hamiltoniano deve começar pelo vértice A.
```bash
python main.py --input grafo.txt --all
```
Lista todos os caminhos Hamiltonianos encontrados (pode ser lento em grafos maiores, pois o número cresce exponencialmente).
```bash
python main.py --input grafo.txt --directed
```
Força a interpretação do grafo como dirigido, mesmo que o arquivo contenha DIRECTED=0.

### Saida Esperada
Se encontrar pelo menos um Caminho Hamiltoniano:
```bash
FOUND
Path: A -> B -> C -> D
```

Se a opção --all for usada:
```bash
FOUND
1: A -> B -> C -> D
2: D -> C -> B -> A
...
```

Caso não exista caminho Hamiltoniano:
```bash
NOT-FOUND
```

---

## Complexidade

O problema de encontrar Caminho Hamiltoniano é NP-completo.
A implementação via backtracking possui complexidade exponencial no pior caso mas funciona corretamente para grafos pequenos ou médios.

---

## Lógica do Algoritmo Implementado

O algoritmo utiliza a técnica de **backtracking** para encontrar um Caminho Hamiltoniano. A lógica pode ser resumida em quatro passos principais:

1. **Escolher um vértice inicial**: o algoritmo começa a busca a partir de um vértice do grafo (escolhido pelo usuário com `--start` ou automaticamente se não especificado).  
2. **Marcar como visitado**: o vértice inicial é marcado como visitado e adicionado ao caminho atual.  
3. **Explorar vizinhos não visitados**: para o vértice atual, o algoritmo tenta seguir para cada vizinho ainda não visitado, expandindo o caminho.  
4. **Retroceder se não houver saída**: se chegar em um vértice sem vizinhos válidos ou o caminho não puder ser completado, o algoritmo volta (backtrack), remove o último vértice e tenta outra opção.  

Esse processo continua recursivamente até que:
- Todos os vértices sejam visitados exatamente uma vez (**caminho Hamiltoniano encontrado**), ou  
- Todas as possibilidades sejam esgotadas (**nenhum caminho existe**).  

---

## Relatório Técnico

### Análise da Complexidade Computacional

#### Classes P, NP, NP-Completo e NP-Difícil
O problema de encontrar um **Caminho Hamiltoniano** é classificado como **NP-Completo**.  

- **P**: Conjunto de problemas que podem ser resolvidos em tempo polinomial. O Caminho Hamiltoniano **não** pertence a essa classe (não existe algoritmo conhecido em tempo polinomial que resolva o problema em geral).  
- **NP**: Problemas cujas soluções podem ser **verificadas** em tempo polinomial. Se alguém fornece um caminho Hamiltoniano como resposta, podemos verificar em tempo polinomial se o caminho é válido (basta checar se cada vértice é visitado exatamente uma vez e se as arestas existem).  
- **NP-Completo**: São os problemas mais difíceis dentro de NP. O Caminho Hamiltoniano é **NP-Completo** porque qualquer problema em NP pode ser reduzido a ele em tempo polinomial.  
- **Relação com o Problema do Caixeiro Viajante (TSP)**: O TSP é uma generalização do Caminho Hamiltoniano. Enquanto o Caminho Hamiltoniano pergunta apenas **se existe um caminho que passa por todos os vértices**, o TSP procura o caminho de **menor custo**. Por isso, ambos são NP-Completo.  

---

### Análise da Complexidade Assintótica de Tempo
O algoritmo implementado utiliza **backtracking** para explorar todas as possíveis sequências de vértices.

- Em um grafo com **n vértices**, o número de permutações possíveis é da ordem de `n!` (fatorial de n).  
- Portanto, a **complexidade temporal** é **O(n!)**, já que no pior caso o algoritmo precisa verificar todas as ordens possíveis de visitação.  

#### Método Utilizado
A análise foi feita por **contagem de operações**:  
- Para cada vértice inicial, o algoritmo tenta visitar recursivamente todos os vizinhos não visitados.  
- Isso gera uma árvore de busca com ramificação que, no pior caso, percorre todas as permutações.  
- Assim, a complexidade é **fatorial**.

---

### Aplicação do Teorema Mestre
O **Teorema Mestre** é usado para resolver recorrências da forma:  
`T(n) = aT(n/b) + f(n)`  

No entanto, o algoritmo de backtracking para Caminho Hamiltoniano **não gera uma recorrência nesse formato**, já que o número de subproblemas diminui de forma **não uniforme** (depende do grau de cada vértice e das escolhas de visita).  

👉 Portanto, **não é possível aplicar o Teorema Mestre** diretamente.  
A análise deve ser feita pela **contagem de estados explorados** (n!) e não pela expansão de uma recorrência divide-and-conquer.

---

### Análise dos Casos de Complexidade

- **Pior Caso**: O grafo não possui caminho Hamiltoniano. O algoritmo precisará explorar **todas as combinações possíveis** antes de concluir que não existe solução. Complexidade: **O(n!)**.  
- **Melhor Caso**: O algoritmo encontra rapidamente um caminho Hamiltoniano logo no início da busca (por exemplo, em grafos completos, o primeiro caminho tentado já é válido). Complexidade: **O(n)** até **O(n²)** dependendo da verificação.  
- **Caso Médio**: Em grafos aleatórios, o algoritmo explora apenas uma fração das possibilidades antes de encontrar um caminho ou concluir que não existe, mas ainda assim a complexidade média é **exponencial**.  

#### Impacto no desempenho
- Em grafos pequenos (até 10 ou 12 vértices), o algoritmo é viável.  
- Em grafos maiores, o tempo cresce rapidamente, o que reflete a natureza **intrinsecamente difícil** do problema.  
- Estratégias como heurísticas ou poda de estados podem ajudar, mas não eliminam o crescimento exponencial.  

---

## Ponto Extra — Visualização do Caminho Hamiltoniano

Além da execução tradicional, o projeto inclui um visualizador opcional (`view.py`) que desenha o grafo e destaca o Caminho Hamiltoniano encontrado.

### Requisitos de instalação
Para gerar a visualização, instale as bibliotecas necessárias:
```bash
py -m pip install networkx matplotlib
```
#### Rodar o programa com visualização do grafo 
É so trocar :
```bash
main.py
```
por :
```bash
view.py
```
na hora de mandar o codigo no terminal .

exemplos :
```bash
python view.py --input grafo.txt
```
```bash
python view.py --input grafo.txt --start A
```
```bash
python view.py --input grafo.txt --all
```
```bash
python view.py --input grafo.txt --directed
```

### O que o programa faz
O programa:

1. Desenha o grafo original com todos os nós e arestas.  
2. Destaca em vermelho as arestas que compõem o Caminho Hamiltoniano encontrado.  
3. Exporta automaticamente uma imagem PNG para a pasta `assets/`.  
   - O arquivo gerado por padrão é `assets/hamiltoniano.png`.  
   - É possível alterar o nome com a opção `--output`.  


O grafo é exibido com todos os vértices, e o Caminho Hamiltoniano aparece em vermelho, destacado das demais arestas.

Apos rodar, é indicado :
ex:
```bash
FOUND
Path: A -> B -> C -> D
Imagem gerada em: assets/hamiltoniano.png
```
a imagem do grafo vai para a pasta /assets e é gerado um cache na pasta /_ pycache _

---

### Imagem Exemplo:

 <img src="https://github.com/SthelTorres/trabalho_individual_3_FPAA/blob/main/FotoExemplo/GrafoExTrabalho3.png?raw=true" alt="Exemplo de Caminho Hamiltoniano" width="600"/> 

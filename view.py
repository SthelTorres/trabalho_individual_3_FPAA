#!/usr/bin/env python
"""
view.py — Visualização do Caminho Hamiltoniano (ponto extra)

Requisitos:
  pip install networkx matplotlib

Uso:
  python view.py --input grafo.txt
  python view.py --input grafo.txt --start A
  python view.py --input grafo.txt --output assets/hamiltoniano.png
"""

import os
import argparse

# Evita depender de backend gráfico (funciona em qualquer ambiente)
import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import networkx as nx

# Importa funções do seu main.py (não executa o main por causa do if __name__ == "__main__")
from main import parse_graph, hamiltonian_paths


def build_nx_graph(g):
    """Converte o Graph do main.py para um grafo networkx."""
    G = nx.DiGraph() if g.directed else nx.Graph()
    # Adiciona nós
    for v in g.adj.keys():
        G.add_node(v)
    # Adiciona arestas (networkx lida com duplicadas)
    for u, nbrs in g.adj.items():
        for v in nbrs:
            G.add_edge(u, v)
    return G


def draw_graph(G, path=None, output_path="assets/hamiltoniano.png"):
    """Desenha o grafo e destaca o caminho (se existir)."""
    # Layout estável
    pos = nx.spring_layout(G, seed=42)

    # Desenha grafo base
    plt.figure(figsize=(8, 6), dpi=140)
    nx.draw_networkx_nodes(G, pos, node_size=800)
    nx.draw_networkx_edges(G, pos, width=1.5, arrows=G.is_directed())
    nx.draw_networkx_labels(G, pos, font_size=10, font_weight="bold")

    # Destaca o caminho encontrado
    if path and len(path) >= 2:
        # Lista de arestas do caminho em ordem
        path_edges = list(zip(path, path[1:]))

        # Desenha por cima em destaque
        nx.draw_networkx_edges(
            G, pos,
            edgelist=path_edges,
            width=3.0,
            edge_color="red",
            arrows=G.is_directed(),
        )

        # Opcional: legenda simples
        plt.title("Caminho Hamiltoniano: " + " → ".join(path), fontsize=10)
    else:
        plt.title("Grafo (nenhum caminho Hamiltoniano encontrado)", fontsize=10)

    # Garante pasta
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


def main():
    parser = argparse.ArgumentParser(description="Visualizar Caminho Hamiltoniano.")
    parser.add_argument("-i", "--input", required=True, help="Arquivo do grafo (.txt ou .json).")
    parser.add_argument("--start", help="Vértice inicial (opcional).")
    parser.add_argument("--output", default="assets/hamiltoniano.png",
                        help="Caminho do PNG de saída (padrão: assets/hamiltoniano.png)")
    args = parser.parse_args()

    # Carrega grafo pelo mesmo parser do seu main.py
    g = parse_graph(args.input)

    # Busca um caminho (primeiro encontrado)
    paths = hamiltonian_paths(g, start=args.start, all_paths=False)
    if paths:
        path = paths[0]
        print("FOUND")
        print("Path:", " -> ".join(path))
        G = build_nx_graph(g)
        draw_graph(G, path=path, output_path=args.output)
        print(f"Imagem gerada em: {args.output}")
    else:
        print("NOT-FOUND")
        G = build_nx_graph(g)
        draw_graph(G, path=None, output_path=args.output)
        print(f"Imagem do grafo (sem caminho) gerada em: {args.output}")

if __name__ == "__main__":
    main()

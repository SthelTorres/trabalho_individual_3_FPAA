#!/usr/bin/env python
"""
main.py — Caminho Hamiltoniano (backtracking) em grafos dirigidos ou não-dirigidos.

Formato de entrada (arquivo texto simples):
- Linha opcional: DIRECTED=0 ou DIRECTED=1   (0 = não-dirigido, 1 = dirigido)
- Linha opcional: V= v1 v2 v3 ...            (declara todos os vértices, inclusive isolados)
- Demais linhas: arestas "u v" (uma por linha), separadas por espaço.
- Linhas em branco e comentários iniciados por '#' são ignorados.

Exemplo (não-dirigido):
DIRECTED=0
V= A B C D
A B
B C
C D
A D

Execução:
$ python main.py --input grafo.txt
$ python main.py --input grafo.txt --start A
$ python main.py --input grafo.txt --all
$ python main.py --input grafo.txt --directed   (força como dirigido, ignora DIRECTED= na entrada)

Saída:
- Se encontrar pelo menos um Caminho Hamiltoniano, imprime "FOUND" e um caminho (ou todos com --all).
- Caso contrário, imprime "NOT-FOUND".

Observação:
Enumerar *todos* os caminhos hamiltonianos pode ser exponencial. Use --all com cautela.
"""

from __future__ import annotations
from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, List, Set, Iterable, Tuple, Optional
import argparse
import sys
import json
import os


@dataclass
class Graph:
    directed: bool = False
    adj: Dict[str, Set[str]] = None

    def __post_init__(self):
        if self.adj is None:
            self.adj = defaultdict(set)

    def add_vertex(self, v: str) -> None:
        _ = self.adj[v]  # força a criação

    def add_edge(self, u: str, v: str) -> None:
        self.adj[u].add(v)
        if not self.directed:
            self.adj[v].add(u)

    @property
    def vertices(self) -> List[str]:
        return list(self.adj.keys())

    def neighbors(self, u: str) -> Iterable[str]:
        return self.adj[u]


def parse_graph(path: str, directed_override: Optional[bool] = None) -> Graph:
    """
    Aceita dois formatos:
      1) .json: {"directed": true/false, "adj": {"A": ["B","C"], "B": ["C"], ...}}
      2) .txt (formato simples descrito no cabeçalho)
    """
    if path.lower().endswith(".json"):
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        g = Graph(bool(data.get("directed", False)))
        for u, nbrs in data.get("adj", {}).items():
            g.add_vertex(u)
            for v in nbrs:
                g.add_vertex(v)
                g.add_edge(u, v)
        if directed_override is not None and directed_override != g.directed:
            # Se o usuário quiser forçar outra direção, reconstruímos
            g2 = Graph(directed_override)
            # Reinsere as arestas respeitando a direção desejada
            for u, nbrs in g.adj.items():
                for v in nbrs:
                    if g.directed or directed_override:  # se qualquer um for dirigido, u->v é mantido
                        g2.add_vertex(u); g2.add_vertex(v); g2.add_edge(u, v)
                    else:
                        g2.add_vertex(u); g2.add_vertex(v); g2.add_edge(u, v)  # não dirigido já duplica
            return g2
        return g

    # Formato .txt
    directed = False
    declared_vertices: List[str] = []
    edges: List[Tuple[str, str]] = []

    with open(path, "r", encoding="utf-8") as f:
        for raw in f:
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            if line.upper().startswith("DIRECTED="):
                value = line.split("=", 1)[1].strip()
                directed = value in ("1", "true", "True", "TRUE")
                continue
            if line.upper().startswith("V="):
                after = line.split("=", 1)[1].strip()
                declared_vertices.extend(after.split())
                continue
            # aresta "u v"
            parts = line.split()
            if len(parts) != 2:
                raise ValueError(f"Linha inválida na entrada: {line!r}. Esperado formato 'u v'.")
            u, v = parts
            edges.append((u, v))

    if directed_override is not None:
        directed = directed_override

    g = Graph(directed=directed)
    for v in declared_vertices:
        g.add_vertex(v)
    for u, v in edges:
        g.add_vertex(u)
        g.add_vertex(v)
        g.add_edge(u, v)
    return g


def _order_candidates_by_heuristic(g: Graph, candidates: Iterable[str]) -> List[str]:
    """Heurística simples: ordena por grau crescente para reduzir branching."""
    return sorted(candidates, key=lambda x: len(g.adj[x]))


def hamiltonian_paths(g: Graph, start: Optional[str] = None, all_paths: bool = False) -> List[List[str]]:
    """
    Retorna uma lista com 1 ou vários caminhos hamiltonianos.
    - start: vértice inicial fixo, se None tenta iniciar de cada vértice.
    - all_paths: se True, coleta todos os caminhos; senão, para ao achar o primeiro.

    Complexidade: O(exponencial) no pior caso, típico de backtracking.
    """
    n = len(g.adj)
    if n == 0:
        return []

    results: List[List[str]] = []
    vertices = list(g.adj.keys())

    def backtrack(curr: str, visited: Set[str], path: List[str]) -> bool:
        if len(path) == n:
            results.append(path.copy())
            return not all_paths  # True se queremos parar cedo

        # candidatos são vizinhos ainda não visitados
        nxt_candidates = [v for v in g.neighbors(curr) if v not in visited]

        # heurística de ordenação
        for nxt in _order_candidates_by_heuristic(g, nxt_candidates):
            visited.add(nxt)
            path.append(nxt)
            should_stop = backtrack(nxt, visited, path)
            path.pop()
            visited.remove(nxt)
            if should_stop:
                return True
        return False

    def try_from(source: str) -> bool:
        visited: Set[str] = {source}
        return backtrack(source, visited, [source])

    if start is not None:
        if start not in g.adj:
            raise ValueError(f"O vértice inicial '{start}' não existe no grafo.")
        try_from(start)
    else:
        # Tenta iniciar por todos os vértices (ordenados por grau crescente como heurística extra)
        for v in _order_candidates_by_heuristic(g, vertices):
            should_stop = try_from(v)
            if (not all_paths) and results:
                break

    return results


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Busca Caminho Hamiltoniano via backtracking."
    )
    parser.add_argument("-i", "--input", help="Caminho do arquivo do grafo (.txt ou .json).", required=True)
    parser.add_argument("--start", help="Vértice inicial (opcional).")
    parser.add_argument("--all", action="store_true", help="Listar todos os caminhos hamiltonianos encontrados.")
    parser.add_argument("--directed", action="store_true", help="Força interpretação como grafo dirigido (ignora DIRECTED=).")
    args = parser.parse_args(argv)

    if not os.path.exists(args.input):
        print(f"Arquivo não encontrado: {args.input}", file=sys.stderr)
        return 2

    try:
        g = parse_graph(args.input, directed_override=True if args.directed else None)
    except Exception as e:
        print(f"Erro ao carregar grafo: {e}", file=sys.stderr)
        return 2

    try:
        paths = hamiltonian_paths(g, start=args.start, all_paths=args.all)
    except Exception as e:
        print(f"Erro na busca: {e}", file=sys.stderr)
        return 2

    if not paths:
        print("NOT-FOUND")
        return 1

    print("FOUND")
    if args.all:
        for idx, p in enumerate(paths, 1):
            print(f"{idx}: {' -> '.join(p)}")
    else:
        print("Path:", " -> ".join(paths[0]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

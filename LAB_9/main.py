import networkx as nx
import matplotlib.pyplot as plt
from collections import deque


def check_bipartite(edges, n):
    graph = [[] for _ in range(n + 1)]
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)
    
    color = [-1] * (n + 1)
    for start in range(1, n + 1):
        if color[start] == -1:
            queue = deque([start])
            color[start] = 0
            while queue:
                u = queue.popleft()
                for v in graph[u]:
                    if color[v] == -1:
                        color[v] = color[u] ^ 1
                        queue.append(v)
                    elif color[v] == color[u]:
                        return False, color
    return True, color

def make_bipartite(edges):
    all_nodes = set()
    for u, v in edges:
        all_nodes.add(u)
        all_nodes.add(v)
    n = max(all_nodes)
    
    current_edges = edges[:]
    for _ in range(len(edges)):
        ok, color = check_bipartite(current_edges, n)
        if ok:
            return current_edges, color
        
        for u, v in current_edges:
            if color[u] == color[v]:
                current_edges.remove((u, v))
                break
    
    return current_edges, color

def kuhn(edges, left, right, n):
    graph = [[] for _ in range(n + 1)]
    for u, v in edges:
        graph[u].append(v)
    
    match_to = {}
    match_from = {}
    
    def dfs(v):
        for to in graph[v]:
            if used[to]:
                continue
            used[to] = True
            if to not in match_to or dfs(match_to[to]):
                match_to[to] = v
                match_from[v] = to
                return True
        return False
    
    matching = []
    for v in left:
        used = [False] * (n + 1)
        if dfs(v):
            matching.append((v, match_from[v]))
    return matching

def ford_fulkerson(edges, left, right, n):
    source, sink = 0, n + 1
    cap = {}
    adj = [[] for _ in range(n + 2)]
    
    def add_edge(u, v, c):
        adj[u].append(v)
        adj[v].append(u)
        cap[(u, v)] = c
        cap[(v, u)] = 0
    
    for u in left:
        add_edge(source, u, 1)
    for u, v in edges:
        add_edge(u, v, 1)
    for v in right:
        add_edge(v, sink, 1)
    
    def bfs(parent):
        visited = [False] * (n + 2)
        q = deque([source])
        visited[source] = True
        while q:
            u = q.popleft()
            for v in adj[u]:
                if not visited[v] and cap.get((u, v), 0) > 0:
                    visited[v] = True
                    parent[v] = u
                    if v == sink:
                        return True
                    q.append(v)
        return False

    parent = [-1] * (n + 2)
    while bfs(parent):
        v = sink
        while v != source:
            u = parent[v]
            cap[(u, v)] -= 1
            cap[(v, u)] += 1
            v = u
        parent = [-1] * (n + 2)
    
    matching = []
    used_right = set()
    
    for u in left:
        for v in adj[u]:
            if v != source and v != sink and cap.get((u, v), 0) == 0:
                if (u, v) in edges or (v, u) in edges:
                    if v not in used_right:
                        matching.append((u, v))
                        used_right.add(v)
                        break
    
    return matching

def visualize(edges, matching, title):
    G = nx.Graph()
    G.add_edges_from(edges)
    pos = nx.spring_layout(G, seed=1, k=2)
    
    plt.figure(figsize=(8, 6))
    nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=500)
    nx.draw_networkx_edges(G, pos, edgelist=edges, edge_color='gray', width=1)
    nx.draw_networkx_edges(G, pos, edgelist=matching, edge_color='red', width=3)
    nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold')
    plt.title(title)
    plt.axis('off')

if __name__ == '__main__':
    edges = [
    (4, 6), (2, 14), (5, 14), (7, 14), (10, 14), (7, 16), (6, 9),
    (3, 16), (6, 7), (3, 14), (12, 14), (9, 14), (2, 6), (6, 12),
    (6, 15), (10, 16), (13, 14), (2, 16), (13, 16), (3, 6),
    (9, 16), (6, 10), (11, 14), (6, 13), (6, 8), (4, 16),
    (6, 11), (5, 6), (11, 16), (14, 15), (12, 16), (8, 16),
    (5, 16), (8, 14), (15, 16)
    ]
    all_nodes = set()
    for u, v in edges:
        all_nodes.add(u)
        all_nodes.add(v)
    n = max(all_nodes)

    is_bip, colors = check_bipartite(edges, n)
    if is_bip:
        print("Граф двудольный")
        bip_edges = edges
    else:
        print("Граф не двудольный")
        bip_edges, colors = make_bipartite(edges)
        print(f"Удалено ребер: {len(edges) - len(bip_edges)}")

    left = [v for v in range(1, n + 1) if colors[v] == 0]
    right = [v for v in range(1, n + 1) if colors[v] == 1]

    print(f"\nЛевая доля: {left}")
    print(f"Правая доля: {right}")

    matching_kuhn = kuhn(bip_edges, left, right, n)
    print(f"\nАлгоритм увеличивающих цепей: паросочетание размера {len(matching_kuhn)}")
    print(f"Паросочетание: {matching_kuhn}")

    matching_ff = ford_fulkerson(bip_edges, left, right, n)
    print(f"\nАлгоритм Форда-Фалкерсона: паросочетание размера {len(matching_ff)}")
    print(f"Паросочетание: {matching_ff}")

    visualize(bip_edges, matching_kuhn, "Максимальное паросочетание\nАлгоритм увеличивающих цепей")
    visualize(bip_edges, matching_ff, "Максимальное паросочетание\nАлгоритм Форда-Фалкерсона")
    plt.show()
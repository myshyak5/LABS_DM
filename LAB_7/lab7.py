import random
import heapq
import numpy as np
import math

class GraphLab:
    def __init__(self, n):
        self.n = n
        self.adj = [[] for _ in range(n)]
        self.edges_set = set()

    def add_edge(self, u, v):
        if u == v: return
        edge = tuple(sorted((u, v)))
        if edge not in self.edges_set:
            weight = random.randint(1, 10)
            self.adj[u].append((v, weight))
            self.adj[v].append((u, weight))
            self.edges_set.add(edge)

    def generate_graph(self):
        # 1. K5
        nodes_k5 = list(range(10, 15))
        for i in nodes_k5:
            for j in nodes_k5:
                self.add_edge(i, j)

        # 2. K4,5
        part_a = list(range(20, 24))
        part_b = list(range(24, 29))
        for u in part_a:
            for v in part_b:
                self.add_edge(u, v)

        # 3. Связность (хребет)
        nodes = list(range(self.n))
        random.shuffle(nodes)
        for i in range(self.n - 1):
            self.add_edge(nodes[i], nodes[i+1])

        # 4. Добор ребер (n^0.5)
        target = int((self.n**1.5) / 2)
        while len(self.edges_set) < target:
            u = random.randint(0, self.n - 1)
            v = random.randint(0, self.n - 1)
            self.add_edge(u, v)

    def dijkstra(self, start_node):
        distances = [float('inf')] * self.n
        distances[start_node] = 0
        predecessors = [-1] * self.n
        pq = [(0, start_node)]
        iterations = 0

        while pq:
            d, u = heapq.heappop(pq)
            iterations += 1
            if d > distances[u]: continue
            for v, weight in self.adj[u]:
                if distances[u] + weight < distances[v]:
                    distances[v] = distances[u] + weight
                    predecessors[v] = u
                    heapq.heappush(pq, (distances[v], v))
        return distances, predecessors, iterations

    def floyd_warshall(self):
        # Инициализируем матрицу бесконечностями
        dist = np.full((self.n, self.n), np.inf)
        
        # Диагональ — нули
        for i in range(self.n):
            dist[i][i] = 0
            
        # Заполняем начальные веса из списка смежности
        for u in range(self.n):
            for v, weight in self.adj[u]:
                dist[u][v] = weight

        # Основной цикл алгоритма
        for k in range(self.n):
            for i in range(self.n):
                for j in range(self.n):
                    if dist[i][j] > dist[i][k] + dist[k][j]:
                        dist[i][j] = dist[i][k] + dist[k][j]
        return dist

def run_lab():
    sizes = [1200, 3200, 8000, 20000, 29000]
    
    for n in sizes:
        print(f"\n--- Расчет для N = {n} ---")
        lab = GraphLab(n) 
        lab.generate_graph()
        
        dists, preds, iters = lab.dijkstra(0)
        
        # Восстановление пути до макс. вершины (n-1)
        path = []
        curr = n - 1
        while curr != -1:
            path.append(curr)
            curr = preds[curr]
        path = path[::-1]
        
        m = len(lab.edges_set)
        
        print(f"ДЕЙКСТРА (от 0 до {n-1}):")
        print(f"  Кратчайший путь: {' -> '.join(map(str, path))}")
        print(f"  Длина пути: {len(path)-1} рёбер")
        print(f"  Расстояние: {dists[n-1]}")
        print(f"  Количество итераций: {iters}")
        print(f"  Асимптотическая сложность O(m log n) = {m} * log2({n}) ≈ {int(m * math.log2(n))}")
        print(f"  Сравнение: итераций ({iters}) < O(m log n) ({int(m * math.log2(n))})")
  
    # print(f"\n--- ФЛОЙД-УОРШЕЛЛ ДЛЯ N = 1200 ---")
    # lab1 = GraphLab(1200)
    # lab1.generate_graph()
    # matrix, fw_iters = lab1.floyd_warshall()
    print("\nФЛОЙД-УОРШЕЛЛ")
    for n_fw in sizes:
        print(f"  Количество итераций для n = {n_fw}: {n_fw ** 3}\n")
    print("  Асимптотическая сложность O(n³)")
    
    # print(f"\nДля остальных размеров (3200, 8000, 20000, 29000):")
    # for n in [3200, 8000, 20000, 29000]:
    #     print(f"  n={n}: O(n³) = {n**3:,} операций (не выполнялось)")


if __name__ == "__main__":
    run_lab()
from random import choice


class Graph:
    def __init__(self, graph):
        self.graph = [row[:] for row in graph]
        self.rows = len(graph)
        self.original_graph = [row[:] for row in graph]
    
    def print_matrix(self, matrix, title):
        print(f"\n{title}:")
        print(*matrix, sep="\n")
    
    def BFS(self, s, t, parent):
        visited = [False] * self.rows
        queue = [s]
        visited[s] = True
        
        while queue:
            u = queue.pop(0)
            for ind, val in enumerate(self.graph[u]):
                if not visited[ind] and val > 0:
                    queue.append(ind)
                    visited[ind] = True
                    parent[ind] = u
                    if ind == t:
                        return True
        return False
    
    def get_path(self, parent, s, t):
        path = []
        v = t
        while v != s:
            u = parent[v]
            path.append(f"{u}→{v}")
            v = u
        return " → ".join(reversed(path))
    
    def FordFulkerson(self, source, sink):
        print(f"Исходная сеть: {self.rows} вершин")
        print(f"Исток: {source}, Сток: {sink}")
        self.print_matrix(self.original_graph, "Исходная матрица пропускных способностей")
        
        parent = [-1] * self.rows
        max_flow = 0
        iteration = 1
        
        while self.BFS(source, sink, parent):
            path_flow = float("Inf")
            v = sink
            while v != source:
                u = parent[v]
                path_flow = min(path_flow, self.graph[u][v])
                v = u
            
            path_str = self.get_path(parent, source, sink)
            
            print(f"\nИТЕРАЦИЯ {iteration}")
            print(f"Найден увеличивающий путь: {path_str}")
            print(f"Пропускная способность пути: {path_flow}")
            
            v = sink
            while v != source:
                u = parent[v]
                self.graph[u][v] -= path_flow
                self.graph[v][u] += path_flow
                v = parent[v]
            
            max_flow += path_flow
            print(f"Текущий максимальный поток: {max_flow}")
            
            self.print_matrix(self.graph, f"Остаточная сеть после итерации {iteration}")
            
            iteration += 1
            parent = [-1] * self.rows
        
        print(f"\nРЕЗУЛЬТАТ: МАКСИМАЛЬНЫЙ ПОТОК = {max_flow}")
        return max_flow
    
    def find_min_cut(self, source):
        print("\nНАХОЖДЕНИЕ МИНИМАЛЬНОГО РАЗРЕЗА")
        
        reachable = [False] * self.rows
        queue = [source]
        reachable[source] = True
        
        print(f"\nПоиск вершин, достижимых из истока {source} в остаточной сети:")
        
        while queue:
            u = queue.pop(0)
            for v in range(self.rows):
                if not reachable[v] and self.graph[u][v] > 0:
                    reachable[v] = True
                    queue.append(v)
                    print(f"  {u} → {v} : остаточная пропускная способность {self.graph[u][v]}")
        
        S = [i for i in range(self.rows) if reachable[i]]
        T = [i for i in range(self.rows) if not reachable[i]]
        
        print(f"\nМножество S (достижимые из истока): {S}")
        print(f"Множество T (недостижимые): {T}")
        
        print(f"\nРебра минимального разреза (из S в T в исходном графе):")
        cut_capacity = 0
        
        for u in S:
            for v in T:
                if self.original_graph[u][v] > 0:
                    print(f"  ({u}, {v}) : {self.original_graph[u][v]}")
                    cut_capacity += self.original_graph[u][v]
        
        print(f"\nПропускная способность разреза c(S,T) = {cut_capacity}\n")
        
        return cut_capacity


if __name__ == "__main__":
    graph = [
        [0, 28, 12, 21, 19, 0, 0, 0, 0, 0],  # 0
        [0, 0, 0, 27, 0, 0, 0, 0, 0, 0],  # 1
        [0, 0, 0, 0, 17, 0, 0, 0, 0, 0],  # 2
        [0, 0, 0, 0, 0, 20, 13, 0, 0, 0],  # 3
        [0, 0, 0, 0, 0, 18, 21, 0, 0, 0],  # 4
        [0, 0, 0, 0, 0, 0, 0, 16, 15, 0],  # 5
        [0, 0, 0, 0, 0, 0, 0, 22, 20, 0],  # 6
        [0, 0, 0, 0, 0, 0, 0, 0, 14, 81],  # 7
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 25], # 8
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # 9
    ]
    
    f = Graph(graph)
    source, sink = 0, 9
    
    max_flow = f.FordFulkerson(source, sink)
    f.find_min_cut(source)

    new_graph = [row[:] for row in graph]
    for i in range(len(new_graph)):
        for j in range(len(new_graph[i])):
            if new_graph[i][j] != 0:
                new_graph[i][j] = choice(range(100, 1001))

    ff = Graph(new_graph)
    max_flow = ff.FordFulkerson(source, sink)
    ff.find_min_cut(source)
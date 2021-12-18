def dijkstra(graph, source):
    pass
# 2
# 3      create vertex set Q
# 4
# 5      for each vertex v in Graph:
#     6          dist[v] ← INFINITY
# 7          prev[v] ← UNDEFINED
# 8          add v to Q
# 9      dist[source] ← 0
# 10
# 11      while Q is not empty:
#     12          u ← vertex in Q with min dist[u]
# 13
# 14          remove u from Q
# 15
# 16          for each neighbor v of u still in Q:
#     17              alt ← dist[u] + length(u, v)
# 18              if alt < dist[v]:
#     19                  dist[v] ← alt
# 20                  prev[v] ← u
# 21
# 22      return dist[], prev[]
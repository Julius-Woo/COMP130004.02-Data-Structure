alp = {chr(i + 65): i for i in range(26)}
with open ('./project2/edge.txt', 'r', encoding = "utf-8") as f:
    data = f.read()

# Parsing the data and building the adjacency list
def build_graph(data):
    graph = {}
    for line in data.strip().split('\n'):
        if line.startswith('#'):
            continue
        from_node, to_node, weight = line.split()
        weight = float(weight)

        if from_node not in graph:
            graph[from_node] = []
        if to_node not in graph:
            graph[to_node] = []

        graph[from_node].append((to_node, weight))
        # Assuming the graph is undirected
        graph[to_node].append((from_node, weight))
    return graph


# Constructing an adjacency matrix
def build_matrix(graph):
    matrix = [[0 for _ in range(len(graph))] for _ in range(len(graph))]
    for node, edges in graph.items():
        for edge in edges:
            matrix[alp[node]][alp[edge[0]]] = edge[1]
    return matrix

# graph = build_graph(data)
# matrix = build_matrix(graph)

# output
{
    'A': [('B', 7.64), ('F', 5.43)],
    'B': [('A', 7.64), ('E', 2.28)],
    'F': [('A', 5.43), ('I', 4.39), ('G', 1.5)],
    'E': [('B', 2.28), ('D', 2.54), ('L', 8.17)],
    'C': [('D', 2.36), ('G', 3.19)],
    'D': [('C', 2.36), ('H', 2.88), ('E', 2.54)],
    'G': [('C', 3.19), ('F', 1.5), ('H', 2.01), ('J', 3.94)],
    'H': [('D', 2.88), ('G', 2.01), ('K', 3.94)],
    'L': [('E', 8.17), ('K', 2.32), ('P', 3.69), ('M', 1.93)],
    'I': [('F', 4.39), ('J', 2.32), ('V', 11.04)],
    'J': [('G', 3.94), ('I', 2.32), ('K', 2.32), ('N', 3.23)],
    'K': [('H', 3.94), ('J', 2.32), ('O', 3.82), ('L', 2.32)],
    'V': [('I', 11.04), ('W', 2.76)],
    'N': [('J', 3.23), ('S', 2.91), ('O', 1.4)],
    'O': [('K', 3.82), ('N', 1.4), ('P', 2.13), ('T', 1.79)],
    'P': [('L', 3.69), ('O', 2.13), ('U', 2.47), ('Q', 2.2)],
    'M': [('L', 1.93), ('Q', 3.08)],
    'Q': [('M', 3.08), ('P', 2.2)],
    'S': [('N', 2.91), ('R', 0.84), ('T', 1.43), ('W', 2.46)],
    'T': [('O', 1.79), ('S', 1.43), ('X', 2.77), ('U', 2.18)],
    'U': [('P', 2.47), ('T', 2.18), ('Y', 1.67)],
    'R': [('S', 0.84), ('W', 3.1)],
    'W': [('R', 3.1), ('S', 2.46), ('V', 2.76), ('X', 1.43)],
    'X': [('T', 2.77), ('W', 1.43), ('Y', 2.04)],
    'Y': [('U', 1.67), ('X', 2.04), ('Z', 2.52)],
    'Z': [('Y', 2.52)]
}
def toposort(graph):
    """
    Parameters:
        - graph: a dictionary representing a graph
        
    Returns:
        - a list of vertices in topological order
    """
    def dfs(v):
        # depth first search from vertex v
        visited.add(v)
        for u, _ in graph[v]:
            if u not in visited:
                dfs(u)
        result.append(v)

    visited = set()  # visited vertices
    result = []  # topological order of vertices

    for v in graph:
        if v not in visited:
            dfs(v)

    return result[::-1]  # reverse order

def dag_longest(graph):
    '''
    Parameters:
        - graph: a dictionary representing a graph
        
    Returns:
        - a list of vertices in the longest dist, and the length of the dist
    '''
    # Perform a Topological Sort on the graph
    topo_order = toposort(graph)
    # Initialize the maximum distance and corresponding dist
    max_dist = float('-inf')
    longest_path = []
    # Check each vertex as a starting point
    for s in topo_order:
        # Initialize the distance to each vertex to be -inf and the parent to be None
        dist = {v: (float('-inf'), None) for v in graph}
        dist[s] = (0, None)
        # Relax each edge in the topological order
        for v in topo_order:
            for u, w in graph[v]:
                if dist[v][0] + w > dist[u][0]:
                    dist[u] = (dist[v][0] + w, v)
        # Find the vertex with the largest distance from s
        max_dist_cur = max(dist.values(), key=lambda x: x[0])[0]
        # Update the maximum distance and corresponding dist
        if max_dist_cur > max_dist:
            max_dist = max_dist_cur
            max_v = max(dist, key=lambda x: dist[x][0])  # the vertex with the largest distance from s
            path_tmp = []
            while max_v:
                path_tmp.append(max_v)
                max_v = dist[max_v][1]
            longest_path = path_tmp[::-1]
    
    return longest_path, max_dist


# test
# {job1: [(job2, weight), (job3, weight), ...], ...}
example1 = {1: [(2, 4), (3, 5), (4, 4)],
            2: [(5, 4), (7, 6)],
            3: [(5, 5), (6, 6)],
            4: [(6, 7)],
            5: [(7, 3), (8, 4)],
            6: [(8, 2), (9, 2)],
            7: [(10, 3)],
            8: [(10, 2)],
            9: [(10, 5)],
            10: []}
result1 = dag_longest(example1)
print("eg1. Longest path: ", result1[0], " total weights: ", result1[1])


example2 = {1: [(2, 3), (3, 2)],
            2: [(4, 2), (5, 3)],
            3: [(4, 4), (6, 3)],
            4: [(6, 2)],
            5: [(6, 1)],
            6: []}
result2 = dag_longest(example2)
print("eg2. Longest path: ", result2[0], " total weights: ", result2[1])

example3 = {1: [(2, 3), (3, 8)],
            2: [(4, 9), (5, 6)],
            3: [(2, 4), (5, 10)],
            4: [(6, 6)],
            5: [(6, 9)],
            6: []}
result3 = dag_longest(example3)
print("eg3. Longest path: ", result3[0], " total weights: ", result3[1])

example4 = {1: [(2, 2), (3, 5), (5, 5)],
            2: [(3, 2), (4, 3)],
            3: [(5, 1), (6, 3)],
            4: [(6, 2)],
            5: [(7, 6)],
            6: [(7, 3), (8, 4)],
            7: [(9, 4)],
            8: [(9, 2)],
            9: []}
result4 = dag_longest(example4)
print("eg4. Longest path: ", result4[0], " total weights: ", result4[1])
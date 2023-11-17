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
        for u in graph[v]:
            if u not in visited:
                dfs(u)
        result.append(v)
    
    visited = set()  # visited vertices
    result = []  # topological order of vertices
    
    for v in graph:
        if v not in visited:
            dfs(v)
            
    return result[::-1]  # reverse order

# test
# map course to index
courses = {
    'Java or C++': 0,
    'Web Application': 1,
    'Object Oriented Programming': 2,
    'Data Structure and Algorithm': 3,
    'Database': 4,
    'Software Engineering': 5,
    'Computer Architecture': 6,
    'Computer Systems': 7,
    'Calculus': 8,
    'Project Management': 9,
    'Computer Network': 10,
    'Intelligent Systems': 11,
    'Probability and Statistics': 12,
    'Discrete Mathematics': 13
}
graph = {0: [1,2,3], 
        1: [],
        2: [1,5],
        3: [5,11],
        4: [1,5],
        5: [9,11],
        6: [],
        7: [5,6,10],
        8: [6,12],
        9: [],
        10: [5],
        11: [],
        12: [3,11],
        13: [11]
        }

print("***Course order***")
courseindex = toposort(graph)
# print(courseindex)
for i in courseindex:
    for k, v in courses.items():
        if v == i:
            print(k)
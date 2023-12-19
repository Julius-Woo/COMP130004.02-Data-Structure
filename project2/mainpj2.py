import heapq


alp = {chr(i + 65): i for i in range(26)}  # A-Z -> 0-25

class Vertex:
    def __init__(self, id):
        '''
        Initialize a vertex of the graph.
        
        Parameters:
            - id: the id of the vertex, letter A-Z in this case.
            - ad: a dictionary of the adjacent vertices of the vertex, e.g., {'B': 7.64, 'F': 5.43}.
            - d: the distance from some source vertex to the vertex, default is infinity.
            - pi: the predecessor of the vertex, default is None.
            - paths: a list of paths from some source vertex to the vertex, e.g., [[A, B, C], [A, D, C]].
        '''
        self.id = id
        self.ad = {}
        self.d = float('inf')
        self.pi = None
        self.paths = []
        self.rank = 0  # only used in union-by-rank in Kruskal's algorithm
    
    def add_neighbour(self, neighbour, weight):
        '''Add a neighbour to the vertex.'''
        self.ad[neighbour] = weight
        
    def set_distance(self, distance):
        '''Set the distance of the vertex.'''
        self.d = distance
    
    def set_predecessor(self, predecessor):
        '''Set the predecessor of the vertex.'''
        self.pi = predecessor
    
    def set_rank(self, rank):
        '''Set the rank of the vertex.'''
        self.rank = rank
        
    def __str__(self):
        """ String representation of the vertex. """
        return self.id
    
    def __eq__(self, other):
        '''Override the default Equals behavior.'''
        return self.id == other.id

    def __hash__(self):
        '''Override the default hash behavior (so that returns the id).'''
        return hash(self.id)
    
    def __lt__(self, other):
        '''Override the default Less than behavior.'''
        return self.id < other.id

class Graph:
    def __init__(self, vertices=None):
        '''
        Initialize a graph object.
        
        Parameters:
            - vertices: a list of vertices in the graph, default is None.
            - allpaths: a 2D list of all shortest paths between any two vertices, e.g., all_paths[U][V] = [[U, X, Y, V], [U, Z, V], ...]
        '''
        self.v = vertices if vertices is not None else []
        self.allpaths = [[[] for _ in range(len(self.v))] for _ in range(len(self.v))]
        
        for i in range(len(self.v)):
            self.allpaths[i][i].append([self.v[i]])
    
    def get_edges(self):
        '''Get the edges of the graph.'''
        edges = []
        for u in self.v:
            for v in u.ad:
                edges.append((u, v, u.ad[v]))
        return edges
    
    def get_matrix(self):
        '''Get the adjacency matrix of the graph.'''
        n = len(self.v)
        matrix = [[float('inf')] * n for _ in range(n)]
        for u in self.v:
            for v in u.ad:
                matrix[alp[u.id]][alp[v.id]] = u.ad[v]
        for i in range(n):
            matrix[i][i] = 0
        return matrix
    
    '''
    For finding the single-source shortest path.
    '''
    
    def _inti_singlesource(self, s):
        '''Initialize the single-source shortest path.'''
        for v in self.v:
            v.set_distance(float('inf'))
            v.set_predecessor(None)
            v.paths = []
        s.set_distance(0)
        s.paths = [[s]]
        
    def _relax(self, u, v):
        '''Relax the edge (u, v).'''
        if v.d > u.d + u.ad[v]:
            v.set_distance(u.d + u.ad[v])
            v.set_predecessor(u)
            v.paths = [path + [v] for path in u.paths]  # update the paths
        # if there are multiple shortest paths
        elif v.d == u.d + u.ad[v]:
            add_paths = [path + [v] for path in u.paths]  # add the paths
            v.paths.extend(add_paths)
    
    def dijkstra(self, s):
        '''Dijkstra's algorithm for finding the single-source shortest path.'''
        # initialize the single-source shortest path
        self._inti_singlesource(s)
        # initialize the priority queue
        pq = []
        # initialize the vertices
        for v in self.v:
            heapq.heappush(pq, (v.d, v))
        s.paths = [[s]]  # initialize the paths
        # while the priority queue is not empty
        while pq:
            # extract the vertex with the minimum distance
            cur_d, u = heapq.heappop(pq)
            if cur_d > u.d:  # if the distance is not updated, skip
                continue
            # for each vertex v adjacent to u
            for v in u.ad:
                old_d = v.d
                # relax the edge (u, v)
                self._relax(u, v)
                # if the distance is updated, reinsert v with new distance
                if v.d < old_d:
                    heapq.heappush(pq, (v.d, v))
        # update the allpaths
        for u in self.v:
            self.allpaths[alp[s.id]][alp[u.id]] = u.paths
    
    '''
    For finding the all-pairs shortest path.
    '''
    
    def floydwarshall(self):
        '''Floyd-Warshall algorithm for finding the all-pairs shortest path.'''
        W = self.get_matrix()  # get the adjacency matrix
        n = len(W)
        D = W.copy()  # initialize the distance matrix
        # initialize the allpaths
        self.allpaths = [[[] for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if i == j:
                    self.allpaths[i][j] = [[self.v[i]]]
                elif W[i][j] != float('inf'):
                    self.allpaths[i][j] = [[self.v[i], self.v[j]]]
        # Update the distance and paths matrices
        for k in range(n):
            Dk = D.copy()
            for i in range(n):
                for j in range(n):
                    if D[i][j] > D[i][k] + D[k][j]:
                        Dk[i][j] = D[i][k] + D[k][j]
                        # update the paths
                        self.allpaths[i][j] = [
                            path1 + (path2 if len(path2) == 1 else path2[1:])
                            for path1 in self.allpaths[i][k]
                            for path2 in self.allpaths[k][j]
                        ]
                    elif D[i][j] == D[i][k] + D[k][j] and i != k and j != k:
                        # add the paths
                        add_paths = [path1 + path2[1:] for path1 in self.allpaths[i][k] for path2 in self.allpaths[k][j]]
                        for path in add_paths:
                            if path not in self.allpaths[i][j]:
                                self.allpaths[i][j].append(path)
            D = Dk.copy()
        return D
    
    def dijkstra_allpairs(self):
        '''Dijkstra's algorithm for finding the all-pairs shortest path.'''
        # initialize the allpaths
        for i in range(len(self.v)):
            self.allpaths[i][i].append([self.v[i]])
        # for each vertex s
        for s in self.v:
            self.dijkstra(s)

    def get_pathstr(self, u, v):
        '''Get the shortest path from vertex u to vertex v as a string.'''
        paths = self.allpaths[alp[u.id]][alp[v.id]]
        if not paths:
            return 'No path from {} to {} exists.'.format(u.id, v.id)
        paths_str = []
        for path in paths:
            path_str = ' -> '.join(str(vertex) for vertex in path)
            paths_str.append(path_str)

        return '\n'.join(paths_str)
    
    def calc_path(self, path):
        '''Calculate the length of a path, e.g. [A,B,C,...]'''
        length = 0
        for i in range(len(path) - 1):
            length += path[i].ad[path[i + 1]]
        return f'{length:.2f}'
    
    '''
    For constructing the minimum spanning tree.
    '''
    
    def mst_kruskal(self):
        '''
        Krukal's algorithm for finding the minimum spanning tree of a graph.
        
        Returns:
            - mst: the minimum spanning tree of the graph.
        '''
        # initialize the minimum spanning tree
        mst = []
        # initialize the disjoint-set data structure
        for v in self.v:
            self._makeset(v)
        # sort the edges of the graph by weight
        edges = self.get_edges()
        edges.sort(key=lambda x: x[2])
        for u, v, w in edges:
            # if the two vertices are in different sets
            if self._findset(u) != self._findset(v):
                # add the edge to the minimum spanning tree
                mst.append((u, v, w))
                # union the two sets
                self._unionset(u, v)
        return mst

    def _makeset(self, x):
        '''Make a set containing x.'''
        x.pi = x
        x.rank = 0

    def _unionset(self, x, y):
        '''Union the sets that contain x and y.'''
        self._linkset(self._findset(x), self._findset(y))

    def _linkset(self, x, y):
        '''Link the set that contains x to the set that contains y.'''
        if x.rank > y.rank:
            y.pi = x
        else:
            x.pi = y
            if x.rank == y.rank:
                y.rank += 1

    def _findset(self, x):
        '''Find the set that contains x.'''
        # if x is not the root
        if x != x.pi:
            # set the parent of x to the root of the set that contains x
            x.pi = self._findset(x.pi)
        return x.pi

    def mst_prim(self, r):
        '''
        Prim's algorithm for finding the minimum spanning tree of a graph.
        
        Parameters:
            - r: the root of the minimum spanning tree.
        
        Returns:
            - mst: the minimum spanning tree of the graph.
        '''
        # initialize
        for u in self.v:
            u.set_distance(float('inf'))
            u.set_predecessor(None)
        r.set_distance(0)
        pq = []
        in_pq = set()  # a set of vertices in the priority queue
        for v in self.v:
            heapq.heappush(pq, (v.d, v))
            in_pq.add(v.id)
        while pq:
            _, u = heapq.heappop(pq)
            if u.id in in_pq:
                in_pq.remove(u.id)
            else:
                continue
            for v in u.ad:
                if v.id in in_pq and u.ad[v] < v.d:
                    v.set_distance(u.ad[v])
                    v.set_predecessor(u)
                    heapq.heappush(pq, (v.d, v))
        # construct the minimum spanning tree
        mst = []
        for u in self.v:
            if u.pi is not None:
                mst.append((u.pi, u, u.ad[u.pi]))
        return mst

    def print_mst(self, mst):
        '''Print the mst and the total weight.'''
        total_weight = 0
        for u, v, w in mst:
            print('{} -> {} : {}'.format(u.id, v.id, w))
            total_weight += w
        print(f'Total weight: {total_weight:.2f}')
        return f'{total_weight:.2f}'
    
    '''
    For finding the bus route.
    '''
    
    def maxpathcount(self):
        '''Show the max count of the shortest path between any two vertices'''
        self.dijkstra_allpairs()
        max_paths = 0
        n = len(self.v)
        for i in range(n):
            for j in range(n):
                tmp = len(self.allpaths[i][j])
                if tmp > max_paths:
                    max_paths = tmp
        return max_paths

    def bus_route(self, r):
        '''Find the bus route from the root r.'''
        self.dijkstra_allpairs()
        sid = alp[r.id]
        # store the bus route edges, avoiding duplicates
        edges = set()
        # total length of the bus route
        total = 0
        for paths in self.allpaths[sid]:
            if paths:
                path = paths[0]
                if len(path) == 1:
                    continue
                for i in range(len(path) - 1):
                    u, v = path[i], path[i + 1]
                    edge = (u, v) if u.id < v.id else (v, u)
                    if edge not in edges:
                        edges.add(edge)
                        total += u.ad[v]
        return f'{total:.2f}', edges

    '''
    Initialize the graph.
    '''
    
    def init_adjlist(self, filename):
        '''Parsing the data and building the adjacency list'''
        with open (filename, 'r', encoding = "utf-8") as f:
            data = f.read()
        graphtmp = {}
        for line in data.strip().split('\n'):
            if line.startswith('#'):
                continue
            from_id, to_id, weight = line.split()
            weight = float(weight)
            if from_id not in graphtmp:  # if the vertex is not in the graph, add it
                graphtmp[from_id] = Vertex(from_id)
            if to_id not in graphtmp:
                graphtmp[to_id] = Vertex(to_id)
            graphtmp[from_id].add_neighbour(graphtmp[to_id], weight)  # add the edge
            graphtmp[to_id].add_neighbour(graphtmp[from_id], weight)
        self.v = sorted(graphtmp.values(), key=lambda x: x.id)  # sort the vertices by id(A-Z)
        self.allpaths = [[[] for _ in range(len(self.v))] for _ in range(len(self.v))]
        for i in range(len(self.v)):
            self.allpaths[i][i].append([self.v[i]])



# filepath = './edge.txt'
# map1 = Graph()
# map1.init_adjlist(filepath)
# n = len(map1.v)
# # print(map1.maxpathcount())
# # print(map1.bus_route(map1.v[2])[0])
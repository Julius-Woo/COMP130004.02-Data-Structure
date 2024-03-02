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
        '''
        self.id = id
        self.ad = {}
        self.d = float('inf')
        self.pi = None
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
        """ String representation of the vertex and its neighbors. """
        return f"Vertex {self.id}, neighbors: {self.ad}"
    
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
        '''
        self.v = vertices if vertices is not None else []
    
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
        for v in self.v:
            heapq.heappush(pq, (v.d, v))
        while pq:
            cur_d, u = heapq.heappop(pq)
            if cur_d > u.d:
                continue
            for v in u.ad:
                if v in pq and v.d > u.ad[v]:
                    v.set_distance(u.ad[v])
                    v.set_predecessor(u)
                    heapq.heappush(pq, (v.d, v))
        # construct the minimum spanning tree
        mst = []
        for u in self.v:
            if u.pi is not None:
                mst.append((u.pi, u, u.ad[u.pi]))
        return mst
    
    def _inti_singlesource(self, s):
        '''Initialize the single-source shortest path.'''
        for v in self.v:
            v.set_distance(float('inf'))
            v.set_predecessor(None)
        s.set_distance(0)
        
    def _relax(self, u, v):
        '''Relax the edge (u, v).'''
        if v.d > u.d + u.ad[v]:
            v.set_distance(u.d + u.ad[v])
            v.set_predecessor(u)
    
    def djkstra(self, s):
        '''Dijkstra's algorithm for finding the single-source shortest path.'''
        # initialize the single-source shortest path
        self._inti_singlesource(s)
        # initialize the priority queue
        pq = []
        # initialize the vertices
        for v in self.v:
            heapq.heappush(pq, (v.d, v))
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
    
    def bellmanford(self, s):
        '''Bellman-Ford algorithm for finding the single-source shortest path.'''
        # initialize the single-source shortest path
        self._inti_singlesource(s)
        # for i in range(len(self.v) - 1)
        for _ in range(len(self.v) - 1):
            # for each edge (u, v)
            for u in self.v:
                for v in u.ad:
                    # relax the edge (u, v)
                    self._relax(u, v)
        # for each edge (u, v)
        for u in self.v:
            for v in u.ad:
                # if there is a negative-weight cycle
                if v.d > u.d + u.ad[v]:
                    # return False
                    return False
        # return True
        return True
    
    def floydwarshall(self):
        '''Floyd-Warshall algorithm for finding the all-pairs shortest path.'''
        W = self.get_matrix()  # get the adjacency matrix
        n = len(W)
        D = W.copy()  # initialize the distance matrix
        # initialize the predecessor matrix
        Pi = [[None] * n for _ in range(n)]
        for u in self.v:
            for v in u.ad:
                Pi[alp[u.id]][alp[v.id]] = u
        # Update the distance and predecessor matrices
        for k in range(n):
            Dk = D.copy()
            for i in range(n):
                for j in range(n):
                    if D[i][j] > D[i][k] + D[k][j]:
                        Dk[i][j] = D[i][k] + D[k][j]
                        Pi[i][j] = Pi[k][j]
            D = Dk.copy()
        return D, Pi
    
    def johnson(self):
        '''Johnson's algorithm for finding the all-pairs shortest path.'''
        # initialize the single-source shortest path
        g1 = Graph(self.v)  # copy the graph
        s = Vertex('s')  # add a new vertex s
        g1.v.append(s)
        for v in g1.v:
            s.add_neighbour(v, 0)
        # run Bellman-Ford algorithm
        if not g1.bellmanford(s):  # if there is a negative-weight cycle
            return False
        # reweight the graph
        h = {}
        for u in g1.v:
            h[u] = u.d
            for v in u.ad:
                u.ad[v] += h[u] - h[v]
        # initialize the all-pairs shortest path
        n = len(self.v)
        D = [[float('inf')] * n for _ in range(n)]
        for i in range():
            D[i][i] = 0
            
        # initialize the predecessor matrix
        Pi = [[None] * n for _ in range(n)]
        for u in self.v:
            for v in u.ad:
                Pi[alp[u.id]][alp[v.id]] = u
        # run Dijkstra's algorithm for each vertex
        for u in self.v:
            self.djkstra(u)
            for v in self.v:
                D[alp[u.id]][alp[v.id]] = v.d + h[v] - h[u]
                if v.pi is not None:
                    Pi[alp[u.id]][alp[v.id]] = v.pi
                else:
                    Pi[alp[u.id]][alp[v.id]] = None
        # restore the graph
        for u in g1.v:
            for v in u.ad:
                u.ad[v] -= h[u] - h[v]
        return D, Pi
    
    def johnson_simple(self):
        '''Johnson's algorithm in a graph without negative-weight cycles.'''
        # initialize the all-pairs shortest path
        n = len(self.v)
        D = [[float('inf')] * n for _ in range(n)]
        for i in range(n):
            D[i][i] = 0
        # initialize the predecessor matrix
        Pi = [[None] * n for _ in range(n)]
        for u in self.v:
            for v in u.ad:
                Pi[alp[u.id]][alp[v.id]] = u
        # run Dijkstra's algorithm for each vertex
        for u in self.v:
            self.djkstra(u)
            for v in self.v:
                D[alp[u.id]][alp[v.id]] = v.d
                if v.pi is not None:
                    Pi[alp[u.id]][alp[v.id]] = v.pi
                else:
                    Pi[alp[u.id]][alp[v.id]] = None
        return D, Pi
    
    def pathprint(self, s, v):
        '''Print the path from vertex s to vertex v.'''
        if v == s:
            print(s.id, end = ' ')
        elif v.pi is None:
            print('No path from', s.id, 'to', v.id, 'exists.')
        else:
            self.pathprint(s, v.pi)
            print(v.id, end = '-->')
    
    def print_reverse(self, s, v):
        '''Print the path from vertex v to vertex s.'''
        if v == s:
            print(s.id, end = ' ')
        elif v.pi is None:
            print('No path from', s.id, 'to', v.id, 'exists.')
        else:
            print(v.id, end = '-->')
            self.print_reverse(s, v.pi)
    
    def print_allpairs(self, Pi, s, v):
        '''Print all paths from vertex s to vertex v.'''
        if v == s:
            print(s.id, end = ' ')
        elif Pi[s][v] is None:
            print('No path from', s.id, 'to', v.id, 'exists.')
        else:
            self.print_allpairs(Pi, s, Pi[s][v])
            print(v.id, end = '-->')
    
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



path = './project2/edge.txt'
mapnav = Graph()
mapnav.init_adjlist(path)
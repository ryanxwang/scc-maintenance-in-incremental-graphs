import heapq as heapq
import scc_maintainer
from scc_maintainer.scc_maintainer import SCC_Maintainer

class Vertex:
    def __init__(self, id: int, birthday: int):
        self.id = id
        self.birthday = birthday
        self.in_vertices = set([id])
        self.out_vertices = set([id])
        self.root = id
    
    def __lt__(self, other):
        return self.birthday < other.birthday


class Edge:
    def __init__(self, u: int, v: int, birthday: int):
        self.u = u
        self.v = v
        self.birthday = birthday
    
    def __lt__(self, other):
        return self.birthday < other.birthday


class SCCUnionFind(SCC_Maintainer):
    def __init__(self):
        self._time = 0
        self.unprocessed_vertices = []
        self.unprocessed_edges = []
        self.vertices = {}
        # the format for historical scc's is (leader id, birthtime (inclusive),
        # deathtime (exclusive))
        self.historical_sccs = []
    
    @property
    def time(self):
        return self._time

    @time.setter
    def time(self, t: int):
        if t < self._time:
            raise ValueError("Cannot go back in time")
        self._time = t
        self.__process()

    def get_scc_count(self) -> int:
        return len(set(map(self.__find, self.vertices)))

    def __find(self, v: int) -> int:
        """Find the root of a vertex. """
        assert (v in self.vertices), "Vertex does not exist yet"

        if self.vertices[v].root != v:
            self.vertices[v].root = self.__find(self.vertices[v].root)
        return self.vertices[v].root
    
    def __update(self, u: Vertex, v: Vertex) -> None:
        """Update the in and out sets of the structure with an added u->v edge. """
        for x in u.in_vertices:
            self.vertices[x].out_vertices.update(v.out_vertices)
            self.vertices[x].out_vertices = set(map(self.__find, self.vertices[x].out_vertices))
        
        for x in v.out_vertices:
            self.vertices[x].in_vertices.update(u.in_vertices)
            self.vertices[x].in_vertices = set(map(self.__find, self.vertices[x].in_vertices))

    def __union(self, u: Vertex, v: Vertex, t: int) -> None:
        """Merge the SCC's of u and v given an u->v edge. """
        merged_vertices = u.in_vertices.intersection(v.out_vertices)
        leaderID = next(iter(merged_vertices)) # get an arbitrary element
        for vertexID in merged_vertices:
            if self.vertices[vertexID] < self.vertices[leaderID]: # use the comparision we wrote for vertices
                leaderID = vertexID
        
        # Collect relevant information of the leader vertex and kill all merged
        # SCC's
        leader = self.vertices[leaderID]
        for vertexID in merged_vertices:
            if vertexID == leaderID:
                continue
            
            vertex = self.vertices[vertexID]
            self.historical_sccs.append((vertex.id, vertex.birthday, t))
            vertex.root = leaderID

            leader.in_vertices.update(vertex.in_vertices)
            leader.out_vertices.update(vertex.out_vertices)
        
        leader.in_vertices = set(map(self.__find, leader.in_vertices))
        leader.out_vertices = set(map(self.__find, leader.out_vertices))

        # Update relevant vertices in the graph
        for x in leader.in_vertices:
            self.vertices[x].out_vertices.update(leader.out_vertices)
            self.vertices[x].out_vertices = set(map(self.__find, self.vertices[x].out_vertices))
        
        for x in leader.out_vertices:
            self.vertices[x].in_vertices.update(leader.in_vertices)
            self.vertices[x].in_vertices = set(map(self.__find, self.vertices[x].in_vertices))

    def __process(self) -> None:
        """Process all unprocessed additions that took place before or at 
        `self.time`. 
        """
        # first process all the vertices
        while len(self.unprocessed_vertices) != 0:
            if self.unprocessed_vertices[0].birthday > self.time:
                break
            id = self.unprocessed_vertices[0].id
            self.vertices[id] = heapq.heappop(self.unprocessed_vertices)
        
        # then add the edges
        while len(self.unprocessed_edges) != 0:
            if self.unprocessed_edges[0].birthday > self.time:
                break
            edge = heapq.heappop(self.unprocessed_edges)
            u = self.__find(edge.u)
            v = self.__find(edge.v)

            # if the edge does not do anything then ignore it
            if v in self.vertices[u].out_vertices:
                continue

            # if edge does not merge SCC's then update in and out sets
            if v not in self.vertices[u].in_vertices:
                self.__update(self.vertices[u], self.vertices[v])
            
            # if edge merges SCC's
            if v in self.vertices[u].in_vertices:
                self.__union(self.vertices[u], self.vertices[v], edge.birthday)

    def __add_vertex(self, v: Vertex) -> None:
        heapq.heappush(self.unprocessed_vertices, v)
        self.__process()

    def add_vertex(self, id: int, birthday: int) -> None:
        """Add a vertex to the structure. """
        assert (self.time <= birthday), "Cannot change history"

        self.__add_vertex(Vertex(id, birthday))

    def __add_edge(self, e: Edge) -> None:
        heapq.heappush(self.unprocessed_edges, e)
        self.__process()
    
    def add_edge(self, u: int, v: int, birthday: int) -> None:
        """Add an edge to the structure. """
        assert (self.time <= birthday), "Cannot change history"

        self.__add_edge(Edge(u, v, birthday))

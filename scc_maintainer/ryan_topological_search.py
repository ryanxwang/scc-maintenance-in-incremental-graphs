from distutils import errors
from distutils.log import error
from scc_maintainer import SCC_Maintainer
import heapq

class Vertex:
    def __init__(self, id: int, birthday: int):
        self.id = id
        self.birthday = birthday
        self.root = id
        self.next = set() # all the immediately reachable vertices
        self.prev = set() # all the vertices immediately reachable to me

    def __lt__(self, other):
        return self.birthday < other.birthday

class Edge:
    def __init__(self, u: int, v: int, birthday: int):
        self.u = u
        self.v = v
        self.birthday = birthday
        
    def __lt__(self, other):
        return self.birthday < other.birthday


class TopoSearchSCCMaintainer(SCC_Maintainer):
    def __init__(self):
        self._time = 0
        self.unprocessed_vertices = []
        self.unprocessed_edges = []
        self.vertices = [] # topologically ordered
        self.position = {}
    
    @property
    def time(self):
        return self._time
    
    @time.setter
    def time(self, t: int):
        if t < self._time:
            raise ValueError("Cannot go back in time")
        self._time = t
        self.__process()
    
    def __find(self, v: int) -> int:
        """Find the root of a vertex. """
        # assert (v in self.vertices), "Vertex does not exist yet"

        if self.vertices[self.position[v]].root != v:
            self.vertices[self.position[v]].root = self.__find(self.vertices[self.position[v]].root)
        return self.vertices[self.position[v]].root

    def __topological_search(self, u: Vertex, v: Vertex):
        F = []
        B = []
        F.append(v)
        B.append(u)
        i, j = self.position[v.id], self.position[u.id]
        
        if i <= j:
            self.vertices[j].next.add(v.id)
            self.vertices[i].prev.add(u.id)
            return

        self.vertices[i] = None
        self.vertices[j] = None

        # run topological search
        while True:
            i = i - 1
            while i > j:
                reachable = False
                for f in F:
                    if self.vertices[i].id in f.next:
                        reachable = True
                        break
                if reachable:
                    break
                else:
                    i = i - 1
            if i == j:
                break
            else:
                F.append(self.vertices[i])
                self.vertices[i] = None
            
            j = j + 1
            while i > j:
                reachable = False
                for b in B:
                    if self.vertices[j].id in b.prev:
                        reachable = True
                        break
                if reachable:
                    break
                else:
                    j = j + 1
            if i == j:
                break
            else:
                B.append(self.vertices[j])
                self.vertices[j] = None

        # handle cycles
        hasCycle = False
        for f in F:
            for b in B:
                if b.id in f.next:
                    hasCycle = True

        # reorder
        while len(F) != 0:
            if self.vertices[i] is not None:
                reachable = False
                for f in F:
                    if self.vertices[i].id in f.next:
                        reachable = True
                        break
                if reachable:
                    F.append(self.vertices[i])
                    self.vertices[i] = None
            
            if self.vertices[i] is None:
                x = F.pop(0)
                self.vertices[i] = x
                self.position[x.id] = i
            i = i - 1

        while len(B) != 0:
            j = j + 1
            if self.vertices[j] is not None:
                reachable = False
                for b in B:
                    if self.vertices[j].id in b.prev:
                        reachable = True
                        break
                if reachable:
                    B.append(self.vertices[j])
                    self.vertices[j] = None
            
            if self.vertices[j] is None:
                x = B.pop(0)
                self.vertices[j] = x
                self.position[x.id] = j
        
        # if there is a cycle, merge, otherwise add edge
        if hasCycle:
            raise ValueError("Has cycle")
            # TODO implement this
        else:
            self.vertices[self.position[u.id]].next.add(v.id)
            self.vertices[self.position[v.id]].prev.add(u.id)


    def __process(self):
        """Process all unprocessed additions that took place before or at 
        `self.time`. 
        """
        # first process all the vertices
        while len(self.unprocessed_vertices) != 0:
            if self.unprocessed_vertices[0].birthday > self.time:
                break
            v = heapq.heappop(self.unprocessed_vertices)
            self.vertices.append(v)
            self.position[v.id] = len(self.vertices) - 1
        
        # then add the edges
        while len(self.unprocessed_edges) != 0:
            if self.unprocessed_edges[0].birthday > self.time:
                break
            edge = heapq.heappop(self.unprocessed_edges)
            u = self.__find(edge.u)
            v = self.__find(edge.v)

            self.__topological_search(self.vertices[self.position[u]], self.vertices[self.position[v]])

    def get_scc_count(self) -> int:
        return len(list(map(lambda x: self.__find(x.id), self.vertices)))

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

S = TopoSearchSCCMaintainer()
S.add_vertex(0, 0)
S.add_vertex(1, 1)
S.add_edge(1, 0, 1)
S.time = 1
S.add_vertex(2, 2)
S.add_edge(2, 1, 2)
S.add_edge(2, 0, 2)
S.add_edge(0, 2, 2)
S.time = 2
pass
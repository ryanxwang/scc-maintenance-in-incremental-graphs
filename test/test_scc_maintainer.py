import unittest
from src.topological_search import TopoSearchSCCMaintainer

# change this line to change the implementation tested
target = TopoSearchSCCMaintainer
# target = SCCUnionFind

def try_filtration_scc_count(vertices, edges, time):
    S = target()
    for vertex in vertices:
        S.add_vertex(vertex[0], vertex[1])
    for edge in edges:
        S.add_edge(edge[0], edge[1], edge[2])
    
    actual = []
    for i in range(time + 1):
        S.time = i
        actual.append(S.get_scc_count())
    
    return actual


class TestSCCMaintainer(unittest.TestCase):
    def testSmallFiltrations(self):
        self.assertListEqual(try_filtration_scc_count(
            vertices = [(1, 1), (2, 1), (3, 2), (4, 2), (5, 3)],
            edges = [(1, 2, 1), (3, 1, 2), (3, 4, 2), (2, 4, 2), (3, 5, 3), (4, 1, 3), (2, 5, 3), (4, 5, 3)],
            time = 3,
        ), [0, 2, 4, 3])

        self.assertListEqual(try_filtration_scc_count(
            vertices = [(1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1), (8, 1)],
            edges = [(1, 4, 1), (2, 3, 1), (3, 5, 1), (4, 5, 1), (4, 7, 1), (5, 6, 1), (5, 6, 1), (6, 8, 1), (7, 8, 1), (7, 1, 2), (8, 3, 2)], 
            time = 2,
        ), [0, 8, 3])

        self.assertListEqual(try_filtration_scc_count(
            vertices = [(1, 1), (2, 1), (3, 1), (4, 1)],
            edges = [(1, 2, 1), (1, 3, 1), (1, 4, 1), (1, 1, 1), (3, 2, 2), (4, 3, 2), (3, 1, 3)],
            time = 3,
        ), [0, 4, 4, 2])
    
    def testChain(self):
        S = target()
        S.add_vertex(0, 0)
        for i in range(1, 1000):
            S.add_vertex(i, i)
            S.add_edge(i - 1, i, i)
            S.time = i
            self.assertEquals(S.get_scc_count(), i + 1)
        
        S = target()
        S.add_vertex(0, 0)
        for i in range(1, 1000):
            S.add_vertex(i, i)
            S.add_edge(i, i - 1, i)
            S.time = i
            self.assertEquals(S.get_scc_count(), i + 1)
    
    def testCompleteDAG(self):
        S = target()
        S.add_vertex(0, 0)
        for i in range(1, 500):
            S.add_vertex(i, i)
            for j in range(i):
                S.add_edge(i, j, i)
            S.time = i
            self.assertEquals(S.get_scc_count(), i + 1)

    def testCompleteGraph(self):
        S = target()
        S.add_vertex(0, 0)
        for i in range(1, 1500):
            S.add_vertex(i, i)
            for j in range(i):
                S.add_edge(i, j, i)
                S.add_edge(j, i, i)
            S.time = i
            self.assertEquals(S.get_scc_count(), 1)


if __name__ == '__main__':
    unittest.main()

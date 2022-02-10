# scc-maintenance-in-incremental-graphs
Implementation of relevant algorithms to the maintenance of strong components in incremental graphs

Currently has:
- implementation of a naive algorithm (`scc_union_find.py`)
- (under work) implementation of the topological search algorithm as per [Haeupler et al](https://dl.acm.org/doi/10.1145/2071379.2071382).

Preliminary benchmarking (using the stopwatch on my phone) shows that to pass all the test cases on my computer:
- topological search takes ~18 seconds
- SCC union find takes ~65 seconds
- Implementation of a naive algorithm (`scc_union_find.py`)
- Implementation of the topological search algorithm as per [Haeupler et al](https://dl.acm.org/doi/10.1145/2071379.2071382).

Both implementations above pass the tests in `test/test_scc_maintainer.py` (as of 09/02/2022)

import os
import sys
from dependency_graph import DependencyGraph, CDG
from dependency_graph.dependency_graph_utils import get_code_list, get_oec

def test_CDG():
    filename = sys.argv[1]
    code_list = get_code_list(filename)
    oec = get_oec(filename)
    graph = CDG()
    graph.build(code_list)
    paths = graph.gen_exec_path(mode='oec', oec=oec)
    print('Total: ', len(paths))


if __name__ == '__main__':
    main()
    test_CDG()

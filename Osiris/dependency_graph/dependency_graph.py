import ast
import numpy as np
import json
from _ast import *
from .func_calls_visitor import get_func_calls
from .vars_visitor import get_vars

class FilterTransformer(ast.NodeTransformer):
    def __init__(self):
        self.class_names = []
    def visit_ClassDef(self, node):
        self.class_names += [node.name]
        return None

def get_fun_ref_id(tree):
    func_ref_ids = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import) :
            items = [nn.__dict__ for nn in node.names]
            for d in items:
                if d['asname'] is None:
                    func_ref_ids += [d['name']]
                else:
                    func_ref_ids += [d['asname']]
        if isinstance(node, ast.ImportFrom):
            items = [nn.__dict__ for nn in node.names]
            for d in items:
                if d['asname'] is None:
                    func_ref_ids += [d['name']]
                else:
                    func_ref_ids += [d['asname']]
    return func_ref_ids

class DependencyGraph:
    def __init__(self):
        self.vars_table_list = []
        self.func_table_list = []
        self.adj_mat = None
    def update_symbol_table(self, node):
        transfomer = FilterTransformer()  # remove classes 
        node = transfomer.visit(node)
        func_records = get_func_calls(node)  # function calls (no object's  member included)
        vars_records = get_vars(node)        # variables / objects 
        func_ref_ids = get_fun_ref_id(node)  # from import names

        class_ref_ids = transfomer.class_names  # get class names
        func_records = [(tmp,'def') for tmp in class_ref_ids+func_ref_ids] + func_records # make sure defs are ahead of load
        vars_records = [(tmp, 'store') for tmp in class_ref_ids+func_ref_ids] + vars_records

        func_table = {}
        vars_table = {}

        for item in func_records:
            if item[0] in func_table:
                func_table[item[0]] += [item[1]]
            else:
                func_table[item[0]] = [item[1]]

        for item in vars_records:
            if item[0] in vars_table:
                vars_table[item[0]] += [item[1]]
            else:
                vars_table[item[0]] = [item[1]]
        self.vars_table_list += [vars_table]
        self.func_table_list += [func_table]

    def is_dependent(self, i, j):
        for name, val in self.func_table_list[i].items():
            if val[0] == 'load':
                if name in self.func_table_list[j] and self.func_table_list[j][name][0] == 'def':
                        self.adj_mat[j][i] = 1
        # otherwise this fun is defined then skip
        for name, val in self.vars_table_list[i].items():
            if val[0] == 'load':
                if name in self.vars_table_list[j]:
                    all_actions = self.vars_table_list[j][name]
                    for tmp in all_actions:
                        if tmp == 'store':
                            self.adj_mat[j][i] = 1
                            break

    def build(self, code_list):
        n = len(code_list)
        mat = np.zeros((n, n))
        self.adj_mat = np.zeros((n, n))
        for idx, code in enumerate(code_list):
            try:
                tree = ast.parse(code, mode='exec')
                self.update_symbol_table(tree)
            except(SyntaxError):
                tree = ast.parse("", mode='exec')
                self.update_symbol_table(tree)
                print('warning!! Synatx Error')
        for i in range(n):
            for j in range(i):
                self.is_dependent(i, j)
        return self.adj_mat

    def get_topological_order(self):
        from copy import deepcopy
        adj_mat = deepcopy(self.adj_mat)
        exec_order = []
        n = adj_mat.shape[0] 
        in_degrees = np.sum(self.adj_mat, axis=0)
        todo_node_idx = (in_degrees==0).nonzero()[0].tolist()# in-degree=0 
        while len(exec_order)<n:
            for i in todo_node_idx:
                if i not in exec_order:
                    exec_order += [i]
                    adj_mat[i] = np.zeros(n)
            in_degrees = np.sum(adj_mat, axis=0)
            todo_node_idx = (in_degrees==0).nonzero()[0].tolist()# in-degree=0
        exec_order = [i+1 for i in exec_order]
        return exec_order
    def bfs(self, adj_mat):
        print(adj_mat)
        in_degrees = np.sum(self.adj_mat, axis=0)
        N = adj_mat.shape[0]
        q = queue.Queue()
        visited = [False]*N
        visit_order = []
        todo_nodes = (in_degrees==0).nonzero()[0].tolist()# nodes where in-degree=0
        for n in todo_nodes:
            q.put(n)

        while not q.empty():
            n = q.get()
            visited[n] = True
            visit_order += [n]
            todo_nodes = self.adj_mat[n].nonzero()[0].tolist()
            for tmp in todo_nodes:
                if not visited[tmp] and tmp not in q.queue:
                    q.put(tmp)
        return visit_order

    def get_all_order(self):
        N = self.adj_mat.shape[0]
        adj_mat1 = deepcopy(self.adj_mat)
        adj_mat2 = deepcopy(self.adj_mat)
        key_nodes = []
        visited = [False]*N
        N = self.adj_mat.shape[0]
        for i in range(N):
            for j in range(N):
                for g in range(N):
                    if self.adj_mat[i][j]==1 and self.adj_mat[i][g]==1 and self.adj_mat[g][j]==1:
                        adj_mat1[g][j]=0
                        adj_mat2[i][j]=0
        order1 = self.bfs(adj_mat1)
        order2 =  self.bfs(adj_mat2)
        return [order1, order2]

    def gen_exec_path(self, mode='single'):
        if mode == 'single':
            self.get_topological_order()
        elif mode == 'multiple':
            self.get_all_order()


import ast
import numpy as np
import json
from _ast import *
from .func_calls_visitor import get_func_calls
from .vars_visitor import get_vars
from copy import deepcopy
import queue

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

class DependencyGraph():

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
        self.N = len(code_list)
        mat = np.zeros((self.N, self.N))
        self.adj_mat = np.zeros((self.N, self.N), dtype=int)
        for idx, code in enumerate(code_list):
            try:
                tree = ast.parse(code, mode='exec')
                self.update_symbol_table(tree)
            except(SyntaxError):
                tree = ast.parse("", mode='exec')
                self.update_symbol_table(tree)
                print('warning!! Synatx Error')
        for i in range(self.N):
            for j in range(i):
                self.is_dependent(i, j)
        return self.adj_mat

    def get_topological_order(self):
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
 
        return exec_order

    def all_topo_util(self,all_paths, res, visited, in_degrees):
        flag = False
        for i in range(self.N):
            if in_degrees[i] ==0 and visited[i]==False:
                adj_nodes = self.adj_mat[i].nonzero()[0].tolist()
                in_degrees[adj_nodes] = in_degrees[adj_nodes]-1
                res.append(i)
                visited[i] = True
                self.all_topo_util(all_paths, res, visited, in_degrees)
                # backtracking 
                visited[i] = False
                res.pop()
                in_degrees[adj_nodes] += 1
                flag = True
        if not flag:
            print(res)
            all_paths.append(deepcopy(res))

    def alltopologicalSort(self, all_paths):
        visited = [False]*self.N
        in_degrees = np.sum(self.adj_mat, axis=0)
        res = []
        self.all_topo_util(all_paths, res, visited, in_degrees)

    def all_topo_with_oec_util(self, all_paths, res, in_degrees):
        if len(res) >= self.max_oec:
            oec_tmp = [0]*self.N
            counter = 0
            for i in res:
                counter += 1
                oec_tmp[i] = counter
            if oec_tmp == self.oec:
               all_paths.append(deepcopy(res))
            return

        for i in range(self.N):
            if in_degrees[i] <=0:
                adj_nodes = self.adj_mat[i].nonzero()[0].tolist()
                in_degrees[adj_nodes] = in_degrees[adj_nodes]-1
                res.append(i)
                self.all_topo_with_oec_util(all_paths, res, in_degrees)
                res.pop()
                in_degrees[adj_nodes] += 1


    def all_topo_with_oec(self, all_paths, oec):
        in_degrees = np.sum(self.adj_mat, axis=0)
        res = []
        self.oec = oec
        self.max_oec = max(self.oec)
        oec_tmp = [0]*self.N
        counter = 0
        self.all_topo_with_oec_util(all_paths, res, in_degrees)


    def gen_exec_path(self, mode='single', oec=[]):
        if mode == 'single':
            return self.get_topological_order()
        if mode == 'all':
            all_paths = []
            self.alltopologicalSort(all_paths)
            return all_paths
        if mode == 'oec':
            all_paths = []
            self.all_topo_with_oec(all_paths, oec)
            return all_paths

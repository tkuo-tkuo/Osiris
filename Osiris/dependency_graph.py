import ast
import _ast
import numpy as np
import json
from _ast import *
from .func_calls_visitor import get_func_calls
from .vars_visitor import get_vars

class DependencyGraph:
    def __init__(self):
        self.vars_table_list = []
        self.func_table_list = []

    def update_symbol_table(self, node):

        func_records = get_func_calls(node)
        vars_records = get_vars(node)
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
 
    def build(self, code_list):
        n = len(code_list)
        mat = np.zeros((n, n))
        for idx, code in enumerate(code_list):
            try:
                tree = ast.parse(code, mode='exec')
                self.update_symbol_table(tree)
            except(SyntaxError):
                print('Synatx Error')
                pass

        for i in range(n):

            for name, val in self.func_table_list[i].items():
                if val[0] == 'load':
                    for j in range(i):
                        if name in self.func_table_list[j] and self.func_table_list[j][name][0] == 'def':
                                mat[i][j] += 1
                # otherwise this fun is defined then skip
            for name, val in self.vars_table_list[i].items():
                # this var is loaded at the first occurence, it's store action
                # must be found
                if val[0] == 'load':
                    for j in range(i):
                        if name in self.vars_table_list[j]:
                            all_actions = self.vars_table_list[j][name]
                            for tmp in all_actions:
                                if tmp == 'store':
                                    mat[i][j] += 1
                                    break
        return mat

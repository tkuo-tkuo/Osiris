import ast
from  _ast import *
import json
import sys, os
import pkgutil

def iter_fields(node):
    """
    Yield a tuple of ``(fieldname, value)`` for each field in ``node._fields``
    that is present on *node*.
    """
    for field in node._fields:
        try:
            yield field, getattr(node, field)
        except AttributeError:
            pass

def iter_child_nodes(node):
    """
    Yield all direct child nodes of *node*, that is, all fields that are nodes
    and all items of fields that are lists of nodes.
    """
    for name, field in iter_fields(node):
        if isinstance(field, AST):
            yield field
        elif isinstance(field, list):
            for item in field:
                if isinstance(item, AST):
                    yield item

def get_code_list(path):
    content = open(path).read()
    content = json.loads(content)
    if 'worksheets' in content:
        cells = content['worksheets'][0]['cells']
        source_flag = 'input'
    else:
        cells = content['cells']
        source_flag = 'source'
    cells = list(filter(lambda x:x['cell_type']=='code', cells))
    sources = []
    for cell in cells:
        # filter out cells without execution count
        if cell['execution_count'] is not None:
            # remove magic functions
            code_lines = list(filter(lambda x:x[0]!='%', cell[source_flag])) #
            s = "".join(code_lines)
            sources.append(s)
    return sources

def find_local_modules(import_smts):
    smts = "\n".join(import_smts)
    tree = ast.parse(smts, mode='exec')
    search_path = ['.']
    module_names = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import) :
            for nn in node.names:
                module_names.add(nn.name)
        if isinstance(node, ast.ImportFrom):
            if node.level==2:
                search_path += ['..']
            if node.module is not None:
                module_names.add(node.module)
            else:
                for nn in node.names:
                    module_names.add(nn.name)

    search_path = list(set(search_path))
    all_modules = [x[1] for x in pkgutil.iter_modules(path=search_path)]
    all_modules += list(sys.builtin_module_names) + ['random']
    result = []
    for m_name in module_names:
        if m_name not in all_modules:
            result  += [m_name]
    return result


def get_path_by_extension(root_dir, num_of_required_paths, flag='.ipynb'):
    paths = []
    for root, dirs, files in os.walk(root_dir):
        files = [f for f in files if not f[0] == '.'] 
        dirs[:] = [d for d in dirs if not d[0] == '.']
        for file in files:
            if file.endswith(flag):
                paths.append(os.path.join(root, file))
                if len(paths) == num_of_required_paths:
                    return paths

    return paths



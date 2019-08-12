from vars_visitor import get_vars
import ast

source = """s += a\ns = s+a """
tree = ast.parse(source)
s = get_vars(tree)
print(s)
print(ast.dump(tree))

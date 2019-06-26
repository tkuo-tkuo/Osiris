import nbformat

def combine_two_commands(CMD1, CMD2):
    if CMD1 == '':
        return CMD2
    else:
        return CMD1 + ' && ' + CMD2


def store_nb(nb, relative_path):
    with open(relative_path, 'w') as f:
        nbformat.write(nb, f)

def combine_two_commands(CMD1, CMD2):
    if CMD1 == '':
        return CMD2
    else:
        return CMD1 + ' && ' + CMD2

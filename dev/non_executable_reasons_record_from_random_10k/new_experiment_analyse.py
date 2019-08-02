error_whitelist = ['ImportError', 'NameError', 'ModuleNotFoundError', 'FileNotFoundError', 'IOError', 'TypeError', 'ValueError', 'AttributeError', 'SyntaxError', 'PermissionError', 'StdinNotImplementedError', 'RuntimeError', 'KeyError', 'OSError', 'TclError', 'IndentationError', 'PermissionDeniedError', 'OperationalError', 'IndexError', 'HTTPError', 'LookupError', 'ZeroDivisionError', 'UsageError', 'AssertionError', 'InvalidArgumentError', 'TabError', 'NotImplementedError', 'UnboundLocalError', 'UnicodeDecodeError', 'JSONDecodeError', 'OptionError', 'TraitError', 'NotFittedError', 'NonExistentTimeError', 'CParserError', 'Exception', 'StopIteration', 'SystemExit', 'Cell execution timed out', 'NoSuchDocumentFound']
error_count_list = [0] * len(error_whitelist)
other_error_count = 0

num_of_notebooks = 10000

py27_count, empty_return_count = 0, 0

filter_out_count = 0
executable_count = 0
non_executable_count = 0
for i in range(1, num_of_notebooks+1):
    file_name = str(i)+'.txt'

    # Dump txt file to result
    f = open(file_name, 'r')
    result = f.read()
    f.close()

    # Break the dumped string into a list 
    result_in_lines = result.split('\n')

    # Start processing 
    # print("Processing {i} th notebooks".format(i=i))
    # print("Processing {i} th notebooks".format(i=i), end="\r")
    
    py_version = result_in_lines[0].strip()
    # Totally 3657 notebooks satisfy using python2.7 or kernel py27
    if py_version == '2.7' or (result_in_lines[1] == 'No such kernel named python2'):
        py27_count += 1
        filter_out_count += 1
        continue 
    # Totally 1265 notebooks we can not extract its python version (e.g., 3.4 or 3.5) 
    elif result_in_lines == ['', '', '']: 
        empty_return_count += 1
        filter_out_count += 1
        continue

    # Extract executability of the given experimental result 
    try:
        executability = result_in_lines[1].split(':')[1].strip()
    except:
        pass 

    if executability == 'True':
        executable_count += 1
    else:
        non_executable_count += 1

        is_error_found = False
        # If executabiliy of the given notebook is NOT True
        # -> further classify the root causes of non-executability   
        for statement_idx, statement in enumerate(result_in_lines):
            
            # Once we detect one of defined errors, 
            # -> record and jump to next notebook
            if any(substr in statement for substr in error_whitelist):
                
                # 1. Record
                for error_idx, error in enumerate(error_whitelist):
                    if error in statement:
                        error_count_list[error_idx] += 1
                        is_error_found = True
                        break 

                # 2. Jump to next notebook
                break

        if not is_error_found:
            other_error_count += 1


assert (filter_out_count + executable_count + non_executable_count) == num_of_notebooks
assert (sum(error_count_list) + other_error_count) == non_executable_count
print('Executability ratio:'.rjust(30), executable_count/(executable_count+non_executable_count-other_error_count))
print()

decreasing_order = sorted(range(len(error_count_list)),key=error_count_list.__getitem__)[::-1]

for i in decreasing_order:
    print(error_whitelist[i].rjust(29)+':', error_count_list[i])

print(filter_out_count, py27_count, empty_return_count)



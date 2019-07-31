error_whitelist = ['ModuleNotFoundError: No module named']
other_error_count = 0
module_not_found_count = 0
module_not_found_list = []
num_of_notebooks = 10000

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
    
    # First of all, filter out python2.7 for further calculation
    py_version = result_in_lines[0].strip()
    if py_version == '2.7' or (result_in_lines == ['', '', '']) or (result_in_lines[1] == 'No such kernel named python2'):
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
                        module = statement.split("'")[1]
                        module_not_found_list.append(module)
                        module_not_found_count += 1
                        is_error_found = True
                        break 

                # 2. Jump to next notebook
                break

        if not is_error_found:
            other_error_count += 1


assert (filter_out_count + executable_count + non_executable_count) == num_of_notebooks
assert (module_not_found_count) == (len(module_not_found_list))

count_for_modules = [ (i,module_not_found_list.count(i)) for i in set(module_not_found_list) ]
count_for_modules = sorted(count_for_modules, key=lambda tup: tup[1])[::-1]
for count_for_module in count_for_modules:
    module, count = count_for_module
    if not ('#' in module):
        print(module.rjust(29)+':', count)

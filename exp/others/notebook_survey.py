import os
import sys
import re
import json

def main():
    filenames = open('../oec/non_strong_repro_OEC_improved.txt').readlines()
    count = 0
    for fn in filenames:
        content = open(fn.strip()).read()
        try:
            content = json.loads(content)
            if 'worksheets' in content:
                cells = content['worksheets'][0]['cells']
            else:
                cells = content['cells']
            cells = list(filter(lambda x:x['cell_type']=='code', cells))
            for c in cells:
                out_str = ""
                if len(c['outputs'])==0:
                    continue
                c_o_1 = c['outputs'][0]
                c_o_2 = c['outputs'][1]
                if c_o_1['output_type'] == 'stream':
                    out_str = " ".join(c_o_1['text'])
                elif c_o_1['output_type']=='execute_result':
                    out_str = " ".join( c_o_1['data']['text/plain'])
                #res = re.findall(r'<matplotlib(.+?)at(.+?)>', out_str)
                res = re.findall(r'<(.+?)at 0x(.+?)>', out_str)
                if len(res)>0 and 'image/png' in c_o_2['data']:  # go to the next file if one found
                    count +=1
                    print(fn.strip())
                    break
        except:
            pass
    print(count)

if __name__ == '__main__':
    main()



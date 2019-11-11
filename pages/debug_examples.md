# Debugging module

As stated in the Section 5.4, OSIRIS the targeted failure debugging module of Osiris aims to locate the suspicious statements (which is likely to induce non-reproducibility). Currently, it will return the line index of the first found suspicious statement.  

Below examples demonstrate the usage of our debugging module, where source code of notebooks are also provided.   

### Example 1

Notebook link: https://github.com/FHainzl/SD-TSIA211/blob/master/TP2/TP2.ipynb

```
cell index: 11
Execution order: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
The potential statement for causing status difference is line 8
-------------->  time1 = time.time()
```

Part of source code (cell of which suspicious statement is detected):
 <img src="p2.png" align="center" border="0" width="800" height="300"/>   

### Example 2

Notebook link: https://github.com/nakanodaiki/probrobo2017/blob/master/probrob.ipynb
```
cell index: 7
Execution order: [0, 1, 2, 3, 4, 5, 6, 7]
The potential statement for causing status difference is line 7
-------------->  measurements = [observations(actual_x, actual_landmarks)]
```

Part of source code (cell of which suspicious statement is detected):
 <img src="p3.png" align="center" border="0" width="800" height="500"/>   

 ### Example 3

Notebook link: https://github.com/mat-esp-2015/python-intro-2-joao_leticia_dyellen/blob/master/jupyter-notebook-tour.ipynb

```
cell index: 4
Execution order: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
The potential statement for causing status difference is line 1
-------------->  random.shuffle(lista)
```

Part of source code (cell of which suspicious statement is detected):
 <img src="p1.png" align="center" border="0" width="800" height="80"/>  



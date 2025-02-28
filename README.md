# Osiris

**Devlopment repository of Jiawei Wang, Tzu-yang Kuo, Li Li, Andreas Zeller, Assessing and Restoring Reproducibility of Jupyter Notebooks, The 35th IEEE/ACM International Conference on Automated Software Engineering (ASE 2020), 2020**

Osiris is a tool for programmers to analyze Jupyter Notebook files before releasement. We discovered that plentiful Jupyter Notebook files pushed on GitHub cannot reproduce anticipated outputs. Alternatively, even worse, some Jupyter Notebook files can even not be executed on different end devices.

Osiris aims to eliminate this problem. One can leverage Osiris to analyze their Jupyter Notebook files before releasement to the public, which can conclude potential reasons for causing non-reproducibility. By the assistance of Osiris, programmers can properly refine their Jupyter Notebook files and enhance reproducibility of Jupyter Notebook files. 

## Getting Started

These instructions will go through execution environments setup, usage, and unit tests for users to check functionalities of Osiris. 

### Prerequisites

Make sure both Conda and Pip installed. Install Conda via [the official website](https://www.anaconda.com/) or by pip. 

```
pip install conda 
```

### Setup 

Before the usage of Osiris, to cope with various python version and package requirements for Jupyter Notebook files. A setup.sh needs to be executed to deploy several Conda environments with several combinations between different versions python and ten selected packages. (Currently, Osiris has more than 200 packages pre-installed)

```
cd envs 
source ./setup.sh
```

### Running unit tests for Osiris 

To guarantee all functionalities of Osiris functions accurately. Please run unit tests by instructions below. These unit tests will analyze Jupyter notebook files stored in the tests folder to verify the correctness of Osiris in diverse circumstances. 

Note that for analyzing Jupyter Notebook files, Osiris requires some additional packages installed. For simplicity, activate the default environment of Osiris before running unit tests. 

```
conda activate Osiris_default
python3 test.py -b
```

## Benchbook 

```
conda activate Osiris_default
python3 benchbook_test.py -b
```

## Usage 

Follow instructions demonstrate how users can analyze their Jupyter Notebook files. To avoid unexpected failures, activate Osiris_default before leveraging Osiris. 

```
conda activate Osiris_default 
```

### Parameters 

For Osiris, there are several parameters for users to specify during usage. Below list out all parameters and the corresponding description. Please refer to the Terminology section for more illustration. 

- <b>notebook_path</b> (required) <br/>
  Please specify the relative path from runOsiris.sh. For instance, notebook.ipynb or folder/notebook.ipynb. 
  
- <b>execute</b> (required) <br/>
  <b>options: normal/OEC/dependency</b> <br/>
  Please specify the execute strategy for analyzing Jupyter Notebook files. <br/>
  Currently, Osiris has three execute strategies, including normal (top-to-down), OEC (original execution_count), and dependency. Each of them executes Jupyter Notebook files in different order. 
  
- <b>verbose</b> (optional) <br/>
  <b>Usage: -v</b> <br/>
  If False, Osiris will filter out all processing/debugging information, leaving only statistic results  — for instance, executability and reproducibility ratio. In contrast, if True, all processing/debugging information like the source code of non-reproducible cells will be listed out. 
  
- <b>match pattern</b> (optional) <br/>
  <b>Usage: -m pattern</b> <br/>
  <b>options: strong/weak/best_effort</b> <br/>
  Set this option to analyze reproducibility of Jupyter Notebook files. Osiris automatically executes and compares outputs of Jupyter Notebook files according to match pattern given. 
  
- <b>self reproducibility</b> (optional) <br/>
  <b>Usage: -s</b> <br/>
  Set this option as True to activate analyses on self-reproducibility of cells. Osiris will analyze whether cells in Jupyter Notebook files are self-reproducible or not. If a cell is self-reproducible, it indicates the status of variables is equivalent for executing a cell once or multiple times.  
  
- <b>all potential execution paths</b> (optional) <br/>
  <b>Usage: -a</b> <br/>
  Set this option as True to activate analyses on all potential execution paths according to the Cell-Dependency Graph. Osiris will analyze each potential execution path individually and display corresponding analytical results. 
  
- <b>debug</b> (optional) <br/>
  <b>Usage: -d cell_index</b> <br/>
  <b>options: a valid number, where 0 indicates the first cell be executed</b> <br/>
  Set this option to analyze a specific cell in details for debugging purpose. Osiris will examine the status difference line by line and locate suspicious statement which may potentially induce the non-reproducibility.   
  

### Examples 

example 1: analyze whether a notebook is executable in normal (top-to-down) order

```
source ./runOsiris.sh target_notebook.ipynb normal 
```

example 2: analyze reproducibility of a given notebook, using strong match pattern, in OEC (original execution count) order

```
source ./runOsiris.sh target_notebook.ipynb OEC "-m strong"
```

example 3: analyze reproducibility of a given notebook, using strong match pattern, in OEC (original execution count) order with full information 

```
source ./runOsiris.sh target_notebook.ipynb OEC "-m strong -v"
```

example 4: analyze self-reproducibility of a given notebook in dependency order  

```
source ./runOsiris.sh target_notebook.ipynb dependency "-s"
```

example 5: analyze the first cell of a given notebook in normal (top-to-down) order, where Osiris will locate suspicious statement causing the status difference of variables. 

```
source ./runOsiris.sh target_notebook.ipynb normal "-d 0"
```

example 6: analyze both reproducibility of a given notebook, using strong match pattern, and self-reproducibility in OEC (original execution count) order with full information 

```
source ./runOsiris.sh target_notebook.ipynb OEC "-m strong -s -v"
```
  
## Implementation Details 

- Before any re-execution and analyze, Osiris will preprocess the given Jupyter Notebook file, removing all markdown cells/raw cells/cells without Execution Count. 

## Side Questions 

**Why it's called Osiris? <br/>**
Osiris is the god of the afterlife, the underworld, and rebirth in ancient Egyptian religion. Our tool aims to enable Jupyter Notebook files to be executable, more reproducible, giving these files rebirth on different machines. That is the inspiration why I would like to name our tool as Jupyter Osiris. 

## (Unofficial) Reference 

João Felipe Pimentel, Leonardo Murta, Vanessa Braganholo, and Juliana Freire <br/> 
A large-scale study about quality and reproducibility of jupyter notebooks in Proceedings of the 16th International Conference on Mining Software Repositories

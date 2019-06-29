import unittest
import warnings
import csv 

import sys
sys.path.append('/home/dabao/Osiris')

import Osiris
from Osiris.analysizer import Analysizer
from Osiris.utils import store_nb

naive_notebook_path = 'test_case_1.ipynb'
image_IPythonDisplay_notebook_path = 'test_case_2.ipynb'
image_Matplotlib_notebook_path = 'test_case_3.ipynb'
relative_notebook_path = 'folder/test_case_4.ipynb'
analyze_strategy_notebook_path = 'test_case_5.ipynb'

def massive_notebooks_analyze(start_idx, end_idx):
    csv_file = open('downloaded_notebooks.csv', 'r', encoding='utf-8')
    reader = csv.reader(csv_file)

    analyse_results = []

    for row_idx, row in enumerate(reader):
        nb_idx = row_idx + 1
        if nb_idx >= start_idx and nb_idx <= end_idx:
            original_repo_path, notebook_path = row[0], row[1]
            original_repo_path_lst = original_repo_path.split('/')
            folder_path = original_repo_path_lst[0]+'@'+original_repo_path_lst[1]

            path = '/mnt/fit-Knowledgezoo/jupyternotebooks/'+folder_path+'/'+notebook_path

            try:
                interface = Osiris.UserInterface(path)
                analyse_results.append(interface.analyse(verbose=False, store=False))
            except Exception as e:
                print(e)

    return analyse_results
                                

class TestOsiris(unittest.TestCase):

    def setUp(self):
        warnings.simplefilter('ignore', category=ImportWarning)
        warnings.simplefilter('ignore', category=DeprecationWarning)
        warnings.simplefilter('ignore', category=ResourceWarning)

    def test_naive_notebook_executability(self):
        f = open(naive_notebook_path, 'r', encoding='utf-8')
        analysizer = Analysizer(f)
        self.assertTrue(analysizer.check_executability(verbose=False))
    
    def test_naive_notebook_reproductivity(self):
        f = open(naive_notebook_path, 'r', encoding='utf-8')
        analysizer = Analysizer(f)
        num_of_reproductive_cells, num_of_cells, reproductivity_ratio, reproductive_cell_idx, _ = analysizer.check_reproductivity(
            verbose=False)
        self.assertEqual(num_of_reproductive_cells, 1)
        self.assertEqual(num_of_cells, 3)
        self.assertAlmostEqual(reproductivity_ratio, 1/3)
        self.assertEqual(reproductive_cell_idx, [0])

    def test_naive_notebook_idempotent(self):
        f = open(naive_notebook_path, 'r', encoding='utf-8')
        analysizer = Analysizer(f)
        num_of_idempotent_cells, num_of_cells, idempotent_ratio, idempotent_cell_idx = analysizer.check_idempotent(
            verbose=False)
        self.assertEqual(num_of_idempotent_cells, 1)
        self.assertEqual(num_of_cells, 3)
        self.assertAlmostEqual(idempotent_ratio, 1/3)
        self.assertEqual(idempotent_cell_idx, [0])

    def test_check_reproductivity_for_image_IPythonDisplay(self):
        f = open(image_IPythonDisplay_notebook_path, 'r', encoding='utf-8')
        analysizer = Analysizer(f)
        num_of_reproductive_cells, num_of_cells, reproductivity_ratio, reproductive_cell_idx, _ = analysizer.check_reproductivity(verbose=False)
        self.assertEqual(num_of_reproductive_cells, 1)

    def test_check_reproductivity_for_image_Matplotlib(self):
        f = open(image_Matplotlib_notebook_path,'r', encoding='utf-8')
        analysizer = Analysizer(f)
        num_of_reproductive_cells, num_of_cells, reproductivity_ratio, reproductive_cell_idx, _ = analysizer.check_reproductivity(verbose=False)
        self.assertEqual(num_of_reproductive_cells, 2)        

    # Conda environment required
    def test_relative_path(self):
        interface = Osiris.UserInterface(relative_notebook_path)

        # 'interface.analyse' use 'return subprocess.call' at the code of the function
        # Subprocess.call returns 'actual process return code'
        # 1 for false process execution; 0 for successful process execution
        analyse_result = interface.analyse(verbose=False)
        self.assertEqual(analyse_result, 0)

    # Conda environment required
    # Downloading massive notebooks required (This unit test should be removed when Osiris is officially released) 
    @unittest.skip('Currently, we do not need to test for massive analyses. Leave it after all tests on individual notebook are completed.')
    def test_multiple_notebook_analyses(self):
        
        # Test 3 notebooks in 3 corresponding repositories with multiple paths relative to this test.py 
        # A 'downloaded_notebooks.csv' will be used for traversing through the file system 
        # Currently, all downloaded GitHub repos are stored in /mnt/fit-Knowledgezoo 
        analyse_results = massive_notebooks_analyze(3, 3) 
        self.assertEqual(analyse_results, [0]) 

    def test_top_down_analyze_strategy(self):
        pass 

    def test_OEC_analyze_strategy(self):
        pass 
    
    def test_dependency_analyze_strategy(self):
        pass 
    


if __name__ == '__main__':
    unittest.main()

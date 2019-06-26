import unittest
import warnings

# These two lines should be replaced in the Linux environment 
import sys
sys.path.append('/home/dabao/Osiris')

import Osiris
from Osiris.analysizer import Analysizer

naive_notebook_path = 'test_case_1.ipynb'
image_IPythonDisplay_notebook_path = 'test_case_2.ipynb'
image_Matplotlib_notebook_path = 'test_case_3.ipynb'
relative_notebook_path = 'folder/test_case_4.ipynb'


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
        num_of_reproductive_cells, num_of_cells, reproductivity_ratio, reproductive_cell_idx = analysizer.check_reproductivity(
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
        num_of_reproductive_cells, num_of_cells, reproductivity_ratio, reproductive_cell_idx = analysizer.check_reproductivity(
            verbose=False)
        self.assertEqual(num_of_reproductive_cells, 1)

    def test_check_reproductivity_for_image_Matplotlib(self):
        f = open(image_Matplotlib_notebook_path,'r', encoding='utf-8')
        analysizer = Analysizer(f)
        num_of_reproductive_cells, num_of_cells, reproductivity_ratio, reproductive_cell_idx = analysizer.check_reproductivity(
            verbose=False)
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
    def test_multiple_notebook_analyses(self):
        # Test 3 notebooks in 3 corresponding repositories with multiple paths relative to this test.py 
        # A all_urls.csv will be used for traversing through the file system 
        
        # 3 repos (PENDING)
        # A all_urlscsv file for testing (PENDING)

        pass


if __name__ == '__main__':
    unittest.main()

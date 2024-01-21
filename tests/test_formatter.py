import unittest
import os
import sys
from glob import glob
from functools import partial

# Adjust the path for importing the formatter module
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, '..', 'src')
sys.path.append(src_dir)

from grey import formatter

def read_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

class TestGreyFormatter(unittest.TestCase):

    def run_test_case(self, source_file, expected_file):
        source_code = read_file(source_file)
        expected_output = read_file(expected_file)
        self.assertEqual(formatter.format_code(source_code), expected_output)

def generate_test_cases():
    test_data_dir = os.path.join(current_dir, 'test_data')
    source_files = glob(os.path.join(test_data_dir, '*_source.py'))

    for source_file in source_files:
        expected_file = source_file.replace('_source.py', '_expected.py')

        # Define a closure that captures the current source_file and expected_file
        def test_method(self, source_file=source_file, expected_file=expected_file):
            self.run_test_case(source_file, expected_file)

        # Set a dynamic method name
        test_method_name = f'test_{os.path.basename(source_file)}'
        setattr(TestGreyFormatter, test_method_name, test_method)

generate_test_cases()

if __name__ == '__main__':
    unittest.main()

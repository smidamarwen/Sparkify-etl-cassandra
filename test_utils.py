import os
import tempfile
from unittest import TestCase

from utils import load_files_list


class Test(TestCase):
    def test_load_files_list(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create some dummy CSV files
            file1 = os.path.join(temp_dir, "file1.csv")
            file2 = os.path.join(temp_dir, "file2.csv")
            file3 = os.path.join(temp_dir, "file3.txt")
            with open(file1, "w") as f:
                f.write("file1")
            with open(file2, "w") as f:
                f.write("file2")
            with open(file3, "w") as f:
                f.write("file3")
            # Call the load_files_list function
            result = load_files_list(temp_dir)
            # Check that only the CSV files are loaded
            assert len(result) == 2
            assert file1 in result
            assert file2 in result
            assert file3 not in result
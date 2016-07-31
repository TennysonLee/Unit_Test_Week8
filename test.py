import unittest

import warnings, os, urllib2, pandas as pd
from requester import url_to_csv, batch_url_to_csv, url_to_df


# unittest documentation
valid_csv_url = "https://archive.ics.uci.edu/ml/machine-learning-databases/abalone/abalone.data"
valid_csv_url_v2 = "http://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.data"
valid_csv_url_v3 = "https://archive.ics.uci.edu/ml/machine-learning-databases/autos/imports-85.data"
invalid_url = "http://www.example.com/junk"
invalid_csv_url = "http://stackoverflow.com/questions/1393324/in-python-given-a-url-to-a-text-file-what-is-the-simplest-way-to-read-the-cont"
invalid_csv_url_v2 = "https://archive.ics.uci.edu/ml/datasets/Adult"

urls = [valid_csv_url, valid_csv_url_v2, valid_csv_url_v3, invalid_url, invalid_csv_url, invalid_csv_url_v2]
filenames = ["valid_csv_url", "valid_csv_url_v2", "valid_csv_url_v3", "invalid_url", "invalid_csv_url", "invalid_csv_url_v2"]


class TestURLToCSV(unittest.TestCase):

    def test_type_error_v1(self): # Unit Test #1
        with self.assertRaises(TypeError):
            url_to_csv(invalid_csv_url)


    def test_type_error_v2(self): # Unit Test #1
        with self.assertRaises(TypeError):
            url_to_csv(invalid_csv_url_v2)


    def test_value_error_v2(self): # Unit Test #2
        with self.assertRaises(ValueError):
            url_to_csv(invalid_url)


class TestBatchURLToCSV(unittest.TestCase):

    def test_catch_runtimewarnings(self): # Unit Test #3
        with warnings.catch_warnings(record=True) as w:
            # Cause all warnings to always be triggered.
            warnings.simplefilter("always")
            # Trigger a warning.
            batch_url_to_csv(urls, filenames)
            # Verify some things
            assert len(w) == 3
            assert issubclass(w[-1].category, RuntimeWarning)
            assert "An invalid URL was found. File was not created." in str(w[-1].message)


    def test_correct_number_of_files_created(self): # Unit Test #4
        res = batch_url_to_csv(urls, filenames)
        self.assertEqual(len(res), 3)

    def test_unique_csv_contents(self): # Unit Test #5
        res = batch_url_to_csv(urls, filenames)
        for i in range(len(res)):
            for j in range(len(res)):
                if i == j:
                    # print i, j, "same"
                    pass
                else:
                    # print i, j, "diff"
                    file_i = pd.read_csv(res[i])
                    file_j = pd.read_csv(res[j])
                    self.assertNotEqual(file_i.equals(file_j), True)

    def test_correct_filenames_generated(self):
        res = batch_url_to_csv(urls, filenames)
        valid_filenames = ["valid_csv_url", "valid_csv_url_v2", "valid_csv_url_v3"]
        for i in range(len(res)):
            print i
            self.assertEquals(res[i], os.path.join(os.path.dirname(__file__), valid_filenames[i]))



if __name__ == '__main__':
    unittest.main(verbosity=20)
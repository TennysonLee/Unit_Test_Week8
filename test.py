import unittest

import warnings, os, urllib2, pandas as pd, requests
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
            url_to_csv(invalid_csv_url, "type_Error")

    def test_value_error_v2(self): # Unit Test #2
        with self.assertRaises(ValueError):
            url_to_csv(invalid_url, "value_error")


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

    def test_valid_urls(self): # Unit Test #4
        valid_urls = [valid_csv_url, valid_csv_url_v2, valid_csv_url_v3]
        valid_filenames = ["valid_csv_url", "valid_csv_url_v2", "valid_csv_url_v3"]
        res = batch_url_to_csv(valid_urls, valid_filenames)
        for i in range(len(res)):
            self.assertEquals(res[i], os.path.join(os.path.dirname(__file__), valid_filenames[i])+".csv")

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

    def test_correct_filenames_returned(self): # Unit Test #6
        url_test = [valid_csv_url, invalid_url]
        filename_test = ["valid_csv_url", "invalid_url"]
        res = batch_url_to_csv(url_test, filename_test)
        self.assertEquals(res[0], os.path.join(os.path.dirname(__file__), "valid_csv_url.csv"))

    def test_correct_number_files_generated(self): # Unit Test #7
        res = batch_url_to_csv(urls, filenames)
        self.assertEquals(len(res), 3)

    def test_duplicate_url_found(self): # Unit Test #8
        with self.assertRaises(AssertionError):
            url_test = [valid_csv_url, valid_csv_url]
            filename_test = ["valid_csv_url", "valid_csv_url"]
            batch_url_to_csv(url_test, filename_test)

class TestURLToDF(unittest.TestCase):

    def test_pd_dataframe_object_returned_valid_csv(self): # Unit Test #9
        res = url_to_df(valid_csv_url)
        self.assertTrue(type(res), pd.DataFrame())

    def test_pd_dataframe_and_url_to_df_have_same_rows(self): # Unit Test #10
        valid_url_with_no_header = "https://archive.ics.uci.edu/ml/machine-learning-databases/abalone/abalone.data"
        url_to_df_data = url_to_df(valid_url_with_no_header)
        url_to_df_rows = url_to_df_data.shape[0]

        url_data = pd.read_csv(valid_url_with_no_header)
        url_data_rows = url_data.shape[0]

        self.assertEquals(url_to_df_rows, url_data_rows)

if __name__ == '__main__':
    unittest.main(verbosity=30)
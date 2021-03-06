



#  Unit Test Assignment: Week 8
#  Tennyson Lee

import pandas as pd
import os
import urllib2
import warnings





def url_to_csv(url, filename="csv_test"):
    """Takes a URL to a CSV file, downloads it, and saves it to a file.

    Args:
        url: valid or invalid urls.
        filename (str): Name of file created. If no filename is given, the
            default is "csv_test".

    Returns:
        filepath of the csv
    """
    try:
        data_from_url = pd.read_csv(url)
        csv_name = ("%s.csv" % filename)
        data_from_url.to_csv(csv_name)
    except urllib2.HTTPError:
        raise ValueError('The URL does not exist. Please enter a valid URL.')
    except:
        raise TypeError('The URL cannot be parsed into a csv. Please try another URL.')

    # print filename
    # print data_from_url
    # print os.path.abspath(csv_name)
    return os.path.abspath(csv_name)


def batch_url_to_csv(urls, filenames):
    """Takes a list of URLs to CSV files, downloads them, and saves them to files given by the
    list of names in fnames. Returns a list of the filenames saved.

    Args:
        urls (list of urls): could be valid or invalid urls
        filenames (list of string names): Name of files created

    Returns:
        list of all valid URL file paths
    """
    result_filenames = []
    for i in range(len(urls)):
        for j in range(len(urls)):
            if i == j:
                pass
            elif urls[i] == urls[j]:
                raise AssertionError("Duplicate URLs cannot be present in the parameter 'urls'.")
    for i in range(len(urls)):
        try:
            path = url_to_csv(urls[i], filenames[i])
            # print path
            result_filenames.append(path)
        except Exception:
            warnings.warn('An invalid URL was found. File was not created.', RuntimeWarning)
    return result_filenames


def url_to_df(url):
    """Takes a URL to a CSV file and returns the contents of the URL as a Pandas DataFrame.

    Args:
        url: valid url

    Returns:
        pandas dataframe
    """
    dataframe = pd.read_csv(url)
    # print dataframe
    return dataframe


if __name__ == "__main__":

    valid_csv_url = "https://archive.ics.uci.edu/ml/machine-learning-databases/abalone/abalone.data"
    valid_csv_url_v2 = "http://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.data"
    invalid_url = "http://www.example.com/junk"
    invalid_csv_url = "http://stackoverflow.com/questions/1393324/in-python-given-a-url-to-a-text-file-what-is-the-simplest-way-to-read-the-cont"
    invalid_csv_url_v2 = "https://archive.ics.uci.edu/ml/datasets/Adult"

    # url_to_csv(invalid_csv_url)

    batch_urls = [valid_csv_url, valid_csv_url_v2, invalid_url, invalid_csv_url, invalid_csv_url_v2]
    batch_filenames = ["valid_csv_url", "valid_csv_url_v2", "invalid_url", "invalid_csv_url", "invalid_csv_url_v2"]
    # batch_url_to_csv(batch_urls, batch_filenames)

    # url_to_df(valid_csv_url)




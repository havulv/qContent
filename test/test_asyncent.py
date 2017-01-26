#! usr/bin/env python3

'''
    Testing for asyncent. Go to level above module and run tests with
        python -m test.test_asyncent

    Currently, testing is only implemented for synchronous functions
        Discussions are ongoing for how to test asynchronous functions
            without being an ass.

        (And by 'discussions' I mean talking to my self in a mirror.
            Sometimes several mirrors. For a conference discussion.
            Also, weekly skype meetings.
                [And by skype meetings I mean setting up multiple
                    laptops all facing myself])
'''

import asyncent

import unittest, configparser, os

class TestTemplate(unittest.TestCase):

    def setUp(self):
        with open("sample_test.txt", "w") as sample:
            sample.write("http://www.example.com/ NOHASH"
            "\nhttp://www.feedforall.com/sample.xml NOHASH\n")
        with open("bad_sample_test_1.txt", "w") as sample:
            sample.write("www.example.com/ NOHASH"
            "\nhttp://www.feedforall.com/sample.xml NOHASH\n")
        with open("bad_sample_test_2.txt", "w") as sample:
            sample.write("http://www.example.com/ NOHASH"
            "\nhttp://www.feedforall.com/sample.xml\n")
        config = configparser.ConfigParser(
                os.path.normpath('asyncent\\asyncent.config'))
        with open(os.path.normpath(
            "asyncent\\asyncent_copy.config"), 'w') as configfile:
            config.write(configfile)
        sample_config = configparser.ConfigParser()
        sample_config["DEFAULT"] = {"FilePath" : "sample_test.txt"}
        with open(os.path.normpath(
            "asyncent\\asyncent.config"), 'w') as configfile:
            sample_config.write(configfile)


    def tearDown(self):
        config = configparser.ConfigParser().read(
                            "asyncent\\asyncent_copy.config")
        with open(os.path.normpath(
            "asyncent\\asyncent.config"), 'w') as configfile:
            config.write(configfile)
        os.remove("asyncent\\asyncent_copy.config")
        os.remove("sample_test.txt")
        os.remove("bad_sample_test_1.txt")
        os.remove("bad_sample_test_2.txt")

class TestFetch(TestTemplate):

    # fetch_main is not tested because it is literally some stdout
    # if it fails then it is the least of all problems

    def test_update_cache(self):
        pass
    def test_update_cache_no_updates(self):
        pass
    def test_update_cache_bad_path(self):
        pass
    def test_update_cache_no_listing(self):
        pass
    def test_update_cache_bad_listing(self):
        pass
    def test_write_cache(self):
        pass
    def test_write_cache_bad_path(self):
        pass
    def test_write_cache_bad_listing_site(self):
        pass
    def test_write_cache_bad_listing_no_hash(self):
        pass
    def test_write_cache_bad_listing_bad_hash(self):
        pass
    def test_get_cache(self):
        pass
    def test_get_cache_bad_path(self):
        pass
    def test_get_cache_bad_listing_file_1(self):
        pass
    def test_get_cache_bad_listing_file_2(self):
        pass
    def test_get_content(self):
        pass
    def test_get_content_bad_path(self):
        pass

class TestFeedRead(TestTemplate):

    # I don't know how to test this yet, because it is basically all async
    # stuff
    pass

class TestMain(TestTemplate):

    '''
        Test the argparser and configparser as well as main actions
    '''
    pass

if __name__ == "__main__":
    print(os.getcwd())


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

import asyncent.fetch as fetch

import unittest, configparser, os, random, time


def cover(filepath, listing):
    def inner(func):
        def wrap(*args, **kwargs):
            ret = func(*args, **kwargs)
            with open(filepath, "w") as sample:
                sample.write(writer(listing))
            return ret
        return wrap
    return inner

# 'one'-liner
def writer(sample_dict):
    return "".join(["\n".join([" ".join(x) for x in
        [ [k,v] if v else [k, "NOHASH"] for k,v in sample_dict.items()]])])


class TestTemplate(unittest.TestCase):

    sample_file = "sample_test.txt"
    bad_1 = "bad_sample_test_1.txt"
    bad_2 = "bad_sample_test_2.txt"
    config = os.path.normpath("asyncent\\asyncent.config")
    config_copy = os.path.normpath("asyncent\\asyncent_copy.config")

    sample_list = {"http://www.example.com/" : None,
            "http://www.feedforall.com/sample.xml" : None}
    bad_list_1 = {"www.example.com/" : None,
            "http://www.feedforall.com/sample.xml" : None}
    bad_list_2 = {"http://www.example.com/" : None,
            "http://www.feedforall.com/sample.xml" : " "}

    @classmethod
    def setUpClass(cls):
        with open(TestTemplate.sample_file, "w") as sample:
            sample.write(writer(TestTemplate.sample_list))
        with open(TestTemplate.bad_1, "w") as sample:
            sample.write(writer(TestTemplate.bad_list_1))
        with open(TestTemplate.bad_2, "w") as sample:
            sample.write(writer(TestTemplate.bad_list_2))
        config = configparser.ConfigParser()
        config.read(TestTemplate.config)
        with open(TestTemplate.config_copy, 'w') as configfile:
            config.write(configfile)
        sample_config = configparser.ConfigParser()
        sample_config["DEFAULT"] = {"FilePath" : "sample_test.txt"}
        with open(TestTemplate.config, 'w') as configfile:
            sample_config.write(configfile)

    @classmethod
    def tearDownClass(cls):
        config_copy = configparser.ConfigParser()
        config_copy.read(TestTemplate.config_copy)
        with open(TestTemplate.config, 'w') as configfile:
            config_copy.write(configfile)
        os.remove(TestTemplate.config_copy)
        os.remove(TestTemplate.sample_file)
        os.remove(TestTemplate.bad_1)
        os.remove(TestTemplate.bad_2)

class TestFetch(TestTemplate):

    # fetch_main is not tested because it is literally some stdout
    # if it fails then you should fix your terminal

    @cover(TestTemplate.sample_file, TestTemplate.sample_list)
    def test_update_cache(self):
        new_dict = {k : "1"*128 for k,v in self.sample_list.items()}
        self.assertTrue(fetch.update_cache("sample_test.txt",
                                new_dict.items(), self.sample_list))

    @cover(TestTemplate.sample_file, TestTemplate.sample_list)
    def test_update_cache_no_updates(self):
        self.assertTrue(fetch.update_cache("sample_test.txt",
                                            [], self.sample_list))

    @cover(TestTemplate.sample_file, TestTemplate.sample_list)
    def test_update_cache_bad_path(self):
        new_dict = {k : "1"*128 for k,v in self.sample_list.items()}
        self.assertRaises(FileNotFoundError, fetch.update_cache,
                    "foo_bar.baz", new_dict.items(), self.sample_list)

    @cover(TestTemplate.sample_file, TestTemplate.sample_list)
    def test_update_cache_no_listing(self):
        new_dict = {k : "1"*128 for k,v in self.sample_list.items()}
        self.assertTrue(fetch.update_cache(self.sample_file,
                                            new_dict.items()))

    @cover(TestTemplate.sample_file, TestTemplate.sample_list)
    def test_update_cache_bad_listing(self):
        new_dict = {k : "1"*128 for k,v in self.sample_list.items()}
        self.assertFalse(fetch.update_cache(self.sample_file,
                                        new_dict.items(), self.bad_list_1))

    @cover(TestTemplate.sample_file, TestTemplate.sample_list)
    def test_write_cache(self):
        new_dict = {k : "1"*128 for k,v in self.sample_list.items()}
        self.assertTrue(fetch.write_cache(self.sample_file, new_dict))

    def test_write_cache_bad_path(self):
        new_dict = {k : "1"*128 for k,v in self.sample_list.items()}
        self.assertRaises(FileNotFoundError,
            fetch.write_cache, "foo_bar.baz", new_dict)

    @cover(TestTemplate.bad_1, TestTemplate.bad_list_1)
    def test_write_cache_bad_listing_site(self):
        new_dict = {k : "0"*128 for k,v in self.bad_list_1.items()}
        self.assertFalse(fetch.write_cache(self.bad_1, new_dict))

    @cover(TestTemplate.bad_2, TestTemplate.bad_list_2)
    def test_write_cache_bad_listing_no_hash(self):
        new_dict = { k : " " for k, v in self.bad_list_2.items()}
        self.assertFalse(fetch.write_cache(self.bad_2, new_dict))

    @cover(TestTemplate.bad_2, TestTemplate.bad_list_2)
    def test_write_cache_bad_listing_bad_hash(self):
        new_dict = self.bad_list_2
        new_dict['http://www.feedforall.com/sample.xml'] = '1'*random.randint(1,127)
        self.assertFalse(fetch.write_cache(self.bad_2, new_dict))

    def test_get_cache(self):
        listing = fetch.get_cache(self.sample_file)
        self.assertEqual(self.sample_list, listing)

    def test_get_cache_bad_path(self):
        self.assertRaises(FileNotFoundError,
                    fetch.get_cache, "foo_bar.baz")

    def test_get_cache_bad_listing_file_1(self):
        self.assertRaises(ValueError,
                fetch.get_cache, self.bad_1)

    def test_get_cache_bad_listing_file_2(self):
        self.assertRaises(ValueError,
                fetch.get_cache, self.bad_2)

    @cover(TestTemplate.sample_file, TestTemplate.sample_list)
    def test_get_content(self):
        fetch.get_content(self.sample_file)
        time.sleep(15) # B Nice 2 Da Site
        updates_2 = fetch.get_content(self.sample_file)
        self.assertEqual([], list(updates_2))

    def test_get_content_bad_path(self):
        self.assertRaises(FileNotFoundError,
                fetch.get_content, "foo_bar.baz")

@unittest.skip("Tests are not yet implemented")
class TestFeedRead(TestTemplate):

    # I don't know how to test this yet, because it is basically all async
    # stuff
    pass

@unittest.skip("Tests are not yet implemented")
class TestMain(TestTemplate):

    '''
        Test the argparser and configparser as well as main actions
    '''
    pass

if __name__ == "__main__":
    unittest.main(warnings='ignore', argv=['-b'])


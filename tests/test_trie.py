#!/usr/bin/env python3
""" Module for testing the class Trie """

import unittest
from src.trie import Trie
from src.errors import SearchMiss

file_path_tiny = "../spellchecker/tiny_dictionary.txt"

class TestTrie(unittest.TestCase):
    """ Submodule for unittests, derives from unittest.TestCase """

    def setUp(self):
        """ setup """
        trie = Trie.create_from_file(file_path_tiny)
        self.trie = trie

    #1
    def test_methods_case_sensetive_ok(self):
        """ Test if methods is case sensetive """
        # add_word
        self.trie.add_word("DonkeY")
        add_word_result = self.trie.check_word("donkey")
        self.assertEqual(add_word_result, True, " Should return True ")

        # check_word
        check_word_result_1 = self.trie.check_word("oFFeR")
        self.assertEqual(check_word_result_1, True, " Should return True ")

        # prefix_search
        prefix_search_result = self.trie.prefix_search("oFfE")
        self.assertEqual(prefix_search_result, ['offer'], " Should return ['offer'] ")

        # remove_word
        self.trie.remove_word("PoSSibLe")
        try:
            check_word_result_2 = self.trie.check_word("possible")
        except SearchMiss:
            check_word_result_2 = False
        self.assertEqual(check_word_result_2, False, " Should return False ")

    #2
    def test_add_word_ok(self):
        """ Test if add_word method works correctly """
        self.trie.add_word("computer")
        check_result = self.trie.check_word("computer")
        self.assertEqual(check_result, True, " Should return True ")

    #3
    def test_check_word_in_dict_ok(self):
        """ Test if check_word method works correctly when word is in dict """
        check_result = self.trie.check_word("hungry")
        self.assertEqual(check_result, True, " Should return True ")

    #4
    def test_check_word_not_in_dict_ok(self):
        """
        Test if check_word method works correctly when word is not in dict,
        should raise SearchMiss
        """

        with self.assertRaises(SearchMiss) as _:
            self.trie.check_word("dunderhonung")

    #5
    def test_remove_word_in_dict_ok(self):
        """ Test if remove_word method works correctly when word is in dict """
        self.trie.remove_word("possible")
        try:
            check_result = self.trie.check_word("possible")
        except SearchMiss:
            check_result = False

        self.assertEqual(check_result, False, " Should return False ")

    #6
    def test_remove_word__not_in_dict_ok(self):
        """
        Test if remove_word method works correctly when word is not in dict,
        should raise SearchMiss
        """

        with self.assertRaises(SearchMiss) as _:
            self.trie.remove_word("glassbil")

    #7
    def test_prefix_search_ok(self):
        """ Test if prefix_search method works correctly """
        prefix_result = self.trie.prefix_search("care")
        self.assertEqual(prefix_result, ['carefully'], " Should return ['carefully'] ")

    #8
    def test_get_all_words_count_ok(self):
        """ Test if get_all_words_count method works correctly """
        get_all_words_count_result = self.trie.get_all_words_count(file_path_tiny)
        self.assertEqual(get_all_words_count_result, 170, " Should return 170 ")

    #9
    def test_get_all_words_list_ok(self):
        """ Test if get_all_words_list method works correctly """
        get_all_words_list_result = self.trie.get_all_words_list(file_path_tiny)
        sliced_list = get_all_words_list_result[:5]
        self.assertEqual(sliced_list, ['the', 'done', 'possible', 'fellow', 'lives'],
            " Should return ['the', 'done', 'possible', 'fellow', 'lives'] ")

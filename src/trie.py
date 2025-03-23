#!/usr/bin/env python3
""" Contains the class Trie """
from src.node import Node
from src.errors import SearchMiss

class Trie:
    """ Trie class """
    def __init__(self):
        """ Constructor for class """
        self.root = Node()

    def add_word(self, word):
        """ Add word to trie """
        node = self.root
        word = word.lower()
        for char in word:
            if char not in node.children:
                node.children[char] = Node()
            node = node.children[char]
        node.is_end = True

    def check_word(self, word):
        """ Check if word in trie """
        node = self.root
        word = word.lower()
        for char in word:
            if char not in node.children:
                raise SearchMiss
            node = node.children[char]
        if not node.is_end:
            raise SearchMiss
        return node.is_end

    def remove_word(self, word):
        """ Remove word and unused nodes from trie """
        word = word.lower()
        self._remove_word_helper(self.root, word)
        self._cleanup_unused_nodes(self.root)

    def _remove_word_helper(self, node, word):
        """ Helper for remove_word """
        for char in word:
            if char not in node.children:
                raise SearchMiss
            node = node.children[char]

        if not node.is_end:
            raise SearchMiss
        node.is_end = False

    def _cleanup_unused_nodes(self, node):
        """ Helper for remove_word """
        children_to_delete = []
        for char, child_node in node.children.items():
            if not child_node.is_end and not child_node.children:
                children_to_delete.append(char)
            else:
                self._cleanup_unused_nodes(child_node)

        for char in children_to_delete:
            del node.children[char]

    def prefix_search(self, prefix):
        """ Search for words in trie beginning with prefix """
        words_list = []
        prefix = prefix.lower()
        node = self.root
        for char in prefix:
            if char not in node.children:
                return []
            node = node.children[char]

        self._find_words(node, prefix, words_list)
        return words_list

    def _find_words(self, node, prefix, words_list):
        """ Helper for prefix_search """
        if node.is_end:
            words_list.append(prefix)

        for char, child_node in node.children.items():
            self._find_words(child_node, prefix + char, words_list)

    def get_all_words_count(self, file_path):
        """ Returns number of words in file """
        with open(file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()
            word_count = len(lines)
        return word_count

    def get_all_words_list(self, file_path):
        """ Returns list with all words in file """
        words_list = []
        with open(file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()
            for line in lines:
                word = line.split()
                words_list.extend(word)
        return words_list

    @classmethod
    def create_from_file(cls, file_path = "../spellchecker/dictionary.txt"):
        """ Returns trie object filled with words from file """
        trie = cls()
        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                word = line.strip()
                trie.add_word(word)
        return trie

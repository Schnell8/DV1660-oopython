#!/usr/bin/env python3
""" Contains the class Error """

class Error(Exception):
    """ User defined class for custom exceptions """

class SearchMiss(Error):
    """ Raised when word is missing """

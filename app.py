#!/usr/bin/env python3
""" Spellchecker flask app """

import traceback
import re
import os
from src.errors import SearchMiss
from src.trie import Trie
from flask import Flask, render_template, redirect, request, url_for, session

dict_list = ["../spellchecker/tiny_dictionary.txt", "../spellchecker/dictionary.txt"]

app = Flask(__name__)
app.secret_key = re.sub(r"[^a-z\d]", "", os.path.realpath(__file__))

@app.route('/')
def main():
    """ Main route """

    return render_template('index.html')

@app.route('/init', methods=["POST"])
def init():
    """ Intialize values needed in session """
    session['prefix_input'] = ""
    session['words_to_remove'] = []
    session['dict'] = dict_list[1]

    return redirect(url_for('spellchecker'))

@app.route('/spellchecker', methods=["GET"])
def spellchecker():
    """ Spellchecker route """

    return render_template(
        'spellchecker.html'
        )

@app.route('/check_word', methods=["GET"])
def check_word():
    """ Check route """

    return render_template(
        'check_word.html'
        )

@app.route('/check_word_help', methods=['POST'])
def check_word_help():
    """ Fetch word input and get result """
    trie_obj = Trie.create_from_file(session['dict'])
    check_input = request.form.get("check_input")

    ### check if word is in dictionary ###
    try:
        check_result = trie_obj.check_word(check_input)
    except SearchMiss:
        check_result = False

    return render_template(
        'check_word.html',
        check_result = check_result,
        check_input = check_input
        )

@app.route('/remove_word', methods=["GET"])
def remove_word():
    """ remove route """

    return render_template(
        'remove_word.html'
        )

@app.route('/remove_word_help', methods=['POST'])
def remove_word_help():
    """ Fetch word input, check if in dict, store words in session and finally remove words """
    trie_obj = Trie.create_from_file(session['dict'])
    remove_input = request.form.get("remove_input")

    ### check if word is in dict otherwise redirect ###
    try:
        check_result = trie_obj.check_word(remove_input)
    except SearchMiss:
        check_result = False

    if check_result is False:
        return render_template(
            'remove_word.html',
            check_result = check_result,
            remove_input = remove_input
            )

    ### get words to remove and store new values ###
    words_to_remove = session['words_to_remove']
    words_to_remove.append(remove_input)
    session["words_to_remove"] = words_to_remove

    ### remove words ###
    for word in words_to_remove:
        trie_obj.remove_word(word)

    return render_template(
        'remove_word.html',
        check_result = check_result,
        remove_input = remove_input
        )

@app.route('/prefix_search', methods=["GET"])
def prefix_search():
    """ Prefix search route """
    prefix_input = session['prefix_input']
    prefix_input_len = len(prefix_input)

    return render_template(
        'prefix_search.html',
        prefix_input = prefix_input,
        prefix_input_len = prefix_input_len
        )

@app.route('/prefix_search_help', methods=['POST'])
def prefix_search_help():
    """ Fetch prefix input, store input in session and get result """
    trie_obj = Trie.create_from_file(session['dict'])
    prefix_input = request.form.get("prefix_input")
    prefix_input_len = len(prefix_input)

    ### store prefix input in session ###
    session["prefix-input"] = prefix_input

    ### get result from prefix search ###
    prefix_result = trie_obj.prefix_search(prefix_input)

    return render_template(
        'prefix_search.html',
        prefix_result = prefix_result,
        prefix_input = prefix_input,
        prefix_input_len = prefix_input_len
        )

@app.route('/list_words', methods=["GET"])
def list_words():
    """ List words route """
    trie_obj = Trie.create_from_file(session['dict'])

    ### get words to remove ###
    words_to_remove = session['words_to_remove']

    ### get list with all words ###
    word_list = trie_obj.get_all_words_list(session['dict'])

    ### remove words in list ###
    updated_word_list = []
    for word in word_list:
        if word not in words_to_remove:
            updated_word_list.append(word)

    ### alphabetical order ###
    sorted_updated_word_list = sorted(updated_word_list)

    ### count words from sorted_updated_word_list ###
    word_count = len(sorted_updated_word_list)

    return render_template(
        'list_words.html',
        word_count = word_count,
        sorted_updated_word_list = sorted_updated_word_list
        )

@app.route('/change_dict', methods=["GET"])
def change_dict():
    """ Change dict route """
    current_dict = session['dict']

    return render_template(
        'change_dict.html',
        current_dict = current_dict,
        dict_list = dict_list
        )

@app.route('/change_dict_help', methods=['POST'])
def change_dict_help():
    """ Fetch selected dict, store in session and reset removed words. """
    selected_dict = request.form['selected_dict']
    session['dict'] = selected_dict
    session['words_to_remove'] = []

    return redirect(url_for('change_dict'))

@app.route("/reset")
def reset():
    """ Route for reset session """
    _ = [session.pop(key) for key in list(session.keys())]

    return redirect(url_for('main'))

@app.route('/about')
def about():
    """ About route """
    return render_template('about.html')

@app.errorhandler(404)
def page_not_found(e):
    """ Handler for page not found 404 """
    #pylint: disable=unused-argument
    return "Flask 404 here, but not the page you requested."


@app.errorhandler(500)
def internal_server_error(e):
    """ Handler for internal server error 500 """
    #pylint: disable=unused-argument
    return "<p>Flask 500<pre>" + traceback.format_exc()

if __name__ == "__main__":
    app.run(debug=True)

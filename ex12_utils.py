##############################################################################
# FILE: ex12_utils.py
# WRITERS:
# Dana Aviran, 211326608, dana.av
# Eldad Eliyahu, 318565058, eldad333
# EXERCISE: Intro2cs2 ex12 2021-2022
##############################################################################
import boggle_board_randomizer

WORD_BOOLEAN = 0
PATH_BOOLEAN = 1


def load_words_to_lst(file_name):
    """
    This function loads the words of file_name in a set, so each words appears
    just once.
    :return: A list of all words, created first as a set
    """
    lst_of_words = set()
    with open(file_name) as file:
        file_words = file.readlines()
    for word in file_words:
        lst_of_words.add(word[:-1])
    return list(lst_of_words)


def find_max_word(word_lst):
    word_lst.sort(key=len)
    return len(word_lst[-1])


def board_word_combinations(board, words):
    """

    :param board: board: a randomized board
    :param words: A list of all words
    :return: A list of all words that are comprised of the letters on the board
    """
    lst_of_letters = []
    sorted_lst_of_words = []
    boolean = True
    # Appends to a list all the letters on the board
    for i in range(len(board)):
        for j in range(len(board[0])):
            lst_of_letters.append(board[i][j])
    for word in words:
        for letter in word:
            if letter not in lst_of_letters:
                boolean = False
                break
        if boolean:
            sorted_lst_of_words.append(word)
        boolean = True
    return sorted_lst_of_words


def is_coord_in_board(board, coord):
    """
    A helper function to check if the coords are inside the board.
    :param board: the randomized board
    :param coord: the coord
    :return: True if it is in the board, False otherwise
    """
    row, col = coord
    if col < 0 or row < 0 or col >= len(board[0]) or row >= len(board):
        return False
    else:
        return True


def is_valid_path(board, path, words):
    """
    This function gets a board, a path and a list of words, and checks if the
    path is valid. If the path is valid by instructions og Boggle Game and
    the word is in the word list, it is considered valid.
    :param board: the randomized board
    :param path: the path - a list of tuples - the coords
    :param words: a list of all words
    :return:
    """
    if not path or not is_coord_in_board(board, path[0]):
        return
    if len(path) == 1:
        word = board[0][0]
        if word in words:
            return word
        else:
            return
    word = ""
    prev_row, prev_col = path[0]
    current_path = [path[0]]
    for i in range(1, len(path)):
        cur_coord = path[i]
        row, col = cur_coord
        if ((abs(row - prev_row) + abs(col - prev_col) == 1)
            or (abs(row - prev_row) + abs(col - prev_col) == 2 and
                (row != prev_row and col != prev_col))) and is_coord_in_board\
                    (board, cur_coord) and cur_coord not in current_path:
            current_path.append(cur_coord)
            word += board[prev_row][prev_col]
            prev_row, prev_col = row, col
            if i == len(path) - 1:
                word += board[row][col]
        else:
            return
    if word in words:
        return word


def find_length_n_paths(n, board, words):
    """
    This function gets an integer n, a randomized board and a list of words.
    It uses helper functions in order to return a list of all paths of n cells
    that represent a word that is found in the word list.
    :param n: integer that describes the length of paths we need to find
    :param board: a randomized board
    :param words: a list of words
    :return: A list of lists of tuples, each sub-list represents a path on the
    board, while the tuples are the coordinates. the path represents a valid word.
    """
    # First helper function, returns a list of tuples of (word, path)
    lst_of_all_tuples = find_length_n_helper1(n, board, words, PATH_BOOLEAN)
    # another helper function, returns a list of paths only.
    return separate_tuple_lst_helper1(lst_of_all_tuples)


def find_length_n_words(n, board, words):
    """
    This function gets an integer n, a randomized board and a list of words.
    It uses helper functions in order to return a list of all paths that
    represent words in length n, found on the board.
    :param n:  integer that describes the length of words we need to find
    :param board: a randomized board
    :param words: a list of words
    :return: A list of lists of tuples, each sub-list represents a path on the
    board, while the tuples are the coordinates. the path represents a valid word.
    """
    # First helper function, returns a list of tuples of (word, path)
    lst_of_all_tuples = find_length_n_helper1(n, board, words, WORD_BOOLEAN)
    # another helper function, returns a list of paths only.
    return separate_tuple_lst_helper1(lst_of_all_tuples)


def separate_tuple_lst_helper1(lst_of_all_tuples):
    """
    A helper function that separates the list of tuples of (word, path)
    returned from the first helper function, to a list of sub-lists,
    each contains tuples that represent a path in the board.
    :param lst_of_all_tuples:
    :return: a list of sub-lists, each contains tuples that represent a path
    in the board.
    """
    lst_of_all_paths = []
    for current_tup in lst_of_all_tuples:
        word, path = current_tup
        lst_of_all_paths.append(path)
    return lst_of_all_paths


def find_length_n_helper1(n, board, words, boolean):
    """
    This function returns all the tuples of words and paths of the length n in
    the board and a list of all coordinates of its letters.
    :param n: a word's length (in letters, not in path)
    :param board: a list of lists that represents a board
    :param words: a dictionary of words
    :param boolean: coordinate of result (0 for words, 1 for paths)
    :return: a list of paths of words of length n
    """
    lst_tuples_paths = []
    # iteration over all coordinates of the board
    for row in range(len(board)):
        for col in range(len(board[0])):
            coord_lst_of_tuple_paths = find_length_n_helper2(n, row, col,
                                                             board, words, "",
                                                             [], boolean, [])
            # we check the current list of tuples - (word, path)
            if coord_lst_of_tuple_paths:
                for current_tup in coord_lst_of_tuple_paths:
                    word, path = current_tup
                    if path not in [tup[1] for tup in lst_tuples_paths]:
                        lst_tuples_paths.append(current_tup)
    return lst_tuples_paths


def valid_row_directions_helper2(row, board):
    """
    A helper function of the second helper function.
    It calculates the valid row coordinates that a given coord can go to the
    direction of, according to the instructions and inside the board,
    to build a path in the game.
    :param row: the row of the coord
    :param board: a randomized board
    :return: A list of int numbers that represent the valid rows that a certain
    coord can go towards.
    """
    valid_row_lst = []
    for row in range(row - 1, row + 2):
        if 0 <= row < len(board):
            valid_row_lst.append(row)
    return valid_row_lst


def valid_col_directions_helper2(col, board):
    """
    A helper function of the second helper function.
    It calculates the valid column coordinates that a given coord can go to the
    direction of, according to the instructions and inside the board,
    to build a path in the game.
    :param col: the col of the coord
    :param board: a randomized board
    :return: A list of int numbers that represent the valid cols that a certain
    coord can go towards.
    """
    valid_col_lst = []
    for col in range(col - 1, col + 2):
        if 0 <= col < len(board):
            valid_col_lst.append(col)
    return valid_col_lst


def find_length_n_helper2(n, i, j, board, words, word, path, boolean,
                          word_and_path_lst):
    """
    A recursive second helper function. It gets an integer n that indicates the
    wanted word or path length, according to the boolean argument.
    It also gets the current coordinate on the board by the i, j variables,
    the list of words, the current word, the current path, the boolean mentioned
    and the current list of tuples of (word, path), created by the function.
    :param n:
    :param board:
    :param i: the row of the current coord on the board
    :param j: the column of the current coord on the board
    :param words: the list of valid words
    :param word: the current word, created by the current path of recursive
    iteration on the board
    :param path: the current path, a list of tuples
    :param boolean: a boolean that indicates if the goal is a word or a path of
    length n
    :param word_and_path_lst: the list that contains all of the valid tuples
    :return: The word_and_path_lst list that contains all the tuples of (word,
    path) that represent word of length n or paths of length n (not both),
    according to the boolean.
    """

    # Stop Conditions
    if ((boolean == WORD_BOOLEAN and len(word) == n) or
        (boolean == PATH_BOOLEAN and len(path) == n)) and\
            (word, path) not in word_and_path_lst and word in words:
        word_and_path_lst.append((word, path))
    if (boolean == WORD_BOOLEAN and len(word) > n) or (boolean == PATH_BOOLEAN
                                                       and len(path) > n):
        return
    # Define current word list
    if word:
        cur_word_lst = []
        for cur_word in words:
            if cur_word.startswith(word):
                cur_word_lst.append(cur_word)
        # If no word starts with the current letter, we return None
        if not cur_word_lst:
            return
    else:
        cur_word_lst = words
    # Recursive iteration over the valid directions of current coord
    for row in valid_row_directions_helper2(i, board):
        for col in valid_col_directions_helper2(j, board):
            if (row, col) not in path:
                find_length_n_helper2(n, row, col, board, cur_word_lst,
                                      word + board[row][col],
                                      path + [(row, col)], boolean,
                                      word_and_path_lst)
            else:
                continue
    return word_and_path_lst


def max_score_paths(board, words):
    """
    This function gets a board and a list of words and returns a list of paths
    that represent the maximum score of the game, given the instructions that
    the score is calculated by the length of the path (and not the word).
    :param board: a randomized board
    :param words: a list of words
    :return: A list of paths that represent the maximum score of the game.
    """
    words = board_word_combinations(board, words)
    final_lst = []
    dict_of_optimal_paths = {}
    min, max = 1, find_max_word(words)
    # We use the helper function that returns all paths of length n that
    # represent words from the word list
    while min <= max:
        # We use the function until there are no paths of length n
        lst_of_all_tuples = find_length_n_helper1(min, board, words, PATH_BOOLEAN)
        for cur_tup in lst_of_all_tuples:
            word, path = cur_tup
            if word not in dict_of_optimal_paths:
                dict_of_optimal_paths[word] = path
            elif len(dict_of_optimal_paths[word]) < len(path):
                dict_of_optimal_paths[word] = path
        min += 1
    for word in dict_of_optimal_paths:
        final_lst.append(dict_of_optimal_paths[word])
    return final_lst



##############################################################################
# FILE: boggle.py
# WRITERS:
# Dana Aviran, 211326608, dana.av
# Eldad Eliyahu, 318565058, eldad333
# EXERCISE: Intro2cs2 ex12 2021-2022
##############################################################################

from boggle_board_randomizer import randomize_board
from ex12_utils import *
from application import *



class Boggle:
    """
    The logic class of the Boggle Game. Uses the GUI Application class to
    display the game.
    """
    def __init__(self, file_name):
        # game initializing variables
        self.board = randomize_board()
        self.lst_of_words = load_words_to_lst(file_name)
        self.score = 0
        self.lst_of_found_words = []
        self.current_path = []
        self.keep_countdown = True
        self.is_first_game = True
        # We make an Application object for the game, and send the command
        # functions of each action of the user
        self.app = Application(self.board, self.clicked_on_letter_button,
                               self.clicked_on_submit_word,
                               self.check_if_another_round)

    def start_game(self):
        """
        Starts the Boggle Game using the application GUI
        :return:
        """
        if self.is_first_game:
            self.app.make_init_board_display()
        self.app.make_found_words_label()
        self.app.countdown()
        self.app.start_game()

    def clicked_on_letter_button(self, event):
        """
        This function checks which letter button was clicked and raised an event
        and proceeds accordingly - if the coord is valid, it adds it to the
        :param event: the event raised by clicking the letter button in the GUI
        :return: None
        """
        # going through all the buttons on the board if the button was clicked
        for button in self.app.dict_of_letter_buttons:
            if button is event.widget:
                coord = self.app.dict_of_letter_buttons[button]
                if (len(self.app.current_path) != 0 and
                    self.check_coord(coord)) or not self.app.current_path:
                    self.app.update_chosen_letters_display(coord)
                    self.current_path.append(coord)

    def check_coord(self, coord):
        """
        Checks if the current coord button pressed is a valid one according to
        the previous coord and the rules of the Boggle Game.
        :param coord: the coord the user tried to choose
        :return: True if the coord is valid, False otherwise
        """
        length = len(self.app.current_path)
        prev_row, prev_col = self.app.current_path[length - 1]
        row, col = coord
        if (abs(row - prev_row) + abs(col - prev_col) == 1 or
            (abs(row - prev_row) + abs(col - prev_col) == 2 and
             (row != prev_row and col != prev_col))) and \
                (0 <= col < len(self.board[0]) and 0 <= row < len(self.board)) \
                and coord not in self.app.current_path:
            return True
        else:
            return False

    def clicked_on_submit_word(self, event):
        """
        This function proceeds to the event of clicking the submit word button
        in the user GUI.
        :param event: click on the submit button
        :return: True if the word is in the lst of words, False otherwise
        """
        boolean = True
        if self.app.submit_button is event.widget:
            self.app.init_chosen_letters_display()
            word = self.app.current_word
            if word in self.lst_of_words and word not in self.lst_of_found_words:
                self.lst_of_found_words.append(word)
                self.score += len(word) ** 2
                # update in the display
                self.app.update_score(self.score)
                self.app.lst_of_found_words.append(word)
                self.app.display_found_word()
            else:
                boolean = False
            self.app.init_chosen_letters_display()
            self.current_path = []
            self.app.current_path = []
            self.app.current_word = ""
            return boolean

    def check_if_another_round(self):
        """
        This function is raised when the countdown is finished, and calls the
        message which asks the user if he wants to play again.
        If he does, we initialize the Game and the App variables
        :return:
        """
        is_another_round = self.app.display_another_round_message()
        if is_another_round:
            self.is_first_game = False
            self.board = randomize_board()
            self.score = 0
            self.lst_of_found_words = []
            # In the GUI
            self.app.board = self.board
            self.app.init_app_for_another_round()
            # and starts another round
            self.start_game()
        else:
            self.app.root.destroy()


if __name__ == "__main__":
    boggle_game = Boggle("boggle_dict.txt")
    boggle_game.start_game()

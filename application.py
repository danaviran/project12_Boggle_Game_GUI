##############################################################################
# FILE: application.py
# WRITERS:
# Dana Aviran, 211326608, dana.av
# Eldad Eliyahu, 318565058, eldad333
# EXERCISE: Intro2cs2 ex12 2021-2022
##############################################################################

from tkinter import *
from tkinter import messagebox

HEIGHT = 4
WIDTH = 4
TIME = 180
ROOT_WIDTH = 670
ROOT_HEIGHT = 550
ROOT_TITLE = "BOGGLE GAME"
IS_ANOTHER_ROUND_MSG = "Well Done! \n Do you want to start another round?"
INSTRUCTIONS = "Instructions: \n1. Find as many words as you can in 3 " \
               "minutes. \n" "2. Pick cells only at radius of ONE CELL from " \
               "prev chosen. \n" "3. You can also pick diagonally. \n" \
                    "4. Click SUBMIT to check if the word you picked is " \
               "valid. \n" "5. Press to start game. Good Luck Friend!"
LIMIT_TO_SPLIT = 40


class Application(Frame):
    """
    A class of Application objects, to display the Boggle Game.
    """
    def __init__(self, board, chose_word_action, submit_action,
                 check_if_another_round):
        self.root = Tk()
        Frame.__init__(self, self.root)

        # game configure elements
        self.board = board
        self.time = TIME
        self.current_word = ""
        self.score = 0
        self.current_path = []
        self.lst_of_found_words = []

        # dict of the visual tkinter buttons and their coords on the board
        self.dict_of_letter_buttons = {}

        # commands to call from the App when an event is made
        self.chose_word_action = chose_word_action
        self.submit_command = submit_action
        self.check_if_another_round = check_if_another_round

    def start_game(self):
        """
        starts the main loop.
        :return: None
        """
        self.root.mainloop()

    # SETTINGS OF THE TKINTER GUI
    def init_general_root_settings(self):
        """
        General settings of the root window
        :return: None
        """
        self.root.frame()
        self.root.title(ROOT_TITLE)
        # get the screen dimension
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        # find the center point
        center_x = int(screen_width / 2 - ROOT_WIDTH / 2)
        center_y = int(screen_height / 2 - ROOT_HEIGHT / 1.7)
        # set the position of the window to the center of the screen
        self.root.geometry(
            f'{ROOT_WIDTH}x{ROOT_HEIGHT}+{center_x}+{center_y}')
        # layout on the root window
        self.root.columnconfigure(0, weight=4)
        self.root.columnconfigure(1, weight=1)

    def make_frames_of_root(self):
        """
        Makes different frames of root in order to place widgets on it.
        :return: None
        """
        self.timer_frame = LabelFrame(self.root, padx=1, pady=1)
        self.timer_frame.pack(padx=1, pady=5, side=TOP)

        self.word_label_frame = LabelFrame(self.root, padx=5, pady=5)
        self.word_label_frame.pack(padx=5, pady=5)

        self.board_frame = LabelFrame(self.root, padx=10, pady=10)
        self.board_frame.pack(padx=10, pady=10)

        self.found_words_frame = LabelFrame(self.root, padx=2, pady=2)
        self.found_words_frame.pack(padx=1, pady=1)

    def make_current_word_label(self):
        """
        Makes the word label of chosen letters from the board, that displays
        when a user chooses a cell from the board
        :return: None
        """
        self.current_word = ""
        self.cur_word_text = StringVar(value="")
        self.cur_word_label = Label(self.word_label_frame,
                                    textvariable=self.cur_word_text,
                                    bg="white",
                                    fg="Black", width=30, height=1,
                                    font=('Helvetica', '20'))
        self.cur_word_label.grid(column=2, row=6)

    def make_board_submit_button(self):
        """
        Makes the submit word button.
        :return: None
        """
        self.submit_button = Button(self.word_label_frame, text="SUBMIT",
                                    font=('Helvatical bold', 11),
                                    bg='light green', fg='black')
        self.submit_button.grid(column=2,row=10)
        self.click_on_submit()

    def make_found_words_label(self):
        """
        Makes the found words label to display all the found words added during
        the game.
        :return: None
        """
        self.found_words_text = StringVar(value="FOUND WORDS:\n")
        self.found_words_label = Label(self.found_words_frame,
                                       textvariable=self.found_words_text, height=5,
                                       width=70, font=("courier new", 10),
                                       bg='orange')
        self.found_words_label.grid(row=10, column=2)

    def make_timer_label(self):
        """
        Makes the timer label, to display the current time that is left for the
        current round.
        :return: None
        """
        self.timer_text = StringVar(value="")
        self.timer_label = Label(self.timer_frame,
                                       textvariable=self.timer_text, height=2,
                                       width=10, font=("courier new", 15),
                                       bg='red', fg='black')
        self.timer_label.grid(row=3, column=2)

    def make_score_label(self):
        """
        Makes the score label the is used to display the current score of the
        user.
        :return: None
        """
        self.score_text = StringVar(value="score")
        self.score_label = Label(self.timer_frame,
                                       textvariable=self.score_text, height=2,
                                       width=10, font=("courier new", 15),
                                       bg='green')
        self.score_label.grid(row=3, column=1)

    def make_board_buttons(self, board):
        """
        Makes the letter buttons that will be used as the board of the game.
        :param board: the randomized board of the current round.
        :return: None
        """
        # Makes a SIZE x SIZE grid of text entry boxes
        for i in range(HEIGHT):
            for j in range(WIDTH):
                cur_button = Button(self.board_frame,
                                    text=board[i][j], bg="skyBlue",
                                    fg="Black", width=3, height=1,
                                    font=('Helvetica', '20'))
                self.dict_of_letter_buttons[cur_button] = (i, j)
            i_grid, j_grid = 0, 0
            for button in self.dict_of_letter_buttons:
                if i_grid == HEIGHT and j_grid == WIDTH:
                    break
                if j_grid >= WIDTH:
                    i_grid += 1
                    j_grid = 0
                button.grid(column=j_grid + 5, row=i_grid)
                j_grid += 1
        self.click_on_letters()

    # COUNTDOWN SETTINGS
    def countdown(self):
        """
        Creates the initialized timer of the game and starts its ticking.
        When the countdown is over, we call the function that displays a message.
        :return: None
        """
        current_time = self.time
        if current_time >= 0:
            mins = current_time // 60
            secs = current_time % 60
            timer = '{:02d}:{:02d}'.format(mins, secs)
            self.timer_text.set(timer)
            self.time -= 1
            self.timer_label.after(1000, self.countdown)
        else:
            self.check_if_another_round()

    # COMMANDS SETTINGS
    def click_on_letters(self):
        """
        Binds the action of clicking on a button on the board to the app
        function that calls a command function in the Game class
        :return:
        """
        for button in self.dict_of_letter_buttons:
            button.bind("<Button-1>", self.chose_word_action)

    def click_on_submit(self):
        """
        Binds the action of clicking on submit button to the app function that
        calls a command function in the Game class
        :return:
        """
        self.submit_button.bind("<Button-1>", self.submit_command)

    # UPDATES OF THE GAME
    def update_chosen_letters_display(self, coord):
        """
        Updates the display of current word after choosing a cell from the board
        :param coord: the coord of button pressed on the board
        :return: None
        """
        row, col = coord
        self.current_word += self.board[row][col]
        self.cur_word_text.set(self.current_word)
        self.current_path.append(coord)

    def init_chosen_letters_display(self):
        """ After clicking on submit, the current word label is initialized.
        :return: None
        """
        self.cur_word_text.set("")

    def update_score(self, score):
        """
        Updates the display of score of the game.
        :param score: the current score
        :return: None
        """
        self.score_text.set(score)

    def display_found_word(self):
        """
        Updates the current display of found words
        :return:
        """
        represent_str = ""
        current_segment_length = 0
        for i in range(len(self.lst_of_found_words)):
            represent_str += self.lst_of_found_words[i]
            current_segment_length += len(self.lst_of_found_words[i])
            if i != len(self.lst_of_found_words) - 1:
                represent_str += ", "
                current_segment_length += 2
            if current_segment_length > LIMIT_TO_SPLIT:
                represent_str += "\n"
                current_segment_length = 0
        self.found_words_text.set(represent_str)

    # MESSAGES
    def display_start_message(self):
        """
        Displays a starts message of instructions (starting the countdown when
        the user clicks starts)
        :return:
        """
        messagebox.showinfo('WELCOME TO BOGGLE', message=INSTRUCTIONS)

    @staticmethod
    def display_another_round_message():
        """
        A static method, to get a value from the answer.
        When the countdown is over, displays a message if the user wants to
        play another round or not.
        :return: True if another round, False otherwise.
        """
        return messagebox.askyesno("End of Round", IS_ANOTHER_ROUND_MSG)

    # BUILDING THE GUI FOR THE GAME
    def make_init_board_display(self):
        """
        Initializing all the Application widgets of the game at once.
        :return: None
        """
        self.display_start_message()
        self.init_general_root_settings()
        self.make_frames_of_root()
        self.make_board_buttons(self.board)
        self.make_board_submit_button()
        self.make_timer_label()
        self.make_score_label()
        self.make_current_word_label()

    def init_app_for_another_round(self):
        """
        Initializing the current app object for the next round.
        :return: None
        """
        self.score_text.set('SCORE')
        self.cur_word_text.set(" ")
        self.current_word = ""
        self.current_path = []
        self.found_words_text.set('FOUND WORDS')
        self.time = TIME
        self.lst_of_found_words = []
        self.dict_of_letter_buttons = {}
        self.make_board_buttons(self.board)

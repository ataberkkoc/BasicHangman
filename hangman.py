import curses
import re
from views import levels, select_type_screen
from random import choice
from sentence_types import Types


class Hangman:
    def __init__(self, stdscr):
        self.levels = levels
        self.level_number = 7
        self.stdscr = stdscr
        self.sentences = None
        self.window_size = stdscr.getmaxyx()

    def display_screen(self, word_predicted):
        self.stdscr.clear()
        self.stdscr.addstr(0, 0, self.levels[self.level_number])
        self.stdscr.addstr(self.window_size[0]//3, self.window_size[1]//2, "  ".join(word_predicted))
        self.stdscr.refresh()

    def show_answer(self, word):
        answer = " ".join(list(map(lambda x: "_" + x + "_" if not x.isspace() else " ", word)))
        self.stdscr.addstr(self.window_size[0]//3, self.window_size[1]//2, answer)

    def get_char(self):
        self.stdscr.addstr(self.window_size[0]*3//4, self.window_size[1]*45//100, "Enter a char please: ")
        self.stdscr.refresh()
        pred_char = self.stdscr.getkey()
        return pred_char

    def get_string(self):
        self.stdscr.addstr(self.window_size[0]*3//4, self.window_size[1]*45//100, "Please predict the word: ")
        self.stdscr.refresh()
        pred_word = self.stdscr.getstr().decode()
        return pred_word

    def control_predict(self, pred_word, word):
        if pred_word.lower() == word.lower():
            self.show_answer(word)
            self.stdscr.addstr(self.window_size[0]//15, self.window_size[1]//2, "You predicted!!")
            self.stdscr.refresh()
            return True
        return False

    def game_result(self, pred_char, word, word_predicted):
        char_index = list(re.finditer(pred_char, word))
        if len(char_index) == 0:
            self.level_number -= 1
            if self.level_number == 1:
                self.display_screen(word_predicted)
                self.stdscr.addstr(self.window_size[0]//15,self.window_size[1]//2, "You lost game!!")
                self.show_answer(word)
                self.stdscr.refresh()
                return True
        else:
            for i in char_index:
                word_predicted[i.start()] = "_" + pred_char + "_"
                if "__" not in word_predicted:
                    self.display_screen(word_predicted)
                    self.show_answer(word)
                    self.stdscr.addstr(self.window_size[0]//15, self.window_size[1]//2, "You won game!!")
                    self.stdscr.refresh()
                    return True
        return False

    def play(self):

        word = choice(self.sentences)
        word_predicted = ["__"] * len(word)
        space_index = list(re.finditer(" ", word))
        for i in space_index:
            word_predicted[i.start()] = " "
        while True:
            self.display_screen(word_predicted)
            pred_word = self.get_string()
            self.display_screen(word_predicted)
            if self.control_predict(pred_word, word):
                break
            pred_char = self.get_char()
            if self.game_result(pred_char, word, word_predicted):
                break

    def set_type(self):
        while True:
            self.stdscr.clear()
            self.stdscr.move(self.window_size[0]//4,self.window_size[1]//2)
            for i in select_type_screen:
                self.stdscr.addstr(self.stdscr.getyx()[0], self.window_size[1]//2, i)
            self.stdscr.addstr(self.stdscr.getyx()[0]*7//6, self.window_size[1]*4//9, "Please select type for continue")
            self.stdscr.refresh()
            type_code = self.stdscr.getkey()
            if type_code.isdigit() and 0 <= int(type_code) <= Types.TYPE_COUNT:
                if int(type_code) == 0:
                    exit(0)
                self.get_sentences(int(type_code))
                break

    def get_sentences(self, type_code):
        with open(Types.get_type(type_code)) as f:

            self.sentences = f.read().splitlines()


def main(stdscr):
    curses.echo()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    stdscr.bkgd(' ', curses.color_pair(1) | curses.A_BOLD)
    game = Hangman(stdscr)
    game.set_type()
    game.play()
    stdscr.addstr(game.window_size[0]*3//4, game.window_size[1]*45//100, "Please press any key to quit")
    stdscr.getch()
    curses.endwin()
curses.wrapper(main)


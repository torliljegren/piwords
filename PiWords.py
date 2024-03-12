import random
import threading
import time
import tkinter as tk
import tkinter.ttk as ttk

SUBSTRING = "pi"
WORD_LIST_PATH = "svenska-ord.txt"
TIME_LIMIT_S = 120
REGULAR_FONT_SIZE = 50
HEADING_FONT_SIZE = 71
CLOCK_FONT_SIZE = 90
STAT_FONT_SIZE = 20
CLOCK_COLOR_NORMAL = 'green3'
CLOCK_COLOR_WARNING = 'red'


class PiWords:

    def __init__(self):
        self.running = False
        self.pi_words = self.read_pi_words()
        self.secs = TIME_LIMIT_S
        self.clockthread = threading.Thread(target=self.clock_tick)
        self.entered_words = list()
        self.correct_words = list()
        self.rejected_words = list()

        self.root = tk.Tk()
        self.root.title("PiWords")
        self.frame = ttk.Frame(master=self.root)
        self.lblheading = ttk.Label(master=self.frame, text="Skriv så många ord du kan som innehåller", style="Heading.TLabel")
        self.substringvar = tk.StringVar(master=self.frame, value=SUBSTRING + " t.ex. " + self.random_words(self.pi_words))
        self.lblsubstring = ttk.Label(master=self.frame, textvariable=self.substringvar, style="Heading.TLabel")
        self.lblinfo = ttk.Label(master=self.frame, text="på tiden " + self.time_left(TIME_LIMIT_S))
        self.lblpress = ttk.Label(master=self.frame, text="Tryck Enter efter varje ord")
        self.clockframe = ttk.Frame(master=self.frame, style="Clock.TFrame")
        self.clockvar = tk.StringVar(master=self.frame, value=self.time_left(TIME_LIMIT_S))
        self.clocklbl = ttk.Label(master=self.clockframe, textvariable=self.clockvar, style="Clock.TLabel")
        self.txtvar = tk.StringVar(master=self.frame)
        self.txtfield = ttk.Entry(textvariable=self.txtvar, font=("Helvetica", REGULAR_FONT_SIZE))

        self.frame.grid(sticky='nsew')
        self.lblheading.grid(row=0, column=0, pady=(10, 25))
        self.lblsubstring.grid(row=1, column=0, pady=(5, 50))
        self.lblinfo.grid(row=2, column=0, pady=25)
        self.lblpress.grid(row=3, column=0)
        self.txtfield.grid(row=4, column=0, pady=(20, 100))
        self.clocklbl.grid(row=0, column=0, padx=20, pady=20)
        self.clockframe.grid(row=5, column=0, pady=80)
        self.clockframe.grid_columnconfigure(0, minsize=800)

        self.txtfield.bind("<Return>", self.enter_pressed)
        self.txtfield.bind("<Escape>", lambda e: self.game_over())

        # configure styles #
        self.style = ttk.Style(self.root)
        self.style.configure("TLabel", font=("Helvetica", REGULAR_FONT_SIZE))
        self.style.configure("Heading.TLabel", font=("Helvetica", HEADING_FONT_SIZE, "bold"))
        self.style.configure("Clock.TLabel", font=("Helvetica", CLOCK_FONT_SIZE), foreground=CLOCK_COLOR_NORMAL,
                             background="black", borderwidth=20, bordercolor='black')
        self.style.configure("Clock.TFrame", background="black", bordercolor="grey", borderwidth=4)
        self.style.configure("Stat.TLabel", font=("Helvetica", STAT_FONT_SIZE))
        self.style.configure("Correct.Stat.TLabel", foreground="green")
        self.style.configure("Rejected.Stat.TLabel", foreground="red")

        self.txtfield.focus_set()
        self.root.mainloop()

    def read_pi_words(self) -> tuple:
        i = 0
        txtfile = open(WORD_LIST_PATH, "+r")
        print("Opened " + WORD_LIST_PATH)
        templist = list()
        print("Loading words... ", end="")
        for line in txtfile:
            i += 1
            if SUBSTRING in line:
                templist.append(line.strip("-").strip())
        print("completed!")
        print(WORD_LIST_PATH + " contained " + str(i) + " words")
        print(str(len(templist)) + " words contained the substring" + SUBSTRING + ", for example:")
        print(self.random_words(templist, 3))
        return tuple(templist)

    def enter_pressed(self, e=None):
        if self.txtvar.get() == "":
            self.change_substring_heading_example_word()
            return

        if not self.running:
            self.start_game()

        self.entered_words.append(self.txtvar.get().lower())
        self.txtvar.set("")
        self.txtfield.focus_set()

    def change_substring_heading_example_word(self):
        self.substringvar.set(SUBSTRING + " t.ex. " + self.random_words(self.pi_words))

    def check_words(self):
        for inputword in self.entered_words:
            if inputword in self.pi_words:
                self.correct_words.append(inputword)
            else:
                self.rejected_words.append(inputword)

        self.correct_words = list(set(self.correct_words))
        self.rejected_words = list(set(self.rejected_words))

    def start_game(self):
        self.running = True
        self.clockthread.start()

    @staticmethod
    def string_of_words_from_list(word_list: list, n=1) -> str:
        tempstring = ""
        i = 0
        separator = ""
        for word in word_list:
            if i != 0:
                separator = "\n" if i % n == 0 else ", "
            tempstring = tempstring + separator + word
            i += 1
        return tempstring

    def game_over(self):
        self.running = False
        self.check_words()
        self.show_stat_window()

        # reset the game state #
        # make a new clock thread
        self.clockthread = threading.Thread(target=self.clock_tick)
        # reset time
        self.secs = TIME_LIMIT_S
        self.clockvar.set(self.time_left(TIME_LIMIT_S))
        # reset word lists
        self.entered_words = list()
        self.rejected_words = list()
        self.correct_words = list()

    def show_stat_window(self):
        # show a window with stats
        win = tk.Toplevel()
        fr = ttk.Frame(master=win)
        lbl_info = ttk.Label(master=fr, text="Du klarade " + str(len(self.correct_words)) + " ord.")
        lbl_correct_words = ttk.Label(master=fr, text="Godkända:\n" + self.string_of_words_from_list(self.correct_words, 6), style="Correct.Stat.TLabel")
        lbl_rejected_words = ttk.Label(master=fr, text="Ej godkända:\n" + self.string_of_words_from_list(self.rejected_words, 6), style="Rejected.Stat.TLabel")
        lbl_info.grid(row=0, column=0, pady=20, padx=50)
        lbl_correct_words.grid(row=1, column=0, sticky=tk.W, padx=50)
        lbl_rejected_words.grid(row=2, column=0, sticky=tk.W, padx=50, pady=20)
        fr.grid(row=0, column=0)

    def clock_tick(self):
        while self.secs > 0 and self.running:
            self.secs -= 1
            self.clockvar.set(self.time_left(self.secs))
            if self.secs == 10:
                self.style.configure("Clock.TLabel", foreground=CLOCK_COLOR_WARNING)
            time.sleep(1)
        # restore green color to clock
        self.style.configure("Clock.TLabel", foreground=CLOCK_COLOR_NORMAL)

        # check if game was already aborted
        if self.running:
            self.game_over()

    @staticmethod
    def random_words(wordlist, n=1) -> str:
        words = ""
        for i in range(n):
            if n == 1 or i == 0:
                words = (wordlist[random.randint(0, len(wordlist)-1)])
            else:
                words = (wordlist[random.randint(0, len(wordlist)-1)]) + ", " + words
        return words

    @staticmethod
    def time_left(seconds) -> str:
        if seconds < 60:
            return str(seconds) + " s"
        else:
            mins = int(seconds/60)
            secs = seconds - 60*mins
            return str(mins) + " min " + str(secs) + " s"


if __name__ == "__main__":
    app = PiWords()

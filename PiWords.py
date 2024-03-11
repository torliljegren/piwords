
import tkinter as tk
import tkinter.ttk as ttk
import threading
import time
import random

WORD_LIST_PATH = "svenska-ord.txt"
TIME_LIMIT_S = 10


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
        self.lbl1 = ttk.Label(master=self.frame, text="Skriv så många ord du kan på " + str(TIME_LIMIT_S) + " s")
        self.lbl2 = ttk.Label(master=self.frame, text="Tryck Enter efter varje ord")
        self.clockvar = tk.StringVar(master=self.frame, value=str(TIME_LIMIT_S) + " s")
        self.clocklbl = ttk.Label(master=self.frame, textvariable=self.clockvar)
        self.txtvar = tk.StringVar(master=self.frame)
        self.txtfield = ttk.Entry(textvariable=self.txtvar)

        self.frame.grid(pady=(10, 0))
        self.lbl1.grid(row=0, column=0)
        self.lbl2.grid(row=1, column=0)
        self.txtfield.grid(row=2, column=0, pady=(20, 20))
        self.clocklbl.grid(row=3, column=0, pady=20)

        self.txtfield.bind("<Return>", self.enter_pressed)

        self.root.mainloop()

    def read_pi_words(self) ->tuple:
        i = 0
        txtfile = open(WORD_LIST_PATH, "+r")
        print("Opened " + WORD_LIST_PATH)
        templist = list()
        print("Loading words... ", end="")
        for line in txtfile:
            i += 1
            if "pi" in line:
                templist.append(line.strip("-").strip())
        print("completed!")
        print(WORD_LIST_PATH + " contained " + str(i) + " words")
        print(str(len(templist)) + " words contained the substring pi, for example:")
        print(self.random_words(templist, 3))
        return tuple(templist)

    def enter_pressed(self, e=None):
        if self.txtvar.get() == "":
            return

        if not self.running:
            self.start_game()

        self.entered_words.append(self.txtvar.get())
        self.txtvar.set("")
        self.txtfield.focus_set()

    def check_words(self):
        for inputword in self.entered_words:
            if inputword in self.pi_words:
                self.correct_words.append(inputword)
            else:
                self.rejected_words.append(inputword)

        self.correct_words = list(set(self.correct_words))
        print(self.correct_words)
        self.rejected_words = list(set(self.rejected_words))
        print(self.rejected_words)

    def start_game(self):
        self.running = True
        self.clockthread.start()

    def string_of_words_from_list(self, word_list: list) -> str:
        tempstring = ""
        for word in word_list:
            tempstring = word + "\n" + tempstring
        return tempstring

    def game_over(self):
        self.running = False
        self.check_words()

        # show a window with stats
        win = tk.Toplevel()
        fr = ttk.Frame(master=win)
        lbl_info = ttk.Label(master=fr, text="Du klarade " + str(len(self.correct_words)) + " ord.")
        lbl_correct_words = ttk.Label(master=fr, text="Godkända:\n" + self.string_of_words_from_list(self.correct_words))
        lbl_rejected_words = ttk.Label(master=fr, text="Ej godkända:\n" + self.string_of_words_from_list(self.rejected_words))
        lbl_info.grid(row=0, column=0, pady=20, padx=50)
        lbl_correct_words.grid(row=1, column=0)
        lbl_rejected_words.grid(row=2, column=0)
        fr.grid(row=0, column=0)


        # reset the game state #
        # make a new clock thread
        self.clockthread = threading.Thread(target=self.clock_tick)
        # reset time
        self.secs = TIME_LIMIT_S
        self.clockvar.set(str(TIME_LIMIT_S) + " s")

    def clock_tick(self):
        while self.secs > 0:
            time.sleep(1)
            self.secs -= 1
            self.clockvar.set(str(self.secs) + " s")
        self.game_over()

    def random_words(self, l, n=1) -> str:
        words = ""
        for i in range(n):
            if n == 1 or i == 0:
                words = (l[random.randint(0, len(l)-1)])
            else:
                words = (l[random.randint(0, len(l)-1)]) + ", " + words
        return words

if __name__ == "__main__":
    app = PiWords()

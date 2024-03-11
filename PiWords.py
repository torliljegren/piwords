
import tkinter as tk
import tkinter.ttk as ttk
import threading
import time

class PiWords:

    def __init__(self):
        self.pi_words = tuple()
        self.secs = 30
        self.clockthread = threading.Thread(target=self.clock_tick)
        self.entered_words = list()
        self.correct_words = list()
        self.rejected_words = list()

        self.root = tk.Tk("PiWords")
        self.frame = ttk.Frame(master=self.root)
        self.lbl1 = ttk.Label(master=self.frame, text="Skriv så många ord du kan på 30 s")
        self.lbl2 = ttk.Label(master=self.frame, text="Tryck Enter efter varje ord")
        self.clockvar = tk.StringVar(master=self.frame, value="30 s")
        self.clocklbl = ttk.Label(master=self.frame, textvariable=self.clockvar)
        self.txtvar = tk.StringVar(master=self.frame)
        self.txtfield = ttk.Entry(textvariable=self.txtvar)

        self.frame.grid(pady=(10,0))
        self.lbl1.grid(row=0, column=0)
        self.lbl2.grid(row=1, column=0)
        self.txtfield.grid(row=2, column=0, pady=(20,20))
        self.clocklbl.grid(row=3, column=0, pady=20)

        self.root.mainloop()

    def read_pi_words(self):
        txtfile = open("svenska-ord.txt", "+r")
        templist = list()
        for line in txtfile:
            if "pi" in line:
                templist.append(line.strip(__chars="-"))
        self.pi_words = tuple(templist)

    def word_entered(self, e=None):
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

    def start_game(self):
        self.clockthread.start()

    def game_over(self):
        # show a window with stats
        win = tk.Toplevel(master=self.root)
        fr = ttk.Frame(master=win)
        lbl1 = ttk.Label(master=fr, text="Du klarade " + str(len(self.correct_words)) + " ord.")
        lbl2 = ttk.Label("Godkända:\n" + )
        fr.pack()
        lbl1.pack()

        # reset the game state #
        # make a new clock thread
        self.clockthread = threading.Thread(target=self.clock_tick)
        # reset time
        self.secs = 30

    def clock_tick(self):
        while self.secs > 0:
            time.sleep(1)
            self.secs -= 1
            self.clockvar.set(str(self.secs) + " s")
        self.game_over()

if __name__ == "__main__":
    app = PiWords()
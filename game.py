import time
import threading
import tkinter as tk
from tkinter import ttk
import requests

class Game:
    def __init__(self):
        self.root = tk.Tk()
        self.running = False
        self.key_pressed = None
        self.after_loop = None

        # Get text to copy
        self.res = requests.get(
            'https://random-word-api.herokuapp.com/word?number=5')
        self.text_to_copy = tk.StringVar()
        self.text_to_copy.set(' '.join(self.res.json()))

        # Frame to better organize the smaller widgets
        self.text_frame = ttk.Frame(self.root)
        self.sm_frame = ttk.Frame(self.root)
        self.text_frame.grid(column=0, row=0)
        self.sm_frame.grid(column=0, row=1)

        # Timer var and counter for stat calculations
        self.calc_thread = None
        self.timer = -1
        self.counter = 0

        # Minutes and seconds for timer
        self.minutes = tk.StringVar()
        self.seconds = tk.StringVar()
        self.minutes.set("00")
        self.seconds.set("00")

        # Label to display stats
        self.speed_label = tk.Label(
            self.sm_frame, text="Speed \n 0.0 CPS\n 0.0 CPM", font=("Arial", 12))

        # Instructions
        self.instructions_text = "Please enter the amount of time you wish to test for. To start press tab inside the typing area. To retrieve new words press enter."
        self.instructions = tk.Label(
            self.text_frame, text=self.instructions_text, font=("Arial", 11))

        # Labels and entries to set timer
        self.minutes_label = tk.Label(
            self.sm_frame, text="Minutes", font=("Arial", 12))
        self.seconds_label = tk.Label(
            self.sm_frame, text="Seconds", font=("Arial", 12))
        self.minutes_entry = tk.Entry(self.sm_frame, width=3, font=(
            "Arial", 13), textvariable=self.minutes)
        self.seconds_entry = tk.Entry(self.sm_frame, width=3, font=(
            "Arial", 13), textvariable=self.seconds)

        # Retreived paragraph to copy
        self.text = tk.Label(
            self.text_frame, textvariable=self.text_to_copy, font=("Arial", 16))
        self.text.grid(row=0, column=0, columnspan=2)

        # area to type in
        self.type_area = tk.Entry(self.text_frame, width=40, font=("Arial", 16))
        self.type_area.focus()
        self.type_area.bind("<Tab>", self.start)
        self.type_area.bind("<Return>", self.get_new_words)

        self.quit_btn = ttk.Button(self.sm_frame, text="Quit", command=self.root.destroy)

        self.pause_btn = ttk.Button(self.sm_frame,
                                    text="Pause",
                                    command=self.pause)

        # Layout
        self.text.grid(column=0, row=0, ipadx=20, ipady=20)
        self.type_area.grid(column=0, row=1)
        self.speed_label.grid(column=0, row=2)
        self.instructions.grid(column=0, row=3)
        self.minutes_entry.grid(column=0, row=4, padx=1, pady=1)
        self.minutes_label.grid(column=1, row=4)
        self.seconds_entry.grid(column=2, row=4, padx=1, pady=1)
        self.seconds_label.grid(column=3, row=4)
        self.quit_btn.grid(column=0, row=5)
        self.pause_btn.grid(column=1, row=5)

        self.root.mainloop()

    def count(self, timer):
        """ Counts the timer down starting from where the user sets the time at """
        if self.running:
            if timer > -1:
                mins, secs = divmod(timer, 60)
                self.minutes.set(f"{mins}")
                self.seconds.set(f"{secs}")
                self.timer = timer

            self.after_loop = self.root.after(1000, self.count, timer-1)

        else:
            self.root.after_cancel(self.after_loop)

    def start(self, event):
        """ Starts the game once the user presses the Tab key """
        if not self.running:
            self.running = True

            # Start the timer
            self.counter = int(self.minutes.get())*60 + int(self.seconds.get())
            self.count(self.counter)

            # Start the stat calculation thread
            self.calc_thread = threading.Thread(target=self.calc_stats)
            self.calc_thread.start()

            if self.text_to_copy.get() == self.type_area.get():
                self.type_area.config(fg="green")
            elif (self.key_pressed == 'Return') and not (self.text_to_copy.get() == self.type_area.get()):
                self.type_area.config(fg="red")

    def pause(self, event):
        """ Pauses the game """
        if self.running:
            self.root.after_cancel(self.after_loop)
            self.running = False

        self.key_pressed = event.char

    def calc_stats(self):
        """ Calculate character per minute/second """
        while self.running:
            time.sleep(0.1)
            self.counter += 0.1
            cps = len(self.type_area.get()) / self.counter
            cpm = cps * 60
            self.speed_label.config(text=f"Speed: \n{cps:.2f} CPS\n{cpm:.2f} CPM")

    def get_new_words(self, event):
        """ Retrieve new words when the user presses the correct key """
        self.res = requests.get(
            'https://random-word-api.herokuapp.com/word?number=5')
        self.text_to_copy.set(' '.join(self.res.json()))
        self.key_pressed = event.keysym
        print(self.key_pressed)


Game()

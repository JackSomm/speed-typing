import requests
from datetime import timedelta
from tkinter import ttk 
from tkinter import *

class Game:
  def __init__(self):
    self.root = Tk()
    self.running = False
    self.game_over = False

    self.res = requests.get('https://random-word-api.herokuapp.com/word?number=10')
    self.text_to_copy = StringVar()
    self.text_to_copy.set(' '.join(self.res.json()))


    self.counter = -1

    self.minutes = StringVar() 
    self.seconds = StringVar()
    self.minutes.set("00")
    self.seconds.set("00")

    self.instructions_text = "Please enter the amount of time you wish to test for. To start press tab inside the typing area. To retrieve new words press enter."
    self.instructions = Label(self.root, text=self.instructions_text, font=("Arial", 11))

    self.minutes_label = Label(self.root, text="Minutes", font=("Arial", 18))
    self.seconds_label = Label(self.root, text="Seconds", font=("Arial", 18))
    self.minutes_entry = Entry(self.root, width=3, font=("Arial", 18), textvariable=self.minutes)
    self.seconds_entry = Entry(self.root, width=3, font=("Arial", 18), textvariable=self.seconds)

    # Retreived paragraph to copy
    self.text = Label(self.root, height=4, width=30, textvariable=self.text_to_copy)

    # area to type in
    self.type_area = Text(self.root, width=30, height=4, wrap=WORD)
    self.type_area.focus()
    self.type_area.bind("<Tab>", self.start)
    self.type_area.bind("<Return>", self.get_new_words)

    self.quit_btn = ttk.Button(self.root, text="Quit", command=self.root.destroy)

    self.pause_btn = ttk.Button(self.root, text="Pause", command=self.pause)

    # Layout
    self.text.grid(column=0, row=0, padx=10, pady=10, ipadx=20, ipady=20)
    self.type_area.grid(column=0, row=1, pady=10, padx=10)
    self.instructions.grid(column=0, row=2)
    self.minutes_entry.grid(column=0, row=3, padx=10, pady=10)
    self.minutes_label.grid(column=1, row=3, padx=10, pady=10)
    self.seconds_entry.grid(column=2, row=3, padx=10, pady=10)
    self.seconds_label.grid(column=3, row=3, padx=10, pady=10)
    self.quit_btn.grid(column=0, row=4, pady=10, padx=10)
    self.pause_btn.grid(column=2, row=4, padx=10, pady=10)

    self.root.mainloop()

  def count(self, counter):
    if self.running:
      if counter > -1:
        mins, secs = divmod(counter, 60)
        self.minutes.set("{:02d}".format(mins))
        self.seconds.set("{:02d}".format(secs))
        self.counter = counter

      self.after_loop = self.root.after(1000, self.count, counter-1)

    else:
      self.root.after_cancel(self.after_loop)

  def start(self, event):
    if not self.running:
      self.running = True
      self.counter = int(self.minutes.get())*60 + int(self.seconds.get())
      self.count(self.counter)

  def pause(self):
    if self.running:
      self.root.after_cancel(self.after_loop)
      self.running = False

  def get_new_words(self, event):
    if self.running:
      self.res = requests.get('https://random-word-api.herokuapp.com/word?number=10')
      self.text_to_copy.set(' '.join(self.res.json()))

Game()
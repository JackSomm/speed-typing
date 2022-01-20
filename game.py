import requests
import time
import threading
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

    self.sm_frame = ttk.Frame(self.root)
    self.sm_frame.grid(column=1, row=4)

    self.timer = -1
    self.counter = 0

    self.minutes = StringVar() 
    self.seconds = StringVar()
    self.minutes.set("00")
    self.seconds.set("00")

    self.speed_label = Label(self.sm_frame, text="Speed \n 0.0 CPS\n 0.0 CPM", font=("Arial", 12))

    self.instructions_text = "Please enter the amount of time you wish to test for. To start press tab inside the typing area. To retrieve new words press enter."
    self.instructions = Label(self.root, text=self.instructions_text, font=("Arial", 11))

    self.minutes_label = Label(self.sm_frame, text="Minutes", font=("Arial", 12))
    self.seconds_label = Label(self.sm_frame, text="Seconds", font=("Arial", 12))
    self.minutes_entry = Entry(self.sm_frame, width=3, font=("Arial", 13), textvariable=self.minutes)
    self.seconds_entry = Entry(self.sm_frame, width=3, font=("Arial", 13), textvariable=self.seconds)

    # Retreived paragraph to copy
    self.text = Label(self.root, textvariable=self.text_to_copy, font=("Arial", 16))
    self.text.grid(row=0, column=0, columnspan=2)

    # area to type in
    self.type_area = Entry(self.root, width=40, font=("Arial", 16))
    self.type_area.focus()
    self.type_area.bind("<Tab>", self.start)
    self.type_area.bind("<Return>", self.get_new_words)

    self.quit_btn = ttk.Button(self.sm_frame,
                              text="Quit",
                              command=self.root.destroy)

    self.pause_btn = ttk.Button(self.sm_frame,
                                text="Pause",
                                command=self.pause)

    # Layout
    self.text.grid(column=1, row=0, ipadx=20, ipady=20)
    self.type_area.grid(column=1, row=1)
    self.speed_label.grid(column=1, row=2)
    self.instructions.grid(column=1, row=3)
    self.minutes_entry.grid(column=1, row=4, padx=1, pady=1)
    self.minutes_label.grid(column=2, row=4)
    self.seconds_entry.grid(column=3, row=4, padx=1, pady=1)
    self.seconds_label.grid(column=4, row=4)
    self.quit_btn.grid(column=1, row=5)
    self.pause_btn.grid(column=2, row=5)

    self.root.mainloop()

  def count(self, timer):
    if self.running:
      if timer > -1:
        mins, secs = divmod(timer, 60)
        self.minutes.set("{:02d}".format(mins))
        self.seconds.set("{:02d}".format(secs))
        self.timer = timer

      self.after_loop = self.root.after(1000, self.count, timer-1)

    else:
      self.root.after_cancel(self.after_loop)

  def start(self, event):
    if not self.running:
      self.running = True

      # Start the timer
      self.counter = int(self.minutes.get())*60 + int(self.seconds.get())
      self.count(self.counter)
      
      # Start the stat calculation thread
      t = threading.Thread(target=self.calc_stats)
      t.start()

  def pause(self):
    if self.running:
      self.root.after_cancel(self.after_loop)
      self.running = False

  def calc_stats(self):
    while self.running:
      time.sleep(0.1)
      self.counter += 0.1
      cps = len(self.type_area.get()) / self.counter
      cpm = cps * 60
      self.speed_label.config(text=f"Speed: \n{cps:.2f} CPS\n{cpm:.2f} CPM")

  def get_new_words(self, event):
    if self.running:
      self.res = requests.get('https://random-word-api.herokuapp.com/word?number=10')
      self.text_to_copy.set(' '.join(self.res.json()))

Game()
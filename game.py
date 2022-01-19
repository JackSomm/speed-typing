import requests
from datetime import timedelta
from tkinter import ttk 
from tkinter import *

class Game:
  def __init__(self):
    self.root = Tk()
    self.running = False
    self.game_over = False
    self.text_to_copy = ''
    self.counter = -1
    self.minutes = StringVar() 
    self.seconds = StringVar()
    self.minutes.set("00")
    self.seconds.set("00")

    self.instructions_text = "Please enter the amount of time you wish to test for. The timer will start on first key press."
    self.instructions = Label(self.root, text=self.instructions_text, font=("Arial", 12))

    self.minutes_label = Label(self.root, text="Minutes", font=("Arial", 18))
    self.seconds_label = Label(self.root, text="Seconds", font=("Arial", 18))
    self.minutes_entry = Entry(self.root, width=3, font=("Arial", 18), textvariable=self.minutes)
    self.seconds_entry = Entry(self.root, width=3, font=("Arial", 18), textvariable=self.seconds)

    # Retreived paragraph to copy
    self.text = Text(self.root, height=10, width=95)
    self.text.insert(INSERT, self.text_to_copy)
    self.text.config(state=DISABLED)

    # area to type in
    self.type_area = Text(self.root, width=93, height=10)
    self.type_area.focus()
    self.type_area.bind("<Key>", self.start)

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
      self.counter = int(self.minutes.get())*60 + int(self.seconds.get())
      self.running = True
      self.count(self.counter)

  def pause(self):
    if self.running:
      self.root.after_cancel(self.after_loop)
      self.running = False
    


Game()
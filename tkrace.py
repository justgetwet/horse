import tkinter as tk
from tkinter import ttk
from race import Race
from tkraces import TkRaces

class TkRace:
  
  def __init__(self):
    self.root = tk.Tk()
    self.root.title("race")
    w = 450
    h = 350
    self.root.geometry(f"{w}x{h}+100+50")
    self.frame = tk.Frame(self.root)

    self.races = Race().races()

  def set_button(self, code, held, mainrace):
    f_button = tk.Frame(self.frame)
    f_button.pack(fill=tk.X)
    b_race = ttk.Button(f_button, text=held, command=lambda: self.oneday(held, code))
    b_race.pack(side=tk.LEFT, anchor=tk.W, pady=5)
    l_race = tk.Label(f_button, text=mainrace)
    l_race.pack(side=tk.LEFT, anchor=tk.W, pady=5)

  def oneday(self, held, code):
    tkr = TkRaces(held, code)
    tkr.run()

  def run(self):
    for r in self.races:
      self.set_button(r[1], r[2], r[3])
    self.frame.pack(pady=5)
    self.root.mainloop()

if __name__ == '__main__':


  t = TkRace()
  t.run()
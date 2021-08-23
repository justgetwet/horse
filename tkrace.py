import tkinter as tk
from tkinter import ttk
from race import Race

class TkRace:
  
  def __init__(self):
    self.root = tk.Tk()
    self.root.title("race")
    w = 450
    h = 350
    self.root.geometry(f"{w}x{h}+100+50")
    self.frame = tk.Frame(self.root)

  def set_button(self, held, mainrace):
    f_button = tk.Frame(self.frame)
    f_button.pack(fill=tk.X)
    b_race = ttk.Button(f_button, text=held, command=lambda: self.spam())
    b_race.pack(side=tk.LEFT, anchor=tk.W, pady=5)
    l_race = tk.Label(f_button, text=mainrace)
    l_race.pack(side=tk.LEFT, anchor=tk.W, pady=5)

  def spam(self):
    print("ham eggs")

  def run(self):
    self.frame.pack(pady=5)
    self.root.mainloop()

if __name__ == '__main__':

  r = Race()
  races = r.races()
  t = TkRace()
  for r in races:
    t.set_button(r[2], r[3])
  t.run()
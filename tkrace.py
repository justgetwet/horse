import tkinter as tk
from tkinter import ttk

class TkRace:
  
  def __init__(self):
    self.root = tk.Tk()
    self.root.title("tk title")
    w = 300
    h = 300
    self.root.geometry(f"{w}x{h}+100+50")
    self.frame = tk.Frame(self.root)

  def set_smapfram(self):
    f_spam = tk.Frame(self.frame)
    f_spam.pack(fill=tk.X)
    b_ham = ttk.Button(f_spam, text='spam', command=lambda: self.spam())
    b_ham.pack(side=tk.TOP, expand=True, pady=5)

  def spam(self):
    print("ham eggs")

  def run(self):
    self.frame.pack()
    self.root.mainloop()

if __name__ == '__main__':

  t = TkRace()
  t.set_smapfram()
  t.run()
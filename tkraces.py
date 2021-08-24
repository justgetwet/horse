import tkinter as tk
from tkinter import ttk
import pandas as pd
import unicodedata
import datetime
from races import Races
# import seaborn as sns
from race import Race

class TkRaces:
  
  def __init__(self, tk_title: str, code: list):
    # self.root = tk.Tk()
    self.root = tk.Toplevel()
    self.root.title("Race " + tk_title)
    rs = Races(code)
    races = rs.oneday() 
    self.titles = [d[0] for d in races]
    self.dfs = [d[1] for d in races]
    sizes = self.column_sizes(self.dfs[0])
    w = sum(map(lambda x: x+8, sizes)) + 50
    self.root.geometry(f"{w}x900+200+50")
    
    # date_str = tk_title.split()[0][:-3]
    # self.place = tk_title.split()[1]
    # date_dt = datetime.datetime.strptime(date_str, "%Y年%m月%d日")
    # self.yyyymmdd = date_dt.strftime("%Y%m%d")


  def set_scrollbar(self):
    scroll_range = 1212*4
    self.canvas = tk.Canvas(self.root)
    bar = tk.Scrollbar(self.canvas, orient=tk.VERTICAL)
    bar.pack(side=tk.RIGHT, fill=tk.Y)
    bar.config(command=self.canvas.yview)
    self.canvas.config(yscrollcommand=bar.set)
    # canvasのスクロール範囲
    self.canvas.config(scrollregion=(0, 0, 0, scroll_range))
    self.canvas.pack(fill=tk.BOTH, expand=True) # tk.BOTH：縦横両方向に対して引き伸ばす

  def set_frame_on_canvas(self):
    # canvasにframeを乗せる
    self.canvas.create_window((0,0), window=self.frame, anchor=tk.NW)

  def races(self):
    
    self.frame = tk.Frame(self.canvas)
    seq_rows = list(range(0, len(self.dfs)*2, 2)) # [0, 2, 4, ...]
    for df, title, row in zip(self.dfs, self.titles, seq_rows):
      self.race(self.frame, df, title, row)
    
    self.frame.pack()

  def race(self, frame, df: pd.DataFrame, title, row):
    # label and button
    l_title = tk.Label(frame, text=title, anchor="w")
    l_title.grid(row=row, column=0, sticky=tk.W, pady=10, padx=10)
    # b_quit = ttk.Button(frame, text='Quit', command=lambda: self.root.quit())
    r = int(title.split("R")[0])
    b_quit = ttk.Button(frame, text='more', command=lambda: self.show_detail(r))
    b_quit.grid(row=row, column=1, sticky=tk.E, pady=10, padx=10)

    # treeview
    tree = ttk.Treeview(frame, height=len(df)+1)
    headingcolor = "lightgrey"
    alternatecolor = "whitesmoke"
    # bug fix
    def fixed_map(option):
      # Fix for setting text colour for Tkinter 8.6.9
      # From: https://core.tcl.tk/tk/info/509cafafae
      return [elm for elm in style.map('Treeview', query_opt=option) if elm[:2] != ('!disabled', '!selected')]	
    
    style = ttk.Style()
    style.theme_use("default")
    style.configure("Treeview.Heading", background=headingcolor)
    style.map('Treeview', foreground=fixed_map('foreground'), background=fixed_map('background'))
    # table
    tree["show"] = "headings"
    cols = tuple(range(1, len(df.columns)+1))
    tree['columns'] = cols

    sizes = self.column_sizes(df)
    for i, col, size in zip(cols, df.columns, sizes):
      tree.heading(i, text=f"{col}")
      tree.column(i, width=size+8)
    
    lst = [tuple(t)[1:] for t in df.itertuples()]
    for i, tpl in enumerate(lst):
      tree.insert("", "end", tags=i, values=tpl)
      if i & 1:
        tree.tag_configure(i, background=alternatecolor)
    
    tree.grid(row=row+1, column=0, columnspan=2, pady=10, padx=10)

  def column_sizes(self, df: pd.DataFrame) -> list:

    def east_asian_width_count(text):
      count = 0
      for c in text:
        if unicodedata.east_asian_width(c) in 'FWA':
          count += 2
        else:
          count += 1
      return count * 8
    
    lst_columns = [[col] + list(df[col]) for col in df.columns]
    sizes = []
    for cols in lst_columns:
      max_size = max([east_asian_width_count(str(col)) for col in cols])
      sizes.append(max_size)

    return sizes

  def show_detail(self, r: int):
    pass
    # tp = (self.yyyymmdd, self.place, r)
    # race = OneRace(*tp)
    # title = race.racetitle
    # raps_df = race.entry_raps()
    # latests_df = race.entry_latests()
    # dfs = [raps_df, latests_df]
    # t = TkRace(title, dfs, tp)
    # t.run()

  def run(self):
    self.set_scrollbar()
    self.races()
    self.set_frame_on_canvas()
    self.root.mainloop()


if __name__ == '__main__':

  r = Race()
  tp = r.races()
  code = tp[0][1]

  t = TkRaces("title", code)
  t.run()
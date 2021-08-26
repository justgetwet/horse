import urllib.request
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import re
# import json
# import pathlib
import datetime
from race import Soup, Race

class Analyse(Soup):

  def __init__(self, code):
    url = "https://race.netkeiba.com/race/shutuba.html?race_id=" + code
    self.soup = self.get_soup(url)

  def race(self):
    r = self.soup.select_one("div.RaceList_Item01 span.RaceNum").text
    title = self.soup.select_one("div.RaceName").text.split()[0]
    course = self.soup.select("div.RaceData01 span")[0].text.strip(" ")
    grd, dst = course[0], int(course[1:].strip("m"))

    return r, title, course

  def race_data(self):
    r, title, course = self.race()
    grd, dst = course[0], int(course[1:].strip("m"))
    idx = ["R", "title", "gnd", "dst"]
    sr = pd.Series([r, title, grd, dst], index=idx)

    return sr

  def horse_data(self):
    dfs = self.get_dfs(self.soup)
    df = dfs[0].droplevel(0, axis=1)
    srs = []
    for idx, sr in df.iterrows():
      srs.append(sr.drop(index=["印", "人気", "登録", "メモ"])[:-1])

    return srs

  def past_data(self):
    ubans = [tag for tag in self.soup.select("td[class^=Umaban]")]
    names = [tag for tag in self.soup.select("span.HorseName a")]
    links = [(u.text, n.text, n.get("href")) for u, n in zip(ubans, names)]
    index = ["no", "name", "idx", "date", "held", "R", "title", "odr", "wei", "gnd", "dst", "sec"]
    srs = []
    for no, name, link in links:
      soup = self.get_soup(link)
      dfs = self.get_dfs(soup)
      df = pd.DataFrame()
      if len(dfs) > 3:
        df = dfs[3]
      if len(df.columns) == 28:
        _srs = []
        for idx, row in df.iterrows():
          date = row["日付"]
          hld = row["開催"]
          r = row["R"]
          race = row["レース名"]
          odr = row["着  順"]
          wei = row["斤  量"]
          gnd, dst = row["距離"][0], int(row["距離"][1:])
          cnd = row["馬  場"]
          time_str = row["タイム"]
          sec = np.nan
          if time_str is not np.nan and type(time_str) != float:
            dt = datetime.datetime.strptime(time_str, "%M:%S.%f")
            td = datetime.timedelta(minutes=dt.minute, seconds=dt.second, microseconds=dt.microsecond)
            sec = td.total_seconds()
          rec = [no, name, idx, date, hld, r, race, odr, wei, gnd, dst, sec]
          sr = pd.Series(rec, index=index)
          _srs.append(sr)
        srs.extend(_srs)

    return srs

  def summary(self):
    race = self.race()
    sr = pd.Series(dtype=np.float64)
    if not race[1] in ["2歳新馬", "2歳未勝利", "3歳未勝利"]:
      r_sr = self.race_data()
      data = self.past_data()
      lst = []
      for sr in data:
        if r_sr["gnd"] == sr["gnd"] and r_sr["dst"] == sr["dst"] and sr["sec"] is not np.nan:
          lst.append((sr["no"], sr["name"], sr["sec"]))
      
      rate = round((len(lst) / len(data)) * 100, 1)
      r, title, summary_s = race[0], ' '.join(race[1:]), f"{len(lst)} / {len(data)} : {rate} %"
      # print(r, title, summary_s)
      sr = pd.Series([r, title, summary_s], index=["R", "Title", "data"])
    
    return sr


if __name__ == '__main__':

  # c = "2021040403"
  # ana = Analyse(code)
  # ana.summary()

  races = Race().hold()
  for race in races:
    print(race[2])
    srs = []
    for r in range(1, 12):
      code = race[1] + str(r).rjust(2, "0")
      ana = Analyse(code)
      sr = ana.summary()
      if not sr.empty:
        srs.append(sr)
    df = pd.DataFrame(srs)
    print(df)


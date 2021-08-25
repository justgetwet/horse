import urllib.request
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import re
# import json
# import pathlib
import datetime
from race import Soup

class Analyse(Soup):

  def __init__(self, code):
    url = "https://race.netkeiba.com/race/shutuba.html?race_id=" + code
    self.soup = self.get_soup(url)

  def race_data(self):
    r = self.soup.select_one("div.RaceList_Item01 span.RaceNum").text
    title = self.soup.select_one("div.RaceName").text.split()[0]
    course = self.soup.select("div.RaceData01 span")[0].text.strip(" ")
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
      if len(dfs) > 3:
        df = dfs[3]
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
          if time_str is not np.nan:
            dt = datetime.datetime.strptime(time_str, "%M:%S.%f")
            td = datetime.timedelta(minutes=dt.minute, seconds=dt.second, microseconds=dt.microsecond)
            sec = td.total_seconds()
          rec = [no, name, idx, date, hld, r, race, odr, wei, gnd, dst, sec]
          sr = pd.Series(rec, index=index)
          _srs.append(sr)
        srs.extend(_srs)

    return srs

  def summary(self):
    race = self.race_data()



if __name__ == '__main__':

  code = "202101020310"
  a = Analyse(code)
  race = a.race_data()
  print(list(race))
  data = a.past_data()
  lst = []
  for sr in data:
    if race["gnd"] == sr["gnd"] and race["dst"] == sr["dst"] and sr["sec"] is not np.nan:
      lst.append((sr["no"], sr["name"], sr["sec"]))
  # print(lst)
  rate = round((len(lst) / len(data)) * 100, 1)
  print(f"{len(lst)} / {len(data)} : {rate} %")
  horses = a.horse_data()
  print(horses)

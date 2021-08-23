import urllib.request
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import re
# import json
# import pathlib
import datetime

class Soup:

  def get_soup(self, url: str):
    try: 
      html = urllib.request.urlopen(url)
    except urllib.error.URLError as e:
      print("URLError", e.reason)
      html = "<html></html>"

    soup = BeautifulSoup(html, "lxml")

    return soup

  def get_dfs(self, soup):
    dfs = [pd.DataFrame()]
    if soup.find("table") == None:
      print("get_dfs: a table is not found.")
    else:
      dfs = pd.io.html.read_html(soup.prettify())

    return dfs

  def is_num(self, str_num: str) -> bool:
    try:
      float(str_num)
    except ValueError:
      return False
    else:
      return True

class Urls:

	cc = {}
	cc['札幌'] = '01'
	cc['函館'] = '02'
	cc['福島'] = '03'
	cc['新潟'] = '04'
	cc['東京'] = '05'
	cc['中山'] = '06'
	cc['中京'] = '07'
	cc['京都'] = '08'
	cc['阪神'] = '09'
	cc['小倉'] = '10'

	url_netkeiba = "https://race.netkeiba.com"
	url_shutuba = "/race/shutuba.html?race_id="

	url_yahookeiba = "https://keiba.yahoo.co.jp/"

	race_list = "/top/race_list.html"
	top_nave = "/top/?rf=navi"


class Race(Soup, Urls):
	
	def races(self):
		soup = self.get_soup(self.url_yahookeiba)
		dfs = self.get_dfs(soup)
		df = dfs[5]
		res = []
		for idx, sr in df.iterrows():
			dts = sr[0].split()
			date_str = "2021年" + dts[0]
			date_dt = datetime.datetime.strptime(date_str, "%Y年%m月%d日")
			place = re.sub("回", " ", sr[1]).split()[1][:2]
			k, d = re.sub(place, " ", sr[1]).split()
			code = str(date_dt.year) 
			code += self.cc[place] + k.strip("回").rjust(2, "0") + d.strip("日").rjust(2, "0")
			held = date_dt.strftime("%Y年%m月%d日") + "(" + dts[1][0] + ") " + place
			mainrace = sr[2]
			res.append((idx, code, held, mainrace)) # (0, '010203', '2021年08月21日 札幌', '札幌日刊スポーツ杯')

		return res

if __name__ == '__main__':

	r = Race()
	print(r.races())

	
	# url_r = "https://race.netkeiba.com/race/result.html?race_id=202104040401&rf=race_list"
	# url_s = "https://race.netkeiba.com/race/shutuba.html?race_id=202104040401&rf=race_submenu"
	# soup = s.get_soup(url_s)
	# dfs = s.get_dfs(soup)
	# print(dfs[0])

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
	
	url_yahookeiba = "https://keiba.yahoo.co.jp/"

	race_list = "/top/race_list.html"
	top_nave = "/top/?rf=navi"


class Race(Soup, Urls):
	pass

if __name__ == '__main__':

	s, u = Soup(), Urls()
	
	url = u.url_netkeiba + u.top_nave
	soup = s.get_soup(u.url_yahookeiba)
	dfs = s.get_dfs(soup)
	df = dfs[5]
	for i, sr in df.iterrows():
		date_str = "2021年" + sr[0].split()[0]
		date_dt = datetime.datetime.strptime(date_str, "%Y年%m月%d日")
		place = re.sub("回", " ", sr[1]).split()[1][:2]
		times, dt = re.sub(place, " ", sr[1]).split()
		code = times.strip("回").rjust(2, "0") + dt.strip("日").rjust(2, "0")
		print(i, date_dt.strftime("%Y年%m月%d日"), place, u.cc[place], code)
		print(sr[2])
	
	# url_r = "https://race.netkeiba.com/race/result.html?race_id=202104040401&rf=race_list"
	# url_s = "https://race.netkeiba.com/race/shutuba.html?race_id=202104040401&rf=race_submenu"
	# soup = s.get_soup(url_s)
	# dfs = s.get_dfs(soup)
	# print(dfs[0])

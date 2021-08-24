import urllib.request
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import re
# import json
# import pathlib
import datetime
from race import Soup

def main(code):
	s = Soup()
	url = "https://race.netkeiba.com/race/shutuba.html?race_id=" + code
	soup = s.get_soup(url)

	ubans = [tag for tag in soup.select("td[class^=Umaban]")]
	names = [tag for tag in soup.select("span.HorseName a")]
	links = [(u.text, n.text, n.get("href")) for u, n in zip(ubans, names)]

	data = []
	for no, name, link in links:
		soup = s.get_soup(link)
		dfs = s.get_dfs(soup)
		if len(dfs) > 3:
			df = dfs[3]
			lst = []
			for idx, row in df.iterrows():
				date = row["日付"]
				hld = row["開催"]
				r = row["R"]
				race = row["レース名"]
				wei = row["斤  量"]
				grd, dst = row["距離"][0], int(row["距離"][1:])
				cnd = row["馬  場"]
				time_str = row["タイム"]
				dt = datetime.datetime.strptime(time_str, "%M:%S.%f")
				td = datetime.timedelta(minutes=dt.minute, seconds=dt.second, microseconds=dt.microsecond)
				sec = td.total_seconds()
				lst.append((no, name, idx, date, hld, r, race, wei, grd, dst, sec))
			data.extend(lst)

	return data

if __name__ == '__main__':

	code = "202101020311"
	data = main(code)
	for row in data:
		print(row)
import pandas as pd
import re
# import json
# import pathlib
import pandas as pd
import datetime
from race import Race

class Races(Race):

	def __init__(self, code: str):
		self.url_race = self.url_netkeiba + self.url_shutuba + code

	def oneday(self):
		# races = self.races()
		# code = races[0][1]
		races = []
		for r in range(1,13):
			url = self.url_race + str(r).rjust(2,"0")
			soup = self.get_soup(url)
			r = soup.select_one("div.RaceList_Item01 span.RaceNum").text
			title = soup.select_one("div.RaceName").text.split()[0]
			course = soup.select("div.RaceData01 span")[0].text
			ls = [r, title, course]
			ls += [tag.text for tag in soup.select("div.RaceData02 span")[3:8]]
			title = " ".join(ls)
			# print(label)
			dfs = self.get_dfs(soup)
			df = dfs[0].droplevel(0, axis=1)
			srs = []
			for idx, sr in df.iterrows():
				srs.append(sr.drop(index=["印", "人気", "登録", "メモ"])[:-1])
			race_df = pd.DataFrame(srs)
			# print(race_df)
			races.append((title, race_df))

		return races

if __name__ == '__main__':

	r = Race()
	tpls = r.races()
	code = tpls[0][1]
	rs = Races(code)
	races = rs.oneday()
	print(races)

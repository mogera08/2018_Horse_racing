# -*- coding: utf-8 -*-
from selenium.webdriver import Firefox, FirefoxOptions
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support import expected_conditions
#from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import time

url = "https://db.netkeiba.com/?pid=race_search_detail"
base = "https://db.netkeiba.com"
all_data = []
num = 1

# Firefoxをヘッドレスモードを有効にする
options = FirefoxOptions()
#options.add_argument('-headless')

# Firefoxを起動する
browser = Firefox(options=options)

# URLを読み込む
browser.get(url)

time.sleep(3)

# 下にスクロール
browser.execute_script("window.scrollTo(0, 200);")

#期間を選択
#開始年
frm_year_start = browser.find_element_by_name('start_year')
frm_select_element = Select(frm_year_start)
frm_select_element.select_by_value('2018')

#開始月
frm_mon_start = browser.find_element_by_name('start_mon')
frm_select_element_mon = Select(frm_mon_start)
frm_select_element_mon.select_by_value('1')

#終了年
frm_year_end = browser.find_element_by_name('end_year')
frm_select_element_end_year = Select(frm_year_end)
frm_select_element_end_year.select_by_value('2018')

#終了月
frm_mon_end = browser.find_element_by_name('end_mon')
frm_select_element_end_year = Select(frm_mon_end)
frm_select_element_end_year.select_by_value('12')

#競馬場選択
jyo_1 = browser.find_element_by_id("check_Jyo_01")
jyo_1.click()
jyo_2 = browser.find_element_by_id("check_Jyo_02")
jyo_2.click()
jyo_3 = browser.find_element_by_id("check_Jyo_03")
jyo_3.click()
jyo_4 = browser.find_element_by_id("check_Jyo_04")
jyo_4.click()
jyo_5 = browser.find_element_by_id("check_Jyo_05")
jyo_5.click()
jyo_6 = browser.find_element_by_id("check_Jyo_06")
jyo_6.click()
jyo_7 = browser.find_element_by_id("check_Jyo_07")
jyo_7.click()
jyo_8 = browser.find_element_by_id("check_Jyo_08")
jyo_8.click()
jyo_9 = browser.find_element_by_id("check_Jyo_09")
jyo_9.click()
jyo_10 = browser.find_element_by_id("check_Jyo_10")
jyo_10.click()

# 検索結果表示を100件にする
kensaku_num = browser.find_element_by_name('list')
kensaku_select_num = Select(kensaku_num)
kensaku_select_num.select_by_value('100')

# 検索結果ボタンクリック
search_btn = browser.find_element_by_css_selector('input[value=検索]')
search_btn.submit()

time.sleep(3)

while num <= 36:
	if num == 1:
		a = browser.find_elements_by_css_selector(".txt_l a")
		for i in a:
			race = i.get_attribute('href')
			if "https://db.netkeiba.com/race/" in race:
				html = urlopen(race)
				bsObj = BeautifulSoup(html,"lxml")
				table = bsObj.findAll("table",{"class":"race_table_01 nk_tb_common"})[0]
				rows = table.findAll("tr")
				del rows[0]
				for a in rows:
					kyaku = a.findAll("td")[0].text
					w_jyun = a.findAll("td")[1].text
					u_jyun = a.findAll("td")[2].text
					toshi = a.findAll("td")[4].text
					tansyo = a.findAll("td")[12].text
					ninki = a.findAll("td")[13].text
					taijyu = a.findAll("td")[14].text
					all_data.append((kyaku, w_jyun, u_jyun, toshi, tansyo, ninki, taijyu))
		next_btn = browser.find_element_by_css_selector('.pager a')
		next_btn.click()
		time.sleep(3)
		browser.save_screenshot("next.png")
		num += 1

	elif num >= 2:
		a = browser.find_elements_by_css_selector(".txt_l a")
		for i in a:
			race = i.get_attribute('href')
			if "https://db.netkeiba.com/race/" in race:
				html = urlopen(race)
				bsObj = BeautifulSoup(html,"lxml")
				table = bsObj.findAll("table",{"class":"race_table_01 nk_tb_common"})[0]
				rows = table.findAll("tr")
				del rows[0]
				for a in rows:
					kyaku = a.findAll("td")[0].text
					w_jyun = a.findAll("td")[1].text
					u_jyun = a.findAll("td")[2].text
					toshi = a.findAll("td")[4].text
					tansyo = a.findAll("td")[12].text
					ninki = a.findAll("td")[13].text
					taijyu = a.findAll("td")[14].text
					all_data.append((kyaku, w_jyun, u_jyun, toshi, tansyo, ninki, taijyu))
		if num <= 35 :
			next_btn = browser.find_elements_by_css_selector('.pager a')[1]
			next_btn.click()
			time.sleep(3)
			browser.save_screenshot("next.png")
	num += 1


df = pd.DataFrame(all_data, columns = ['着順', '枠番', '馬番', '性齢', '単勝', '人気', '体重'])
df.index = df.index + 1
df.to_csv('keiba_2018.csv')
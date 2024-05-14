import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import time
from datetime import datetime,timedelta 

from selenium.webdriver.support.ui import Select

def set_search_period(driver, start_date, end_date):
    start_date_str = start_date.strftime("%Y-%m-%d")
    end_date_str = end_date.strftime("%Y-%m-%d")
    print(f"search period: \n\start: {start_date_str} \t end: {end_date_str}")

    # 시작 날짜 설정
    start_year_select = Select(driver.find_element(By.ID, "STA_Y"))
    start_year_select.select_by_value(str(start_date.year))

    start_month_select = Select(driver.find_element(By.ID,"STA_M"))
    start_month_select.select_by_value(str(start_date.month).zfill(2))

    start_day_select = Select(driver.find_element(By.ID,"STA_D"))
    start_day_select.select_by_value(str(start_date.day).zfill(2))

    # 종료 날짜 설정
    end_year_select = Select(driver.find_element(By.ID, "END_Y"))
    end_year_select.select_by_value(str(end_date.year))

    end_month_select = Select( driver.find_element(By.ID,"END_M"))
    end_month_select.select_by_value(str(end_date.month).zfill(2))

    end_day_select = Select(driver.find_element(By.ID,"END_D"))
    end_day_select.select_by_value(str(end_date.day).zfill(2))

    # 검색 버튼 클릭
    date_search_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "btn_type1"))
    )
    date_search_btn.click()
    csv_save_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "btn_Csv"))
    )
    driver.execute_script("arguments[0].click();", csv_save_btn)
    

    time.sleep(10)

def price_crawling(start_date, end_date):


    target_url = "https://www.opinet.co.kr/user/dopospdrg/dopOsPdrgSelect.do#" 

    with webdriver.Chrome(service=Service(ChromeDriverManager().install())) as driver:
        driver.get(target_url)
        driver.implicitly_wait(10)
        


        set_search_period(driver, start_date, end_date)
        time.sleep(10)   

end_date = datetime.today()
start_date = datetime.today() - timedelta(days=365)
price_crawling(start_date,end_date)
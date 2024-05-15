
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import time
from datetime import datetime,timedelta 

from selenium.webdriver.support.ui import Select

import boto3
from botocore.exceptions import NoCredentialsError


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
    current_directory = os.getcwd()

    # 다운로드 경로 설정: 현재 작업 디렉토리 + 'load' 폴더
    download_path = os.path.join(current_directory, 'load')

    # ChromeOptions 생성
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # 다운로드 경로 지정
    prefs = {"download.default_directory": download_path,}
    chrome_options.add_experimental_option("prefs", prefs)
    with webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=chrome_options) as driver:
        driver.get(target_url)
        driver.implicitly_wait(10)
        if os.path.exists("load\주유소_평균판매가격_제품별.csv"):
            os.remove("load\주유소_평균판매가격_제품별.csv")


        set_search_period(driver, start_date, end_date)
        time.sleep(10)


def upload_to_s3(file_path, object_name=None):
    """
    S3 버킷으로 파일 업로드
    - file_path: 업로드할 파일 경로
    - object_name: S3 버킷 내 파일 이름 (없을 경우 파일명 사용)
    - return: 성공 여부
    """
    # AWS 계정 정보 및 S3 버킷 정보 설정
    aws_access_key_id = ''
    aws_secret_access_key = ''
    bucket_name = ''

    # S3 클라이언트 생성
    s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

    # S3에 업로드할 파일명 설정
    if object_name is None:
        object_name = file_path

    try:
        s3.upload_file(file_path, bucket_name, object_name)
        print(f"파일 {file_path}을(를) S3 버킷 {bucket_name}에 업로드했습니다.")
        return True
    except FileNotFoundError:
        print(f"파일 {file_path}을(를) 찾을 수 없습니다.")
        return False
    except NoCredentialsError:
        print("AWS 인증 정보가 잘못되었습니다.")
        return False
    except Exception as e:
        print(f"파일 업로드 중 오류 발생: {e}")
        return False
    
def clean_broken_chars(text):
    # 깨진 문자열을 제거하는 함수
    cleaned_text = text.replace("?", "")
    return cleaned_text

end_date = datetime.today()
start_date = datetime.today() - timedelta(days=365)#오늘부터 며칠 전까지 조회할지
#price_crawling(start_date,end_date)

filename ="load\주유소_평균판매가격_제품별.csv"
output_filename = "oil_price.csv"
with open(filename, newline='', encoding='EUC-KR') as csvfile:
    csvreader = csv.reader(csvfile)
    cleaned_data = []
    for row in csvreader:
        # 첫 번째 열의 깨진 문자열을 제거합니다.
        print(row[0])
        cleaned_first_column = clean_broken_chars(row[0])
        # 나머지 열은 그대로 출력합니다.
        rest_of_columns = row[1:]
        # 클린업된 첫 번째 열과 나머지 열을 조합하여 출력합니다.
        cleaned_row = [cleaned_first_column] + rest_of_columns
        cleaned_data.append(cleaned_row)
with open(output_filename, 'w', newline='', encoding='utf-8') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerows(cleaned_data)
#upload_to_s3("load\주유소_평균판매가격_제품별.csv","oilprice.csv")
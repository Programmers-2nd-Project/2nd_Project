#!/usr/bin/env python
# coding: utf-8

import requests
import xmltodict
import tkinter as tk
from tkinter import ttk
import pandas as pd
from pandas import json_normalize
import xml.etree.ElementTree as ET
import schedule
import time
import boto3

def main():
    print(2)
    Key = '******'

    # prodcd : 제품구분(휘발유:B027, 경유:D047, 고급휘발유: B034, 실내등유:C004, 자동차부탄: K015)
    # area : 지역구분 (미입력시 전국, 시도코드(2자리):해당시도 기준, 시군코드(4자리):해당시군 기준)
    # 지역 코드 : http://www.opinet.co.kr/api/areaCode.do?out=xml&code=XXXXXX&area=01

    ## 지역코드
    url = f'http://www.opinet.co.kr/api/areaCode.do?out=xml&code={Key}'
    area_result = xmltodict.parse(requests.get(url).content)
    area_result

    area_df = json_normalize(area_result['RESULT']['OIL'])
    area_df


    ## 지역별 최저가 20개
    all_results = []

    brand_mapping = {
        'SKE': 'SK에너지',
        'GSC': 'GS칼텍스',
        'HDO': '현대오일뱅크',
        'SOL': 'S-OIL',
        'RTE': '자영알뜰',
        'RTX': '고속도로알뜰',
        'NHO': '농협알뜰',
        'ETC': '자가상표',
        'E1G': 'E1',
        'SKG': 'SK가스',
        'RTO': '기타'
    }

    # 각 지역에 대해 데이터를 가져오고, AREA_NM을 함께 결과에 추가하여 리스트에 저장
    for area_data in area_result['RESULT']['OIL']:
        area_cd = area_data['AREA_CD']
        area_nm = area_data['AREA_NM']
        url = f'http://www.opinet.co.kr/api/lowTop10.do?out=xml&code={Key}&prodcd=B027&area={area_cd}&cnt=20'
        response = xmltodict.parse(requests.get(url).content)
        result = json_normalize(response['RESULT']['OIL'])
        result['AREA_NM'] = area_nm
        
        all_results.append(result)

    # 결과 출력/저장
    final_result = pd.concat(all_results, ignore_index=True)
    df = pd.DataFrame(final_result)
    df['POLL_DIV_CO'] = df['POLL_DIV_CO'].map(brand_mapping)

    df.to_csv('LowestPrice.csv', index=False, encoding="utf-8-sig", mode='w')


    file_name = r"LowestPrice.csv" # 파일 경로
    bucket_name = 'doyoung-test-bucket' # 본인 버킷 이름
    object_name = 'proj2/LowestPrice.csv'  # 버킷 내의 특정 경로에 저장할 수 있도록 지정 >> 버킷내의 폴더 이름/csv저장 파일 이름

    upload_successful = upload_csv_to_s3(file_name, bucket_name, object_name)
    if upload_successful:
        print(f'{file_name} uploaded successfully to {bucket_name} as {object_name}.')
    else:
        print(f'Failed to upload {file_name} to {bucket_name}.')


# 매일 정해진 시간에 작업을 실행하도록 스케줄링
print(1)
schedule.every().day.at("09:00").do(main)
# ---------------------------------------------------------------------------------------------------------------
# S3 업로드 하는 코드
# 터미널에서 aws configure 실행 후 s3 버킷 권한 있는 aws 사용자의 액세스 키, 시크릿 키, 리전 입력하고 사용
# 연결됐는지 확인하려면 터미널에서 >> aws s3 ls 했을 때 자신의 버킷이 나와야 함
# 이후 코드 실행하면 s3로 저장됨
def upload_csv_to_s3(file_name, bucket_name, object_name=None):
    """Upload a CSV file to an S3 bucket."""
    if object_name is None:
        object_name = os.path.basename(file_name)  # 파일 이름을 기반으로 객체 키 생성
    
    # Create an S3 client
    s3_client = boto3.client('s3')
    
    try:
        # Upload the file
        response = s3_client.upload_file(file_name, bucket_name, object_name)
    except Exception as e:
        print(e)
        return False
    return True

while True:
    schedule.run_pending()
    time.sleep(1)

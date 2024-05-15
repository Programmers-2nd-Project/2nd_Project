#!/usr/bin/env python
# coding: utf-8

import requests
import xmltodict
import tkinter as tk
from tkinter import ttk
import pandas as pd
from pandas import json_normalize
import xml.etree.ElementTree as ET



Key = '******'

# prodcd : 제품구분(휘발유:B027, 경유:D047, 고급휘발유: B034, 실내등유:C004, 자동차부탄: K015)
# area : 지역구분 (미입력시 전국, 시도코드(2자리):해당시도 기준, 시군코드(4자리):해당시군 기준)
# 지역 코드 : http://www.opinet.co.kr/api/areaCode.do?out=xml&code=XXXXXX&area=01


# ## 지역코드

url = f'http://www.opinet.co.kr/api/areaCode.do?out=xml&code={Key}'
area_result = xmltodict.parse(requests.get(url).content)
area_result

area_df = json_normalize(area_result['RESULT']['OIL'])
area_df


# ## 지역별 최저가 20개
all_results = []

# 각 지역에 대해 데이터를 가져오고, AREA_NM을 함께 결과에 추가하여 리스트에 저장
for area_data in area_result['RESULT']['OIL']:
    area_cd = area_data['AREA_CD']
    area_nm = area_data['AREA_NM']
    url = f'http://www.opinet.co.kr/api/lowTop10.do?out=xml&code={Key}&prodcd=B027&area={area_cd}&cnt=20'
    response = xmltodict.parse(requests.get(url).content)
    result = json_normalize(response['RESULT']['OIL'])
    result['AREA_NM'] = area_nm
    
    all_results.append(result)

# 결과 출력
final_result = pd.concat(all_results, ignore_index=True)
# final_result


final_result.to_csv('LowestPrice.csv', index=False, encoding="utf-8-sig")


## 최저가 주유소

url = f'http://www.opinet.co.kr/api/lowTop10.do?out=xml&code={Key}&prodcd=B027&area=0101&cnt=20'
result = xmltodict.parse(requests.get(url).content)
result

df = json_normalize(result['RESULT']['OIL'])

df = df[['OS_NM', 'PRICE', 'VAN_ADR', 'NEW_ADR']]

url = f'https://www.opinet.co.kr/api/avgLastWeek.do?code={Key}&out=xml'
week_result = xmltodict.parse(requests.get(url).content)
week_result





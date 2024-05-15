#!/usr/bin/env python
# coding: utf-8

# In[4]:


import requests
import pandas as pd



def fetch_data(url, params):
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to fetch data:", response.status_code)
        return {}
    
 #API 정보입력
api_key = 'F240513146'  # Opinet에서 발급받은 API 키를 입력하세요.
url = 'http://www.opinet.co.kr/api/pollAvgRecentPrice.do'
params = {
    'code': api_key,
    'out': 'json',
    'prodcd': 'B027'  # 보통휘발유
}

data = fetch_data(url, params)

# 데이터 전처리
if data:
    oil_data = pd.DataFrame(data['RESULT']['OIL'])
else:
    print("No data available.Please put Opinet APIacesskey")
    

# 데이터를 브랜드 코드별로 그룹화하고 평균 가격을 계산
grouped_data = oil_data.groupby('POLL_DIV_CD').mean().round(2)
brand_sorted_data = grouped_data.sort_values(by='PRICE', ascending=True)

# 그룹화된 데이터를 CSV 파일로 저장
brand_sorted_data.to_csv('brand_sorted_data.csv')

print("Grouped data has been saved to 'brand_sorted_data.csv'")


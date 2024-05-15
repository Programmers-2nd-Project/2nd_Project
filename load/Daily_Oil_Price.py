import requests
import datetime
from bs4 import BeautifulSoup 
# pip install lxml
import pandas as pd

def get_oil_data():
    res = requests.get("https://www.opinet.co.kr/api/avgRecentPrice.do?out=xml&code=******") # code = 'api 인증키 작성'
    soup = BeautifulSoup(res.text, 'lxml')
    all_data = soup.find_all("OIL")
    data_list = []

    for data in all_data:
        date_str = data.DATE.text
        date_obj = datetime.datetime.strptime(date_str, '%Y%m%d').date()
        prod_cd = data.PRODCD.text
        oil_type = get_oil_type(prod_cd)
        price = data.PRICE.text
        data_list.append([date_obj, prod_cd, oil_type, price])

    return data_list

def get_oil_type(prod_cd):
    oil_types = {
        'B027': 'High_grade_Gasolin',
        'B034': 'Normal_Gasolin',
        'C004': 'kerosene',
        'D047': 'Diesel',
        'K015': 'butane'
    }
    return oil_types.get(prod_cd, 'Unknown')

# 파일 최신화
def main():
    oil_data = get_oil_data()
    df = pd.DataFrame(oil_data, columns=['DATE', 'PRODCD', 'TYPE', 'PRICE'])
    # mode = 'w' >> 같은 이름 있는 파일 있으면 새로운 파일로 덮어씀
    df.to_csv(r"datafile\Daily_Oil_Price.csv", index=False, mode='w')

# 새로운 데이터 추가
# def main():
#     oil_data = get_oil_data()
#     df = pd.DataFrame(oil_data, columns=['DATE', 'PRODCD', 'TYPE', 'PRICE'])
#     df.to_csv("datafile\Daily_Oil_Price.csv", index=False, mode='a',
#               header=not os.path.exists("datafile\Daily_Oil_Price.csv"))  
    

if __name__ == "__main__":
    main()

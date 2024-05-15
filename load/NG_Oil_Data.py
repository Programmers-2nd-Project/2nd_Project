import requests
from bs4 import BeautifulSoup
# pip install lxml
import pandas as pd

def main():
    # 데이터 수집
    res = requests.get("http://www.opinet.co.kr/api/avgSidoPrice.do?out=xml&code=******&prodcd=B027")
    soup = BeautifulSoup(res.text, 'lxml')

    # XML 데이터 파싱
    all_data = soup.find_all("OIL")

    # 데이터 프레임 생성을 위한 리스트 초기화
    NG_df = []

    # XML 데이터를 리스트로 변환
    for data in all_data:
        ls = [data.SIDOCD.text, data.SIDONM.text, data.PRICE.text]  # 지역 코드, 지역명, 가격
        NG_df.append(ls)

    # 전국 데이터 삭제 (지역별 데이터만 남김)
    NG_df = NG_df[1:]

    # 데이터 프레임 생성
    data_frame = pd.DataFrame(NG_df, columns=['Code', 'SIDO', 'Price'])

    # 위도 경도 매핑
    coordinates = {
        '서울': [37.5665, 126.9780],
        '경기': [37.4138, 127.5183],
        '강원': [37.8228, 128.1555],
        '충북': [36.8001, 127.7996],
        '충남': [36.3482, 126.8289],
        '전북': [35.7175, 127.1530],
        '전남': [34.8679, 126.9910],
        '경북': [36.5763, 128.5055],
        '경남': [35.4606, 128.2132],
        '부산': [35.1796, 129.0756],
        '제주': [33.4996, 126.5312],
        '대구': [35.8714, 128.6014],
        '인천': [37.4563, 126.7052],
        '광주': [35.1595, 126.8526],
        '대전': [36.3504, 127.3845],
        '울산': [35.5384, 129.3114],
        '세종': [36.4801, 127.2882]
    }

    # 위도 경도 데이터 추가
    data_frame['Latitude'] = data_frame['SIDO'].map(lambda x: coordinates[x][0])
    data_frame['Longitude'] = data_frame['SIDO'].map(lambda x: coordinates[x][1])

    # ISO 코드 매핑
    code = {
        '서울': 'KR-11', '경기': 'KR-41', '강원': 'KR-42', '충북': 'KR-43',
        '충남': 'KR-44', '전북': 'KR-45', '전남': 'KR-46', '경북': 'KR-47',
        '경남': 'KR-48', '부산': 'KR-26', '제주': 'KR-49', '대구': 'KR-27',
        '인천': 'KR-28', '광주': 'KR-29', '대전': 'KR-30', '울산': 'KR-31',
        '세종': 'KR-50'
    }

    # ISO 코드 데이터 추가
    data_frame['ISO_Code'] = data_frame['SIDO'].map(lambda x: code[x])

    # CSV 파일로 저장
    data_frame.to_csv(r"datafile\NG_sido_oil_price.csv", header=None, index=False, encoding='utf-8-sig', mode='w')

if __name__ == "__main__":
    main()

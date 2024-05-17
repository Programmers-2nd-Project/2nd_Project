import requests
from bs4 import BeautifulSoup
# pip install lxml
import pandas as pd
import os
import boto3

# 파일 저장 자동화
import schedule
import time
# pip install snowflake-connector-python
import snowflake.connector

def main():
    # 데이터 수집
    res = requests.get("http://www.opinet.co.kr/api/avgSidoPrice.do?out=xml&code=******&prodcd=B027")
    soup = BeautifulSoup(res.text, 'xml')

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
    print("csv file download complete")
    
    # S3에 바로 저장 사용 예시
    file_name = r"datafile\NG_sido_oil_price.csv" # 파일 경로
    bucket_name = 'doyoung-test-bucket' # 본인 버킷 이름
    object_name = 'proj2/NG_sido_oil_price.csv'  # 버킷 내의 특정 경로에 저장할 수 있도록 지정 >> 버킷내의 폴더 이름/csv저장 파일 이름

    upload_successful = upload_csv_to_s3(file_name, bucket_name, object_name)
    if upload_successful:
        print(f'{file_name} uploaded successfully to {bucket_name} as {object_name}.')
    else:
        print(f'Failed to upload {file_name} to {bucket_name}.')
        
    # snowflake
    conn = snowflake.connector.connect(
    user='', # snowflake ID
    password='', # snowflake password
    account='', # snowflake Locator ex) XQB*****
    warehouse='COMPUTE_WH',
    database='PROJ',
    schema='RAW_DATA'
    )

    # SQL 쿼리 실행
    try:
        cursor = conn.cursor()
        
        # 테이블 생성 쿼리 실행
        cursor.execute("""
            CREATE OR REPLACE TABLE PROJ.RAW_DATA.NG_OIL_DATA (
                CODE NUMBER(38,0),
                SIDO VARCHAR(16777216),
                PRICE NUMBER(38,2),
                LATITUDE NUMBER(38,4),
                LONGITUDE NUMBER(38,4),
                ISO_CODE VARCHAR(16777216)
            )
        """)
        
        # S3 데이터를 테이블에 복사하는 쿼리 실행
        cursor.execute("""
            COPY INTO PROJ.RAW_DATA.NG_OIL_DATA
            FROM 's3://doyoung-test-bucket/proj2/NG_sido_oil_price.csv'
            CREDENTIALS=(
                AWS_KEY_ID=''
                AWS_SECRET_KEY=''
            )
            FILE_FORMAT = (type='CSV' skip_header=0 FIELD_OPTIONALLY_ENCLOSED_BY='"')
        """)
        
        cursor.close()
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()
    print("Snowflake Process Complete")


# 매일 정해진 시간에 작업을 실행하도록 스케줄링
schedule.every().day.at("09:00").do(main)
# schedule.every(10).seconds.do(main)

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


# 스케줄러 실행
while True:
    schedule.run_pending()
    time.sleep(1)

# if __name__ == "__main__":
#     main()
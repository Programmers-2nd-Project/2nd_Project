import requests
import pandas as pd
import schedule
import time
import datetime
import boto3
# pip install snowflake-connector-python
import snowflake.connector


print('시작')


def fetch_data(url, params):
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to fetch data:", response.status_code)
        return {}



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


def fetch_and_save_data():
    
    ### 데이터 수집 및 csv파일 저장
    #오피넷 API로 데이터 수집 /API key입력
    api_key = '*****'  # Opinet에서 발급받은 API 키를 입력하세요.
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

    # 상표명 매핑 딕셔너리
    brand_mapping = {
        'SKE': 'SK에너지',
        'GSC': 'GS칼텍스',
        'HDO': '현대오일뱅크',
        'SOL': 'S-OIL',
        'RTO': '자영알뜰',
        'RTX': '고속도로알뜰',
        'NHO': '농협알뜰',
        'ETC': '자가상표'
    }

    # "POLL_DIV_CD" 열의 값을 상표명으로 변경하고 브랜드, 가격 컬럼만 남기기
    oil_data['POLL_DIV_CD'] = oil_data['POLL_DIV_CD'].map(brand_mapping)
    selected_columns = oil_data.loc[:, ['POLL_DIV_CD', 'PRICE']]

    # 브랜드별 Groupby/평균/오름차순정렬/PRICE 정수선언 
    grouped_data = selected_columns.groupby('POLL_DIV_CD').mean()
    brand_sorted_data = grouped_data.sort_values(by='PRICE', ascending=True)
    brand_sorted_data['PRICE'] = brand_sorted_data['PRICE'].astype(int)
    
    # CSV 파일로 저장
    file_name = "../datafile/brand_sorted_data_ko.csv"
    brand_sorted_data.to_csv(file_name, mode='w')
    print(f"Grouped data has been saved to '{file_name}'")



    ### S3 지정된 버킷으로 csv파일 업로드

    file_name = "../datafile/brand_sorted_data_ko.csv" # 파일 경로
    bucket_name = 'doyoung-test-bucket' # 본인 버킷 이름
    object_name = 'proj2/brand_sorted_data_ko.csv'  # 버킷 내의 특정 경로에 저장할 수 있도록 지정 >> 버킷내의 폴더 이름/csv저장 파일 이름

    upload_successful = upload_csv_to_s3(file_name, bucket_name, object_name)
    if upload_successful:
        print(f'S3, {file_name} uploaded successfully to {bucket_name} as {object_name}.')
    else:
        print(f'Failed to upload {file_name} to {bucket_name}.')


    
    ### Snowflake Connector 연동 및 테이블 업데이트
    conn = snowflake.connector.connect(
    user='*****', # snowflake ID
    password='*****', # snowflake password
    account='*****', # snowflake Locator ex) XQB*****
    )

    # SQL 쿼리 실행
    try:
        cursor = conn.cursor()

        # 테이블 생성 쿼리 실행
        cursor.execute("""
             CREATE OR REPLACE TABLE proj.raw_data.brand_sorted_oil_price(
                POLL_DIV_CD VARCHAR(10),
                PRICE INT
            )
        """)

        # S3 데이터를 테이블에 복사하는 쿼리 실행
        cursor.execute("""
             COPY INTO proj.raw_data.brand_sorted_gas_price
            FROM 's3://doyoung-test-bucket/proj2/brand_sorted_data_ko.csv'
            credentials=(
                       AWS_KEY_ID='*****' 
                       AWS_SECRET_KEY='*****')
            FILE_FORMAT = (type='CSV' skip_header=1 FIELD_OPTIONALLY_ENCLOSED_BY='"');
            )
        """)

        cursor.close()
        

    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()
    print("Snowflake Process Complete")





# 10초마다 실행되도록 스케줄 설정
#schedule.every(10).seconds.do(fetch_and_save_data)

#해당시간에만 실행
schedule.every().day.at("09:00").do(fetch_and_save_data)

# 스케줄러 실행
while True:
    schedule.run_pending()
    time.sleep(1) #프로그램 멈춤
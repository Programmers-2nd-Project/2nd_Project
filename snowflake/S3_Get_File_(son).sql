/* 이 작업으로 프리셋이 snowflake에 접근 가능도록 허가
CREATE NETWORK POLICY PRESET_WHITELIST
ALLOWED_IP_LIST = ('35.161.45.11', '54.244.23.85', '52.32.136.34') */

/*
CREATE DATABASE pro2;

-- 3개의 스키마 생성
CREATE SCHEMA pro2.raw_data;
CREATE SCHEMA pro2.analytics;
CREATE SCHEMA pro2.adhoc;
*/
-- 아래 코드는 병합을 위해서 데이터베이스.스키마.테이블 구조 >> 스키마.테이블 구조로 수정
-- oil_price 데이터

-- raw_data 밑에 테이블 생성
CREATE OR REPLACE TABLE raw_data.oil_price (
    oil_date timestamp,
    prodcd varchar(4),
    oil_type varchar(32),
    price float);

-- s3에 적재한 데이터 테이블에 복사
-- Daily_Oil_Price.csv
COPY INTO raw_data.oil_price
FROM '파일 저장된 S3 URL'
credentials=(AWS_KEY_ID='******' AWS_SECRET_KEY='******')
FILE_FORMAT = (type='CSV' skip_header=1 FIELD_OPTIONALLY_ENCLOSED_BY='"');

-- 날짜별로 5개씩 가져와졌는지 확인
SELECT oil_date, COUNT(*) 
FROM raw_data.oil_price
GROUP BY 1;


-- 지역별 경유 가격 데이터

-- raw_data 밑에 테이블 생성
create or replace TABLE RAW_DATA.Diesel_OIL_DATA (
	CODE NUMBER(38,0),
	SIDO VARCHAR(16777216),
	PRICE NUMBER(38,2),
	LATITUDE NUMBER(38,4),
	LONGITUDE NUMBER(38,4),
	ISO_CODE VARCHAR(16777216)
);
    
-- s3에 적재한 데이터 테이블에 복사
-- Diesel_sido_oil_price.csv
COPY INTO RAW_DATA.Diesel_OIL_DATA
FROM '파일 저장된 S3 URL'
credentials=(AWS_KEY_ID='******' AWS_SECRET_KEY='******')
FILE_FORMAT = (type='CSV' skip_header=0 FIELD_OPTIONALLY_ENCLOSED_BY='"');

-- 데이터 확인
SELECT * FROM RAW_DATA.Diesel_OIL_DATA;


-- 지역별 일반 휘발유 가격 데이터

-- raw_data 밑에 테이블 생성
create or replace TABLE RAW_DATA.NG_OIL_DATA (
	CODE NUMBER(38,0),
	SIDO VARCHAR(16777216),
	PRICE NUMBER(38,2),
	LATITUDE NUMBER(38,4),
	LONGITUDE NUMBER(38,4),
	ISO_CODE VARCHAR(16777216)
);
    
-- s3에 적재한 데이터 테이블에 복사
-- NG_sido_oil_price.csv
COPY INTO RAW_DATA.NG_OIL_DATA
FROM '파일 저장된 S3 URL'
credentials=(AWS_KEY_ID='******' AWS_SECRET_KEY='******')
FILE_FORMAT = (type='CSV' skip_header=0 FIELD_OPTIONALLY_ENCLOSED_BY='"');

-- 데이터 확인
SELECT * FROM RAW_DATA.NG_OIL_DATA;

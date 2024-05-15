-- DATABASE 생성
CREATE DATABASE PROJ;

-- 스키마생성
CREATE SCHEMA RAW_DATA;
CREATE SCHEMA ANALYTICS;
CREATE SCHEMA ADHOC;

-- row_data table 생성
CREATE TABLE ROW_DATA.LOWESTPRICE (
 UNI_ID varchar(32) primary key,
 PRICE integer,
 POLL_DIV_CO varchar(32),
 OS_NM varchar(32),
 VAN_ADR varchar(32),
 NEW_ADR varchar(32),
 GIS_X_COOR float,
 GIS_Y_COOR float,
 AREA_NM varchar(32)
);

CREATE TABLE ROW_DATA.MONTHOIL (
 date DATE,
 gasoline NUMBER(10, 2),
 diesel NUMBER(10, 2)
);

CREATE TABLE ROW_DATA.CAR (
 year INTEGER,
 All_sum integer,
 Gasoline integer,
 Diesel integer,
 LPG integer,
 Electric integer,
 Hybrid integer,
 CNG integer,
 etc integer
);

-- S3데이터
COPY INTO RAW_DATA.CAR
FROM 's3://doyoung-test-bucket/proj2/용도별_차종별_규모별_연료별_자동차검사현황_20240514173832.csv'
credentials=(AWS_KEY_ID='******' AWS_SECRET_KEY='******')
FILE_FORMAT = (type='CSV' skip_header=1 FIELD_OPTIONALLY_ENCLOSED_BY='"');

COPY INTO RAW_DATA.LOWESTPRICE
FROM 's3://doyoung-test-bucket/proj2/LowestPrice.csv'
credentials=(AWS_KEY_ID='******' AWS_SECRET_KEY='******')
FILE_FORMAT = (type='CSV' skip_header=1 FIELD_OPTIONALLY_ENCLOSED_BY='"');

COPY INTO RAW_DATA.MONTHOIL
FROM 's3://doyoung-test-bucket/proj2/monoil.csv'
credentials=(AWS_KEY_ID='******' AWS_SECRET_KEY='******')
FILE_FORMAT = (type='CSV' skip_header=1 FIELD_OPTIONALLY_ENCLOSED_BY='"');


-- data 확인
select * from analytics.fuel_per;

select * from RAW_DATA.monthoil;

select * from RAW_DATA.lowestprice;

select AREA_NM, AVG(PRICE) as avg_price
from RAW_DATA.lowestprice
group by area_nm;

select GASOLINE, DIESEL, LPG, ELECTRIC, HYBRID, CNG, ETC
from car
where YEAR=2022;

select AREA_NM, MIN(PRICE)
from RAW_DATA.lowestprice
group by AREA_NM;


-- 차량 퍼센트 테이블생성
-- CREATE TABLE analytics.car_percent AS
-- SELECT
--     (GASOLINE / ALL_SUM * 100) AS GASOLINE_PERCENT,
--     (DIESEL / ALL_SUM * 100) AS DIESEL_PERCENT,
--     (LPG / ALL_SUM * 100) AS LPG_PERCENT,
--     (ELECTRIC / ALL_SUM * 100) AS ELECTRIC_PERCENT,
--     (HYBRID / ALL_SUM * 100) AS HYBRID_PERCENT,
--     (CNG / ALL_SUM * 100) AS CNG_PERCENT,
--     (ETC / ALL_SUM * 100) AS ETC_PERCENT
-- FROM raw_data.car
-- WHERE YEAR = 2022;

-- 차량 퍼센트 테이블생성
CREATE TABLE analytics.fuel_per AS
SELECT 'GASOLINE' AS Fuel, (GASOLINE / ALL_SUM * 100) AS Percent
FROM raw_data.car
WHERE YEAR = 2022
UNION ALL
SELECT 'DIESEL', (DIESEL / ALL_SUM * 100)
FROM raw_data.car
WHERE YEAR = 2022
UNION ALL
SELECT 'LPG', (LPG / ALL_SUM * 100)
FROM raw_data.car
WHERE YEAR = 2022
UNION ALL
SELECT 'ELECTRIC', (ELECTRIC / ALL_SUM * 100)
FROM raw_data.car
WHERE YEAR = 2022
UNION ALL
SELECT 'HYBRID', (HYBRID / ALL_SUM * 100)
FROM raw_data.car
WHERE YEAR = 2022
UNION ALL
SELECT 'CNG', (CNG / ALL_SUM * 100)
FROM raw_data.car
WHERE YEAR = 2022
UNION ALL
SELECT 'ETC', (ETC / ALL_SUM * 100)
FROM raw_data.car
WHERE YEAR = 2022;

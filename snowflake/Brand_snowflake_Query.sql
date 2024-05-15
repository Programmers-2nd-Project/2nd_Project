--DATABASE 생성
CREATE DATABASE dev_proj;



--SCHEMA 생성
CREATE TABLE dev_proj.raw_data.brand_sorted_gas_price(
    POLL_DIV_CD VARCHAR(10),
    PRICE FLOAT
);

--S3 데이터 불러오기 
--※ Access key 수정필요!
COPY INTO dev_proj.raw_data.brand_sorted_gas_price
FROM 's3butterjelly-test-bucket2nd_projbrand_sorted_data_ko.csv'
credentials=(AWS_KEY_ID='Your KEY_ID' AWS_SECRET_KEY='Your SCERET_KEY')
FILE_FORMAT = (type='CSV' skip_header=1 FIELD_OPTIONALLY_ENCLOSED_BY='');


--Data 불러오기 확인
SELECT 
FROM dev_proj.raw_data.brand_sorted_gas_price;
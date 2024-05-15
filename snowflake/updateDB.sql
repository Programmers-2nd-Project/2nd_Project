DELETE FROM DEV.RAW_DATA.OIL;

create or replace TABLE DEV.RAW_DATA.OIL (
	DATE DATE,
	premium DECIMAL,
    regular DECIMAL,
    diesel DECIMAL,
    etc DECIMAL
);

COPY INTO dev.raw_data.oil
FROM 's3://mybucket1qwd/oilprice/oil_price.csv'
credentials=(
    AWS_KEY_ID=''
    AWS_SECRET_KEY=''
)
FILE_FORMAT = (
    TYPE='CSV'
    SKIP_HEADER=1
    FIELD_OPTIONALLY_ENCLOSED_BY='"'
    DATE_FORMAT='YYYYMMDD'

);
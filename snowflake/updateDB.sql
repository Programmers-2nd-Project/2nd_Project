
DELETE FROM DEV.RAW_DATA.OIL;

create or replace TABLE DEV.RAW_DATA.OIL (
	DATE DATE,
	premium DECIMAL,
    regular DECIMAL,
    diesel DECIMAL,
    etc DECIMAL
);

COPY INTO dev.raw_data.oil
FROM ''
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
CREATE OR REPLACE TABLE DEV.RAW_DATA.OIL_VOLATILITY (
    DATE DATE,
    premium_volatility DECIMAL,
    regular_volatility DECIMAL,
    diesel_volatility DECIMAL
);



CREATE OR REPLACE TABLE DEV.RAW_DATA.OIL_VOLATILITY (
    DATE DATE,
    premium_volatility DECIMAL,
    regular_volatility DECIMAL,
    diesel_volatility DECIMAL
);


INSERT INTO DEV.RAW_DATA.OIL_VOLATILITY (DATE, premium_volatility, regular_volatility, diesel_volatility)
SELECT
    DATE,
    (premium - LAG(premium) OVER (ORDER BY DATE)),

    (regular - LAG(regular) OVER (ORDER BY DATE)),
    (diesel - LAG(diesel) OVER (ORDER BY DATE)),
FROM
    DEV.RAW_DATA.OIL;


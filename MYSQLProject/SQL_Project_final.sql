-- Global Resilience Project
-- ============================================================
-- ============================================================
CREATE DATABASE IF NOT EXISTS global_resilience;
USE global_resilience;


-- =============================================
-- SECTION 1: DIMENSION & FACT TABLES
-- =============================================


-- =============================================
-- DIMENSION TABLES
-- =============================================
 
 
-- Country dimension table
-- PK: country_key (auto-increment)
-- Country Code remains the natural/business key
 
DROP TABLE IF EXISTS dim_country;
CREATE TABLE dim_country (
    country_key   INT          NOT NULL AUTO_INCREMENT,
    `Country Code` CHAR(3)     NOT NULL,
    `Country Name` VARCHAR(100) NOT NULL,
    Region         VARCHAR(50)  NOT NULL,
    PRIMARY KEY (country_key),
    UNIQUE KEY uq_country_code (`Country Code`)
);
 
INSERT INTO dim_country (`Country Code`, `Country Name`, Region)
SELECT
    `Country Code`,
    `Country Name`,
    CASE
        WHEN `Country Code` IN ('MAR','TUN','MOZ','ZMB','BWA','NAM','RWA','ETH','GHA','TGO','BFA','SWZ','MDG','MUS') THEN 'Africa'
        WHEN `Country Code` IN ('SAU','ARE','KWT','OMN','JOR','BHR') THEN 'Middle East'
        WHEN `Country Code` IN ('IND','PAK','BGD','LKA','NPL') THEN 'South Asia'
        WHEN `Country Code` IN ('CHN','IDN','MYS','THA','VNM','KHM','PHL','SGP','KOR','MNG') THEN 'East Asia'
        WHEN `Country Code` IN ('KAZ','UZB','KGZ','TJK','AZE','ARM','GEO') THEN 'Central Asia'
        WHEN `Country Code` IN (
            'DEU','FRA','ITA','ESP','PRT','NLD','BEL','AUT','CHE','LUX','IRL','GBR','NOR','SWE',
            'FIN','DNK','ISL','POL','CZE','SVK','HUN','ROU','GRC','EST','LVA','LTU','SVN','HRV',
            'BIH','MKD','ALB','UKR','BLR','MDA','RUS','MLT','CYP','TUR'
        ) THEN 'Europe'
        WHEN `Country Code` IN ('USA','CAN','MEX') THEN 'North America'
        WHEN `Country Code` IN ('BRA','COL','CHL','PER','URY','PRY','BOL','ECU') THEN 'South America'
        WHEN `Country Code` IN ('AUS','NZL') THEN 'Oceania'
        WHEN `Country Code` IN ('GTM','SLV','NIC','PAN','CRI','DOM','JAM') THEN 'Central America & Caribbean'
        ELSE 'Other'
    END AS Region
FROM (
    SELECT DISTINCT `Country Name`, `Country Code`
    FROM (
        SELECT `Country Name`, `Country Code` FROM `fixed_broadband_subscriptions` WHERE `Year` NOT IN (2024,2025)
        UNION ALL
        SELECT `Country Name`, `Country Code` FROM `internet_users` WHERE `Year` NOT IN (2024,2025)
        UNION ALL
        SELECT `Country Name`, `Country Code` FROM `gdp_growth` WHERE `Year` NOT IN (2024,2025)
        UNION ALL
        SELECT `Country Name`, `Country Code` FROM `inflation` WHERE `Year` NOT IN (2024,2025)
        UNION ALL
        SELECT `Country Name`, `Country Code` FROM `food_imports___of_merchandise_imports` WHERE `Year` NOT IN (2024,2025)
        UNION ALL
        SELECT `Country Name`, `Country Code` FROM `prevalence_of_undernourishment` WHERE `Year` NOT IN (2024,2025)
        UNION ALL
        SELECT `Country Name`, `Country Code` FROM `global_health_expenditure` WHERE `Year` NOT IN (2024,2025)
        UNION ALL
        SELECT `Country Name`, `Country Code` FROM `hospitals` WHERE `Attribute` NOT IN (2024,2025)
        UNION ALL
        SELECT `Country Name`, `Country Code` FROM `physicians` WHERE `Year` NOT IN (2024,2025)
        UNION ALL
        SELECT `Country Name`, `Country Code` FROM `political_stability` WHERE `Year` NOT IN (2024,2025)
        UNION ALL
        SELECT `Country Name`, `Country Code` FROM `access_to_electricity` WHERE `Year` NOT IN (2024,2025)
        UNION ALL
        SELECT `Country Name`, `Country Code` FROM `clean_fuel_access` WHERE `Year` NOT IN (2024,2025)
        UNION ALL
        SELECT `Country Name`, `Country Code` FROM `co2_emissions__` WHERE `Year` NOT IN (2024,2025)
        UNION ALL
        SELECT `Country Name`, `Country Code` FROM `renewable_energy__` WHERE `Year` NOT IN (2024,2025)
        UNION ALL
        SELECT `Country Name`, `Country Code` FROM `electricity_consumption__` WHERE `Year` NOT IN (2024,2025)
    ) all_data
    WHERE `Country Code` IN (
        'GEO','MDA','ESP','CHE','GBR','HUN','MYS','RUS','CAN','ISL','NZL','TUR','KOR','MUS','THA',
        'JOR','KAZ','BLR','PHL','KGZ','AUS','BWA','COL','ARM','USA','CHL','LKA','MEX','IND','TUN',
        'AZE','BIH','UKR','CRI','ALB','ARE','URY','JAM','BRA','SLV','NOR','PER','AUT','BEL','CHN',
        'DEU','LVA','CZE','EST','FRA','IRL','ITA','MLT','NLD','PRT','PAK','IDN','FIN','LTU',
        'ROU','SVK','SVN','SWE','MNG','HRV','PAN','DNK','ECU','GRC','OMN','POL','SGP','BGD','BHR',
        'CYP','MAR','MKD','LUX','MOZ','BOL','KWT','ZMB','SAU','NPL','BFA','NIC','VNM','GTM',
        'KHM','RWA','PRY','TJK','TGO','ETH','SWZ','GHA','NAM','MDG','DOM','UZB'
    )
    AND `Country Name` NOT IN ('Egypt, Arab Rep.', 'Israel')
) base_countries;
 
 
-- Indicator dimension table
-- PK: indicator_key (auto-increment)
-- Indicator Code remains the natural/business key
 
DROP TABLE IF EXISTS dim_indicator;
CREATE TABLE dim_indicator (
    indicator_key  INT           NOT NULL AUTO_INCREMENT,
    `Indicator Code` VARCHAR(50) NOT NULL,
    `Indicator Name` VARCHAR(255) NOT NULL,
    Domain           VARCHAR(50)  NOT NULL,
    PRIMARY KEY (indicator_key),
    UNIQUE KEY uq_indicator_code (`Indicator Code`)
);
 
INSERT INTO dim_indicator (`Indicator Code`, `Indicator Name`, Domain)
SELECT DISTINCT
    `Indicator Code`,
    `Indicator Name`,
    CASE
        WHEN `Indicator Code` = 'IT.NET.BBND.P2'       THEN 'Digital Infrastructure'
        WHEN `Indicator Code` = 'IT.NET.USER.ZS'       THEN 'Digital Infrastructure'
        WHEN `Indicator Code` = 'NY.GDP.MKTP.KD.ZG'    THEN 'Economic Fragility'
        WHEN `Indicator Code` = 'FP.CPI.TOTL.ZG'       THEN 'Economic Fragility'
        WHEN `Indicator Code` = 'TM.VAL.FOOD.ZS.UN'    THEN 'Food Security'
        WHEN `Indicator Code` = 'SN.ITK.DEFC.ZS'       THEN 'Food Security'
        WHEN `Indicator Code` = 'SH.XPD.CHEX.GD.ZS'   THEN 'Healthcare'
        WHEN `Indicator Code` = 'SH.MED.BEDS.ZS'       THEN 'Healthcare'
        WHEN `Indicator Code` = 'SH.MED.PHYS.ZS'       THEN 'Healthcare'
        WHEN `Indicator Code` = 'PV.EST'                THEN 'Political Stability'
        WHEN `Indicator Code` = 'EG.ELC.ACCS.ZS'       THEN 'Climate & Energy'
        WHEN `Indicator Code` = 'EG.CFT.ACCS.ZS'       THEN 'Climate & Energy'
        WHEN `Indicator Code` = 'EG.FEC.RNEW.ZS'       THEN 'Climate & Energy'
        WHEN `Indicator Code` = 'EG.USE.ELEC.KH.PC'    THEN 'Climate & Energy'
        WHEN `Indicator Code` = 'EN.GHG.CO2.PC.CE.AR5' THEN 'Climate & Energy'
        ELSE 'Other'
    END AS Domain
FROM (
    SELECT `Indicator Code`, `Indicator Name` FROM `fixed_broadband_subscriptions`
    UNION ALL SELECT `Indicator Code`, `Indicator Name` FROM `internet_users`
    UNION ALL SELECT `Indicator Code`, `Indicator Name` FROM `gdp_growth`
    UNION ALL SELECT `Indicator Code`, `Indicator Name` FROM `inflation`
    UNION ALL SELECT `Indicator Code`, `Indicator Name` FROM `food_imports___of_merchandise_imports`
    UNION ALL SELECT `Indicator Code`, `Indicator Name` FROM `prevalence_of_undernourishment`
    UNION ALL SELECT `Indicator Code`, `Indicator Name` FROM `global_health_expenditure`
    UNION ALL SELECT `Indicator Code`, `Indicator Name` FROM `hospitals`
    UNION ALL SELECT `Indicator Code`, `Indicator Name` FROM `physicians`
    UNION ALL SELECT `Indicator Code`, `Indicator Name` FROM `political_stability`
    UNION ALL SELECT `Indicator Code`, `Indicator Name` FROM `access_to_electricity`
    UNION ALL SELECT `Indicator Code`, `Indicator Name` FROM `clean_fuel_access`
    UNION ALL SELECT `Indicator Code`, `Indicator Name` FROM `co2_emissions__`
    UNION ALL SELECT `Indicator Code`, `Indicator Name` FROM `electricity_consumption__`
    UNION ALL SELECT `Indicator Code`, `Indicator Name` FROM `renewable_energy__`
) all_indicators;
 
 
-- Year dimension table
-- PK: year_key 
 
DROP TABLE IF EXISTS dim_year;
CREATE TABLE dim_year (
    year_key INT  NOT NULL,
    Year     INT  NOT NULL,
    Decade   VARCHAR(10) NOT NULL,
    PRIMARY KEY (year_key),
    UNIQUE KEY uq_year (Year)
);
 
INSERT INTO dim_year (year_key, Year, Decade)
SELECT
    ROW_NUMBER() OVER (ORDER BY Year) AS year_key,
    Year,
    CASE
        WHEN Year BETWEEN 2000 AND 2009 THEN '2000s'
        WHEN Year BETWEEN 2010 AND 2019 THEN '2010s'
        WHEN Year BETWEEN 2020 AND 2029 THEN '2020s'
        ELSE 'Other'
    END AS Decade
FROM (
    SELECT DISTINCT Year
    FROM (
        SELECT `Year` FROM fixed_broadband_subscriptions WHERE `Year` NOT IN (2024,2025)
        UNION
        SELECT `Year` FROM internet_users WHERE `Year` NOT IN (2024,2025)
        UNION
        SELECT `Year` FROM gdp_growth WHERE `Year` NOT IN (2024,2025)
        UNION
        SELECT `Year` FROM inflation WHERE `Year` NOT IN (2024,2025)
        UNION
        SELECT `Year` FROM food_imports___of_merchandise_imports WHERE `Year` NOT IN (2024,2025)
        UNION
        SELECT `Year` FROM prevalence_of_undernourishment WHERE `Year` NOT IN (2024,2025)
        UNION
        SELECT `Year` FROM global_health_expenditure WHERE `Year` NOT IN (2024,2025)
        UNION
        SELECT `Year` FROM physicians WHERE `Year` NOT IN (2024,2025)
        UNION
        SELECT `Year` FROM political_stability WHERE `Year` NOT IN (2024,2025)
        UNION
        SELECT `Year` FROM access_to_electricity WHERE `Year` NOT IN (2024,2025)
        UNION
        SELECT `Year` FROM clean_fuel_access WHERE `Year` NOT IN (2024,2025)
        UNION
        SELECT `Year` FROM co2_emissions__ WHERE `Year` NOT IN (2024,2025)
        UNION
        SELECT `Year` FROM electricity_consumption__ WHERE `Year` NOT IN (2024,2025)
        UNION
        SELECT `Year` FROM renewable_energy__ WHERE `Year` NOT IN (2024,2025)
        UNION
        SELECT `Attribute` AS Year FROM hospitals WHERE `Attribute` NOT IN (2024,2025)
    ) y
) y2;
 
 
-- =============================================
-- STAGING / HELPER TABLES
-- =============================================
 
 
-- Raw fact table -- stacks all 15 source tables into one place
 
DROP TABLE IF EXISTS raw_fact;
CREATE TABLE raw_fact AS
SELECT `Country Name`, `Country Code`, `Indicator Code`, `Year`, `Value`
FROM `fixed_broadband_subscriptions` WHERE `Year` NOT IN (2024,2025)
UNION ALL
SELECT `Country Name`, `Country Code`, `Indicator Code`, `Year`, `Value`
FROM `internet_users` WHERE `Year` NOT IN (2024,2025)
UNION ALL
SELECT `Country Name`, `Country Code`, `Indicator Code`, `Year`, `Value`
FROM `gdp_growth` WHERE `Year` NOT IN (2024,2025)
UNION ALL
SELECT `Country Name`, `Country Code`, `Indicator Code`, `Year`, `Value`
FROM `inflation` WHERE `Year` NOT IN (2024,2025)
UNION ALL
SELECT `Country Name`, `Country Code`, `Indicator Code`, `Year`, `Value`
FROM `food_imports___of_merchandise_imports` WHERE `Year` NOT IN (2024,2025)
UNION ALL
SELECT `Country Name`, `Country Code`, `Indicator Code`, `Year`, `Value`
FROM `prevalence_of_undernourishment` WHERE `Year` NOT IN (2024,2025)
UNION ALL
SELECT `Country Name`, `Country Code`, `Indicator Code`, `Year`, `Value`
FROM `global_health_expenditure` WHERE `Year` NOT IN (2024,2025)
UNION ALL
SELECT `Country Name`, `Country Code`, `Indicator Code`, `Attribute` AS `Year`, `Value`
FROM `hospitals` WHERE `Attribute` NOT IN (2024,2025)
UNION ALL
SELECT `Country Name`, `Country Code`, `Indicator Code`, `Year`, `Value`
FROM `physicians` WHERE `Year` NOT IN (2024,2025)
UNION ALL
SELECT `Country Name`, `Country Code`, `Indicator Code`, `Year`, `Value`
FROM `political_stability` WHERE `Year` NOT IN (2024,2025)
UNION ALL
SELECT `Country Name`, `Country Code`, `Indicator Code`, `Year`, `Value`
FROM `access_to_electricity` WHERE `Year` NOT IN (2024,2025)
UNION ALL
SELECT `Country Name`, `Country Code`, `Indicator Code`, `Year`, `Value`
FROM `clean_fuel_access` WHERE `Year` NOT IN (2024,2025)
UNION ALL
SELECT `Country Name`, `Country Code`, `Indicator Code`, `Year`, `Value`
FROM `co2_emissions__` WHERE `Year` NOT IN (2024,2025)
UNION ALL
SELECT `Country Name`, `Country Code`, `Indicator Code`, `Year`, `Value`
FROM `electricity_consumption__` WHERE `Year` NOT IN (2024,2025)
UNION ALL
SELECT `Country Name`, `Country Code`, `Indicator Code`, `Year`, `Value`
FROM `renewable_energy__` WHERE `Year` NOT IN (2024,2025);
 
 
-- Pre-calculate min and max for each indicator
 
DROP TABLE IF EXISTS minmax_per_indicator;
CREATE TABLE minmax_per_indicator AS
SELECT
    f.`Indicator Code`,
    MIN(f.`Value`) AS min_val,
    MAX(f.`Value`) AS max_val
FROM raw_fact f
JOIN dim_country c ON f.`Country Code` = c.`Country Code`
GROUP BY f.`Indicator Code`;
 
 
-- =============================================
-- FACT TABLES
-- =============================================
 
 
-- Main fact table
-- FKs: country_key → dim_country, indicator_key → dim_indicator, year_key → dim_year
-- country_key and indicator_key are pulled from the existing dim joins
 
DROP TABLE IF EXISTS fact_global_indicators;
CREATE TABLE fact_global_indicators (
    fact_id          BIGINT       NOT NULL AUTO_INCREMENT,
    country_key      INT          NOT NULL,
    indicator_key    INT          NOT NULL,
    year_key         INT          NOT NULL,
    `Country Code`   CHAR(3)      NOT NULL,
    `Indicator Code` VARCHAR(50)  NOT NULL,
    `Value`          DOUBLE,
    min_val          DOUBLE,
    max_val          DOUBLE,
    normalized_raw   DOUBLE,
    `Normalized Value` DOUBLE,
    PRIMARY KEY (fact_id),
    CONSTRAINT fk_fgi_country   FOREIGN KEY (country_key)   REFERENCES dim_country   (country_key),
    CONSTRAINT fk_fgi_indicator FOREIGN KEY (indicator_key) REFERENCES dim_indicator (indicator_key),
    CONSTRAINT fk_fgi_year      FOREIGN KEY (year_key)      REFERENCES dim_year      (year_key)
);
 
INSERT INTO fact_global_indicators (
    country_key,
    indicator_key,
    year_key,
    `Country Code`,
    `Indicator Code`,
    `Value`,
    min_val,
    max_val,
    normalized_raw,
    `Normalized Value`
)
SELECT
    c.country_key,
    d.indicator_key,
    y.year_key,
    f.`Country Code`,
    f.`Indicator Code`,
    f.`Value`,
    mm.min_val,
    mm.max_val,
    -- normalization formula: scale value to 0.01-1.00 range
    CASE
        WHEN mm.max_val = mm.min_val THEN 0.5
        ELSE 0.01 + ((f.`Value` - mm.min_val) / (mm.max_val - mm.min_val)) * 0.99
    END AS normalized_raw,
    -- invert score for indicators where high = bad
    CASE
        WHEN f.`Indicator Code` IN (
            'FP.CPI.TOTL.ZG',
            'NY.GDP.MKTP.KD.ZG',
            'TM.VAL.FOOD.ZS.UN',
            'SN.ITK.DEFC.ZS',
            'EG.USE.ELEC.KH.PC'
        )
        THEN 1 - (
            CASE
                WHEN mm.max_val = mm.min_val THEN 0.5
                ELSE 0.01 + ((f.`Value` - mm.min_val) / (mm.max_val - mm.min_val)) * 0.99
            END
        )
        ELSE
            CASE
                WHEN mm.max_val = mm.min_val THEN 0.5
                ELSE 0.01 + ((f.`Value` - mm.min_val) / (mm.max_val - mm.min_val)) * 0.99
            END
    END AS `Normalized Value`
FROM raw_fact f
JOIN dim_country       c  ON f.`Country Code`   = c.`Country Code`
JOIN dim_indicator     d  ON f.`Indicator Code` = d.`Indicator Code`
JOIN dim_year          y  ON f.`Year`           = y.`Year`
JOIN minmax_per_indicator mm ON f.`Indicator Code` = mm.`Indicator Code`
WHERE f.`Country Code` IN (
    'GEO','MDA','ESP','CHE','GBR','HUN','MYS','RUS','CAN','ISL','NZL','TUR','KOR','MUS','THA',
    'JOR','KAZ','BLR','PHL','KGZ','AUS','BWA','COL','ARM','USA','CHL','LKA','MEX','IND','TUN',
    'AZE','BIH','UKR','CRI','ALB','ARE','URY','JAM','BRA','SLV','NOR','PER','AUT','BEL','CHN',
    'DEU','LVA','CZE','EST','FRA','IRL','ITA','MLT','NLD','PRT','PAK','IDN','FIN','LTU',
    'ROU','SVK','SVN','SWE','MNG','HRV','PAN','DNK','ECU','GRC','OMN','POL','SGP','BGD','BHR',
    'CYP','MAR','MKD','LUX','MOZ','BOL','KWT','ZMB','SAU','NPL','BFA','NIC','VNM','GTM',
    'KHM','RWA','PRY','TJK','TGO','ETH','SWZ','GHA','NAM','MDG','DOM','UZB'
);


-- =============================================
-- Food price fact table
-- FK: year_key → dim_year, type_key → dim_type
 
-- =============================================
-- LOOKUP / TYPE DIMENSION TABLE
-- PK: type_key
-- =============================================

CREATE TABLE IF NOT EXISTS dim_type (
    type_key  TINYINT      NOT NULL AUTO_INCREMENT,
    type_name VARCHAR(20)  NOT NULL,
    PRIMARY KEY (type_key)
);

INSERT INTO dim_type (type_key, type_name) VALUES
(1, 'Food'),
(2, 'Meat'),
(3, 'Dairy'),
(4, 'Cereals'),
(5, 'Oils'),
(6, 'Sugar')
ON DUPLICATE KEY UPDATE type_name = VALUES(type_name);

SELECT * FROM dim_type ORDER BY type_key;


DROP TABLE IF EXISTS fact_food_index;
CREATE TABLE fact_food_index (
    food_fact_id   INT      NOT NULL AUTO_INCREMENT,
    year_key       INT      NOT NULL,
    type_key       TINYINT  NOT NULL,
    Month          TINYINT  NOT NULL,
    `Price Index`  DOUBLE,
    `Price Category` VARCHAR(30),
    PRIMARY KEY (food_fact_id),
    CONSTRAINT fk_ffi_year FOREIGN KEY (year_key) REFERENCES dim_year (year_key),
    CONSTRAINT fk_ffi_type FOREIGN KEY (type_key) REFERENCES dim_type (type_key)
);
 
INSERT INTO fact_food_index (year_key, type_key, Month, `Price Index`, `Price Category`)
 
SELECT
    y.year_key,
    1 AS type_key,
    MONTH(STR_TO_DATE(`Date`, '%d/%m/%Y')) AS Month,
    `Food Price Index` AS `Price Index`,
    CASE
        WHEN `Food Price Index` < 50  THEN 'Extremely Cheap'
        WHEN `Food Price Index` < 60  THEN 'Very Cheap'
        WHEN `Food Price Index` < 70  THEN 'Cheap'
        WHEN `Food Price Index` < 80  THEN 'Slightly Cheap'
        WHEN `Food Price Index` < 90  THEN 'Below Normal'
        WHEN `Food Price Index` < 100 THEN 'Near Normal'
        WHEN `Food Price Index` < 110 THEN 'Slightly Expensive'
        WHEN `Food Price Index` < 120 THEN 'Moderately Expensive'
        WHEN `Food Price Index` < 140 THEN 'Expensive'
        ELSE 'Very Expensive'
    END AS `Price Category`
FROM fao_food_price_index
JOIN dim_year y ON YEAR(STR_TO_DATE(`Date`, '%d/%m/%Y')) = y.Year
WHERE YEAR(STR_TO_DATE(`Date`, '%d/%m/%Y')) NOT IN (2024,2025,2026)
 
UNION ALL
 
SELECT
    y.year_key,
    2,
    MONTH(STR_TO_DATE(`Date`, '%d/%m/%Y')),
    `Meat Price Index`,
    CASE
        WHEN `Meat Price Index` < 50  THEN 'Extremely Cheap'
        WHEN `Meat Price Index` < 60  THEN 'Very Cheap'
        WHEN `Meat Price Index` < 70  THEN 'Cheap'
        WHEN `Meat Price Index` < 80  THEN 'Slightly Cheap'
        WHEN `Meat Price Index` < 90  THEN 'Below Normal'
        WHEN `Meat Price Index` < 100 THEN 'Near Normal'
        WHEN `Meat Price Index` < 110 THEN 'Slightly Expensive'
        WHEN `Meat Price Index` < 120 THEN 'Moderately Expensive'
        WHEN `Meat Price Index` < 140 THEN 'Expensive'
        ELSE 'Very Expensive'
    END
FROM fao_food_price_index
JOIN dim_year y ON YEAR(STR_TO_DATE(`Date`, '%d/%m/%Y')) = y.Year
WHERE YEAR(STR_TO_DATE(`Date`, '%d/%m/%Y')) NOT IN (2024,2025,2026)
 
UNION ALL
 
SELECT
    y.year_key,
    3,
    MONTH(STR_TO_DATE(`Date`, '%d/%m/%Y')),
    `Dairy Price Index`,
    CASE
        WHEN `Dairy Price Index` < 50  THEN 'Extremely Cheap'
        WHEN `Dairy Price Index` < 60  THEN 'Very Cheap'
        WHEN `Dairy Price Index` < 70  THEN 'Cheap'
        WHEN `Dairy Price Index` < 80  THEN 'Slightly Cheap'
        WHEN `Dairy Price Index` < 90  THEN 'Below Normal'
        WHEN `Dairy Price Index` < 100 THEN 'Near Normal'
        WHEN `Dairy Price Index` < 110 THEN 'Slightly Expensive'
        WHEN `Dairy Price Index` < 120 THEN 'Moderately Expensive'
        WHEN `Dairy Price Index` < 140 THEN 'Expensive'
        ELSE 'Very Expensive'
    END
FROM fao_food_price_index
JOIN dim_year y ON YEAR(STR_TO_DATE(`Date`, '%d/%m/%Y')) = y.Year
WHERE YEAR(STR_TO_DATE(`Date`, '%d/%m/%Y')) NOT IN (2024,2025,2026)
 
UNION ALL
 
SELECT
    y.year_key,
    4,
    MONTH(STR_TO_DATE(`Date`, '%d/%m/%Y')),
    `Cereals Price Index`,
    CASE
        WHEN `Cereals Price Index` < 50  THEN 'Extremely Cheap'
        WHEN `Cereals Price Index` < 60  THEN 'Very Cheap'
        WHEN `Cereals Price Index` < 70  THEN 'Cheap'
        WHEN `Cereals Price Index` < 80  THEN 'Slightly Cheap'
        WHEN `Cereals Price Index` < 90  THEN 'Below Normal'
        WHEN `Cereals Price Index` < 100 THEN 'Near Normal'
        WHEN `Cereals Price Index` < 110 THEN 'Slightly Expensive'
        WHEN `Cereals Price Index` < 120 THEN 'Moderately Expensive'
        WHEN `Cereals Price Index` < 140 THEN 'Expensive'
        ELSE 'Very Expensive'
    END
FROM fao_food_price_index
JOIN dim_year y ON YEAR(STR_TO_DATE(`Date`, '%d/%m/%Y')) = y.Year
WHERE YEAR(STR_TO_DATE(`Date`, '%d/%m/%Y')) NOT IN (2024,2025,2026)
 
UNION ALL
 
SELECT
    y.year_key,
    5,
    MONTH(STR_TO_DATE(`Date`, '%d/%m/%Y')),
    `Oils Price Index`,
    CASE
        WHEN `Oils Price Index` < 50  THEN 'Extremely Cheap'
        WHEN `Oils Price Index` < 60  THEN 'Very Cheap'
        WHEN `Oils Price Index` < 70  THEN 'Cheap'
        WHEN `Oils Price Index` < 80  THEN 'Slightly Cheap'
        WHEN `Oils Price Index` < 90  THEN 'Below Normal'
        WHEN `Oils Price Index` < 100 THEN 'Near Normal'
        WHEN `Oils Price Index` < 110 THEN 'Slightly Expensive'
        WHEN `Oils Price Index` < 120 THEN 'Moderately Expensive'
        WHEN `Oils Price Index` < 140 THEN 'Expensive'
        ELSE 'Very Expensive'
    END
FROM fao_food_price_index
JOIN dim_year y ON YEAR(STR_TO_DATE(`Date`, '%d/%m/%Y')) = y.Year
WHERE YEAR(STR_TO_DATE(`Date`, '%d/%m/%Y')) NOT IN (2024,2025,2026)
 
UNION ALL
 
SELECT
    y.year_key,
    6,
    MONTH(STR_TO_DATE(`Date`, '%d/%m/%Y')),
    `Sugar Price Index`,
    CASE
        WHEN `Sugar Price Index` < 50  THEN 'Extremely Cheap'
        WHEN `Sugar Price Index` < 60  THEN 'Very Cheap'
        WHEN `Sugar Price Index` < 70  THEN 'Cheap'
        WHEN `Sugar Price Index` < 80  THEN 'Slightly Cheap'
        WHEN `Sugar Price Index` < 90  THEN 'Below Normal'
        WHEN `Sugar Price Index` < 100 THEN 'Near Normal'
        WHEN `Sugar Price Index` < 110 THEN 'Slightly Expensive'
        WHEN `Sugar Price Index` < 120 THEN 'Moderately Expensive'
        WHEN `Sugar Price Index` < 140 THEN 'Expensive'
        ELSE 'Very Expensive'
    END
FROM fao_food_price_index
JOIN dim_year y ON YEAR(STR_TO_DATE(`Date`, '%d/%m/%Y')) = y.Year
WHERE YEAR(STR_TO_DATE(`Date`, '%d/%m/%Y')) NOT IN (2024,2025,2026);



-- =============================================

-- =============================================
-- SECTION 2: QUICK MEASURES / CHECKS
-- =============================================

-- just running these to check key numbers before building the full KPI section

SELECT AVG(f.`Normalized Value`) AS avg_resilience_score
FROM fact_global_indicators f;

SELECT AVG(f.`Normalized Value`) AS avg_risk_score
FROM fact_global_indicators f
JOIN dim_indicator d ON f.indicator_key = d.indicator_key
WHERE d.Domain IN ('Economic Fragility', 'Political Stability');

SELECT AVG(f.`Value`) AS food_dependency_rate
FROM fact_global_indicators f
WHERE f.`Indicator Code` = 'TM.VAL.FOOD.ZS.UN';

SELECT AVG(f.`Normalized Value`) AS food_vulnerability_score
FROM fact_global_indicators f
JOIN dim_indicator d ON f.indicator_key = d.indicator_key
WHERE d.Domain = 'Food Security';

SELECT MAX(country_avg) AS highest_survival_score
FROM (
    SELECT c.`Country Name`, AVG(f.`Normalized Value`) AS country_avg
    FROM fact_global_indicators f
    JOIN dim_country c ON f.country_key = c.country_key
    GROUP BY c.`Country Name`
) t;

-- =============================================
-- SECTION 3: KPI QUERIES
-- =============================================

-- same as section 2 but formatted with ROUND for the final report

SELECT ROUND(AVG(f.`Normalized Value`), 2) AS `Average Resilience Score`
FROM fact_global_indicators f;

SELECT ROUND(AVG(f.`Normalized Value`), 2) AS `Average Risk Score`
FROM fact_global_indicators f
JOIN dim_indicator d ON f.indicator_key = d.indicator_key
WHERE d.Domain IN ('Economic Fragility', 'Political Stability');

SELECT ROUND(AVG(f.`Value`), 2) AS `Food Dependency Rate`
FROM fact_global_indicators f
WHERE f.`Indicator Code` = 'TM.VAL.FOOD.ZS.UN';

SELECT ROUND(AVG(f.`Normalized Value`), 2) AS `Food Vulnerability Score`
FROM fact_global_indicators f
JOIN dim_indicator d ON f.indicator_key = d.indicator_key
WHERE d.Domain = 'Food Security';

SELECT ROUND(MAX(country_avg), 2) AS `Highest Survival Score`
FROM (
    SELECT c.`Country Name`, AVG(f.`Normalized Value`) AS country_avg
    FROM fact_global_indicators f
    JOIN dim_country c ON f.country_key = c.country_key
    GROUP BY c.`Country Name`
) t;

SELECT ROUND(MIN(country_avg), 2) AS `Lowest Stability Score`
FROM (
    SELECT c.`Country Name`, AVG(f.`Normalized Value`) AS country_avg
    FROM fact_global_indicators f
    JOIN dim_country   c ON f.country_key   = c.country_key
    JOIN dim_indicator d ON f.indicator_key = d.indicator_key
    WHERE d.Domain = 'Political Stability'
    GROUP BY c.`Country Name`
) t;

SELECT c.`Country Name` AS `Most Resilient Country`
FROM (
    SELECT f.country_key, AVG(f.`Normalized Value`) AS avg_score
    FROM fact_global_indicators f
    GROUP BY f.country_key
    ORDER BY avg_score DESC
    LIMIT 1
) best
JOIN dim_country c ON best.country_key = c.country_key;


SELECT COUNT(*) AS `High Risk Countries`
FROM (
    SELECT f.country_key, AVG(f.`Normalized Value`) AS avg_score
    FROM fact_global_indicators f
    GROUP BY f.country_key
    HAVING avg_score < 0.5
) t;


SELECT COUNT(*) AS `Number of Stable Countries`
FROM (
    SELECT f.country_key, AVG(f.`Normalized Value`) AS avg_score
    FROM fact_global_indicators f
    GROUP BY f.country_key
    HAVING avg_score >= 0.5
) t;


SELECT d.Domain AS `Strongest Domain`
FROM (
    SELECT d.Domain, AVG(f.`Normalized Value`) AS domain_avg
    FROM fact_global_indicators f
    JOIN dim_indicator d ON f.indicator_key = d.indicator_key
    GROUP BY d.Domain
    ORDER BY domain_avg DESC
    LIMIT 1
) AS d;


SELECT d.Domain AS `Weakest Domain`
FROM (
    SELECT d.Domain, AVG(f.`Normalized Value`) AS domain_avg
    FROM fact_global_indicators f
    JOIN dim_indicator d ON f.indicator_key = d.indicator_key
    GROUP BY d.Domain
    ORDER BY domain_avg ASC
    LIMIT 1
) AS d;


SELECT c.Region AS `Top Region`
FROM (
    SELECT c.Region, AVG(f.`Normalized Value`) AS region_avg
    FROM fact_global_indicators f
    JOIN dim_country c ON f.country_key = c.country_key
    GROUP BY c.Region
    ORDER BY region_avg DESC
    LIMIT 1
)AS c;


SELECT c.Region AS `Lowest Region`
FROM (
    SELECT c.Region, AVG(f.`Normalized Value`) AS region_avg
    FROM fact_global_indicators f
    JOIN dim_country c ON f.country_key = c.country_key
    GROUP BY c.Region
    ORDER BY region_avg ASC
    LIMIT 1
) as c ;


SELECT c.`Country Name` AS `Most Balanced Country`
FROM (
    SELECT inner_t.country_key, STDDEV_POP(domain_avg) AS domain_stddev
    FROM (
        SELECT f.country_key, d.Domain, AVG(f.`Normalized Value`) AS domain_avg
        FROM fact_global_indicators f
        JOIN dim_indicator d ON f.indicator_key = d.indicator_key
        GROUP BY f.country_key, d.Domain
    ) inner_t
    GROUP BY country_key
    ORDER BY domain_stddev ASC
    LIMIT 1
) t
JOIN dim_country c ON t.country_key = c.country_key;


SELECT c.`Country Name` AS `Lowest Risk Country`
FROM (
    SELECT f.country_key, AVG(f.`Normalized Value`) AS risk_avg
    FROM fact_global_indicators f
    JOIN dim_indicator d ON f.indicator_key = d.indicator_key
    WHERE d.Domain IN ('Economic Fragility', 'Political Stability')
    GROUP BY f.country_key
    ORDER BY risk_avg ASC
    LIMIT 1
) t
JOIN dim_country c ON t.country_key = c.country_key;


SELECT ROUND(AVG(f.`Value`), 2) AS `Undernourishment Rate`
FROM fact_global_indicators f
WHERE f.`Indicator Code` = 'SN.ITK.DEFC.ZS';



SELECT c.`Country Name` AS `Highest Improving Country`
FROM (
    SELECT
        f.country_key,
        AVG(CASE WHEN y.Decade = '2000s' THEN f.`Normalized Value` END) AS early_avg,
        AVG(CASE WHEN y.Decade = '2020s' THEN f.`Normalized Value` END) AS recent_avg
    FROM fact_global_indicators f
    JOIN dim_year y ON f.year_key = y.year_key
    GROUP BY f.country_key
    HAVING early_avg IS NOT NULL AND recent_avg IS NOT NULL
    ORDER BY (recent_avg - early_avg) DESC
    LIMIT 1
) t
JOIN dim_country c ON t.country_key = c.country_key;



-- =============================================
-- SECTION 4: ANALYTICAL QUERIES
-- =============================================

-- A1: Country ranking by overall resilience score
SELECT
    c.`Country Name`,
    c.Region,
    ROUND(AVG(f.`Normalized Value`), 2) AS `Composite Resilience Score`
FROM fact_global_indicators f
JOIN dim_country c ON f.country_key = c.country_key
GROUP BY c.`Country Name`, c.Region
ORDER BY `Composite Resilience Score` DESC;


-- A2: Domain score per country
SELECT
    c.`Country Name`,
    c.Region,
    d.Domain,
    ROUND(AVG(f.`Normalized Value`), 2) AS `Domain Score`
FROM fact_global_indicators f
JOIN dim_country   c ON f.country_key   = c.country_key
JOIN dim_indicator d ON f.indicator_key = d.indicator_key
GROUP BY c.`Country Name`, c.Region, d.Domain
ORDER BY c.`Country Name`, d.Domain;


-- A3: Global average per domain
SELECT
    d.Domain,
    ROUND(AVG(f.`Normalized Value`), 2) AS `Global Domain Average`
FROM fact_global_indicators f
JOIN dim_indicator d ON f.indicator_key = d.indicator_key
GROUP BY d.Domain
ORDER BY `Global Domain Average` DESC;


-- A4: Region x Domain score matrix
SELECT
    c.Region,
    d.Domain,
    ROUND(AVG(f.`Normalized Value`), 2) AS `Avg Resilience Score`
FROM fact_global_indicators f
JOIN dim_country   c ON f.country_key   = c.country_key
JOIN dim_indicator d ON f.indicator_key = d.indicator_key
GROUP BY c.Region, d.Domain
ORDER BY c.Region, d.Domain;


-- A5: Yearly trend
SELECT
    y.`Year`,
    y.Decade,
    ROUND(AVG(f.`Normalized Value`), 2) AS `Avg Resilience`
FROM fact_global_indicators f
JOIN dim_year y ON f.year_key = y.year_key
GROUP BY y.`Year`, y.Decade
ORDER BY y.`Year`;


-- A6: Decade-level trend
SELECT
    y.Decade,
    ROUND(AVG(f.`Normalized Value`), 2) AS `Avg Resilience`
FROM fact_global_indicators f
JOIN dim_year y ON f.year_key = y.year_key
GROUP BY y.Decade
ORDER BY y.Decade;


-- A7: Domain scores side by side per country (pivot using CASE WHEN)
SELECT
    c.`Country Name`,
    c.Region,
    ROUND(AVG(CASE WHEN d.Domain = 'Climate & Energy'       THEN f.`Normalized Value` END), 2) AS `Climate & Energy`,
    ROUND(AVG(CASE WHEN d.Domain = 'Digital Infrastructure' THEN f.`Normalized Value` END), 2) AS `Digital Infrastructure`,
    ROUND(AVG(CASE WHEN d.Domain = 'Economic Fragility'     THEN f.`Normalized Value` END), 2) AS `Economic Fragility`,
    ROUND(AVG(CASE WHEN d.Domain = 'Food Security'          THEN f.`Normalized Value` END), 2) AS `Food Security`,
    ROUND(AVG(CASE WHEN d.Domain = 'Healthcare'             THEN f.`Normalized Value` END), 2) AS Healthcare,
    ROUND(AVG(CASE WHEN d.Domain = 'Political Stability'    THEN f.`Normalized Value` END), 2) AS `Political Stability`,
    ROUND(AVG(f.`Normalized Value`), 2)                                                         AS `Composite Score`
FROM fact_global_indicators f
JOIN dim_country   c ON f.country_key   = c.country_key
JOIN dim_indicator d ON f.indicator_key = d.indicator_key
GROUP BY c.`Country Name`, c.Region
ORDER BY `Composite Score` DESC;


-- A8: Countries with score below 0.5 = high risk
SELECT
    c.`Country Name`,
    c.Region,
    ROUND(AVG(f.`Normalized Value`), 2) AS `Composite Score`,
    'High Risk' AS `Risk Category`
FROM fact_global_indicators f
JOIN dim_country c ON f.country_key = c.country_key
GROUP BY c.`Country Name`, c.Region
HAVING AVG(f.`Normalized Value`) < 0.5
ORDER BY `Composite Score` ASC;


-- A9: Countries with score >= 0.5 = stable
SELECT
    c.`Country Name`,
    c.Region,
    ROUND(AVG(f.`Normalized Value`), 2) AS `Composite Score`,
    'Stable' AS `Risk Category`
FROM fact_global_indicators f
JOIN dim_country c ON f.country_key = c.country_key
GROUP BY c.`Country Name`, c.Region
HAVING AVG(f.`Normalized Value`) >= 0.5
ORDER BY `Composite Score` DESC;


-- =============================================
-- SECTION 5: FOOD INDEX ANALYSIS
-- =============================================

-- A10: Food price trend by commodity type
SELECT
    y.Year,
    t.type_name AS Type,
    ROUND(AVG(fi.`Price Index`), 2) AS `Avg Annual Price Index`,
    MAX(fi.`Price Index`)           AS `Max Price Index`,
    MIN(fi.`Price Index`)           AS `Min Price Index`,
    fi.`Price Category`
FROM fact_food_index fi
JOIN dim_year y ON fi.year_key = y.year_key
JOIN dim_type t ON fi.type_key = t.type_key
GROUP BY y.Year, t.type_name, fi.`Price Category`
ORDER BY y.Year, t.type_name;


-- A11: Price category distribution by commodity
SELECT
    t.type_name AS Type,
    fi.`Price Category`,
    COUNT(*) AS `Month Count`,
    ROUND(AVG(fi.`Price Index`), 2) AS `Avg Index`
FROM fact_food_index fi
JOIN dim_type t ON fi.type_key = t.type_key
GROUP BY t.type_name, fi.`Price Category`
ORDER BY t.type_name, `Avg Index`;


-- A12: Peak price year per commodity
SELECT
    t.type_name AS Type,
    y.Year      AS `Peak Year`,
    ROUND(AVG(fi.`Price Index`), 2) AS `Avg Price Index`
FROM fact_food_index fi
JOIN dim_year y ON fi.year_key = y.year_key
JOIN dim_type t ON fi.type_key = t.type_key
GROUP BY t.type_name, y.Year
ORDER BY t.type_name, `Avg Price Index` DESC;


-- =============================================
-- SECTION 6: MULTI-DECADE & ADVANCED ANALYSIS
-- =============================================

-- A13: Score comparison across 3 decades + improvement score
SELECT
    c.`Country Name`,
    c.Region,
    ROUND(AVG(CASE WHEN y.Decade = '2000s' THEN f.`Normalized Value` END), 2) AS Score_2000s,
    ROUND(AVG(CASE WHEN y.Decade = '2010s' THEN f.`Normalized Value` END), 2) AS Score_2010s,
    ROUND(AVG(CASE WHEN y.Decade = '2020s' THEN f.`Normalized Value` END), 2) AS Score_2020s,
    ROUND(
        AVG(CASE WHEN y.Decade = '2020s' THEN f.`Normalized Value` END)
        - AVG(CASE WHEN y.Decade = '2000s' THEN f.`Normalized Value` END),
    2) AS Decade_Improvement
FROM fact_global_indicators f
JOIN dim_country c ON f.country_key = c.country_key
JOIN dim_year    y ON f.year_key    = y.year_key
GROUP BY c.`Country Name`, c.Region
ORDER BY Decade_Improvement DESC;


-- A14: Raw indicator averages (before normalization)
SELECT
    c.`Country Name`,
    c.Region,
    f.`Indicator Code`,
    d.Domain,
    ROUND(AVG(f.`Value`), 2) AS `Avg Raw Value`
FROM fact_global_indicators f
JOIN dim_country   c ON f.country_key   = c.country_key
JOIN dim_indicator d ON f.indicator_key = d.indicator_key
GROUP BY c.`Country Name`, c.Region, f.`Indicator Code`, d.Domain
ORDER BY c.`Country Name`, d.Domain;


-- A15: Political stability trend over time
SELECT
    y.`Year`,
    ROUND(AVG(f.`Value`), 2) AS `Avg Political Stability Index`
FROM fact_global_indicators f
JOIN dim_year y ON f.year_key = y.year_key
WHERE f.`Indicator Code` = 'PV.EST'
GROUP BY y.`Year`
ORDER BY y.`Year`;


-- A16: Top 10 most resilient countries
SELECT
    c.`Country Name`,
    c.Region,
    ROUND(AVG(f.`Normalized Value`), 2) AS `Composite Score`
FROM fact_global_indicators f
JOIN dim_country c ON f.country_key = c.country_key
GROUP BY c.`Country Name`, c.Region
ORDER BY `Composite Score` DESC
LIMIT 10;


-- A17: Bottom 10 least resilient countries
SELECT
    c.`Country Name`,
    c.Region,
    ROUND(AVG(f.`Normalized Value`), 2) AS `Composite Score`
FROM fact_global_indicators f
JOIN dim_country c ON f.country_key = c.country_key
GROUP BY c.`Country Name`, c.Region
ORDER BY `Composite Score` ASC
LIMIT 10;


-- A18: Region ranking
-- using RANK() here because ties should get the same rank
SELECT
    RANK() OVER (ORDER BY `Region Resilience Score` DESC) AS `Rank`,
    Region,
    `Region Resilience Score`,
    `Country Count`
FROM (
    SELECT
        c.Region,
        ROUND(AVG(f.`Normalized Value`), 2)      AS `Region Resilience Score`,
        COUNT(DISTINCT c.`Country Name`)          AS `Country Count`
    FROM fact_global_indicators f
    JOIN dim_country c ON f.country_key = c.country_key
    GROUP BY c.Region
) ranked
ORDER BY `Rank`;


-- A19: Outlier detection using Z-score
-- any row more than 3 standard deviations from the mean = outlier

SELECT
    c.`Country Name`,
    f.`Indicator Code`,
    y.`Year`,
    f.`Value`,
    ROUND((f.`Value` - stats.mean_val) / NULLIF(stats.std_val, 0), 2) AS Z_Score,
    CASE
        WHEN ABS((f.`Value` - stats.mean_val) / NULLIF(stats.std_val, 0)) > 3 THEN 'Outlier'
        ELSE 'Normal'
    END AS Outlier_Flag
FROM fact_global_indicators f
JOIN dim_country c ON f.country_key = c.country_key
JOIN dim_year    y ON f.year_key    = y.year_key
JOIN (
    SELECT
        `Indicator Code`,
        AVG(`Value`)        AS mean_val,
        STDDEV_POP(`Value`) AS std_val
    FROM fact_global_indicators
    GROUP BY `Indicator Code`
) stats ON f.`Indicator Code` = stats.`Indicator Code`
WHERE ABS((f.`Value` - stats.mean_val) / NULLIF(stats.std_val, 0)) > 3
ORDER BY ABS((f.`Value` - stats.mean_val) / NULLIF(stats.std_val, 0)) DESC;


-- A20: Tier segmentation based on composite score
SELECT
    c.`Country Name`,
    c.Region,
    ROUND(AVG(f.`Normalized Value`), 2) AS `Composite Score`,
    CASE
        WHEN AVG(f.`Normalized Value`) >= 0.70 THEN 'High Resilience'
        WHEN AVG(f.`Normalized Value`) >= 0.55 THEN 'Medium-High'
        WHEN AVG(f.`Normalized Value`) >= 0.40 THEN 'Medium-Low'
        ELSE 'Low Resilience'
    END AS `Resilience Tier`
FROM fact_global_indicators f
JOIN dim_country c ON f.country_key = c.country_key
GROUP BY c.`Country Name`, c.Region
ORDER BY `Composite Score` DESC;


-- A21: Volatility per domain (how spread out are the scores?)
SELECT
    d.Domain,
    ROUND(AVG(f.`Normalized Value`),     2) AS `Avg Normalized`,
    ROUND(STDDEV_POP(f.`Normalized Value`), 2) AS `StdDev Normalized`,
    ROUND(MAX(f.`Normalized Value`),     2) AS `Max Normalized`,
    ROUND(MIN(f.`Normalized Value`),     2) AS `Min Normalized`
FROM fact_global_indicators f
JOIN dim_indicator d ON f.indicator_key = d.indicator_key
GROUP BY d.Domain
ORDER BY `StdDev Normalized` DESC;


-- A22: Double exposure -- countries that are weak in both healthcare AND food security
-- using subqueries instead of CTEs to keep it simpler

SELECT
    h.`Country Name`,
    h.Region,
    ROUND(h.health_score, 2)          AS `Healthcare Score`,
    ROUND(f.undernourishment_pct, 2)  AS `Avg Undernourishment %`,
    CASE
        WHEN h.health_score < 0.4 AND f.undernourishment_pct > 10 THEN 'Double Risk'
        ELSE 'Single / No Risk'
    END AS `Exposure Type`
FROM (
    SELECT c.`Country Name`, c.Region, AVG(f.`Normalized Value`) AS health_score
    FROM fact_global_indicators f
    JOIN dim_country   c ON f.country_key   = c.country_key
    JOIN dim_indicator d ON f.indicator_key = d.indicator_key
    WHERE d.Domain = 'Healthcare'
    GROUP BY c.`Country Name`, c.Region
) h
JOIN (
    SELECT c.`Country Name`, AVG(f.`Value`) AS undernourishment_pct
    FROM fact_global_indicators f
    JOIN dim_country c ON f.country_key = c.country_key
    WHERE f.`Indicator Code` = 'SN.ITK.DEFC.ZS'
    GROUP BY c.`Country Name`
) f ON h.`Country Name` = f.`Country Name`
ORDER BY h.health_score ASC, f.undernourishment_pct DESC;


-- A23: Internet penetration growth over time
SELECT
    y.`Year`,
    ROUND(AVG(f.`Value`), 2) AS `Mean Internet Users %`
FROM fact_global_indicators f
JOIN dim_year y ON f.year_key = y.year_key
WHERE f.`Indicator Code` = 'IT.NET.USER.ZS'
GROUP BY y.`Year`
ORDER BY y.`Year`;


-- A24: GDP shock years -- years where average growth was very low
SELECT
    y.`Year`,
    ROUND(AVG(f.`Value`), 2) AS `Avg GDP Growth %`,
    ROUND(MIN(f.`Value`), 2) AS `Min GDP Growth %`,
    ROUND(MAX(f.`Value`), 2) AS `Max GDP Growth %`
FROM fact_global_indicators f
JOIN dim_year y ON f.year_key = y.year_key
WHERE f.`Indicator Code` = 'NY.GDP.MKTP.KD.ZG'
GROUP BY y.`Year`
ORDER BY y.`Year`;


-- A25: 2022 food price shock -- how much did prices jump vs pre-pandemic 2020?
SELECT
    t.type_name AS Type,
    ROUND(AVG(CASE WHEN y.Year = 2020 THEN fi.`Price Index` END), 2) AS Avg_2020,
    ROUND(AVG(CASE WHEN y.Year = 2022 THEN fi.`Price Index` END), 2) AS Avg_2022,
    ROUND(
        (AVG(CASE WHEN y.Year = 2022 THEN fi.`Price Index` END) - AVG(CASE WHEN y.Year = 2020 THEN fi.`Price Index` END))
        / NULLIF(AVG(CASE WHEN y.Year = 2020 THEN fi.`Price Index` END), 0) * 100,
    2) AS Pct_Change_vs_2020
FROM fact_food_index fi
JOIN dim_year y ON fi.year_key = y.year_key
JOIN dim_type t ON fi.type_key = t.type_key
GROUP BY t.type_name
ORDER BY Pct_Change_vs_2020 DESC;


-- =============================================
-- SECTION 7: FOOD INDEX DEEP DIVES
-- =============================================

-- A28: Oils price history
SELECT
    y.Year,
    ROUND(AVG(fi.`Price Index`), 2) AS `Avg Oils Index`,
    MAX(fi.`Price Index`)           AS `Max Oils Index`,
    MIN(fi.`Price Index`)           AS `Min Oils Index`
FROM fact_food_index fi
JOIN dim_year y ON fi.year_key = y.year_key
JOIN dim_type t ON fi.type_key = t.type_key
WHERE t.type_name = 'Oils'
GROUP BY y.Year
ORDER BY y.Year;


-- A29: Meat price volatility per year
SELECT
    y.Year,
    ROUND(AVG(fi.`Price Index`),        2) AS `Avg Meat Index`,
    ROUND(STDDEV_POP(fi.`Price Index`), 2) AS `Meat StdDev`
FROM fact_food_index fi
JOIN dim_year y ON fi.year_key = y.year_key
JOIN dim_type t ON fi.type_key = t.type_key
WHERE t.type_name = 'Meat'
GROUP BY y.Year
ORDER BY y.Year;


-- A30: Price category share by decade

SELECT
    CASE
        WHEN y.Year BETWEEN 2000 AND 2009 THEN '2000s'
        WHEN y.Year BETWEEN 2010 AND 2019 THEN '2010s'
        WHEN y.Year BETWEEN 2020 AND 2029 THEN '2020s'
    END AS Decade,

    fi.`Price Category`,

    COUNT(*) AS Record_Count,

    ROUND(
        COUNT(*) * 100.0 /
        SUM(COUNT(*)) OVER (
            PARTITION BY
            CASE
                WHEN y.Year BETWEEN 2000 AND 2009 THEN '2000s'
                WHEN y.Year BETWEEN 2010 AND 2019 THEN '2010s'
                WHEN y.Year BETWEEN 2020 AND 2029 THEN '2020s'
            END
        ),
        2
    ) AS `Pct of Decade`

FROM fact_food_index fi
JOIN dim_year y
    ON fi.year_key = y.year_key

GROUP BY
    CASE
        WHEN y.Year BETWEEN 2000 AND 2009 THEN '2000s'
        WHEN y.Year BETWEEN 2010 AND 2019 THEN '2010s'
        WHEN y.Year BETWEEN 2020 AND 2029 THEN '2020s'
    END,
    fi.`Price Category`

ORDER BY
    Decade,
    fi.`Price Category`;


-- A31: How expensive was 2022 compared to the full historical average?
SELECT
    t.type_name AS Type,
    ROUND(AVG(CASE WHEN y.Year = 2022 THEN fi.`Price Index` END), 2) AS Avg_2022,
    ROUND(AVG(fi.`Price Index`), 2)                                   AS All_Period_Avg,
    ROUND(
        (AVG(CASE WHEN y.Year = 2022 THEN fi.`Price Index` END) - AVG(fi.`Price Index`))
        / NULLIF(AVG(fi.`Price Index`), 0) * 100,
    2) AS `2022_Premium_%`
FROM fact_food_index fi
JOIN dim_year y ON fi.year_key = y.year_key
JOIN dim_type t ON fi.type_key = t.type_key
GROUP BY t.type_name
ORDER BY `2022_Premium_%` DESC;


-- =============================================
-- SECTION 8: CROSS-DOMAIN ANALYSIS
-- =============================================

-- A32: Full multi-domain scorecard per country
SELECT
    c.`Country Name`,
    c.Region,
    ROUND(AVG(CASE WHEN d.Domain = 'Digital Infrastructure' THEN f.`Normalized Value` END), 2) AS `Digital Score`,
    ROUND(AVG(CASE WHEN d.Domain = 'Economic Fragility'     THEN f.`Normalized Value` END), 2) AS `Economic Score`,
    ROUND(AVG(CASE WHEN d.Domain = 'Healthcare'             THEN f.`Normalized Value` END), 2) AS `Health Score`,
    ROUND(AVG(CASE WHEN d.Domain = 'Political Stability'    THEN f.`Normalized Value` END), 2) AS `Stability Score`,
    ROUND(AVG(CASE WHEN d.Domain = 'Food Security'          THEN f.`Normalized Value` END), 2) AS `Food Score`,
    ROUND(AVG(CASE WHEN d.Domain = 'Climate & Energy'       THEN f.`Normalized Value` END), 2) AS `Energy Score`,
    ROUND(AVG(f.`Normalized Value`), 2)                                                         AS `Composite Score`
FROM fact_global_indicators f
JOIN dim_country   c ON f.country_key   = c.country_key
JOIN dim_indicator d ON f.indicator_key = d.indicator_key
GROUP BY c.`Country Name`, c.Region
ORDER BY `Digital Score` DESC;


-- A33: Countries with very low political stability (WB score below -0.5)
SELECT
    c.`Country Name`,
    c.Region,
    ROUND(AVG(f.`Value`),             2) AS `Avg Political Stability Index`,
    ROUND(AVG(f.`Normalized Value`),  2) AS `Normalized Stability Score`
FROM fact_global_indicators f
JOIN dim_country c ON f.country_key = c.country_key
WHERE f.`Indicator Code` = 'PV.EST'
GROUP BY c.`Country Name`, c.Region
HAVING AVG(f.`Value`) < -0.50
ORDER BY `Avg Political Stability Index` ASC;


-- A34: Electricity access tiers
SELECT
    c.`Country Name`,
    c.Region,
    ROUND(AVG(f.`Value`), 2) AS `Avg Electricity Access %`,
    CASE
        WHEN AVG(f.`Value`) >= 95 THEN 'Full Access (>=95%)'
        WHEN AVG(f.`Value`) >= 50 THEN 'Partial Access (50-94%)'
        ELSE 'Low Access (<50%)'
    END AS `Access Tier`
FROM fact_global_indicators f
JOIN dim_country c ON f.country_key = c.country_key
WHERE f.`Indicator Code` = 'EG.ELC.ACCS.ZS'
GROUP BY c.`Country Name`, c.Region
ORDER BY `Avg Electricity Access %` DESC;


-- A35: Does high food price today lead to more undernourishment 2 years later?
-- joining the food price table with undernourishment data shifted by 2 years

SELECT
    y_fi.Year                         AS `Year`,
    ROUND(AVG(fi.`Price Index`),  2)  AS `Avg Food Price Index`,
    ROUND(AVG(shifted.val),       2)  AS Undernourishment_2yr_Later
FROM fact_food_index fi
JOIN dim_year y_fi ON fi.year_key = y_fi.year_key
JOIN dim_type t    ON fi.type_key = t.type_key
LEFT JOIN (
    SELECT f2.`Value` AS val, y2.Year AS fact_year
    FROM fact_global_indicators f2
    JOIN dim_year y2 ON f2.year_key = y2.year_key
    WHERE f2.`Indicator Code` = 'SN.ITK.DEFC.ZS'
) shifted ON shifted.fact_year = y_fi.Year + 2
WHERE t.type_name = 'Food'
GROUP BY y_fi.Year
ORDER BY y_fi.Year;


-- =============================================
-- SECTION 9: RISK SCORE TABLE
-- =============================================

-- A36: Full risk score sheet with domain-specific scaling
-- note: different domains use different scales intentionally
-- e.g. Digital and Climate are x100, Healthcare is x10, Energy is raw kWh

SELECT
    RANK() OVER (ORDER BY `Composite Score` DESC) AS `Rank`,
    `Country`,
    Region,
    `Composite Score`,
    `Digital Score`,
    `Health Score`,
    `Energy Score (kWh)`,
    `Climate Score`,
    `Political Stability Score`,
    `Economic Fragility Score`
FROM (
    SELECT
        c.`Country Name` AS `Country`,
        c.Region,
        ROUND(AVG(f.`Normalized Value`) * 100, 2) AS `Composite Score`,
        ROUND(AVG(CASE WHEN d.Domain = 'Digital Infrastructure' THEN f.`Normalized Value` END) * 100, 2) AS `Digital Score`,
        ROUND(AVG(CASE WHEN d.Domain = 'Healthcare' THEN f.`Normalized Value` END) * 10, 2) AS `Health Score`,
        ROUND(AVG(CASE WHEN f.`Indicator Code` = 'EG.USE.ELEC.KH.PC' THEN f.`Value` END), 2) AS `Energy Score (kWh)`,
        ROUND(AVG(CASE WHEN d.Domain = 'Climate & Energy'
                       AND f.`Indicator Code` != 'EG.USE.ELEC.KH.PC'
                       THEN f.`Normalized Value` END) * 100, 2) AS `Climate Score`,
        ROUND(AVG(CASE WHEN d.Domain = 'Political Stability' THEN f.`Value` END), 2) AS `Political Stability Score`,
        ROUND(AVG(CASE WHEN d.Domain = 'Economic Fragility' THEN f.`Normalized Value` END) * 10, 2) AS `Economic Fragility Score`
    FROM fact_global_indicators f
    JOIN dim_country c
        ON f.country_key = c.country_key
    JOIN dim_indicator d
        ON f.indicator_key = d.indicator_key
    GROUP BY c.`Country Name`, c.Region
) ranked

ORDER BY `Rank`;

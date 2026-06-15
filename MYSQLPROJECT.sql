-- ============================================================
-- GLOBAL RESILIENCE PROJECT — MySQL Final Script

CREATE DATABASE IF NOT EXISTS GLOBAL_RESILIENCE;
USE GLOBAL_RESILIENCE;

-- ============================================================
-- SECTION 1: DIMENSION & FACT VIEWS
-- ============================================================

-- ------------------------------------------------------------
-- VIEW 1: vw_Dim_Country
-- ------------------------------------------------------------
CREATE OR REPLACE VIEW vw_Dim_Country AS
WITH base AS (
    SELECT DISTINCT `Country Name`, `Country Code`
    FROM (
        SELECT `Country Name`, `Country Code` FROM `fixed_broadband_subscriptions`          WHERE `Year`      NOT IN (2024,2025)
        UNION ALL
        SELECT `Country Name`, `Country Code` FROM `internet_users`                         WHERE `Year`      NOT IN (2024,2025)
        UNION ALL
        SELECT `Country Name`, `Country Code` FROM `gdp_growth`                             WHERE `Year`      NOT IN (2024,2025)
        UNION ALL
        SELECT `Country Name`, `Country Code` FROM `inflation`                              WHERE `Year`      NOT IN (2024,2025)
        UNION ALL
        SELECT `Country Name`, `Country Code` FROM `food_imports___of_merchandise_imports`  WHERE `Year`      NOT IN (2024,2025)
        UNION ALL
        SELECT `Country Name`, `Country Code` FROM `prevalence_of_undernourishment`         WHERE `Year`      NOT IN (2024,2025)
        UNION ALL
        SELECT `Country Name`, `Country Code` FROM `global_health_expenditure`              WHERE `Year`      NOT IN (2024,2025)
        UNION ALL
        SELECT `Country Name`, `Country Code` FROM `hospitals`                              WHERE `Attribute` NOT IN (2024,2025)
        UNION ALL
        SELECT `Country Name`, `Country Code` FROM `physicians`                             WHERE `Year`      NOT IN (2024,2025)
        UNION ALL
        SELECT `Country Name`, `Country Code` FROM `political_stability`                    WHERE `Year`      NOT IN (2024,2025)
        UNION ALL
        SELECT `Country Name`, `Country Code` FROM `access_to_electricity`                  WHERE `Year`      NOT IN (2024,2025)
        UNION ALL
        SELECT `Country Name`, `Country Code` FROM `clean_fuel_access`                      WHERE `Year`      NOT IN (2024,2025)
        UNION ALL
        SELECT `Country Name`, `Country Code` FROM `co2_emissions__`                        WHERE `Year`      NOT IN (2024,2025)
        UNION ALL
        SELECT `Country Name`, `Country Code` FROM `renewable_energy__`                     WHERE `Year`      NOT IN (2024,2025)
        UNION ALL
        SELECT `Country Name`, `Country Code` FROM `electricity_consumption__`              WHERE `Year`      NOT IN (2024,2025)
    ) combined
    WHERE `Country Code` IN (
        'GEO','MDA','ESP','CHE','GBR','HUN','MYS','RUS','CAN','ISL','NZL','TUR','KOR','MUS','THA',
        'JOR','KAZ','BLR','PHL','KGZ','AUS','BWA','COL','ARM','USA','CHL','LKA','MEX','IND','TUN',
        'AZE','BIH','UKR','CRI','ALB','ARE','URY','JAM','BRA','SLV','NOR','PER','AUT','BEL','CHN',
        'DEU','ISR','LVA','CZE','EST','FRA','IRL','ITA','MLT','NLD','PRT','PAK','IDN','FIN','LTU',
        'ROU','SVK','SVN','SWE','MNG','HRV','PAN','DNK','ECU','GRC','OMN','POL','SGP','BGD','BHR',
        'CYP','MAR','MKD','EGY','LUX','MOZ','BOL','KWT','ZMB','SAU','NPL','BFA','NIC','VNM','GTM',
        'KHM','RWA','PRY','TJK','TGO','ETH','SWZ','GHA','NAM','MDG','DOM','UZB'
    )
    AND `Country Name` NOT IN ('Egypt, Arab Rep.','Israel')
),
with_region AS (
    SELECT
        `Country Code`,
        `Country Name`,
        CASE
            WHEN `Country Code` IN ('MAR','TUN','MOZ','ZMB','BWA','NAM','RWA','ETH','GHA','TGO','BFA','SWZ','MDG','MUS')
                THEN 'Africa'
            WHEN `Country Code` IN ('SAU','ARE','KWT','OMN','JOR','BHR')
                THEN 'Middle East'
            WHEN `Country Code` IN ('IND','PAK','BGD','LKA','NPL')
                THEN 'South Asia'
            WHEN `Country Code` IN ('CHN','IDN','MYS','THA','VNM','KHM','PHL','SGP','KOR','MNG')
                THEN 'East Asia'
            WHEN `Country Code` IN ('KAZ','UZB','KGZ','TJK','AZE','ARM','GEO')
                THEN 'Central Asia'
            WHEN `Country Code` IN (
                'DEU','FRA','ITA','ESP','PRT','NLD','BEL','AUT','CHE','LUX','IRL','GBR','NOR','SWE',
                'FIN','DNK','ISL','POL','CZE','SVK','HUN','ROU','GRC','EST','LVA','LTU','SVN','HRV',
                'BIH','MKD','ALB','UKR','BLR','MDA','RUS','MLT','CYP','TUR'
            ) THEN 'Europe'
            WHEN `Country Code` IN ('USA','CAN','MEX')
                THEN 'North America'
            WHEN `Country Code` IN ('BRA','COL','CHL','PER','URY','PRY','BOL','ECU')
                THEN 'South America'
            WHEN `Country Code` IN ('AUS','NZL')
                THEN 'Oceania'
            WHEN `Country Code` IN ('GTM','SLV','NIC','PAN','CRI','DOM','JAM')
                THEN 'Central America & Caribbean'
            ELSE 'Other'
        END AS Region
    FROM base
)
SELECT
    ROW_NUMBER() OVER (ORDER BY `Country Code`) AS Country_Key,
    `Country Code`,
    `Country Name`,
    Region
FROM with_region;


-- ------------------------------------------------------------
-- VIEW 2: vw_Dim_Indicator
-- ------------------------------------------------------------
CREATE OR REPLACE VIEW vw_Dim_Indicator AS
SELECT
    ROW_NUMBER() OVER (ORDER BY `Indicator Code`) AS Indicator_Key,
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
    SELECT DISTINCT `Indicator Code`, `Indicator Name`
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
    ) all_indicators
) distinct_indicators;


-- ------------------------------------------------------------
-- VIEW 3: vw_Dim_Year
-- ------------------------------------------------------------
CREATE OR REPLACE VIEW vw_Dim_Year AS
WITH all_years AS (
    SELECT DISTINCT `Year` FROM (
        SELECT `Year` FROM `fixed_broadband_subscriptions`          WHERE `Year`      NOT IN (2024,2025)
        UNION ALL SELECT `Year` FROM `internet_users`               WHERE `Year`      NOT IN (2024,2025)
        UNION ALL SELECT `Year` FROM `gdp_growth`                   WHERE `Year`      NOT IN (2024,2025)
        UNION ALL SELECT `Year` FROM `inflation`                    WHERE `Year`      NOT IN (2024,2025)
        UNION ALL SELECT `Year` FROM `food_imports___of_merchandise_imports` WHERE `Year` NOT IN (2024,2025)
        UNION ALL SELECT `Year` FROM `prevalence_of_undernourishment`        WHERE `Year` NOT IN (2024,2025)
        UNION ALL SELECT `Year` FROM `global_health_expenditure`    WHERE `Year`      NOT IN (2024,2025)
        UNION ALL SELECT `Year` FROM `physicians`                   WHERE `Year`      NOT IN (2024,2025)
        UNION ALL SELECT `Year` FROM `political_stability`          WHERE `Year`      NOT IN (2024,2025)
        UNION ALL SELECT `Year` FROM `access_to_electricity`        WHERE `Year`      NOT IN (2024,2025)
        UNION ALL SELECT `Year` FROM `clean_fuel_access`            WHERE `Year`      NOT IN (2024,2025)
        UNION ALL SELECT `Year` FROM `co2_emissions__`              WHERE `Year`      NOT IN (2024,2025)
        UNION ALL SELECT `Year` FROM `electricity_consumption__`    WHERE `Year`      NOT IN (2024,2025)
        UNION ALL SELECT `Year` FROM `renewable_energy__`           WHERE `Year`      NOT IN (2024,2025)
        UNION ALL SELECT `Attribute` AS `Year` FROM `hospitals`     WHERE `Attribute` NOT IN (2024,2025)
    ) y
)
SELECT
    (ROW_NUMBER() OVER (ORDER BY `Year`) - 1) AS Year_Key,
    `Year`,
    CONCAT(CAST(FLOOR(`Year` / 10) * 10 AS CHAR), 's') AS Decade
FROM all_years;


-- ------------------------------------------------------------
-- VIEW 4: vw_Raw_Fact
-- ------------------------------------------------------------
CREATE OR REPLACE VIEW vw_Raw_Fact AS
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


-- ------------------------------------------------------------
-- VIEW 5: vw_MinMax_Per_Indicator
-- ------------------------------------------------------------
CREATE OR REPLACE VIEW vw_MinMax_Per_Indicator AS
SELECT
    f.`Indicator Code`,
    MIN(f.`Value`) AS min_val,
    MAX(f.`Value`) AS max_val
FROM vw_Raw_Fact f
JOIN vw_Dim_Country c ON f.`Country Code` = c.`Country Code`
GROUP BY f.`Indicator Code`;


-- ------------------------------------------------------------
-- VIEW 6: vw_Fact_Global_Indicators (CORE FACT TABLE)
-- Business logic: normalization + inversion for inverse indicators
-- ------------------------------------------------------------
CREATE OR REPLACE VIEW vw_Fact_Global_Indicators AS
SELECT
    f.`Country Code`,
    f.`Indicator Code`,
    f.`Year`,
    f.`Value`,
    c.Country_Key,
    c.`Country Name`,
    c.Region,
    d.Indicator_Key,
    d.Domain,
    y.Year_Key,
    y.Decade,
    mm.min_val,
    mm.max_val,
    CASE
        WHEN mm.max_val = mm.min_val THEN 0.5
        ELSE 0.01 + ((f.`Value` - mm.min_val) / (mm.max_val - mm.min_val)) * 0.99
    END AS normalized_raw,
    CASE
        WHEN f.`Indicator Code` IN (
            'FP.CPI.TOTL.ZG','NY.GDP.MKTP.KD.ZG',
            'TM.VAL.FOOD.ZS.UN','SN.ITK.DEFC.ZS','EG.USE.ELEC.KH.PC'
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
FROM vw_Raw_Fact f
JOIN vw_Dim_Country c           ON f.`Country Code`   = c.`Country Code`
JOIN vw_Dim_Indicator d         ON f.`Indicator Code` = d.`Indicator Code`
JOIN vw_Dim_Year y              ON f.`Year`           = y.`Year`
JOIN vw_MinMax_Per_Indicator mm ON f.`Indicator Code` = mm.`Indicator Code`
WHERE f.`Country Code` IN (
    'GEO','MDA','ESP','CHE','GBR','HUN','MYS','RUS','CAN','ISL','NZL','TUR','KOR','MUS','THA',
    'JOR','KAZ','BLR','PHL','KGZ','AUS','BWA','COL','ARM','USA','CHL','LKA','MEX','IND','TUN',
    'AZE','BIH','UKR','CRI','ALB','ARE','URY','JAM','BRA','SLV','NOR','PER','AUT','BEL','CHN',
    'DEU','LVA','CZE','EST','FRA','IRL','ITA','MLT','NLD','PRT','PAK','IDN','FIN','LTU',
    'ROU','SVK','SVN','SWE','MNG','HRV','PAN','DNK','ECU','GRC','OMN','POL','SGP','BGD','BHR',
    'CYP','MAR','MKD','LUX','MOZ','BOL','KWT','ZMB','SAU','NPL','BFA','NIC','VNM','GTM',
    'KHM','RWA','PRY','TJK','TGO','ETH','SWZ','GHA','NAM','MDG','DOM','UZB'
);


-- ------------------------------------------------------------
-- VIEW 7: vw_Fact_Food_Index
-- ------------------------------------------------------------
CREATE OR REPLACE VIEW vw_Fact_Food_Index AS
WITH unpivoted AS (
    SELECT
        MONTH(STR_TO_DATE(`Date`, '%Y-%m-%d')) AS Month,
        YEAR(STR_TO_DATE(`Date`, '%Y-%m-%d'))  AS Year,
        'Food'                                  AS Type,
        `Food Price Index`                      AS `Price Index`
    FROM `fao_food_price_index`
    WHERE YEAR(STR_TO_DATE(`Date`, '%Y-%m-%d')) NOT IN (2024,2025,2026)

    UNION ALL
    SELECT
        MONTH(STR_TO_DATE(`Date`, '%Y-%m-%d')),
        YEAR(STR_TO_DATE(`Date`, '%Y-%m-%d')),
        'Meat', `Meat Price Index`
    FROM `fao_food_price_index`
    WHERE YEAR(STR_TO_DATE(`Date`, '%Y-%m-%d')) NOT IN (2024,2025,2026)

    UNION ALL
    SELECT
        MONTH(STR_TO_DATE(`Date`, '%Y-%m-%d')),
        YEAR(STR_TO_DATE(`Date`, '%Y-%m-%d')),
        'Dairy', `Dairy Price Index`
    FROM `fao_food_price_index`
    WHERE YEAR(STR_TO_DATE(`Date`, '%Y-%m-%d')) NOT IN (2024,2025,2026)

    UNION ALL
    SELECT
        MONTH(STR_TO_DATE(`Date`, '%Y-%m-%d')),
        YEAR(STR_TO_DATE(`Date`, '%Y-%m-%d')),
        'Cereals', `Cereals Price Index`
    FROM `fao_food_price_index`
    WHERE YEAR(STR_TO_DATE(`Date`, '%Y-%m-%d')) NOT IN (2024,2025,2026)

    UNION ALL
    SELECT
        MONTH(STR_TO_DATE(`Date`, '%Y-%m-%d')),
        YEAR(STR_TO_DATE(`Date`, '%Y-%m-%d')),
        'Oils', `Oils Price Index`
    FROM `fao_food_price_index`
    WHERE YEAR(STR_TO_DATE(`Date`, '%Y-%m-%d')) NOT IN (2024,2025,2026)

    UNION ALL
    SELECT
        MONTH(STR_TO_DATE(`Date`, '%Y-%m-%d')),
        YEAR(STR_TO_DATE(`Date`, '%Y-%m-%d')),
        'Sugar', `Sugar Price Index`
    FROM `fao_food_price_index`
    WHERE YEAR(STR_TO_DATE(`Date`, '%Y-%m-%d')) NOT IN (2024,2025,2026)
)
SELECT
    u.Month,
    u.Year,
    u.Type,
    u.`Price Index`,
    CASE
        WHEN u.`Price Index` < 50  THEN 'Extremely Cheap'
        WHEN u.`Price Index` < 60  THEN 'Very Cheap'
        WHEN u.`Price Index` < 70  THEN 'Cheap'
        WHEN u.`Price Index` < 80  THEN 'Slightly Cheap'
        WHEN u.`Price Index` < 90  THEN 'Below Normal'
        WHEN u.`Price Index` < 100 THEN 'Near Normal'
        WHEN u.`Price Index` < 110 THEN 'Slightly Expensive'
        WHEN u.`Price Index` < 120 THEN 'Moderately Expensive'
        WHEN u.`Price Index` < 140 THEN 'Expensive'
        ELSE 'Very Expensive'
    END AS `Price Category`
FROM unpivoted u;
-- ------------------------------------------------------------

CREATE TABLE IF NOT EXISTS Dim_Type (
    Type_Key   TINYINT      NOT NULL AUTO_INCREMENT,
    Type       VARCHAR(20)  NOT NULL,
    CONSTRAINT pk_Dim_Type PRIMARY KEY (Type_Key)
);
 
-- ------------------------------------------------------------
INSERT INTO Dim_Type (Type_Key, Type) VALUES
(1, 'Food'),
(2, 'Meat'),
(3, 'Dairy'),
(4, 'Cereals'),
(5, 'Oils'),
(6, 'Sugar')
ON DUPLICATE KEY UPDATE Type = VALUES(Type);
 
SELECT * FROM Dim_Type ORDER BY Type_Key;
 

-- ============================================================
-- SECTION 2: MEASURES
-- ============================================================

SELECT AVG(`Normalized Value`) AS `Average Resilience Score` FROM vw_Fact_Global_Indicators;

SELECT AVG(`Normalized Value`) AS `Average Risk Score`
FROM vw_Fact_Global_Indicators WHERE Domain IN ('Economic Fragility','Political Stability');

SELECT AVG(`Value`) AS `Food Dependency Rate`
FROM vw_Fact_Global_Indicators WHERE `Indicator Code` = 'TM.VAL.FOOD.ZS.UN';

SELECT AVG(`Normalized Value`) AS `Food Vulnerability Score`
FROM vw_Fact_Global_Indicators WHERE Domain = 'Food Security';

SELECT MAX(country_avg) AS `Highest Survival Score`
FROM (SELECT `Country Name`, AVG(`Normalized Value`) AS country_avg FROM vw_Fact_Global_Indicators GROUP BY `Country Name`) t;

SELECT MIN(country_avg) AS `Lowest Stability Score`
FROM (SELECT `Country Name`, AVG(`Normalized Value`) AS country_avg FROM vw_Fact_Global_Indicators WHERE Domain = 'Political Stability' GROUP BY `Country Name`) t;

SELECT `Country Name` AS `Most Resilient Country`, AVG(`Normalized Value`) AS avg_resilience
FROM vw_Fact_Global_Indicators GROUP BY `Country Name` ORDER BY avg_resilience DESC LIMIT 1;

SELECT COUNT(*) AS `High Risk Countries`
FROM (SELECT `Country Name`, AVG(`Normalized Value`) AS avg_resilience FROM vw_Fact_Global_Indicators GROUP BY `Country Name` HAVING avg_resilience < 0.5) t;

SELECT COUNT(*) AS `Number of Stable Countries`
FROM (SELECT `Country Name`, AVG(`Normalized Value`) AS avg_resilience FROM vw_Fact_Global_Indicators GROUP BY `Country Name` HAVING avg_resilience >= 0.5) t;

SELECT `Country Name` AS `Most Balanced Country`, STDDEV_POP(domain_avg) AS domain_stddev
FROM (SELECT `Country Name`, Domain, AVG(`Normalized Value`) AS domain_avg FROM vw_Fact_Global_Indicators GROUP BY `Country Name`, Domain) t
GROUP BY `Country Name` ORDER BY domain_stddev ASC LIMIT 1;

SELECT `Country Name` AS `Highest Improving Country`, (recent_avg - early_avg) AS improvement
FROM (
    SELECT `Country Name`,
           AVG(CASE WHEN Decade = '2000s' THEN `Normalized Value` END) AS early_avg,
           AVG(CASE WHEN Decade = '2020s' THEN `Normalized Value` END) AS recent_avg
    FROM vw_Fact_Global_Indicators GROUP BY `Country Name`
) t WHERE early_avg IS NOT NULL AND recent_avg IS NOT NULL ORDER BY improvement DESC LIMIT 1;

SELECT `Country Name` AS `Lowest Risk Country`, AVG(`Normalized Value`) AS risk_avg
FROM vw_Fact_Global_Indicators WHERE Domain IN ('Economic Fragility','Political Stability')
GROUP BY `Country Name` ORDER BY risk_avg ASC LIMIT 1;

SELECT Domain AS `Strongest Domain`, AVG(`Normalized Value`) AS domain_avg
FROM vw_Fact_Global_Indicators GROUP BY Domain ORDER BY domain_avg DESC LIMIT 1;

SELECT Domain AS `Weakest Domain`, AVG(`Normalized Value`) AS domain_avg
FROM vw_Fact_Global_Indicators GROUP BY Domain ORDER BY domain_avg ASC LIMIT 1;

SELECT Region AS `Top Region`, AVG(`Normalized Value`) AS region_avg
FROM vw_Fact_Global_Indicators GROUP BY Region ORDER BY region_avg DESC LIMIT 1;

SELECT Region AS `Lowest Region`, AVG(`Normalized Value`) AS region_avg
FROM vw_Fact_Global_Indicators GROUP BY Region ORDER BY region_avg ASC LIMIT 1;

SELECT AVG(`Value`) AS `Undernourishment Rate`
FROM vw_Fact_Global_Indicators WHERE `Indicator Code` = 'SN.ITK.DEFC.ZS';


-- ============================================================
-- SECTION 3: KPI QUERIES
-- ============================================================

SELECT ROUND(AVG(`Normalized Value`), 4) AS `Average Resilience Score` FROM vw_Fact_Global_Indicators;

SELECT ROUND(AVG(`Normalized Value`), 4) AS `Average Risk Score`
FROM vw_Fact_Global_Indicators WHERE Domain IN ('Economic Fragility','Political Stability');

SELECT ROUND(AVG(`Value`), 4) AS `Food Dependency Rate`
FROM vw_Fact_Global_Indicators WHERE `Indicator Code` = 'TM.VAL.FOOD.ZS.UN';

SELECT ROUND(AVG(`Normalized Value`), 4) AS `Food Vulnerability Score`
FROM vw_Fact_Global_Indicators WHERE Domain = 'Food Security';

SELECT ROUND(MAX(country_avg), 4) AS `Highest Survival Score`
FROM (SELECT `Country Name`, AVG(`Normalized Value`) AS country_avg FROM vw_Fact_Global_Indicators GROUP BY `Country Name`) t;

SELECT ROUND(MIN(country_avg), 4) AS `Lowest Stability Score`
FROM (SELECT `Country Name`, AVG(`Normalized Value`) AS country_avg FROM vw_Fact_Global_Indicators WHERE Domain = 'Political Stability' GROUP BY `Country Name`) t;

SELECT `Country Name` AS `Most Resilient Country`
FROM (SELECT `Country Name`, AVG(`Normalized Value`) AS avg_score FROM vw_Fact_Global_Indicators GROUP BY `Country Name` ORDER BY avg_score DESC LIMIT 1) t;

SELECT COUNT(*) AS `High Risk Countries`
FROM (SELECT `Country Name`, AVG(`Normalized Value`) AS avg_score FROM vw_Fact_Global_Indicators GROUP BY `Country Name` HAVING avg_score < 0.5) t;

SELECT COUNT(*) AS `Number of Stable Countries`
FROM (SELECT `Country Name`, AVG(`Normalized Value`) AS avg_score FROM vw_Fact_Global_Indicators GROUP BY `Country Name` HAVING avg_score >= 0.5) t;

SELECT Domain AS `Strongest Domain`
FROM (SELECT Domain, AVG(`Normalized Value`) AS domain_avg FROM vw_Fact_Global_Indicators GROUP BY Domain ORDER BY domain_avg DESC LIMIT 1) t;

SELECT Domain AS `Weakest Domain`
FROM (SELECT Domain, AVG(`Normalized Value`) AS domain_avg FROM vw_Fact_Global_Indicators GROUP BY Domain ORDER BY domain_avg ASC LIMIT 1) t;

SELECT Region AS `Top Region`
FROM (SELECT Region, AVG(`Normalized Value`) AS region_avg FROM vw_Fact_Global_Indicators GROUP BY Region ORDER BY region_avg DESC LIMIT 1) t;

SELECT Region AS `Lowest Region`
FROM (SELECT Region, AVG(`Normalized Value`) AS region_avg FROM vw_Fact_Global_Indicators GROUP BY Region ORDER BY region_avg ASC LIMIT 1) t;

SELECT `Country Name` AS `Most Balanced Country`
FROM (
    SELECT `Country Name`, STDDEV_POP(domain_avg) AS domain_stddev
    FROM (SELECT `Country Name`, Domain, AVG(`Normalized Value`) AS domain_avg FROM vw_Fact_Global_Indicators GROUP BY `Country Name`, Domain) inner_t
    GROUP BY `Country Name` ORDER BY domain_stddev ASC LIMIT 1
) t;

SELECT `Country Name` AS `Lowest Risk Country`
FROM (SELECT `Country Name`, AVG(`Normalized Value`) AS risk_avg FROM vw_Fact_Global_Indicators WHERE Domain IN ('Economic Fragility','Political Stability') GROUP BY `Country Name` ORDER BY risk_avg ASC LIMIT 1) t;

SELECT ROUND(AVG(`Value`), 4) AS `Undernourishment Rate`
FROM vw_Fact_Global_Indicators WHERE `Indicator Code` = 'SN.ITK.DEFC.ZS';

SELECT `Country Name` AS `Highest Improving Country`
FROM (
    SELECT `Country Name`,
           AVG(CASE WHEN Decade = '2000s' THEN `Normalized Value` END) AS early_avg,
           AVG(CASE WHEN Decade = '2020s' THEN `Normalized Value` END) AS recent_avg
    FROM vw_Fact_Global_Indicators GROUP BY `Country Name`
    HAVING early_avg IS NOT NULL AND recent_avg IS NOT NULL
    ORDER BY (recent_avg - early_avg) DESC LIMIT 1
) t;


-- ============================================================
-- SECTION 4: ANALYTICAL QUERIES
-- ============================================================

-- ANALYTICAL 1: Country Resilience Ranking

SELECT
    RANK() OVER (ORDER BY `Composite Resilience Score` DESC) AS `Rank`,
    `Country Name`, Region, `Composite Resilience Score`
FROM (
    SELECT `Country Name`, Region,
           ROUND(AVG(`Normalized Value`), 4) AS `Composite Resilience Score`
    FROM vw_Fact_Global_Indicators
    GROUP BY `Country Name`, Region
) ranked
ORDER BY `Rank`;

-- ANALYTICAL 2: Domain Scores per Country
SELECT `Country Name`, Region, Domain,
       ROUND(AVG(`Normalized Value`), 6) AS `Domain Score`
FROM vw_Fact_Global_Indicators
GROUP BY `Country Name`, Region, Domain
ORDER BY `Country Name`, Domain;

-- ANALYTICAL 3: All Domain Averages (Global)
SELECT Domain, ROUND(AVG(`Normalized Value`), 4) AS `Global Domain Average`
FROM vw_Fact_Global_Indicators
GROUP BY Domain ORDER BY `Global Domain Average` DESC;

-- ANALYTICAL 4: Region x Domain Score Matrix
SELECT Region, Domain, ROUND(AVG(`Normalized Value`), 4) AS `Avg Resilience Score`
FROM vw_Fact_Global_Indicators
GROUP BY Region, Domain ORDER BY Region, Domain;

-- ANALYTICAL 5: Yearly Trend of Average Resilience
SELECT `Year`, Decade, ROUND(AVG(`Normalized Value`), 4) AS `Avg Resilience`
FROM vw_Fact_Global_Indicators
GROUP BY `Year`, Decade ORDER BY `Year`;

-- ANALYTICAL 6: Decade-Level Resilience Trend
SELECT Decade, ROUND(AVG(`Normalized Value`), 4) AS `Avg Resilience`
FROM vw_Fact_Global_Indicators
GROUP BY Decade ORDER BY Decade;

-- ANALYTICAL 7: Country Domain Score Pivot
SELECT
    `Country Name`, Region,
    ROUND(AVG(CASE WHEN Domain = 'Climate & Energy'       THEN `Normalized Value` END), 4) AS `Climate & Energy`,
    ROUND(AVG(CASE WHEN Domain = 'Digital Infrastructure' THEN `Normalized Value` END), 4) AS `Digital Infrastructure`,
    ROUND(AVG(CASE WHEN Domain = 'Economic Fragility'     THEN `Normalized Value` END), 4) AS `Economic Fragility`,
    ROUND(AVG(CASE WHEN Domain = 'Food Security'          THEN `Normalized Value` END), 4) AS `Food Security`,
    ROUND(AVG(CASE WHEN Domain = 'Healthcare'             THEN `Normalized Value` END), 4) AS Healthcare,
    ROUND(AVG(CASE WHEN Domain = 'Political Stability'    THEN `Normalized Value` END), 4) AS `Political Stability`,
    ROUND(AVG(`Normalized Value`), 4) AS `Composite Score`
FROM vw_Fact_Global_Indicators
GROUP BY `Country Name`, Region ORDER BY `Composite Score` DESC;

-- ANALYTICAL 8: High Risk Country List
SELECT `Country Name`, Region,
       ROUND(AVG(`Normalized Value`), 4) AS `Composite Score`,
       'High Risk' AS `Risk Category`
FROM vw_Fact_Global_Indicators
GROUP BY `Country Name`, Region HAVING AVG(`Normalized Value`) < 0.5
ORDER BY `Composite Score` ASC;

-- ANALYTICAL 9: Stable Countries List
SELECT `Country Name`, Region,
       ROUND(AVG(`Normalized Value`), 4) AS `Composite Score`,
       'Stable' AS `Risk Category`
FROM vw_Fact_Global_Indicators
GROUP BY `Country Name`, Region HAVING AVG(`Normalized Value`) >= 0.5
ORDER BY `Composite Score` DESC;

-- ANALYTICAL 10: Food Price Index Trend by Type
SELECT Year, Type,
       ROUND(AVG(`Price Index`), 2) AS `Avg Annual Price Index`,
       MAX(`Price Index`) AS `Max Price Index`,
       MIN(`Price Index`) AS `Min Price Index`,
       `Price Category`
FROM vw_Fact_Food_Index
GROUP BY Year, Type, `Price Category` ORDER BY Year, Type;

-- ANALYTICAL 11: Food Price Category Distribution
SELECT Type, `Price Category`,
       COUNT(*) AS `Month Count`,
       ROUND(AVG(`Price Index`), 2) AS `Avg Index`
FROM vw_Fact_Food_Index
GROUP BY Type, `Price Category` ORDER BY Type, `Avg Index`;

-- ANALYTICAL 12: Yearly Food Price Peak Detection
SELECT Type, Year AS `Peak Year`,
       ROUND(AVG(`Price Index`), 2) AS `Avg Price Index`
FROM vw_Fact_Food_Index
GROUP BY Type, Year ORDER BY Type, `Avg Price Index` DESC;

-- ANALYTICAL 13: Country Decade Improvement Score
SELECT `Country Name`, Region,
    ROUND(AVG(CASE WHEN Decade = '2000s' THEN `Normalized Value` END), 4) AS Score_2000s,
    ROUND(AVG(CASE WHEN Decade = '2010s' THEN `Normalized Value` END), 4) AS Score_2010s,
    ROUND(AVG(CASE WHEN Decade = '2020s' THEN `Normalized Value` END), 4) AS Score_2020s,
    ROUND(AVG(CASE WHEN Decade = '2020s' THEN `Normalized Value` END)
        - AVG(CASE WHEN Decade = '2000s' THEN `Normalized Value` END), 4) AS Decade_Improvement
FROM vw_Fact_Global_Indicators
GROUP BY `Country Name`, Region ORDER BY Decade_Improvement DESC;

-- ANALYTICAL 14: Raw Indicator Averages per Country
SELECT `Country Name`, Region, `Indicator Code`, Domain,
       ROUND(AVG(`Value`), 4) AS `Avg Raw Value`
FROM vw_Fact_Global_Indicators
GROUP BY `Country Name`, Region, `Indicator Code`, Domain ORDER BY `Country Name`, Domain;

-- ANALYTICAL 15: Political Stability Trend (Global Mean)
SELECT `Year`, ROUND(AVG(`Value`), 4) AS `Avg Political Stability Index`
FROM vw_Fact_Global_Indicators WHERE `Indicator Code` = 'PV.EST'
GROUP BY `Year` ORDER BY `Year`;

-- ANALYTICAL 16: Top 10 Most Resilient Countries
SELECT `Country Name`, Region, ROUND(AVG(`Normalized Value`), 4) AS `Composite Score`
FROM vw_Fact_Global_Indicators
GROUP BY `Country Name`, Region ORDER BY `Composite Score` DESC LIMIT 10;

-- ANALYTICAL 17: Bottom 10 Least Resilient Countries
SELECT `Country Name`, Region, ROUND(AVG(`Normalized Value`), 4) AS `Composite Score`
FROM vw_Fact_Global_Indicators
GROUP BY `Country Name`, Region ORDER BY `Composite Score` ASC LIMIT 10;

-- ANALYTICAL 18: Region Composite Ranking
SELECT
    RANK() OVER (ORDER BY `Region Resilience Score` DESC) AS `Rank`,
    Region, `Region Resilience Score`, `Country Count`
FROM (
    SELECT Region,
           ROUND(AVG(`Normalized Value`), 4)    AS `Region Resilience Score`,
           COUNT(DISTINCT `Country Name`)        AS `Country Count`
    FROM vw_Fact_Global_Indicators GROUP BY Region
) ranked
ORDER BY `Rank`;

-- ANALYTICAL 19: Outlier Detection per Indicator (Z-Score)
WITH stats AS (
    SELECT `Indicator Code`,
           AVG(`Value`)        AS mean_val,
           STDDEV_POP(`Value`) AS std_val
    FROM vw_Fact_Global_Indicators GROUP BY `Indicator Code`
)
SELECT f.`Country Name`, f.`Indicator Code`, f.`Year`, f.`Value`,
       ROUND((f.`Value` - s.mean_val) / NULLIF(s.std_val, 0), 4) AS Z_Score,
       CASE WHEN ABS((f.`Value` - s.mean_val) / NULLIF(s.std_val, 0)) > 3 THEN 'Outlier' ELSE 'Normal' END AS Outlier_Flag
FROM vw_Fact_Global_Indicators f
JOIN stats s ON f.`Indicator Code` = s.`Indicator Code`
WHERE ABS((f.`Value` - s.mean_val) / NULLIF(s.std_val, 0)) > 3
ORDER BY ABS((f.`Value` - s.mean_val) / NULLIF(s.std_val, 0)) DESC;

-- ANALYTICAL 20: Composite Score Segments
SELECT `Country Name`, Region,
       ROUND(AVG(`Normalized Value`), 4) AS `Composite Score`,
       CASE
           WHEN AVG(`Normalized Value`) >= 0.70 THEN 'High Resilience'
           WHEN AVG(`Normalized Value`) >= 0.55 THEN 'Medium-High'
           WHEN AVG(`Normalized Value`) >= 0.40 THEN 'Medium-Low'
           ELSE 'Low Resilience'
       END AS `Resilience Tier`
FROM vw_Fact_Global_Indicators
GROUP BY `Country Name`, Region ORDER BY `Composite Score` DESC;

-- ANALYTICAL 21: Domain Volatility (StdDev per Domain)
SELECT Domain,
       ROUND(AVG(`Normalized Value`), 4)        AS `Avg Normalized`,
       ROUND(STDDEV_POP(`Normalized Value`), 4) AS `StdDev Normalized`,
       ROUND(MAX(`Normalized Value`), 4)        AS `Max Normalized`,
       ROUND(MIN(`Normalized Value`), 4)        AS `Min Normalized`
FROM vw_Fact_Global_Indicators
GROUP BY Domain ORDER BY `StdDev Normalized` DESC;

-- ANALYTICAL 22: Food Security Double Exposure
WITH healthcare AS (
    SELECT `Country Name`, Region, AVG(`Normalized Value`) AS health_score
    FROM vw_Fact_Global_Indicators WHERE Domain = 'Healthcare'
    GROUP BY `Country Name`, Region
),
food_sec AS (
    SELECT `Country Name`, AVG(`Value`) AS undernourishment_pct
    FROM vw_Fact_Global_Indicators WHERE `Indicator Code` = 'SN.ITK.DEFC.ZS'
    GROUP BY `Country Name`
)
SELECT h.`Country Name`, h.Region,
       ROUND(h.health_score, 4)         AS `Healthcare Score`,
       ROUND(f.undernourishment_pct, 2) AS `Avg Undernourishment %`,
       CASE WHEN h.health_score < 0.4 AND f.undernourishment_pct > 10 THEN 'Double Risk' ELSE 'Single / No Risk' END AS `Exposure Type`
FROM healthcare h
JOIN food_sec f ON h.`Country Name` = f.`Country Name`
ORDER BY h.health_score ASC, f.undernourishment_pct DESC;

-- ANALYTICAL 23: Internet Growth
SELECT `Year`, ROUND(AVG(`Value`), 2) AS `Mean Internet Users %`
FROM vw_Fact_Global_Indicators WHERE `Indicator Code` = 'IT.NET.USER.ZS'
GROUP BY `Year` ORDER BY `Year`;

-- ANALYTICAL 24: GDP Shock Detection
SELECT `Year`,
       ROUND(AVG(`Value`), 4) AS `Avg GDP Growth %`,
       ROUND(MIN(`Value`), 4) AS `Min GDP Growth %`,
       ROUND(MAX(`Value`), 4) AS `Max GDP Growth %`
FROM vw_Fact_Global_Indicators WHERE `Indicator Code` = 'NY.GDP.MKTP.KD.ZG'
GROUP BY `Year` ORDER BY `Year`;

-- ANALYTICAL 25: Food Price 2022 Multi-Category Shock
SELECT Type,
    ROUND(AVG(CASE WHEN Year = 2020 THEN `Price Index` END), 2) AS Avg_2020,
    ROUND(AVG(CASE WHEN Year = 2022 THEN `Price Index` END), 2) AS Avg_2022,
    ROUND(
        (AVG(CASE WHEN Year = 2022 THEN `Price Index` END) - AVG(CASE WHEN Year = 2020 THEN `Price Index` END))
        / NULLIF(AVG(CASE WHEN Year = 2020 THEN `Price Index` END), 0) * 100, 1
    ) AS Pct_Change_vs_2020
FROM vw_Fact_Food_Index GROUP BY Type ORDER BY Pct_Change_vs_2020 DESC;


-- ============================================================
-- SECTION 6: GOVERNMENT DEBT
-- ============================================================

-- ANALYTICAL 26: Government Debt per Country
SELECT g.`Country Name`, c.Region,
       ROUND(AVG(g.`Value`), 2) AS `Avg Govt Debt % GDP`
FROM `government debt` g
JOIN vw_Dim_Country c ON g.`Country Code` = c.`Country Code`
WHERE g.`Year` NOT IN (2024,2025)
  AND g.`Country Code` IN (
    'GEO','MDA','ESP','CHE','GBR','HUN','MYS','RUS','CAN','ISL','NZL','TUR','KOR','MUS','THA',
    'JOR','KAZ','BLR','PHL','KGZ','AUS','BWA','COL','ARM','USA','CHL','LKA','MEX','IND','TUN',
    'AZE','BIH','UKR','CRI','ALB','ARE','URY','JAM','BRA','SLV','NOR','PER','AUT','BEL','CHN',
    'DEU','LVA','CZE','EST','FRA','IRL','ITA','MLT','NLD','PRT','PAK','IDN','FIN','LTU',
    'ROU','SVK','SVN','SWE','MNG','HRV','PAN','DNK','ECU','GRC','OMN','POL','SGP','BGD','BHR',
    'CYP','MAR','MKD','LUX','MOZ','BOL','KWT','ZMB','SAU','NPL','BFA','NIC','VNM','GTM',
    'KHM','RWA','PRY','TJK','TGO','ETH','SWZ','GHA','NAM','MDG','DOM','UZB'
  )
GROUP BY g.`Country Name`, c.Region ORDER BY `Avg Govt Debt % GDP` DESC;

-- ANALYTICAL 27: Government Debt Yearly Trend
SELECT g.`Year`, ROUND(AVG(g.`Value`), 2) AS `Global Avg Debt % GDP`
FROM `government debt` g
JOIN vw_Dim_Country c ON g.`Country Code` = c.`Country Code`
WHERE g.`Year` NOT IN (2024,2025)
GROUP BY g.`Year` ORDER BY g.`Year`;


-- ============================================================
-- SECTION 7: FOOD INDEX DEEP DIVES
-- ============================================================

-- ANALYTICAL 28: Oils Price History
SELECT Year,
       ROUND(AVG(`Price Index`), 2) AS `Avg Oils Index`,
       MAX(`Price Index`) AS `Max Oils Index`,
       MIN(`Price Index`) AS `Min Oils Index`
FROM vw_Fact_Food_Index WHERE Type = 'Oils'
GROUP BY Year ORDER BY Year;

-- ANALYTICAL 29: Meat Price Stability
SELECT Year,
       ROUND(AVG(`Price Index`), 2)        AS `Avg Meat Index`,
       ROUND(STDDEV_POP(`Price Index`), 2) AS `Meat StdDev`
FROM vw_Fact_Food_Index WHERE Type = 'Meat'
GROUP BY Year ORDER BY Year;

-- ANALYTICAL 30: Near Normal Category Share by Decade

SELECT
    CASE
        WHEN Year BETWEEN 2000 AND 2009 THEN '2000s'
        WHEN Year BETWEEN 2010 AND 2019 THEN '2010s'
        WHEN Year BETWEEN 2020 AND 2029 THEN '2020s'
    END AS Decade,
    `Price Category`,
    COUNT(*) AS Record_Count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (
        PARTITION BY CASE
            WHEN Year BETWEEN 2000 AND 2009 THEN '2000s'
            WHEN Year BETWEEN 2010 AND 2019 THEN '2010s'
            WHEN Year BETWEEN 2020 AND 2029 THEN '2020s'
        END
    ), 1) AS `Pct of Decade`
FROM vw_Fact_Food_Index
GROUP BY Decade, `Price Category`
ORDER BY Decade, `Price Category`;

-- ANALYTICAL 31: 2022 vs All-Time Average
SELECT Type,
    ROUND(AVG(CASE WHEN Year = 2022 THEN `Price Index` END), 2) AS Avg_2022,
    ROUND(AVG(`Price Index`), 2) AS All_Period_Avg,
    ROUND(
        (AVG(CASE WHEN Year = 2022 THEN `Price Index` END) - AVG(`Price Index`))
        / NULLIF(AVG(`Price Index`), 0) * 100, 1
    ) AS `2022_Premium_%`
FROM vw_Fact_Food_Index GROUP BY Type ORDER BY `2022_Premium_%` DESC;


-- ============================================================
-- SECTION 8: CROSS-DOMAIN CORRELATION PROXIES
-- ============================================================

-- ANALYTICAL 32: Digital vs Economic Resilience per Country
SELECT `Country Name`, Region,
    ROUND(AVG(CASE WHEN Domain = 'Digital Infrastructure' THEN `Normalized Value` END), 4) AS `Digital Score`,
    ROUND(AVG(CASE WHEN Domain = 'Economic Fragility'     THEN `Normalized Value` END), 4) AS `Economic Score`,
    ROUND(AVG(CASE WHEN Domain = 'Healthcare'             THEN `Normalized Value` END), 4) AS `Health Score`,
    ROUND(AVG(CASE WHEN Domain = 'Political Stability'    THEN `Normalized Value` END), 4) AS `Stability Score`,
    ROUND(AVG(CASE WHEN Domain = 'Food Security'          THEN `Normalized Value` END), 4) AS `Food Score`,
    ROUND(AVG(CASE WHEN Domain = 'Climate & Energy'       THEN `Normalized Value` END), 4) AS `Energy Score`,
    ROUND(AVG(`Normalized Value`), 4) AS `Composite Score`
FROM vw_Fact_Global_Indicators
GROUP BY `Country Name`, Region ORDER BY `Digital Score` DESC;

-- ANALYTICAL 33: Countries Where Political Stability < -0.5
SELECT `Country Name`, Region,
       ROUND(AVG(`Value`), 4)            AS `Avg Political Stability Index`,
       ROUND(AVG(`Normalized Value`), 4) AS `Normalized Stability Score`
FROM vw_Fact_Global_Indicators WHERE `Indicator Code` = 'PV.EST'
GROUP BY `Country Name`, Region HAVING AVG(`Value`) < -0.50
ORDER BY `Avg Political Stability Index` ASC;

-- ANALYTICAL 34: Electricity Access Bimodal Distribution
SELECT `Country Name`, Region,
       ROUND(AVG(`Value`), 2) AS `Avg Electricity Access %`,
       CASE
           WHEN AVG(`Value`) >= 95 THEN 'Full Access (>=95%)'
           WHEN AVG(`Value`) >= 50 THEN 'Partial Access (50-94%)'
           ELSE 'Low Access (<50%)'
       END AS `Access Tier`
FROM vw_Fact_Global_Indicators WHERE `Indicator Code` = 'EG.ELC.ACCS.ZS'
GROUP BY `Country Name`, Region ORDER BY `Avg Electricity Access %` DESC;

-- ANALYTICAL 35: Food Price -> Undernourishment Lag Analysis
SELECT fi.Year AS `Year`,
       ROUND(AVG(fi.`Price Index`), 2) AS `Avg Food Price Index`,
       ROUND(
           (SELECT AVG(f2.`Value`) FROM vw_Fact_Global_Indicators f2
            WHERE f2.`Indicator Code` = 'SN.ITK.DEFC.ZS' AND f2.`Year` = fi.Year + 2)
       , 2) AS Undernourishment_2yr_Later
FROM vw_Fact_Food_Index fi WHERE fi.Type = 'Food'
GROUP BY fi.Year ORDER BY fi.Year;


-- ============================================================
-- SECTION 9: RISK SCORE TABLE
-- ============================================================

-- ANALYTICAL 36: Full Risk Sheet Reproduction
--      All 6 domain scores, scaling factors fully preserved
SELECT
    RANK() OVER (ORDER BY `Composite Score` DESC) AS `Rank`,
    `Country`, Region, `Composite Score`,
    `Digital Score`, `Health Score`, `Energy Score (kWh)`,
    `Climate Score`, `Political Stability Score`, `Economic Fragility Score`
FROM (
    SELECT
        `Country Name`                                                     AS `Country`,
        Region,
        ROUND(AVG(`Normalized Value`) * 100, 1)                           AS `Composite Score`,
        ROUND(AVG(CASE WHEN Domain = 'Digital Infrastructure'
                       THEN `Normalized Value` END) * 100, 6)             AS `Digital Score`,
        ROUND(AVG(CASE WHEN Domain = 'Healthcare'
                       THEN `Normalized Value` END) * 10, 6)              AS `Health Score`,
        ROUND(AVG(CASE WHEN `Indicator Code` = 'EG.USE.ELEC.KH.PC'
                       THEN `Value` END), 6)                              AS `Energy Score (kWh)`,
        ROUND(AVG(CASE WHEN Domain = 'Climate & Energy'
                       AND `Indicator Code` != 'EG.USE.ELEC.KH.PC'
                       THEN `Normalized Value` END) * 100, 6)             AS `Climate Score`,
        ROUND(AVG(CASE WHEN Domain = 'Political Stability'
                       THEN `Value` END), 6)                              AS `Political Stability Score`,
        ROUND(AVG(CASE WHEN Domain = 'Economic Fragility'
                       THEN `Normalized Value` END) * 10, 6)              AS `Economic Fragility Score`
    FROM vw_Fact_Global_Indicators
    GROUP BY `Country Name`, Region
) ranked
ORDER BY `Rank`;

-- ============================================================
-- END OF SCRIPT
-- ============================================================
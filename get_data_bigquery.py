def get_current_data():
    #run query using Google BigQuery and get results with pandas
    querytext = """SELECT
    ActionGeo_CountryCode AS country, FIRST(ActionGeo_Lat) AS lat, FIRST(ActionGeo_Long) AS long, AVG(ABS(FLOAT(GoldsteinScale))*FLOAT(AvgTone)) AS mean_goldstein_x_tone, COUNT(GoldsteinScale) AS event_count, INTEGER(SQLDATE) AS date
    FROM
    [gdelt-bq:full.events]
    WHERE
    (ActionGeo_CountryCode IS NOT NULL AND ActionGeo_Lat IS NOT NULL AND ActionGeo_Long IS NOT NULL AND GoldsteinScale IS NOT NULL AND AvgTone IS NOT NULL AND SQLDATE IS NOT NULL)
    GROUP BY
    (date), (country)
    ORDER BY
    date ASC"""
    project_id = "dataincubator-1010"
    df = pd.io.gbq.read_gbq(querytext, project_id)
    return df

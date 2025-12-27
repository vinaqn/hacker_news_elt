WITH candidates AS (
    SELECT
        e.earthquake_id,
        g.geoname_id,
        ST_DISTANCE(
            ST_MAKEPOINT(e.longitude, e.latitude),
            ST_MAKEPOINT(g.longitude, g.latitude)
        ) AS distance_meters, --calculate distance between points
        ROW_NUMBER() OVER (
            PARTITION BY e.earthquake_id
            ORDER BY distance_meters
        ) AS rn
    FROM {{ ref('staging_earthquake') }} AS e
    INNER JOIN {{ ref('staging_countries_geocodes') }} AS g
        ON
            g.latitude BETWEEN e.latitude - 1 AND e.latitude + 1
            AND g.longitude BETWEEN e.longitude - 1 AND e.longitude + 1
)

SELECT
    c.earthquake_id,
    c.geoname_id AS nearest_geoname_id
FROM candidates AS c
WHERE c.rn = 1 --limits to the result with the shortest distance
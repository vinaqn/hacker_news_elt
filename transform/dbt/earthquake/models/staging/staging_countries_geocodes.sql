{{
  config(
    materialized='view'
  )
}}
select
    countries.geonameid as geoname_id,
    countries.name,
    countries.longitude::decimal(9, 6) as longitude,
    countries.latitude::decimal(9, 6) as latitude,
    countries.country_code,
    countries.timezone,
    split_part(countries.timezone, '/', 1) as continent
from {{ source('amazon_s3', 'allCountries') }} as countries
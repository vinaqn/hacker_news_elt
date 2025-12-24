{{
  config(
    materialized='view'
  )
}}
select
    countries.geonameid,
    countries.name,
    countries.longitude::decimal(9, 6) as longitude,
    countries.latitude::decimal(9, 6) as latitude,
    countries.country_code,
    countries.timezone,
    split_part(countries.timezone, '/', 1) as continent
from {{ source('all_countries_geocode', 'allcountries') }} as countries
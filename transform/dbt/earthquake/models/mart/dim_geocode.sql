{{
  config(
    materialized="table",
    unique_key="geonameid",
  )
}}

select
    geocode.geoname_id,
    geocode.name,
    geocode.longitude,
    geocode.latitude,
    geocode.country_code,
    geocode.timezone,
    geocode.continent
from {{ ref('staging_countries_geocodes') }} as geocode

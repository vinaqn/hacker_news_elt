{{
  config(
    materialized='view'
  )
}}
select
    countries."ALPHA-2" as country_code_alpha_2,
    countries."ALPHA-3" as country_code_alpha_3,
    countries.NAME as country_name,
    countries.REGION as country_region,
    countries."SUB-REGION" as sub_region,
    countries."INTERMEDIATE-REGION" as intermediate_region
from {{ source('all_countries_geocode', 'countries_regional_codes') }} as countries
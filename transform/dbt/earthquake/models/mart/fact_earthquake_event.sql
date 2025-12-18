{{
  config(
    materialized='table'
  )
}}

select
earthquake_id,
occurred_at,
updated_at,
magnitude,
place,
longitude,
latitude,
depth_km
from {{ref('staging_earthquake')}}
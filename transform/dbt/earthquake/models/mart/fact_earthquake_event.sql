{{
  config(
    materialized="incremental",
    unique_key="earthquake_id",
    incremental_strategy="delete+insert"
  )
}}

select
    e.earthquake_id,
    e.occurred_at,
    e.updated_at,
    e.magnitude,
    e.earthquake_place,
    e.longitude,
    e.latitude,
    e.depth_km,
    e.page_title,
    e.web_url,
    c.nearest_geoname_id
from {{ ref('staging_earthquake') }} as e
left join {{ ref('staging_candidates') }} as c
    on e.earthquake_id = c.earthquake_id
{% if is_incremental() %}
where e.updated_at > (select max(t.updated_at) from {{ this }} as t)
{% endif %}
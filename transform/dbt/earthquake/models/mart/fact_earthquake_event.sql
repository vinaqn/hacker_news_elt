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
    e.web_url
from {{ ref('staging_earthquake') }} as e
{% if is_incremental() %}
where e.updated_at > (select max(t.updated_at) from {{ this }} as t)
{% endif %}
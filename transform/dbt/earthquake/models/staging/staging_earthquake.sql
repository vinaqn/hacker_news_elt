{{
  config(
    materialized="incremental",
    unique_key="earthquake_id",
    incremental_strategy="delete+insert"
  )
}}

select
    e.id as earthquake_id,
    e.cursor_time::integer as cursor_time_ms,
    {{ dbt_date.from_unixtimestamp("cursor_time_ms", format="milliseconds") }}
        as updated_at,
    e.geometry:"coordinates"[0]::decimal(9, 6) as longitude,
    e.geometry:"coordinates"[1]::decimal(9, 6) as latitude,
    e.geometry:"coordinates"[2]::decimal(9, 6) as depth_km,
    e.properties:"mag"::float as magnitude,
    e.properties:"time"::integer as time_ms,
    {{ dbt_date.from_unixtimestamp("time_ms", format="milliseconds") }} as occurred_at,
    e.properties:"url" as web_url,
    e.properties:"magType" as magtype,
    e.properties:"place" as earthquake_place,
    e.properties:"title" as page_title
from {{ source('earthquake', 'earthquake') }} as e

{% if is_incremental() %}
where e.cursor_time::integer > (select max(t.cursor_time_ms) from {{ this }} as t)
{% endif %}
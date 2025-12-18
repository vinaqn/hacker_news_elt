{{
  config(
    materialized="incremental",
    unique_key="earthquake_id",
    incremental_strategy="delete+insert"
  )
}}

select
    id as earthquake_id,
    cast(cursor_time as integer) as cursor_time_ms,
    {{ dbt_date.from_unixtimestamp("cursor_time_ms", format="milliseconds") }} as updated_at,
    geometry:"coordinates"[0]::float as longitude,
    geometry:"coordinates"[1]::float as latitude,
    geometry:"coordinates"[2]::float as depth_km,
    properties:"mag"::float as magnitude,
    cast(properties:"time" as integer) as time_ms,
    {{ dbt_date.from_unixtimestamp("time_ms", format="milliseconds") }} as occurred_at,
    properties:"url" as url,
    properties:"magType" as magType,
    properties:"place" as place,
    properties:"title" as title
from {{ source('earthquake', 'earthquake') }}

{% if is_incremental() %}
where cursor_time_ms > (select max(cursor_time_ms) from {{ this }})
{% endif %}
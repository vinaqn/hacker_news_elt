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
  {{ dbt_date.from_unixtimestamp("cursor_time_ms", format="milliseconds") }} as updated
from {{ source('earthquake', 'earthquake') }}

{% if is_incremental() %}
where cursor_time > (select max(cursor_time) from {{ this }})
{% endif %}
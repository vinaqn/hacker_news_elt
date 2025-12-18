{{
    config(
        materialized="incremental",
        unique_key=["id"],
        incremental_strategy="delete+insert"
        )
}}

select
    id as "earthquake_id",
    cursor_time
    --{{dbt_date.from_unixtimestamp("cursor_time",format="milliseconds")}} as "updated"
from {{ source('earthquake', 'earthquake') }}

{% if is_incremental() %}
    where cursor_time > (select max(cursor_time) from {{ this }} )
{% endif %}

import dagster as dg
from orchestration.defs.assets.airbyte import amazon_s3_job,earthquake_api_job

amazon_s3_every_minute = dg.ScheduleDefinition(
    name="amazon_s3_every_minute",
    cron_schedule="* * * * *",
    target=amazon_s3_job,
)

earthquake_api_every_minute = dg.ScheduleDefinition(
    name="earthquake_api_every_minute",
    cron_schedule="* * * * *",
    target=earthquake_api_job,
)
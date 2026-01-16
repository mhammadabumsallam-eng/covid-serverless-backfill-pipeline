# Design Decisions - COVID Serverless Backfill Pipeline

## Why AWS Lambda?
- Serverless and lightweight for API ingestion
- Easy to run backfills on demand (date ranges)
- Scales without managing servers

## Why Parquet (instead of CSV/JSON)?
- Columnar format optimized for analytics workloads
- Smaller storage footprint than raw JSON/CSV
- Faster query performance in Athena

## Why Snappy compression?
- Good balance between compression and read performance
- Common default choice for analytics pipelines

## Why partition by `date`?
- Enables partition pruning in Athena (scan less, query faster, lower cost)
- Natural fit for time-series data and backfills
- Keeps S3 organized and supports incremental loads later

## Why Glue Crawler (instead of defining schema manually)?
- Quick way to catalog data and partitions during early iterations
- Reduces manual schema work while the dataset evolves
- Makes Athena table management simpler

## Failure handling decisions
- If the API returns no rows for a date, the pipeline skips that date and continues
- Request timeout + retries are used to reduce failures from temporary API issues

## Security / Governance notes
- Configuration is stored in Lambda environment variables (no credentials in code)
- Repo contains no sensitive data; bucket/table names are placeholders

## Future improvements
- Add EventBridge schedule for daily incremental loads
- Add CloudWatch metrics (rows written, skipped days, failures)
- Add idempotency checks (skip upload if partition already exists)
- Add a transformation layer (Glue Job) if business rules grow

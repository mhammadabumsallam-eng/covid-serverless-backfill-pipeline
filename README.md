# COVID Serverless Backfill Pipeline (Lambda → S3 → Glue → Athena)

Serverless pipeline that backfills daily COVID data from a public API, writes partitioned Parquet to Amazon S3, and makes it queryable through AWS Glue Data Catalog and Amazon Athena.

## Architecture
1) AWS Lambda pulls daily data from the API (date range supported)
2) Data is stored in S3 as Parquet with Hive-style partitions: `date=YYYY-MM-DD`
3) AWS Glue Crawler catalogs the dataset
4) Athena queries the data for analytics and reporting

## Tech Stack
- AWS Lambda
- Amazon S3
- AWS Glue Crawler + Data Catalog
- Amazon Athena
- Python (requests, pandas, boto3)
- Parquet (snappy)

## Partitioning
S3 layout:
`s3://<bucket>/<prefix>/date=YYYY-MM-DD/data.parquet`

## Configuration (Environment Variables)
- `BUCKET_NAME` : target S3 bucket
- `API_URL` : API endpoint
- `ISO_CODE` : country ISO code
- `PREFIX` : S3 prefix (e.g. `covid`)

## Lambda Input (event)
```json
{
  "start_date": "2021-01-01",
  "end_date": "2021-01-31"
}

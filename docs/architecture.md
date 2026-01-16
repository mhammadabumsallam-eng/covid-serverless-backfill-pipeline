# Architecture - COVID Serverless Backfill Pipeline

## Goal
Backfill daily COVID data from a public API, store it in Amazon S3 as partitioned Parquet files, and make it queryable through AWS Glue Data Catalog and Amazon Athena.

---

## High-Level Flow
1. **Trigger**
   - AWS Lambda is invoked manually or via test event
   - Input includes `start_date` and `end_date`

2. **Ingestion**
   - Lambda calls the API for each date in the range
   - API response is parsed into a Pandas DataFrame

3. **Storage**
   - Data is written as **Parquet (Snappy compression)**
   - Files are uploaded to Amazon S3

4. **Partitioning**
   - Data is stored using Hive-style partitions:
     - `s3://<bucket>/<prefix>/date=YYYY-MM-DD/data.parquet`

5. **Cataloging**
   - AWS Glue Crawler detects partitions and updates the Data Catalog table

6. **Query Layer**
   - Amazon Athena queries the dataset for reporting and analytics

---

## S3 Layout (Partition Strategy)
Partition key: `date`

Example:
- `s3://<bucket>/<prefix>/date=2021-01-01/data.parquet`
- `s3://<bucket>/<prefix>/date=2021-01-02/data.parquet`

**Why partitioning matters**
- Faster Athena queries (partition pruning)
- Cleaner organization for backfills and incremental loads
- Lower cost by scanning fewer files

---

## Lambda Input Example
```json
{
  "start_date": "2021-01-01",
  "end_date": "2021-01-31"
}


## Output
- Partitioned Parquet files written to S3 under the configured prefix
- Glue Data Catalog table updated with new partitions
- Athena-ready dataset for analytics and reporting


##  Notes / Assumptions

-The API may return empty results for some dates; those dates are skipped and the pipeline continues.
-The S3 layout follows Hive-style partitioning: prefix/date=YYYY-MM-DD/.
-Glue Crawler is expected to be configured to detect partitions under the chosen prefix.
-Parquet files are written to Lambda /tmp then uploaded to S3 (Lambda ephemeral storage).
-Environment variables (BUCKET_NAME, API_URL, ISO_CODE, PREFIX) are configured on the Lambda function.
-This repo contains no sensitive/company data; bucket/table names in docs are placeholders.




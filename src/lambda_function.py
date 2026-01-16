import requests
import json
import pandas as pd
from datetime import date, datetime, timedelta
import boto3
import os

BUCKET_NAME = os.environ["BUCKET_NAME"]
API_URL = os.environ["API_URL"]
ISO_CODE = os.environ["ISO_CODE"]
PREFIX = os.environ["PREFIX"]

s3 = boto3.client("s3")

HEADERS = {
    "Accept": "application/json"
}


def lambda_handler(event, context):

    # ---- NEW PART (date range) ----
    start_date = datetime.strptime(event.get("start_date"), "%Y-%m-%d" ).date()
    end_date = datetime.strptime(event.get("end_date"), "%Y-%m-%d" ).date()

    current_date = start_date

    while current_date <= end_date:

        run_date = current_date.strftime("%Y-%m-%d")

        PARAMS = {
            "iso": ISO_CODE,
            "date": run_date
        }
        print(run_date)
        response = requests.get(API_URL, headers=HEADERS, params=PARAMS)

        print("Status code:", response.status_code)
        print("Final URL:", response.url)

        response.raise_for_status()

        data = response.json()

        df1 = pd.DataFrame(data["data"])
        if df1.empty:
            print(f"[SKIP] No data for {run_date}")
            current_date += timedelta(days=1)
            continue


        print(f'{run_date} successfuly to data frame')

        # 👇 PARTITION AS FOLDER (IMPORTANT)
        file_path = f"/tmp/data.parquet"
        s3_key = f"covid/date={run_date}/data.parquet"

        df1.to_parquet(file_path, compression="snappy", index=False)

        s3.upload_file(
            file_path,
            BUCKET_NAME,
            s3_key
        )

        print(f"Uploaded: s3://{BUCKET_NAME}/{s3_key}")

        current_date += timedelta(days=1)

    return {
        "status": "done",
        "start": start_date.strftime("%Y-%m-%d"),
        "end": end_date.strftime("%Y-%m-%d")
    }

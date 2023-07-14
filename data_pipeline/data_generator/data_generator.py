import os
from datetime import datetime
from io import StringIO
from random import choice, randint
from uuid import uuid4

import boto3
import pandas as pd
import typer

app = typer.Typer()

current_date = datetime.now()


def generate_user_ids(min_num: int, max_num: int):
    users = randint(min_num, max_num)
    return [uuid4().hex for _ in range(users)]


@app.command()
def run_datagen(
    bucket_name: str = typer.Argument(
        ..., help="Name of the bucket that should be filled with data"
    ),
    year: int = typer.Option(current_date.year, help="Year for which generate data"),
    month: int = typer.Option(current_date.month, help="Month for which generate data"),
    day: int = typer.Option(current_date.day, help="Day for which generate data"),
    hour: int = typer.Option(
        current_date.hour - 1, help="Hour for which generate data"
    ),
    min_rows: int = typer.Option(50000, help="Min number of generated rows"),
    max_rows: int = typer.Option(100000, help="Max number of generated rows"),
):
    """
    Simple script for generating data required to solve your assignment.
    """

    bookstore_df = pd.read_csv("../data/bookstore.csv")

    s3 = boto3.client(
        "s3",
        endpoint_url=os.environ.get("S3_ENDPOINT_URL"),
        aws_access_key_id=os.environ.get("MINIO_ROOT_USER"),
        aws_secret_access_key=os.environ.get("MINIO_ROOT_PASSWORD"),
    )
    rows = randint(min_rows, max_rows)
    user_ids = generate_user_ids(rows // 10, rows // 5)
    path = f"year={year:04d}/month={month:02d}/day={day:02d}/hour={hour:02d}"
    file_num = randint(8, 12)

    typer.echo(f"Clearing path: {path}")

    response = s3.list_objects(Bucket=bucket_name, Prefix=path)
    for object in response.get("Contents", []):
        s3.delete_object(Bucket=bucket_name, Key=object["Key"])

    typer.echo(f"Removed {len(response.get('Contents', []))} objects.")

    typer.echo(f"Generating {rows} rows")

    rows_left = rows

    def get_random_row():
        book = bookstore_df.sample()
        return {
            "timestamp": datetime(
                year,
                month,
                day,
                hour,
                randint(0, 59),
                randint(0, 59),
                randint(0, 100000),
            ).isoformat(),
            "user_id": choice(user_ids),
            "ISBN-10": book["ISBN-10"].iloc[0],
        }

    for i in range(file_num):
        file_rows = (
            randint(rows_left // 8, rows_left // 4) if i + 1 < file_num else rows_left
        )
        rows_left -= file_rows

        file_path = path + f"/{i + 1:06d}.csv"
        typer.echo(f"For path {file_path} generating {file_rows} rows")
        df = pd.DataFrame([get_random_row() for _ in range(file_rows)])

        s3_path = f"s3://{bucket_name}/{file_path}"
        csv_buffer = StringIO()
        df.to_csv(csv_buffer, index=False)
        s3.put_object(Bucket=bucket_name, Body=csv_buffer.getvalue(), Key=file_path)
        typer.echo(f"Saved file: {s3_path}")

    typer.echo("Creating FULL marker file")
    s3.put_object(Bucket=bucket_name, Body=b"", Key=path + "/FULL")

    typer.echo("Success! Your data is ready.")


if __name__ == "__main__":
    app()

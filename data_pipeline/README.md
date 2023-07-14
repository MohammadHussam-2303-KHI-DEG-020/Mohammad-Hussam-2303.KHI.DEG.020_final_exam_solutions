# Data pipeline task

You are working as a data engineer for a large online bookstore.
Your boss gave you a task to prepare a report about books purchases in your store.

Files with the purchases data appear in real-time on the `MinIO` S3 bucket in proper hour-partitioned directories. Example directory structure may look like this:

```
s3://YOUR_BUCKET
└── year=2022
    └── month=12
        └── day=08
            ├── hour=01
            │   ├── 000001.csv
            │   ├── 000002.csv
            │   ├── 000003.csv
            │   └── FULL
            ├── hour=02
            │   ├── 000001.csv
            │   └── FULL
            └── hour=03
```

An empty file named `FULL` indicates that the given hour-partition is complete and ready for further processing.

There is a Postgres database with the books details available as well. Both data sources can be joined on `ISBN-10`.

Prepare a pipeline which:
* Runs hourly.
* Downloads files from the bucket and put them in some database (you can create a new table in the already existing database).
* Calculates:
    * (number of sold books, sum of sale values) grouped by `Format`, `Language`,
    * percentage of users who purchesed books in Spanish.

Together with the task there is a python script provided (**do not edit it**). If you run the script, it will generate example data for you.
To run the script, send data to `MinIO` and have the database running you need to do following:
* set `MINIO_ROOT_USER`, `MINIO_ROOT_PASSWORD`, `S3_ENDPOINT_URL` and `POSTGRES_PASSWORD` environment variables,
* deploy the `MinIO` and `Postgres` instances using `docker-compose` (see `docker-compose.yml` file),
* create virtual environment and activate it,
* install packages listed in `data_generator/requirements.txt`,
* run `python3 data_generator/data_generator.py --help` to see available options.

Hints:
* To set environment variables, you can run `export VARIABLE_NAME=variable_value`.
* `sqlalchemy` is a recommended tool for accessing the database from python.

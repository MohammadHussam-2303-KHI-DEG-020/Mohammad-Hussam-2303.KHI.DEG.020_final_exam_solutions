# Kafka-Pyspark task
**For the environment see the Hints section of this document.**

In the `exam_data_preparation.ipynb` file you're given a script that loads data about landslides from files stored in the `data` directory and sends it to two Kafka topics in a batch mode: `landslides_topic` and `countries_topic`.

The data in `landslides_topic` is nested and a sample message has the following shape:
```json
{
    'id': '7541',
    'distance': 1.78429,
    'landslide_size': 'Small',
    'injuries': 0.0,
    'fatalities': 0.0,
    'location_columns': 
        {
            'country_code': 'US',
            'state/province': 'Vermont',
            'city/town': 'Windsor',
            'population': 2066,
            'latitude': 43.4771,
            'longitude': -72.4066
        },
    'time_columns':
        {
            'date': '3/2/16',
            'time': '8:00'
        }
}
```

The sample message in `countries_topic` has following shape:
```json
{
    'country_name': 'Guatemala',
    'country_code': 'GT'
}
```

Your task is to write a notebook with PySpark code that will:
* Provide a schema to read the data from Kafka and allow to operate on the nested columns using PySpark API.
* Denest the data structure from `landslides_topic` so it is flat (all columns on the same level).
* Ensure there are no duplicate rows.
* Ensure that `date`, `state/province`, `city/town`, `distance`, `longitude`, `latitude` and `landslide_size` columns are not null.
* Delete the `time` column.
* Fix the types for `id`, `injuries`, `fatalities` and `date`.
* Replace `NaN` values with `0` in `injuries` and `fatalities` columns.
* Normalize values in `landslide_size` column. I.e. there are e.g. both `small` and `Small` values in this column – one of these should be converted to be the same as the other.
* Join landslides data with countries names data to add `country_name` column.
* Write data as json (a textfile with multiple json lines) locally using `DataFrameWriter`.

Requirements:
* You **can't** (and don't need to) edit `exam_data_preparation.ipynb` file.
* You **can** create any other files you find useful.
* In the submission include the whole working solution – after downloading your solution we should be able to run it in JupyterLab.

Hints:
* Run Kafka cluster using `docker-compose` - see `docker-compose.yaml` file.
* Run the Jupyter Instance with the following command.
```bash
docker run \
	--network="host" \
	--user "$(id -u)" \
	--group-add users \
	--volume "${PWD}":/home/jovyan/workspace \
	jupyter/pyspark-notebook:1840ddc9dc35
```
* If you have trouble accessing the JupyterLab in the browser ensure the ports are not in use. Try running with `sudo` as well. Ultimately, switch `--network="host"` to `-p 8888:8888` (but this will require fixing communication with Kafka). You can modify `docker-compose.yml` to start Jupyter together with Kafka (as another service), then you don't need to run the command shown above.
* Ensure you add `org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.1` package to `SparkSession` to allow Kafka support.

# Architecture task

You are working for a book printing company. Their factory consists of several machines responsible for different book printing process stages and hosts workers on site. They fitted it with sensors, cameras and started collecting logs from their machines (more details below). Your Data Engineering Team is currently working together with a Data Science Team on a system which would monitor the state of the machines, suggest maintanance and predict malfunction risk.

Your task is to propose and architecture of a data pipeline and the data architecture that would make the collected data available to the Data Science team.

## Collected data

### CO<sub>2</sub> and CO levels

The factory is fitted with CO<sub>2</sub> and CO level sensors. Each sensor has its ID and is connected to the Internet. They expose an endpoint allowing user to request a measurement via HTTP GET.

### Movement information

Movement sensors are scattered around the factory. Each sensor has its ID. They send message when movement is detected via HTTP POST to an endpoint user can configure.

### Machine logs

All machines used in a book production process are advanced and have their own computers and dedicated software. While running, they produce logs which are gathered and once every hour a batch of new logs is saved in the MinIO S3 bucket on the on-premise server accessible via network.

### Industrial cameras pictures

The factory is fitted with several industrial cameras taking a picture once every 10 seconds. Each camera has its ID and is connected to the Internet. The pictures are stored in a MinIO S3 bucket on device's storage. Due to limited capacity, data older than 12 hours is deleted.

> Note: Pictures are taken by the cameras regardless of whether anything is happening within the reach of the camera.

## Requirements

Data Science Team requirements:
* Data needs to be delivered with a maximum delay of 1 hour.
* Historical data needs to be available:
  * from last 1 month for CO<sub>2</sub> and CO levels, movement information and machine logs,
  * from last 1 week for industrial cameras pictures.

Product Team requirements:
* Very high availability.
* Mitigate the risk of losing any data in case of partial system failure.
* Cost optimization.

> Hint: Not all industrial camera pictures need to be made available to the Data Science Team. As mentioned above, the pictures are taken even if nothing is happening. These can be filtered out (if you do it, you don't need to explain details of how the filtering would work).

### Non-requirements

* You don't need to design the maintanance, malfunction, ... systems. This is Data Science Team's job. You just need to define the data pipeline and the data architecture.

## Expected output of the task

The output of your tasks should be:
* Diagram of the proposed architecture – submitted as a `png` file.
* Justification of at least 3 technology choices (why this technology? which requirement made you choose it? how it helps satisfy requirements?) – submitted as a pdf file.
  * One of the justified technology choices should be the storage you choose to expose the data to the Data Science Team.

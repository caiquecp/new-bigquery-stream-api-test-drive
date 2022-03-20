# New BigQuery Stream API test drive (Python)

This is a POC to test the new BigQuery Streaming API since this is a bit confusing. The Python API looks like lacks something when compared to the Java.

I'm testing it sending batches of a small message (Customer data; obj with 3 columns) and in my local environment it's sending 500.000 messages per minute from BR to US region. You should account input IO/latency in a real world use case.

## Setup

Required environment variables:

| env | description |
| - | - |
| GOOGLE_APPLICATION_CREDENTIALS | GCP service account JSON file location |
| APP_LOG_LEVEL | Python log level (integer) |
| BQ_PROJECT_ID=playground-344612 | GCP project id |
| BQ_DATASET_ID=bq_stream_test | BigQuery dataset id |
| BQ_TABLE_ID=customer | BigQuery table id |

## Commands

| command | description |
| - | - |
| install | Install Python dependencies through pip |
| run | Run the app |
| format | Format code |
| lint | Run lint |
| build-proto | Build the proto message; requires protoc executable |
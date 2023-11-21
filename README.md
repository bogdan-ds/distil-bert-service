# NER DistilBERT Service

## Table of Contents
1. [Overview](#overview)
2. [Usage](#usage)
3. [Performance and resource usage](#performance)

## Overview
<a name="overview"></a>

The following is a service that uses the DistilBERT model to perform Named Entity Recognition (NER) on a given text.
DistilBERT was chosen as model as it has 40% less parameters than bert-base-uncased, runs 60% faster while preserving over 95% of BERT’s performances as measured on the GLUE language understanding benchmark.
The one used in this service is fine-tuned on the CoNLL-2003 NER dataset by Elastic.

The service consists of two components: API and UI. Both are based on FastAPI and are served using Uvicorn.
They are packaged in Docker containers, uploaded to Dockerhub and can be run using `docker-compose`. The current docker compose file
has a `nginx` container which acts as a reverse proxy and load balancer for the two services. The default algorithm for load 
balancing is used (Round Robin). This means that the requests are distributed evenly between services.

## Usage
<a name="usage"></a>

```bash
git clone git@github.com:bogdan-ds/distil-bert-service.git
cd distil-bert-service
docker-compose up -d
```

The UI should be reachable at `http://localhost/ui`. 

### Scaling

In order to scale the service, you can use the `--scale` option of `docker-compose`. This will create multiple instances of the service, which will be load balanced by the `nginx` container.
For production use this should be done using a container orchestration system such as Docker Swarm or Kubernetes.

```bash
docker-compose up -d --scale web=2 --scale api=2
```

### Tests

Test can be run using `pytest`. First install the requirements:

```bash
pip install -r requirements_local.txt
pytest tests
```


## Performance and resource usage
<a name="performance"></a>

### Document processing time

The following table illustrates the processing time for a single document and for multiple documents (3) using the DistilBERT model and the tokenizer.

| Run # | Single Document Processing Time (seconds) | Multiple Documents (3) Processing Time (seconds) |
|-------|------------------------------------------|--------------------------------------------------|
| 1     | 0.943748                                 | 2.493898869                                      |
| 2     | 0.684602                                 | 2.398287058                                      |
| 3     | 0.707365                                 | 2.424157143                                      |
| 4     | 0.711889                                 | 2.436190844                                      |
| 5     | 1.067672                                 | 3.942704678                                      |
| 6     | 0.912061                                 | 2.841542244                                      |
| 7     | 0.661822                                 | 2.503188133                                      |
| 8     | 0.76396                                  | 2.480777502                                      |
| 9     | 0.722751                                 | 2.469942570                                      |
| 10    | 0.715613                                 | 2.447792530                                      |


### Usage on startup

The model, once loaded, is continuously stored in memory (RAM or VRAM), consuming a fixed amount of space based on its size.

Based on my tests, the process consisting of the FastAPI server and the loaded model consumes about **700MB of RAM**. Example:
I've added the model load time to the `/metrics` endpoint as `startup_time`. The overhead of the FastAPI server is negligible.

### Observability

I've set up a metrics endpoint which shows the memory and CPU usage at any given moment. For an accurate depiction of the usage, 
this endpoint can be added to a monitoring system such as Prometheus. It can be queried continuously and the results can be plotted in a Grafana dashboard.

Endpoint: `/metrics`

Example:

```json
{
"cpu_usage_percent": 16.9,
"memory_usage_bytes": 699359232,
"startup_time": 1.972482442855835
}
```

### Memory usage during inference

During inference, additional memory is used, which can lead to an increase in total memory consumption. 
This increase is temporary and is released once the inference is complete.

As part of the response I've included two metrics: elapsed time and estimated memory use. I measure them by using a timer for the elapsed time and the `psutil` library for the memory usage.
This is an estimate, as the memory usage is measured before and after the inference, and the difference is calculated. This is not the exact memory usage, but it is a good approximation.
It varies depending on the size of the input text.

Example:

```
Estimated memory used: 35.484375 MB
Elapsed time: 2 seconds
```

## Performance improvements

- Processing can be done asynchronously, using a task queue. This would allow the server to respond immediately and process the request in the background.
- Batching is an option, but it depends on the amount of requests processed by the system. If the requests are few and far between, batching would not be a good idea.

## Optimal and minimal host requirements

The optimal host requirements depend on the amount of requests processed by the system and how many instances of the services will be run.
The minimal requirements for a single instance of the DistilBERT REST API and UI are: 2GHz and 2GB of RAM. While the model itself consumes less, 
the FastAPI and Docker add a small overhead which should be accounted for. Based on these numbers and the amount of request and replicas, 
the optimal host requirements can be calculated.
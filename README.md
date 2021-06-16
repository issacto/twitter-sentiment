# IBM stock sentiment visualisation

* Tweet API
* Kafka = data streaming 
* IBM Cloudant Database
* Flask
* Docker = container
* IBM Kubernetes (k8s) = container orchestration

### Kafka
```
cd kafka 
docker-compose up -d
```

### Producer
```
cd producer
docker build -t producer .
```

### Consumer
```
cd client
docker build -t consumer .
```

### Website
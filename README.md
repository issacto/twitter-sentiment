# IBM stock sentiment visualisation

* Tweet API
* Kafka = data streaming 
* IBM Cloudant Database
* Flask
* Docker = container
* Kuubernetes (k8s) = container orchestration

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

### Client
```
cd client
docker build -t client .
```

### Website
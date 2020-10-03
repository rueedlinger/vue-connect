# Example Kafka Connect Docker Image
This is an example Docker image for testing different connectors plugins with *vue-connect*. You 
can modify the [Docker image](Dockerfile) and install additional connectors with the
`confluent-hub` cli you would like to test.

```
RUN confluent-hub install --no-prompt jcustenborder/kafka-connect-spooldir:latest
```
#
# Example Kafka Connect Docker image for testing different connectors
#
FROM confluentinc/cp-kafka-connect-base:6.0.1

## Install connectors
RUN confluent-hub install --no-prompt confluentinc/kafka-connect-datagen:latest
RUN confluent-hub install --no-prompt confluentinc/kafka-connect-jdbc:latest
RUN confluent-hub install --no-prompt confluentinc/kafka-connect-s3:latest
RUN confluent-hub install --no-prompt confluentinc/kafka-connect-elasticsearch:latest
RUN confluent-hub install --no-prompt jcustenborder/kafka-connect-spooldir:latest
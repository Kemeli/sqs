from chalice import Chalice
import boto3
import json


ENDPOINT_URL_SEND ='http://host.docker.internal:4566'
ENDPOINT_URL_RECEIVE = "http://host.docker.internal:4566/_aws/sqs/messages"
QUEUE_URL = "http://queue.localhost.localstack.cloud:4566/000000000000"
QUEUE_NAME = 'passwords'

app = Chalice(app_name='ww')
@app.on_sqs_message(queue=QUEUE_NAME)
def on_event(event):
	for record in event['Records']:
		SQS = boto3.client("sqs", endpoint_url='http://host.docker.internal:4566')
		input_message = record.body
		output_message = input_message.upper()
		queueURL = SQS.get_queue_url(QueueName=QUEUE_NAME).get('QueueUrl')
		resp = SQS.send_message(QueueUrl=QUEUE_URL, MessageBody=output_message)
		print("We have sent a message to the SQS queue")
		print(str(resp))

# awslocal --endpoint-url=http://localhost:4566 sqs receive-message --queue-url http://queue.localhost.localstack.cloud:4566/000000000000/passwords
# awslocal --endpoint-url=http://localhost:4566 sqs send-message --queue-url http://queue.localhost.localstack.cloud:4566/000000000000/passwords --message-body "transforma"

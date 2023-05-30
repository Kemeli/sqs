from chalice import Chalice
import boto3
import json

ENDPOINT_URL_SEND ='http://host.docker.internal:4566'
ENDPOINT_URL_RECEIVE = "http://host.docker.internal:4566/_aws/sqs/messages"
QUEUE_URL = "http://queue.localhost.localstack.cloud:4566/000000000000"
QUEUE_NAME = 'passwords'

app = Chalice(app_name='ww')
app.debug = True

def verify_pass_word(password):
	if len(password) < 8:
		return False
	if not any(char.isdigit() for char in password):
		return False
	if not any(char.isupper() for char in password):
		return False
	if not any(char.islower() for char in password):
		return False
	if not any(not char.isalnum() for char in password):
		return False
	return True

@app.on_sqs_message(queue=QUEUE_NAME)
def on_event(event):
	try:
		for record in event:
			# app.log.debug("Received message with contents: %s", vars(record))
			# app.log.debug("Received message with contents wagratom: %s", record.eventSourceARN)
			SQS = boto3.client("sqs", endpoint_url='http://host.docker.internal:4566')
			input_message = record.body
			app.log.info("The message is: " + input_message)
			output_message = input_message.upper()
			queueURL = SQS.get_queue_url(QueueName=QUEUE_NAME).get('QueueUrl')
			resp = SQS.send_message(QueueUrl=queueURL, MessageBody=output_message)
	except Exception as e:
		print(str(e))

# awslocal sqs create-queue --queue-name passwords
# awslocal sqs list-queues
# awslocal sqs get-queue-url --queue-name passwords
# awslocal sqs delete-queue --queue-url http://queue.localhost.localstack.cloud:4566/000000000000/passwords
# awslocal sqs receive-message --queue-url http://queue.localhost.localstack.cloud:4566/000000000000/passwords
# awslocal sqs send-message --queue-url http://queue.localhost.localstack.cloud:4566/000000000000/passwords --message-body "transforma"



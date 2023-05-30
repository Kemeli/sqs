from chalice import Chalice
import boto3
import json

ENDPOINT_URL_SEND ='http://host.docker.internal:4566'
ENDPOINT_URL_RECEIVE = "http://host.docker.internal:4566/_aws/sqs/messages"
QUEUE_URL = "http://queue.localhost.localstack.cloud:4566/000000000000"
QUEUE_NAME = 'passwords'

app = Chalice(app_name='ww')
app.debug = True
"""
{'_event_dict': {
	'body': 'transforma',
	'receiptHandle': 'YjNlNTRkY2EtOTYyYi00MDc1LTlkNTEtNzA4ODhjNjkyZDZiIGFybjphd3M6c3FzOnVzLWVhc3QtMTowMDAwMDAwMDAwMDA6cGFzc3dvcmRzIGUwZmQxZmIyLWYyZTItNGEwYy1hMjE0LTczY2UwMzY0MjM4ZCAxNjg1NDYwMzU4LjI5Njg1MzU=',
	'md5OfBody': '6c141f9e2921dd4ec07cda05b0e96a89',
	'eventSourceARN': 'arn:aws:sqs:us-east-1:000000000000:passwords',
	'eventSource': 'aws:sqs',
	'awsRegion': 'us-east-1',
	'messageId': 'e0fd1fb2-f2e2-4a0c-a214-73ce0364238d',
	'attributes': {'SenderId': '000000000000',
	'SentTimestamp': '1685460357493',
	'ApproximateReceiveCount': '1',
	'ApproximateFirstReceiveTimestamp': '1685460358296'}, 'messageAttributes': {}}, 'context': <__main__.LambdaContext object at 0x7f444b066bb0>, 'body': 'transforma',
	'receipt_handle': 'YjNlNTRkY2EtOTYyYi00MDc1LTlkNTEtNzA4ODhjNjkyZDZiIGFybjphd3M6c3FzOnVzLWVhc3QtMTowMDAwMDAwMDAwMDA6cGFzc3dvcmRzIGUwZmQxZmIyLWYyZTItNGEwYy1hMjE0LTczY2UwMzY0MjM4ZCAxNjg1NDYwMzU4LjI5Njg1MzU='}
"""
@app.on_sqs_message(queue=QUEUE_NAME)
def on_event(event):
	try:
		for record in event:
			app.log.debug("Received message with contents: %s", vars(record))
			app.log.debug("Received message with contents wagratom: %s", record.eventSourceARN)
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



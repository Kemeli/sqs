from chalice import Chalice, Response
import boto3
import json
import os
import sys

ENDPOINT_INTERNAL ='http://host.docker.internal:4566'
QUEUE_URL = "http://queue.localhost.localstack.cloud:4566/000000000000"

S3_BUCKET = 'resource'
QUEUE_NAME = 'passwords'

s3_client = boto3.client('s3', endpoint_url=ENDPOINT_INTERNAL)
app = Chalice(app_name='ww')
app.debug = True

################################################################################
# 									Index
################################################################################
@app.route('/', methods=['GET'])
def index():
	response = s3_client.get_object(Bucket=S3_BUCKET, Key='index.html')
	page = response['Body'].read().decode('utf-8')
	headers = {'Content-Type': 'text/html'}
	return Response(body=page, status_code=200, headers=headers)

################################################################################
# 									Register
################################################################################
@app.route('/register', methods=['GET'])
def register():
	response = s3_client.get_object(Bucket=S3_BUCKET, Key='register.html')
	page = response['Body'].read().decode('utf-8')
	headers = {'Content-Type': 'text/html'}
	return Response(body=page, status_code=200, headers=headers)

################################################################################
# 									Cadastro
################################################################################

@app.route('/cadastro', methods=['POST'])
def receive_data():
	try:
		body = app.current_request.json_body
		send_message(body)
	except Exception as e:
		return (str(e))

def send_message(body):
	try:
		sqs = boto3.client('sqs', endpoint_url=ENDPOINT_INTERNAL)
		response = sqs.send_message(
			QueueUrl=f'{QUEUE_URL}/{QUEUE_NAME}',
			MessageBody=str(body)
		)
	except Exception as e:
		return (str(e))

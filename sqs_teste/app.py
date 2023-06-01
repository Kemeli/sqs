from chalice import Chalice, Response
import boto3
import json
import os
import sys

ENDPOINT_INTERNAL ='http://host.docker.internal:4566'
QUEUE_URL = "http://queue.localhost.localstack.cloud:4566/000000000000"
QUEUE_NAME = 'passwords'
TABLE_NAME = 'users'

app = Chalice(app_name='ww')
app.debug = True

################################################################################
# 									Index
################################################################################
@app.route('/', methods=['GET'])
def index():
	with open('./index.html') as f:
		content =  f.read()
	headers = {'Content-Type': 'text/html'}
	return Response(body=content, headers=headers)

################################################################################
# 									Register
################################################################################
@app.route('/register', methods=['GET'])
def register():
	with open('./register.html') as f:
		content =  f.read()
	headers = {'Content-Type': 'text/html'}
	return Response(body=content, headers=headers)

################################################################################
# 									Cadastro
################################################################################

@app.route('/cadastro', methods=['POST'])
def receive_data():
	try:
		body = app.current_request.json_body
		send_message(body)
		login = body['Login']
		return get_response(login)
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

def get_response(login):
	try:
		status = get_message_password(login)
		status = {'message': status}
		set_messege_null(login)
		app.log.debug("Message: %s", status)
		return Response(body=status, status_code=200)
	except Exception as e:
		message = {'message': 'Login ainda não consta no banco de dados, tente novamente mais tarde'}
		return Response(body=message, status_code=400)

def get_dynamodb(dynamo_name):
	app.log.info("GETTS DYNAMODB TABLE: %s", dynamo_name)
	dynamo_client = boto3.resource('dynamodb', endpoint_url=ENDPOINT_INTERNAL)
	return dynamo_client.Table(dynamo_name)

def set_messege_null(login):
	table = get_dynamodb(TABLE_NAME)
	response = table.put_item(
		Item={
			'Login': login,
			'Message': 'NULL'
			}
		)

def get_message_password(login):
	table = get_dynamodb(TABLE_NAME)
	response = table.get_item(
		Key={
			'Login': login
		}
	)
	return response['Item']['Message']

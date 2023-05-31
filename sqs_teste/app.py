from chalice import Chalice, Response
import boto3
import json
import os
import sys

# ENDPOINT_URL_RECEIVE = "http://host.docker.internal:4566/_aws/sqs/messages"
ENDPOINT_INTERNAL ='http://host.docker.internal:4566'
QUEUE_URL = "http://queue.localhost.localstack.cloud:4566/000000000000"
QUEUE_NAME = 'passwords'
TABLE_NAME = 'users'

app = Chalice(app_name='ww')
app.debug = True

"""
# Acessar informações da requisição
	http_method  | current_request.method
	headers	  | current_request.headers
	query_params | current_request.query_params
	path_params  | current_request.path_params
	body		 | current_request.json_bod
"""

################################################################################
# 									responses
################################################################################


def get_dynamodb(dynamo_name):
	app.log.info("GETTS DYNAMODB TABLE: %s", dynamo_name)
	dynamo_client = boto3.resource('dynamodb', endpoint_url=ENDPOINT_INTERNAL)
	return dynamo_client.Table(dynamo_name)

@app.route('/cadastro/{login}', methods=['GET'])
def get_response(login):
	try:
		table = get_dynamodb(TABLE_NAME)
		response = table.get_item(
			Key={
				'Login': login
			}
		)
		item = response['Item']
		app.log.debug("Item: %s", item)
		message = item['Message']
		app.log.debug("Message: %s", message)
		return message
	except Exception as e:
		app.log.error("Error in get response: %s", str(e))

def send_message(body):
	try:
		sqs = boto3.client('sqs', endpoint_url=ENDPOINT_INTERNAL)
		response = sqs.send_message(
			QueueUrl=f'{QUEUE_URL}/{QUEUE_NAME}',
			MessageBody=str(body)
		)
	except Exception as e:
		return (str(e))

@app.route('/index', methods=['GET'])
def index():
	with open('./index.html') as f:
		content =  f.read()
	headers = {'Content-Type': 'text/html'}
	return Response(body=content, headers=headers)


@app.route('/cadastro', methods=['POST'])
def receive_data():
	try:
		body = app.current_request.json_body
		send_message(body)
		return f"Seu login está sendo processado, Você pode acompanhar o status em: /cadastro/{(body['Login'])}"
	except Exception as e:
		return (str(e))

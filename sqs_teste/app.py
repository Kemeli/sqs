from chalice import Chalice, Response
import boto3
import json
import os
import sys
from time import sleep as time

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

@app.route('/cadastro/{login}', methods=['GET'])
def get_response(login):
	try:
		status = get_message_password(login)
		set_messege_null(login)
		app.log.debug("Message: %s", status)
		return {'message': status}
	except Exception as e:
		return {'message': str(e)}

def send_message(body):
	try:
		sqs = boto3.client('sqs', endpoint_url=ENDPOINT_INTERNAL)
		response = sqs.send_message(
			QueueUrl=f'{QUEUE_URL}/{QUEUE_NAME}',
			MessageBody=str(body)
		)
	except Exception as e:
		return (str(e))

@app.route('/register', methods=['GET'])
def register():
	with open('./register.html') as f:
		content =  f.read()
	headers = {'Content-Type': 'text/html'}
	return Response(body=content, headers=headers)

@app.route('/', methods=['GET'])
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
		response = {
			'message': f"Seu login está sendo processado. Você pode acompanhar o status em: /cadastro/{body['Login']}"
		}
		redirect_url = f"cadastro/{body['Login']}"
		headers = {'Location': redirect_url}
		return Response(body=response, status_code=302, headers=headers)
	except Exception as e:
		return (str(e))


@app.route('/fluxograma.png/', methods=['GET'])

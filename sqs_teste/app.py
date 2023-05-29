from chalice import Chalice
import boto3
import json

ENDPOINT_URL_SEND ='http://host.docker.internal:4566'
ENDPOINT_URL_RECEIVE = "http://host.docker.internal:4566/_aws/sqs/messages"
QUEUE_URL = "http://queue.localhost.localstack.cloud:4566/000000000000"
QUEUE_NAME = 'passwords'

app = Chalice(app_name='ww')

@app.lambda_function()
def receive_message_sqs(event, context):
	SQS = boto3.client("sqs", endpoint_url=ENDPOINT_URL_RECEIVE)
	response = SQS.receive_message(QueueUrl=f"{QUEUE_URL}/{QUEUE_NAME}")
	if 'Messages' in response:
		body = response['Messages'][0]['Body']
		return  body
	else:
		return {'body': 'No messages found'}

# @app.lambda_function()
# def send_message(event, context):
# 	sqs = boto3.client('sqs', endpoint_url=ENDPOINT_URL_SEND)
# 	response = sqs.send_message(
# 		QueueUrl=f'{QUEUE_URL}/{QUEUE_NAME}',
# 		MessageBody='Hello World2!'
# 	)
# 	return "Success"

"""
# Acessar informações da requisição
	http_method  | current_request.method
	headers	  | current_request.headers
	query_params | current_request.query_params
	path_params  | current_request.path_params
	body		 | current_request.json_bod
"""

# envia para a fila sqs
def send_message(password):
	try:
		sqs = boto3.client('sqs', endpoint_url=ENDPOINT_URL_SEND)
		response = sqs.send_message(
			QueueUrl=f'{QUEUE_URL}/{QUEUE_NAME}',
			MessageBody=str(password)
		)
		return "Seu login está sendo processado, aguarde..."
	except Exception as e:
		return (str(e))

@app.route('/cadastro', methods=['POST'])
def receive_data():
	try:
		paraments = app.current_request.json_body
		name = paraments['Name']
		password = paraments['PassWord']
		return send_message(password)
	except Exception as e:
		return (str(e))


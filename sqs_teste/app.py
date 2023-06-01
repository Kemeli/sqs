from chalice import Chalice, Response
import boto3
import json

ENDPOINT_URL_SEND = 'http://host.docker.internal:4566'
QUEUE_URL = 'http://queue.localhost.localstack.cloud:4566/000000000000'
QUEUE_NAME = 'passwords'

app = Chalice(app_name='ww')
app.debug = True

@app.route('/')
def index():
	with open('index.html', 'r') as file:
		return Response(
			body=file.read(),
			headers={'Content-Type': 'text/html'}
		)

@app.route('/cadastro', methods=['POST'], content_types=['application/json'])
def receive_data():
	app.log.debug("entrei no receive_data")
	try:
		data = app.current_request.json_body
		password = data['PassWord']

		response = send_message_to_queue(password)
		return response
	except Exception as e:
		return str(e)

def send_message_to_queue(password):
	try:
		sqs = boto3.client('sqs', endpoint_url=ENDPOINT_URL_SEND)
		response = sqs.send_message(
			QueueUrl=f'{QUEUE_URL}/{QUEUE_NAME}',
			MessageBody=json.dumps({"password": password})
		)
		return Response(
			body=json.dumps({"message": "Seu login está sendo processado, aguarde..."}),
			headers={'Content-Type': 'application/json'}
		)
	except Exception as e:
		return Response(
			body=json.dumps({"error": str(e)}),
			status_code=500,
			headers={'Content-Type': 'application/json'}
		)





def get_password_SQS(event):
	for record in event:
		SQS = boto3.client("sqs", endpoint_url=ENDPOINT_URL_SEND)
		password = record.body
		return password

@app.on_sqs_message(queue=QUEUE_NAME)
def on_event(event):
	try:
		for record in event:
			password = get_password_SQS(event)
			app.log.debug("look, a Password: %s", password)
	except Exception as e:
		print(str(e))











# from chalice import Chalice, Response
# import boto3
# import json

# ENDPOINT_URL_SEND ='http://host.docker.internal:4566'
# ENDPOINT_URL_RECEIVE = "http://host.docker.internal:4566/_aws/sqs/messages"
# QUEUE_URL = "http://queue.localhost.localstack.cloud:4566/000000000000"
# QUEUE_NAME = 'passwords'

# app = Chalice(app_name='ww')
# app.debug = True

# @app.route('/')
# def index():
# 	with open('index.html', 'r') as file:
# 		return Response(
# 			body=file.read(),
# 			headers={'Content-Type': 'text/html'}
# 		)

# @app.route('/cadastro', methods=['POST'], content_types=['application/x-www-form-urlencoded'])
# def receive_data():
# 	app.log.debug("entrei no receive_data")
# 	try:
# 		parameters = app.current_request.raw_body.decode('utf-8')
# 		password = parse_parameters(parameters)['password']

# 		response = send_message_to_queue(password)
# 		return response
# 	except Exception as e:
# 		return str(e)

# def parse_parameters(parameters):
# 	result = {}
# 	pairs = parameters.split('&')
# 	for pair in pairs:
# 		key, value = pair.split('=')
# 		result[key] = value
# 	return result

# def send_message_to_queue(password):
# 	app.log.debug("entrei")
# 	sqs = boto3.client('sqs', endpoint_url=ENDPOINT_URL_SEND)
# 	response = sqs.send_message(
# 		QueueUrl=f'{QUEUE_URL}/{QUEUE_NAME}',
# 		MessageBody=str(password)
# 	)
# 	app.log.debug("passei do send_message")
# 	return Response(
# 		body="Seu login está sendo processado, aguarde...",
# 		headers={'Content-Type': 'text/plain'}
# 	)










# from chalice import Chalice
# import boto3
# import json

# ENDPOINT_URL_SEND ='http://host.docker.internal:4566'
# ENDPOINT_URL_RECEIVE = "http://host.docker.internal:4566/_aws/sqs/messages"
# QUEUE_URL = "http://queue.localhost.localstack.cloud:4566/000000000000"
# QUEUE_NAME = 'passwords'

# # sns_client = boto3.client('sns', endpoint_url=ENDPOINT_URL_SEND)
# # sns_topic_arn = 'arn:aws:sns:us-east-1:000000000000:topico-senha-sns'

# app = Chalice(app_name='ww')
# app.debug = True

# def check_pass_word(password):
# 	if len(password) < 8:
# 		return False
# 	if not any(char.isdigit() for char in password):
# 		return False
# 	if not any(char.isupper() for char in password):
# 		return False
# 	if not any(char.islower() for char in password):
# 		return False
# 	if not any(not char.isalnum() for char in password):
# 		return False
# 	return True

# def get_password_SQS(event):
# 	for record in event:
# 		SQS = boto3.client("sqs", endpoint_url=ENDPOINT_URL_SEND)
# 		password = record.body
# 		return password

# @app.on_sqs_message(queue=QUEUE_NAME)
# def on_event(event):
# 	app.log.debug("entrei")
# 	try:
# 		for record in event:
# 			password = get_password_SQS(event)
# 			app.log.debug("Password: %s", password)
# 			if check_pass_word(password):
# 				app.log.debug("Password Valida")
# 				resposta = {
# 					'message': 'Senha válida. Seu cadastro foi concluído com sucesso.'
# 				}
# 				response = requests.put(f"{ENDPOINT_URL_SEND}{'/cadastro/responde'}", json=resposta)
# 				app.log.debug("Resposta enviada para o usuário. Status code: %s", response.status_code)
# 				return {'message': 'Resposta enviada com sucesso'}
# 			else:
# 				app.log.debug("Senha errada rapa")
# 	except Exception as e:
# 		print(str(e))

# @app.route('/')
# def index():
# 	with open('index.html', 'r') as file:
# 		return Response(
# 			body=file.read(),
# 			headers={'Content-Type': 'text/html'}
# 		)

# # envia para a fila sqs
# def send_message(password):
# 	try:
# 		sqs = boto3.client('sqs', endpoint_url=ENDPOINT_URL_SEND)
# 		response = sqs.send_message(
# 			QueueUrl=f'{QUEUE_URL}/{QUEUE_NAME}',
# 			MessageBody=str(password)
# 		)
# 		return "Seu login está sendo processado, aguarde..."
# 	except Exception as e:
# 		return (str(e))

# @app.route('/cadastro', methods=['POST'])
# def receive_data():
# 	try:
# 		paraments = app.current_request.json_body
# 		name = paraments['Name']
# 		password = paraments['PassWord']
# 		return send_message(password)
# 	except Exception as e:
# 		return (str(e))










			# sns_client.publish(
				# 	TopicArn=sns_topic_arn,
				# 	Message=json.dumps(resposta)
				# )

# @app.lambda_function()
# def receive_message_sqs():
# 	SQS = boto3.client("sqs", endpoint_url=ENDPOINT_URL_RECEIVE)
# 	response = SQS.receive_message(QueueUrl=f"{QUEUE_URL}/{QUEUE_NAME}")
# 	if 'Messages' in response:
# 		body = response['Messages'][0]['Body']
# 		return  body
# 	else:
# 		return {'body': 'No messages found'}

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

# @app.on_sqs_message(queue=QUEUE_NAME)
# def on_event(event):
# 	for record in event['Records']:
# 		SQS = boto3.client("sqs", endpoint_url='http://host.docker.internal:4566')
# 		input_message = record.body
# 		output_message = input_message.upper()
# 		return (receive_message_sqs(output_message))

# @app.on_sqs_message(queue=QUEUE_NAME)
# def on_event(event):
# 	url = get_deployed_app_url()
# 	if not url:
# 		print("ERROR: Deployed app URL not found.")
# 		return
# 	for record in event['Records']:
# 		SQS = boto3.client("sqs", endpoint_url='http://host.docker.internal:4566')
# 		input_message = record.body
# 		output_message = input_message.upper()
# 		response = requests.post(url, json={'message': output_message})
# 		return (receive_message_sqs())
# 		# return ("message's been processed")

# def modify_deployed_app_url(deployed_url):
# 	modified_url = deployed_url.replace('.execute-api.', '.execute-api.localhost.localstack.cloud:4566.')
# 	return modified_url

# def get_deployed_app_url():
# 	file_path = os.path.join('.chalice', 'deployed', 'dev.json')
# 	try:
# 		with open(file_path, 'r') as f:
# 			data = json.load(f)
# 			resources = data.get('resources', [])
# 			for resource in resources:
# 				if resource.get('name') == 'rest_api':
# 					deployed_url = resource.get('rest_api_url')
# 				if deployed_url:
# 					modified_url = modify_deployed_app_url(deployed_url)
# 					return modified_url
# 	except FileNotFoundError:
# 		print("ERROR: dev.json file not found.")
# 	except (json.JSONDecodeError, KeyError):
# 		print("ERROR: Invalid dev.json file format.")
# 	return None



# pra mandar a texto de volta pro postaman precisaria de um endpoint que recebesse a mensagem e retornasse pro postman
# mas esse endpoint só é gerado depois que o chalice é deployado, então não tem como fazer isso

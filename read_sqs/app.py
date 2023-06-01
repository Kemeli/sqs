from chalice import Chalice
import boto3
import json

ENDPOINT_URL_SEND ='http://host.docker.internal:4566'
ENDPOINT_URL_RECEIVE = "http://host.docker.internal:4566/_aws/sqs/messages"
QUEUE_URL = "http://queue.localhost.localstack.cloud:4566/000000000000"
QUEUE_NAME = 'passwords'

sns_client = boto3.client('sns', endpoint_url=ENDPOINT_URL_SEND)
sns_topic_arn = 'arn:aws:sns:us-east-1:000000000000:topico-senha-sns'

app = Chalice(app_name='ww')
app.debug = True

def check_pass_word(password):
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

def get_password_SQS(event):
	for record in event:
		SQS = boto3.client("sqs", endpoint_url=ENDPOINT_URL_SEND)
		password = record.body
		return password

# @app.on_sqs_message(queue=QUEUE_NAME)
# def on_event(event):
# 	try:
# 		for record in event:
# 			password = get_password_SQS(event)
# 			app.log.debug("Password: %s", password)
# 			if check_pass_word(password):
# 				# app.log.debug("Password Valida")
# 				resposta = {
# 					'message': 'Senha válida. Seu cadastro foi concluído com sucesso.'
# 				}
# 				sns_client.publish(
# 					TopicArn=sns_topic_arn,
# 					Message=json.dumps(resposta)
# 				)
# 				app.log.debug("Resposta enviada para o usuário. Status code: %s", response.status_code)
# 				return {'message': 'Resposta enviada com sucesso'}
# 			else:
# 				app.log.debug("Senha errada rapa")
# 	except Exception as e:
# 		print(str(e))

# app.log.debug("Received message with contents: %s", vars(record))
# app.log.debug("Received message with contents wagratom: %s", record.eventSourceARN)

# awslocal sqs create-queue --queue-name passwords
# awslocal sqs list-queues
# awslocal sqs get-queue-url --queue-name passwords
# awslocal sqs delete-queue --queue-url http://queue.localhost.localstack.cloud:4566/000000000000/passwords
# awslocal sqs receive-message --queue-url http://queue.localhost.localstack.cloud:4566/000000000000/passwords
# awslocal sqs send-message --queue-url http://queue.localhost.localstack.cloud:4566/000000000000/passwords --message-body "transforma"


# export LOCALSTACK_HOSTNAME=localhost
# awslocal sns create-topic --name topico-senha-sns


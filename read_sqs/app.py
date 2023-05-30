from chalice import Chalice
import boto3
import json

ENDPOINT_INTERNAL ='http://host.docker.internal:4566'
ENDPOINT_MSG_SQS = "http://host.docker.internal:4566/_aws/sqs/messages"
ENDPOINT_QUEUE = "http://queue.localhost.localstack.cloud:4566/000000000000"
QUEUE_NAME = 'passwords'
TABLE_NAME = 'users'

app = Chalice(app_name='ww')
app.debug = True

################################################################################
# 									getts
################################################################################


def get_data_SQS(body):
	app.log.info("GETTS PASSWORD FROM SQS")
	app.log.debug("Body: %s", body)

	return body['Login'], body['Senha'],

def get_dynamodb(dynamo_name):
	app.log.info("GETTS DYNAMODB TABLE: %s", dynamo_name)
	dynamo_client = boto3.resource('dynamodb', endpoint_url=ENDPOINT_INTERNAL)
	return dynamo_client.Table(dynamo_name)

def saving_user_in_db(body):
	table = get_dynamodb(TABLE_NAME)

	app.log.info("Saving Item in DynamoDB")
	app.log.debug("Item: %s", body)

	login, password = get_data_SQS(body)
	response = table.put_item(
		Item={
			'Login': login,
			'Senha': password
			}
		)
	app.log.info("Success in create user")

def check_valid_password(password):
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
			body_json = json.loads(record.body)
			login, password = get_data_SQS(body_json)
			if check_valid_password(password):
				saving_user_in_db(body_json)
			else:
				app.log.debug("Senha errada rapa")
	except Exception as e:
		app.log.debug(str(e))

# app.log.debug("Received message with contents: %s", vars(record))
# app.log.debug("Received message with contents wagratom: %s", record.eventSourceARN)

# awslocal sqs create-queue --queue-name passwords
# awslocal sqs list-queues
# awslocal sqs get-queue-url --queue-name passwords
# awslocal sqs delete-queue --queue-url http://queue.localhost.localstack.cloud:4566/000000000000/passwords
# awslocal sqs receive-message --queue-url http://queue.localhost.localstack.cloud:4566/000000000000/passwords
# awslocal sqs send-message --queue-url http://queue.localhost.localstack.cloud:4566/000000000000/passwords --message-body "transforma"


#awslocal dynamodb delete-table --table-name users

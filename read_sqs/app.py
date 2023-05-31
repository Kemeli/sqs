from chalice import Chalice
import boto3
import json

ENDPOINT_INTERNAL ='http://host.docker.internal:4566'
ENDPOINT_MSG_SQS = "http://host.docker.internal:4566/_aws/sqs/messages"
ENDPOINT_QUEUE = "http://queue.localhost.localstack.cloud:4566/000000000000"
QUEUE_NAME = 'passwords'
RESPONSE_NAME = 'responses'
TABLE_NAME = 'users'

app = Chalice(app_name='ww')
app.debug = True

################################################################################
# 									getts
################################################################################

def get_data_SQS(body):
	app.log.debug("Body: %s", body)
	body_json = body.replace("'", '"')
	body_json = json.loads(body_json)
	return body_json['Login'], body_json['Senha']

def get_dynamodb(dynamo_name):
	app.log.info("GETTS DYNAMODB TABLE: %s", dynamo_name)
	dynamo_client = boto3.resource('dynamodb', endpoint_url=ENDPOINT_INTERNAL)
	return dynamo_client.Table(dynamo_name)

def saving_user_in_db(login, message):
	app.log.info("Saving Item in DynamoDB")

	table = get_dynamodb(TABLE_NAME)
	response = table.put_item(
		Item={
			'Login': login,
			'Message': message
			}
		)
	app.log.info("Success in create user")

def get_status_messege(password):
	app.log.info("CHECKING PASSWORD")
	if len(password) < 8:
		return False, 'Password must have at least 8 characters'
	if not any(char.isdigit() for char in password):
		return False, 'Password must have at least 1 digit'
	if not any(char.isupper() for char in password):
		return False, 'Password must have at least 1 uppercase letter'
	if not any(char.islower() for char in password):
		return False, 'Password must have at least 1 lowercase letter'
	if not any(not char.isalnum() for char in password):
		return False, 'Password must have at least 1 special character'
	return True, 'Registration successful!'

@app.on_sqs_message(queue=QUEUE_NAME)
def on_event(event):
	try:
		for record in event:
			app.log.info("RECEIVED MESSAGE FROM SQS")
			login, password = get_data_SQS(record.body)
			status, message = get_status_messege(password)
			saving_user_in_db(login, message)
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

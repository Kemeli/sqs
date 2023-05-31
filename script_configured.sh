echo "Starting localstack"
localstack start -d

echo "Creating table users"
awslocal dynamodb create-table \
    --table-name users\
    --attribute-definitions AttributeName=Login,AttributeType=S \
    --key-schema AttributeName=Login,KeyType=HASH \
    --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5 \
    --region us-east-1

echo "Creating table passwords"
awslocal sqs create-queue --queue-name passwords
awslocal sqs create-queue --queue-name responses

cd ./read_sqs
chalice-local deploy

cd ../sqs_teste
chalice-local deploy && chalice-local local

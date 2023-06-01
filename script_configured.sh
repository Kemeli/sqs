echo "Starting localstack"
localstack start -d

echo "Creating table users"
awslocal dynamodb create-table \
    --table-name users\
    --attribute-definitions AttributeName=Login,AttributeType=S \
    --key-schema AttributeName=Login,KeyType=HASH \
    --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5 \
    --region us-east-1

echo "Creating SQS passwords"
awslocal sqs create-queue --queue-name passwords

echo "Subindo lambdas read"
cd ./read_sqs
chalice-local deploy

echo "Subindo lambdas write"
cd ../sqs_teste
chalice-local deploy

awslocal s3api create-bucket --bucket resource
awslocal s3 cp ./vendor/fluxograma.png s3://resource/fluxograma.png

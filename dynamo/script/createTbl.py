import boto3

dynamodb = boto3.resource(
    'dynamodb',
    aws_access_key_id='fake',
    aws_secret_access_key='fake',
    region_name='us-west-2',
    endpoint_url="http://dynamodb:8000"
)

table = dynamodb.create_table(
    TableName = 'recinfo',
    KeySchema = [{'AttributeName': 'key', 'KeyType': 'HASH'}],
    AttributeDefinitions=[{'AttributeName': 'key','AttributeType': 'S'}],
    ProvisionedThroughput={'ReadCapacityUnits': 10,'WriteCapacityUnits': 10}
)

print("Table status:", table.table_status)

for i in range(10):
    table.put_item(
        Item = {
            'key': str(i),
            'val': i**2,
        }
    )

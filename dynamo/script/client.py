import boto3

dynamodb = boto3.resource(
    'dynamodb',
    aws_access_key_id='fake',
    aws_secret_access_key='fake',
    region_name='us-west-2',
    endpoint_url="http://dynamodb:8000"
)

table=dynamodb.Table('recinfo')

response = table.get_item(
    Key = {
        'key': '1'
    }
)
print("get_item")
print(response['Item']['val'])

response = dynamodb.batch_get_item(
    RequestItems={
        'recinfo': {
            'Keys': [
                {'key': '1'},
                {'key': '2'},
                {'key': '3'},
                {'key': '4'}
            ]
        }
    }
)

print("get_batch_item")
for i in response['Responses']['recinfo']:
    print(i['key'],i['val'])

response = dynamodb.batch_get_item(
    RequestItems={
        'recinfo': {
            'Keys': [
                {'key': '1'},
                {'key': '2'},
                {'key': '3'},
                {'key': '4'}
            ]
        }
    }
)

keys=[]
for i in range(10):
    keys.append({'key': str(i)})

response = dynamodb.batch_get_item(
    RequestItems={
        'recinfo': {
            'Keys': keys
        }
    }
)

print("get_batch_item_dict_keys")
for i in response['Responses']['recinfo']:
    print(i['key'],i['val'])

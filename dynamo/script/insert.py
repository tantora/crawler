import boto3
import csv
import sys

f=[]
csv_file = open(sys.argv[1],"r")
f = csv.reader(
    csv_file, delimiter=",",
    doublequote=True,
    lineterminator="\n",
    quotechar='"',
    skipinitialspace=True
)

dynamodb = boto3.resource(
    'dynamodb',
    aws_access_key_id='fake',
    aws_secret_access_key='fake',
    region_name='us-west-2',
    endpoint_url="http://dynamodb:8000"
)
table=dynamodb.Table('recinfo')
print("Table status:", table.table_status)

for i in f:
    if len(i) == 2 :
        print(i)
        table.put_item(
            Item = {
                'key': i[0],
                'val': i[1],
            }
        )

csv_file.close()

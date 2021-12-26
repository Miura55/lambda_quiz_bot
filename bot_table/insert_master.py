import boto3

dynamodb = boto3.resource(
    'dynamodb',
    endpoint_url='http://localhost:18000',
    region_name='us-east-2',
    aws_access_key_id='ACCESS_ID',
    aws_secret_access_key='ACCESS_KEY'
)

table = dynamodb.Table('scores')

with table.batch_writer() as batch:
    batch.put_item(Item={"question_id": "q1",  "answer": "3", "score": 10})
    batch.put_item(Item={"question_id": "q2",  "answer": "1", "score": 20})
    batch.put_item(Item={"question_id": "q3",  "answer": "2", "score": 20})

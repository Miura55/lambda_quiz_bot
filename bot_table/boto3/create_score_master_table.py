import boto3

# boto3 is the AWS SDK library for Python.
# We can use the low-level client to make API calls to DynamoDB.
client = boto3.client('dynamodb',
                      endpoint_url='http://localhost:18000',
                      region_name='us-east-2',
                      aws_access_key_id='ACCESS_ID',
                      aws_secret_access_key='ACCESS_KEY'
                      )

try:
    resp = client.create_table(
        TableName="scores",
        # Declare your Primary Key in the KeySchema argument
        KeySchema=[
            {
                "AttributeName": "question_id",
                "KeyType": "HASH"
            }
        ],
        # Any attributes used in KeySchema or Indexes must be declared in AttributeDefinitions
        AttributeDefinitions=[
            {
                "AttributeName": "question_id",
                "AttributeType": "S"
            }
        ],
        # ProvisionedThroughput controls the amount of data you can read or write to DynamoDB per second.
        # You can control read and write capacity independently.
        ProvisionedThroughput={
            "ReadCapacityUnits": 1,
            "WriteCapacityUnits": 1
        }
    )
    print("Table created successfully!")
except Exception as e:
    print("Error creating table:")
    print(e)

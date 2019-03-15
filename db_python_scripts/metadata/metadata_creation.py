import boto3

dynamodb = boto3.resource("dynamodb")

table = dynamodb.create_table(
    TableName="metadata",
    KeySchema=[
        {
            "AttributeName": "name",
            "KeyType": "HASH" #Partition key
        }
    ],
    AttributeDefinitions=[
        {
            "AttributeName": "name",
            "AttributeType": "S"
        }
    ],
    ProvisionedThroughput={
        "ReadCapacityUnits":20,
        "WriteCapacityUnits":20
    }
)

table.meta.client.get_waiter("table_exists").wait(TableName="metadata")

print(table.item_count)

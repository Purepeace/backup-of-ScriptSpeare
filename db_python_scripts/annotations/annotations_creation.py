import boto3

dynamodb = boto3.resource("dynamodb")

table = dynamodb.create_table(
    TableName="annotations",
    KeySchema=[
        {
            "AttributeName": "play_name",
            "KeyType": "HASH" #Partition key
        },
        {
            "AttributeName": "line_number",
            "KeyType": "RANGE"
        }
    ],
    AttributeDefinitions=[
        {
            "AttributeName": "play_name",
            "AttributeType": "S"
        },
        {
            "AttributeName": "line_number",
            "AttributeType": "N"
        },
    ],
    ProvisionedThroughput={
        "ReadCapacityUnits":20,
        "WriteCapacityUnits":20
    }
)

table.meta.client.get_waiter("table_exists").wait(TableName="annotations")

print(table.item_count)

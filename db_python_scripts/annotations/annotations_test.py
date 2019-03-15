import boto3

dynamodb = boto3.resource("dynamodb",endpoint_url="http://localhost:8000")

table = dynamodb.Table("annotations")

table.put_item(
    Item = {
        'play_name' : 'Romeo',
        'line_number' : 1,
        'annotation' : "This is a test annotation"
    }
)



table.update_item(
    Key ={
        'play_name':'Romeo',
        'line_number': 1
    },
    UpdateExpression='SET annotation = :val1',
    ExpressionAttributeValues= {
        ':val1':'This is new test annotation'
    }
)

response = table.query{

}

items = response['Items']
print(items)

"""response = table.get_item(
    Key = {
        "play_name":'Romeo',
        'line_number' : 1
    }
)
item = response['Item']
print(item)"""

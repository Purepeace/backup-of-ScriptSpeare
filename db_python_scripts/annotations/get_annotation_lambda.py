import json
import boto3

def lambda_handler(event, context):
    # TODO implement
    dynamodb = boto3.resource("dynamodb")

    table = dynamodb.Table("annotations")

    response = table.get_item(
    Key = {
        'play_name' : event['play_name'],
        'line_number' : event['line_number']
    }
    )


    return {
        'statusCode': 200,
        'body': json.dumps(response['Item'])
    }

import boto3

response = input("Are you sure you want to delete the metadata table and all it's content.(y/n)")

if response == 'y':
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table("metadata")
    table.delete()
    print("Table deleted")
else:
    print("Operation cancelled")

import boto3

dynamodb = boto3.resource("dynamodb",endpoint_url="http://localhost:8000")

table = dynamodb.Table("metadata")


table.put_item(
    Item = {
        'name' : 'MB_1960_Fassbender',
        'edit' : 'none',
        'class': 'none',
        'type': 'none',
        'actors': {
            'Macbeth':'Michael Fassbender',
            'Lady Macbeth': 'Marion Cotillard'
        },
        'accent':'UK',
        'time': 113,
        'producer':'none',
        'director':'Justin Kurzel',
        'writers':{
            '1':'Todd Louiso',
            '2':'Jacob Koskoff',
            '3':'Micheal Lesslie'
        },
        'distributor':{
            '1':'Studio Canal',
            '2':'The Weinstein Company'
        },
        'company':{
            '1':'Anton Capital Entertainment',
            '2':'Creative Scotland',
            '3':'DMC Film',
            '4':'Film 4',
            '5':'See-Saw Films'
        },
        'music': 'Jed Kurzel',
        'location':'none'
    }
)

response = table.get_item(
    Key = {
        "name":'MB_1960_Fassbender',
    }
)
item = response['Item']
print(item)

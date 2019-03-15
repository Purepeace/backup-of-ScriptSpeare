import boto3
import csv
import os

#Takes in an unsplit string with delimiter = '|' and returns a dictionary in from
# '1': 'item1', '2':'item2'....
def spliter(unsplit_data):
    split_data = unsplit_data.split('|')
    if split_data[0] == 'none':
        new_data = 'none'
    else:
        new_data = {}
        for i,item in enumerate(split_data):
            new_data[str(i+1)] = item


    return new_data

file_names = []

for file in os.listdir(os.getcwd()):
    if file.endswith(".tsv"):
        file_names.append(file)

dynamodb = boto3.resource("dynamodb")

table = dynamodb.Table("metadata")

with table.batch_writer() as batch:

    for file_name in file_names:
        print("processing "+file_name)
        with open(file_name) as f:
            csv_reader = csv.reader(f, delimiter='\t')
            line_number = 0
            for line in csv_reader:
                if line_number == 0:
                    fields = line
                    roles = line[fields.index('Location')+1:fields.index('-')]
                else:
                    #Cleanup data here

                    #Replace any empty strings with none as dynamodb will not accept empty strings
                    data = []
                    for i, item in enumerate(line):
                        if item == '':
                            data.append('none')
                        else:
                            data.append(line[i])

                    #Create a dictionary of actors
                    actors = {}
                    for i,role in enumerate(roles):
                        actors[role] = data[fields.index("Location")+i+1]


                    #Create a dictionary for fields that may have multiple values
                    producer = spliter(data[fields.index("Producer")])
                    director = spliter(data[fields.index("Director")])
                    writers = spliter(data[fields.index("Writers")])
                    distributor = spliter(data[fields.index("Distributor")])
                    company = spliter(data[fields.index("Company")])
                    music = spliter(data[fields.index("Music")])



                    batch.put_item(
                    Item = {
                        'name' :        data[fields.index("Name")],
                        'type':         data[fields.index("Type")],
                        'year':         data[fields.index('Year')],
                        'actors':       actors,
                        'accent':       data[fields.index("Accent")],
                        'time':         data[fields.index("Time (m)")],
                        'producer':     producer,
                        'director':     director,
                        'writers':      writers,
                        'distributor':  distributor,
                        'company':      company,
                        'music':        music,
                        'location':     data[fields.index("Location")],
                        'playname':     file_name[file_name.index('-')+2:-4]
                    }
                )

                line_number += 1

response = table.scan(Select='COUNT')

print(response)

import boto3
import os
import csv

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

table = dynamodb.Table("annotations")

with table.batch_writer() as batch:
    for file_name in file_names:
            with open(file_name) as f:
                csv_reader = csv.reader(f, delimiter='\t')
                line_number = 0
                for line in csv_reader:
                    if line_number == 0:
                        fields = line
                    else:

                        #Replace any empty strings with none as dynamodb will not accept empty strings
                        data = []
                        for i, item in enumerate(line):
                            if item == '':
                                data.append('none')
                            else:
                                data.append(line[i])

                        has_data = False

                        #Checks there is actually annotations about the line
                        for d in data[1:]:
                            if d != 'none':
                                has_data = True
                                break


                        if has_data:

                            #get line_number
                            n = data[0].index('^')
                            str_line_number = data[0][:n]
                            new_item = {'line_number':int(str_line_number)}

                            split_data = []
                            #Preform splitter on all fields
                            for field in fields[1:]:
                                split_data = spliter(data[fields.index(field)])
                                new_item[field.lower()] = split_data
                                if split_data == 'none':
                                    new_item['number_'+ field.lower()] = 0
                                else:
                                    new_item['number_'+ field.lower()] = len(split_data.keys())

                            #Add the play name to the item

                            new_item['play_name'] = file_name[file_name.index('-')+2:-4]
                            batch.put_item(Item = new_item)

                    line_number += 1

import boto3
import unittest

dynamodb = boto3.resource("dynamodb")
client = boto3.client('dynamodb')

table = dynamodb.Table("annotations")

class TestDatabaseCreation(unittest.TestCase):

    def test_table_exists(self):
        try:
            table = dynamodb.Table("annotations")
        except:
            self.fail("Table was not created successfully")

    def test_line_81(self):
        response = table.get_item(Key = {'play_name':'Macbeth','line_number':81})
        try:
            item = response['Item']
        except:
            self.fail("Macbeth line 81 is not in the database")

    def test_number_of_items(self):
        response = client.describe_table(TableName='annotations')
        self.assertEqual(response['Table']['ItemCount'],23)


unittest.main()

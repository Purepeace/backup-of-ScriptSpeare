import boto3
import unittest

dynamodb = boto3.resource("dynamodb")
client = boto3.client('dynamodb')

table = dynamodb.Table("metadata")

class TestDatabaseCreation(unittest.TestCase):

    def test_table_exists(self):
        try:
            table = dynamodb.Table("metadata")
        except:
            self.fail("Table was not created successfully")

    def test_Illuminations(self):
        response = table.get_item(Key = {'name':'MB-2001-UK-Stage-Illuminations'})
        try:
            item = response['Item']
        except:
            self.fail("MB-2001-UK-Stage-Illuminations is not present in database")

    def test_number_of_items(self):
        response = client.describe_table(TableName='metadata')
        self.assertEqual(response['Table']['ItemCount'],64)


unittest.main()

# # # import the json utility package since we will be working with a JSON object
# import json
# # import the AWS SDK (for Python the package name is boto3)
# import boto3
# # import two packages to help us with dates and date formatting
# from time import gmtime, strftime

# # create a DynamoDB object using the AWS SDK
# dynamodb = boto3.resource('dynamodb')
# # use the DynamoDB object to select our table
# table = dynamodb.Table('website-db')
# # store the current time in a human readable format in a variable
# now = strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())

# # define the handler function that the Lambda service will use as an entry point
# def lambda_handler(event, context):

# # extract values from the event object we got from the Lambda service and store in a variable
#     name = event['firstName'] +' '+ event['lastName']
# # write name and time to the DynamoDB table using the object we instantiated and save response in a variable
#     response = table.put_item(
#         Item={
#             'id': name,
#             'LatestGreetingTime':now
#             })
# # return a properly formatted JSON object
#     return {
#         'statusCode': 200,
#         'body': json.dumps('Hello from Lambda, ' + name)
#     }

import json
import boto3
from time import gmtime, strftime

# create a DynamoDB object using the AWS SDK
dynamodb = boto3.resource('dynamodb')

# create an SNS client
sns_client = boto3.client('sns')

# use the DynamoDB object to select our table
table = dynamodb.Table('website-db')

# store the current time in a human-readable format in a variable
now = strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())

# define the handler function that the Lambda service will use as an entry point
def lambda_handler(event, context):
    #event['firstName'] = 'sai'
    #event['lastName'] = 'kumar'
    # extract values from the event object we got from the Lambda service and store in a variable
    name = event['firstName'] + ' ' + event['lastName']

    # write name and time to the DynamoDB table using the object we instantiated
    table.put_item(
        Item={
            'id': name,
            'LatestGreetingTime': now
        }
    )

    # create an SNS message
    sns_message = f'Hello from Lambda, {name}'

    # publish the SNS message
    sns_client.publish(
        TopicArn='arn:aws:sns:us-east-2:844149419613:website-sns',
        Message=sns_message
    )

    # return a properly formatted JSON object
    return {
        'statusCode': 200,
        'body': json.dumps(sns_message)
    }

import json
import random
import boto3
from botocore.exceptions import ClientError

# Initialize SQS client
sqs = boto3.client('sqs')
SQS_URL = "https://sqs.us-east-1.amazonaws.com/371894258952/AECoreOutput_Queue"

random_sayings = [
    "Life is what happens when you're busy making other plans.",
    "The way to get started is to quit talking and begin doing.",
    "Life is what we make it, always has been, always will be.",
    "The purpose of our lives is to be happy.",
    "Life is short, and it's up to you to make it sweet."
]

def lambda_handler(event, context):
    path = event.get("path", "")

    if path == '/sendmessage':
        random_saying = random.choice(random_sayings)
        message_body = f"Hello World - {random_saying}. This Lambda function is behind the ALB."

        send_message_params = {
            'MessageBody': message_body,
            'QueueUrl': SQS_URL
        }

        try:
            sqs.send_message(**send_message_params)
            return {
                'isBase64Encoded': False,
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'text/plain'
                },
                'body': 'Message sent to SQS successfully.'
            }
        except ClientError as e:
            print(f"Error sending message to SQS: {e}")
            return {
                'isBase64Encoded': False,
                'statusCode': 500,
                'headers': {
                    'Content-Type': 'text/plain'
                },
                'body': 'Failed to send message to SQS.'
            }

    elif path == '/getmessages':
        receive_message_params = {
            'QueueUrl': SQS_URL,
            'MaxNumberOfMessages': 10  # Retrieve up to 10 messages
        }

        try:
            data = sqs.receive_message(**receive_message_params)
            messages = data.get('Messages', [])
            return {
                'isBase64Encoded': False,
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'application/json'
                },
                'body': json.dumps(messages)
            }
        except ClientError as e:
            print(f"Error retrieving messages from SQS: {e}")
            return {
                'isBase64Encoded': False,
                'statusCode': 500,
                'headers': {
                    'Content-Type': 'text/plain'
                },
                'body': 'Failed to retrieve messages from SQS.'
            }

    else:
        return {
            'isBase64Encoded': False,
            'statusCode': 200,
            'headers': {
                'Content-Type': 'text/plain'
            },
            'body': 'This Lambda function is behind the ALB.'
        }

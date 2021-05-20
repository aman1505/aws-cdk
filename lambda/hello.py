import json

def handler(event, context):
    print('hello world')
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/plain'
        },
        'body': 'Hello, CDK!'
    }
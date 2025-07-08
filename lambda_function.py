import json
import uuid
import os
from decimal import Decimal
import boto3
from urllib.parse import unquote

# DynamoDB setup
dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('TABLE_NAME', 'NotesTable')
table = dynamodb.Table(table_name)

# Convert Decimal to int/float
def decimal_to_native(obj):
    if isinstance(obj, list):
        return [decimal_to_native(i) for i in obj]
    elif isinstance(obj, dict):
        return {k: decimal_to_native(v) for k, v in obj.items()}
    elif isinstance(obj, Decimal):
        return int(obj) if obj % 1 == 0 else float(obj)
    else:
        return obj

def lambda_handler(event, context):
    method = event.get('httpMethod', '')
    path = event.get('path', '')

    # Serve HTML on root path
    if method == 'GET' and path in ['/', '/index.html']:
        try:
            with open('index.html', 'r', encoding='utf-8') as f:
                html = f.read()
            return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'text/html'
                },
                'body': html
            }
        except Exception as e:
            return {
                'statusCode': 500,
                'headers': { 'Content-Type': 'text/plain' },
                'body': f"Failed to load HTML: {str(e)}"
            }

    # POST /note → Add note
    if method == 'POST' and path == '/note':
        try:
            body = json.loads(event.get('body', '{}'))
            content = body.get('content', '').strip()

            if not content:
                return {
                    'statusCode': 400,
                    'headers': { 'Content-Type': 'application/json' },
                    'body': json.dumps({'error': 'Note content is required.'})
                }

            note = {
                'id': str(uuid.uuid4()),
                'content': content,
                'timestamp': int(context.aws_request_id[:8], 16)
            }

            table.put_item(Item=note)

            return {
                'statusCode': 201,
                'headers': { 'Content-Type': 'application/json' },
                'body': json.dumps({'message': 'Note saved.', 'note': note})
            }

        except Exception as e:
            return {
                'statusCode': 500,
                'headers': { 'Content-Type': 'application/json' },
                'body': json.dumps({'error': f'Failed to save note. {str(e)}'})
            }

    # GET /note → List notes
    if method == 'GET' and path == '/note':
        try:
            response = table.scan()
            items = decimal_to_native(response.get('Items', []))
            return {
                'statusCode': 200,
                'headers': { 'Content-Type': 'application/json' },
                'body': json.dumps(items)
            }

        except Exception as e:
            return {
                'statusCode': 500,
                'headers': { 'Content-Type': 'application/json' },
                'body': json.dumps({'error': f'Failed to fetch notes. {str(e)}'})
            }

    # Unsupported
    return {
        'statusCode': 405,
        'headers': { 'Content-Type': 'application/json' },
        'body': json.dumps({'error': 'Method Not Allowed'})
    }

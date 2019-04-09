import datetime
import json
import logging
import os
import uuid

import boto3
from aws_xray_sdk.core import patch_all

patch_all()

logger = logging.getLogger("provisioner_logger")
logger.setLevel(logging.DEBUG)

transcode_pipeline = os.getenv('TRANSCODE_PIPELINE')
table_name = os.getenv('TRANSCODE_TABLE')


etClient = boto3.client('elastictranscoder')

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(table_name)


def handler(event, context):
    logger.debug(event)
    if not event['body']:
        return error_resp(400, "Missing request body")

    try:
        data = json.loads(event['body'])
        input, output = data['input'], data['output']
    except Exception as e:
        return error_resp(400, f"Invalid payload, exception: {str(e)}")

    try:

        transcode_job_id = create_transcode_job(input, output)
        add_to_dynamodb(input, output, transcode_job_id)
        return {
            'statusCode': 200,
            'body': json.dumps({
                "message": "Transcode job has been started",
                "transcode_job_id": transcode_job_id
            })
        }

    except Exception as e:
        return error_resp(500, str(e))


def add_to_dynamodb(input_key, output_key, transcoder_job):
    data = {
        'input_key': input_key,
        'output_key': output_key,
        'id': str(uuid.uuid4()),
        'date': str(datetime.datetime.now()),
        'transcoder_job': transcoder_job,
    }
    table.put_item(
        Item=data
    )
    return data['id']


def create_transcode_job(input_key, output_key):
    resp = etClient.create_job(
        PipelineId=transcode_pipeline,
        Input={
            'Key': input_key,
            'TimeSpan': {
                'Duration': '2.000'
            }
        },
        Output={
            'Key': output_key,
            'PresetId': get_gif_preset()
        }
    )
    logger.debug(resp)
    return resp['Job']['Id']


def error_resp(code, message):
    return {
        'statusCode': code,
        'body': json.dumps({
            'error': message
        })
    }


def get_gif_preset():
    response = etClient.list_presets()
    for preset in response['Presets']:
        if 'Gif' in preset['Name']:
            return preset['Id']

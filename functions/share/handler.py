import json
import logging
import os

import boto3
from botocore.exceptions import ClientError
from aws_xray_sdk.core import patch_all

patch_all()

logger = logging.getLogger("provisioner_logger")
logger.setLevel(logging.DEBUG)

output_bucket = os.getenv('OUTPUT_BUCKET')
notify_topic = os.getenv('NOTIFY_TOPIC')

s3Client = boto3.client('s3')
snsClient = boto3.client('sns')


def handler(event, context):
    try:
        for record in event.get('Records', []):
            message = record['Sns']['Message']
            data = json.loads(message)

            logger.debug(data)
            for output in data['outputs']:
                try:
                    output_key = output['key']
                    pre_signed_url = build_pre_signed_url(output_key)
                    send_notification(pre_signed_url)
                except ClientError as e:
                    logger.error(f"Client error: {str(e)}")

    except Exception as e:
        logger.error(f"Exception: {str(e)}")
        raise e


def build_pre_signed_url(key):
    url = s3Client.generate_presigned_url(
        ClientMethod='get_object',
        Params={
            'Bucket': output_bucket,
            'Key': key
        },
        ExpiresIn=3600)
    logger.info(f"Generated pre-signed URL {url}")
    return url


def send_notification(pre_signed_key):
    snsClient.publish(
        TargetArn=notify_topic,
        Message=f"Video transcode finished: {pre_signed_key}"
    )


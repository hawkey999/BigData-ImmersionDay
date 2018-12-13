import json
import gzip
import boto3
s3 = boto3.client('s3')


def lambda_handler(event, context):
    try:
        print(event)
        print('S3 SQL get data from S3, when column 4 > 50000 ...')
        Bucket = event['Records'][0]['s3']['bucket']['name']
        Key = event['Records'][0]['s3']['object']['key']
        SQLstr = "select s._1,s._4 from s3object s where CAST(s._4 as INTEGER)>50000"
        response = s3.select_object_content(
            Bucket=Bucket,
            Key=Key,
            Expression=SQLstr,
            ExpressionType='SQL',
            RequestProgress={'Enabled': True},
            InputSerialization={
                'CSV': {
                    'FileHeaderInfo': 'NONE',
                    'FieldDelimiter': ' '
                },
                'CompressionType': 'GZIP'
            },
            OutputSerialization={
                'CSV': {
                    'FieldDelimiter': ' '
                }
            }
        )

        print('Get payload data from S3 response...')
        event_stream = response['Payload']
        end_event_received = False
        data = b''
        for event in event_stream:
            # If we received a records event, write the data to a file
            if 'Records' in event:
                data += event['Records']['Payload']
            # If we received a progress event, print the details
            elif 'Progress' in event:
                #print(event['Progress']['Details'])
                pass
            # End event indicates that the request finished successfully
            elif 'End' in event:
                print('Result is complete')
                end_event_received = True
        if not end_event_received:
            raise Exception("End event not received, request incomplete.")

        print('Upload new file to S3...')
        putData_gz = gzip.compress(data)
        response_put_object = s3.put_object(
            Bucket=Bucket,
            Key='converted/s3selected-'+Key,
            Body=putData_gz
        )
    except Except as e:
        return e

    return {
        'statusCode': 200,
        'body': 'ok'
    }

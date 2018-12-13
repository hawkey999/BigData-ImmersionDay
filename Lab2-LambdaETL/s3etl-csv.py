import json
import gzip
import boto3
s3 = boto3.client('s3')


def lambda_handler(event, context):
    try:
        print(event)
        Bucket = event['Records'][0]['s3']['bucket']['name']
        Key = event['Records'][0]['s3']['object']['key']
        print('Download file from S3...')
        response_get_object = s3.get_object(
            Bucket=Bucket,
            Key=Key
        )
        getBody = response_get_object["Body"].read()

        print('Decompress...')
        csvdata_gz = gzip.decompress(getBody)
        csvdata = csvdata_gz.decode('utf-8').splitlines()

        print('Get column 1 and 4 when column 4 > 50000 ...')
        putData = ''
        for line in csvdata:
            d1, d2, d3, d4 = line.split(' ')
            if int(d4) > 50000:
                putData += d1+','+d4+'\n'
        putData_gz = gzip.compress(bytes(putData, 'utf-8'))

        print('Upload new file to S3...')
        response_put_object = s3.put_object(
            Bucket=Bucket,
            Key='converted/'+Key,
            Body=putData_gz
        )
    except Exception as e:
        return e

    return {
        'statusCode': 200,
        'body': 'ok'
    }

import json
import boto3
s3 = boto3.client('s3')


def lambda_handler(event, context):

    print('Download file from S3')
    Bucket = event['Records'][0]['s3']['bucket']['name']
    Key = event['Records'][0]['s3']['object']['key']
    response_get_object = s3.get_object(
        Bucket=Bucket,
        Key=Key
    )

    print('Get userid and username from downloaded file')
    getBody = response_get_object["Body"].read()
    getDataList = getBody.decode('utf-8').splitlines()
    putData = ''
    for n in getDataList:
        userid = json.loads(n)['userid']
        username = json.loads(n)['username']
        data = ({
            "userid": userid,
            "username": username
        })
        putData += json.dumps(data)+'\n'

    print('Upload the new file to S3')
    response_put_object = s3.put_object(
        Bucket=Bucket,
        Key='converted/'+Key,
        Body=bytes(putData, 'utf-8')
    )

    return {
        'statusCode': 200,
        'body': 'ok'
    }

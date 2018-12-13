import boto3
s3 = boto3.client('s3')
Bucket = '<your bucket>'
Key = '<s3 bucket prefix>/pagecounts-20100212-050000.gz'
SQLstr = "select s._1,s._4 from s3object s where CAST(s._4 as INTEGER)>50000 limit 20"

"""
S3 SELECT command SQL refer to:
https://docs.aws.amazon.com/AmazonS3/latest/dev/s3-glacier-select-sql-reference-select.html

S3 SELECT boto3 refer to:
https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.select_object_content
"""
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
            'FieldDelimiter': ','
        }
    }
)
"""
Response of PayLoad is botocore.eventstream.EventStream Object, refer to:
https://botocore.amazonaws.com/v1/documentation/api/latest/reference/eventstream.html#botocore-eventstream
"""
def print_result(response):
    event_stream = response['Payload']
    end_event_received = False
    data = ''
    for event in event_stream:
        # If we received a records event, write the data to a file
        if 'Records' in event:
            data += event['Records']['Payload'].decode("utf-8")
        # If we received a progress event, print the details
        elif 'Progress' in event:
            print(event['Progress']['Details'])
        # End event indicates that the request finished successfully
        elif 'End' in event:
            print('Result is complete')
            end_event_received = True
    if not end_event_received:
        raise Exception("End event not received, request incomplete.")
    print(data)


print_result(response)

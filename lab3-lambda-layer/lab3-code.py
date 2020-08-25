import boto3
import botocore
import subprocess
import os

s3 = boto3.resource('s3')

def lambda_handler(event, context):
    
    # S3 Object Information
    bucket_name = event['Records'][0]['s3']['bucket']['name'] 
    key = event['Records'][0]['s3']['object']['key']
    filename, file_extension = os.path.splitext(key)

    # Temporary/Emphemoral Storage
    bucket_name_thumbnail = 'ENTER_THUMBNAIL_BUCKET_NAME'
    temp_vid_file = '/tmp/' + key
    thumbnail_key = filename + '.png'
    temp_thumbnail_file = '/tmp/' + thumbnail_key
    
    # Download file from S3
    try:
        s3.Bucket(bucket_name).download_file(key, temp_vid_file)
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("The object does not exist.")
        else:
            raise
    
    # Invoking FFmpeg from /opt/bin
    thumbnail_size = '640*360'
    cmd = '/opt/bin/ffmpeg -y -ss 00:00:00.000 -i ' + temp_vid_file + ' -s ' + thumbnail_size + ' -vframes 1 ' + str(temp_thumbnail_file)
    
    print(cmd)
    
    returned_value = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)  # returns the exit code in unix
    
    print(returned_value)
    
    try:
        response = s3.Bucket(bucket_name_thumbnail).upload_file(temp_thumbnail_file, thumbnail_key)
    except Exception as e:
        print('Inside Exception Block')
        print(e)
        return False    
    
    return True


import boto3
import os

#Retrieve ACCESS KEYS from enviroment variables
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")

#Set S3 Configuration
s3 = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    )

#Method to save files to a bucket in S3
def saveFileS3(bucketname, fileKey, fileData):
    s3.put_object(Bucket=bucketname, Key=fileKey, Body=fileData)
    return
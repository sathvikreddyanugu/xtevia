import os
import os.path
import boto3
import argparse

parser = argparse.ArgumentParser(description="File copy between buckets")
parser.add_argument('source_bucket', help="S3 source bucket name")
parser.add_argument('dest_bucket', help="S3 dest bucket name")
parser.add_argument('threshold', help="Threshold value in MB's")
args = parser.parse_args()
aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')

s3 = boto3.client('s3')
contents = s3.list_objects_v2(Bucket=args.source_bucket,  MaxKeys=1000)['Contents']

s3 = boto3.resource(
    's3',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
)
src = s3.Bucket(args.source_bucket)

def move_files():
    for archive in src.objects.all():
        s3.meta.client.copy_object(
            ACL='public-read',
            Bucket=args.dest_bucket,
            CopySource={'Bucket': args.source_bucket, 'Key': archive.key},
            Key=archive.key
        )

for c in contents:
	size = float(c['Size'])/100000
	if str(size) > str(args.threshold):
		print("Found files greater than threshold")
		move_files()
	else:
		print("No files greater than threshold were found")



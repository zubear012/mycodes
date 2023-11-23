#we upload an obect using put_object method and use generate_presigned_url method to get the url to see the content of the file.
import boto3
import json

# Replace 'YOUR_ACCESS_KEY', 'YOUR_SECRET_KEY', and 'YOUR_BUCKET_NAME' with your AWS credentials and S3 bucket name
#no need to send access and secret key if you have configured already in your m/c
# ACCESS_KEY = 'AKIAQSUQHG66YHU6BCUG'
# SECRET_KEY = 'bx5eN3d5/PFuLsUA9HFHt01e/WQfBesglVwHtFo9'
BUCKET_NAME = 'practices-0'
FILE_NAME = 'zubear/test.json'  # The name of the file to be uploaded

# JSON data to be uploaded
data = {
    "id": "1982",
    "name": "haripriya",
    "designation": "software trainee"
}

# Convert Python dictionary to JSON string
json_data = json.dumps(data)

# Initialize S3 client
s3 = boto3.client('s3')

# Upload JSON data to S3 bucket
s3.put_object(Body=json_data, Bucket=BUCKET_NAME, Key=FILE_NAME, ContentType='application/json')

# Generate a pre-signed URL for the uploaded file
url_expiration_time = 3600  # URL expiration time in seconds (1 hour in this example)
presigned_url = s3.generate_presigned_url('get_object', Params={'Bucket': BUCKET_NAME, 'Key': FILE_NAME}, ExpiresIn=url_expiration_time)

# Print the pre-signed URL
print("Pre-signed URL for the uploaded JSON file:")
print("urlis-------------------",presigned_url)

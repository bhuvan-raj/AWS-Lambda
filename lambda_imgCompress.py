import boto3
import os
import io
from PIL import Image

s3 = boto3.client('s3')

def lambda_handler(event, context):
    # Get bucket and object key from event
    source_bucket = "source-image-bucket123"  # Updated bucket name
    destination_bucket = "resized-image-bucket123"  # Updated bucket name
    object_key = event['Records'][0]['s3']['object']['key']
    
    try:
        # Download the image from S3
        file_byte_string = s3.get_object(Bucket=source_bucket, Key=object_key)['Body'].read()
        
        # Open image using PIL
        image = Image.open(io.BytesIO(file_byte_string))
        
        # Resize image (reduce by 50%)
        width, height = image.size
        image = image.resize((width//2, height//2))
        
        # Save to buffer
        buffer = io.BytesIO()
        image.save(buffer, format="JPEG")
        buffer.seek(0)
        
        # Upload resized image to the destination bucket
        resized_key = f"resized-{object_key}"
        s3.put_object(Bucket=destination_bucket, Key=resized_key, Body=buffer, ContentType='image/jpeg')
        
        return {
            'statusCode': 200,
            'body': f"Image {object_key} resized and saved as {resized_key} in {destination_bucket}"
        }
    
    except Exception as e:
        return {
            'statusCode': 500,
            'body': f"Error processing image: {str(e)}"
        }

# AWS Lambda - Comprehensive Guide

## 📌 Introduction to Serverless Technologies

### What is Serverless Computing?

Serverless computing is a cloud computing execution model where the cloud provider manages the infrastructure, allowing developers to focus only on writing and deploying code. The term "serverless" does not mean there are no servers; rather, it implies that developers do not have to manage servers directly.

### Benefits of Serverless Computing

- **No server management**: The cloud provider handles provisioning, scaling, and maintenance.
- **Cost-effective**: Users are billed only for the compute time used.
- **Scalability**: Functions scale automatically based on demand.
- **Improved development speed**: Developers focus solely on code rather than infrastructure.

---

## 📌 Traditional Application Deployment vs. Serverless

### Traditional Deployment Model

- Applications are deployed on physical servers or cloud virtual machines (e.g., AWS EC2).
- Developers must install the OS, dependencies, and maintain security patches.
- Requires manual scaling and monitoring for traffic fluctuations.
- Costly and time-consuming to maintain infrastructure.

### Challenges in Traditional Deployment

- **Infrastructure management** diverts focus from development.
- **Costly** to maintain dedicated teams for infrastructure management.
- **Inefficient resource utilization** leads to increased expenses.

### How Serverless Computing Solves These Issues

- **Removes the need for manual infrastructure management.**
- **Enables event-driven execution**, allowing functions to run only when triggered.
- **Scales automatically**, ensuring high availability and performance.
- **Cost-efficient**, as users pay only for execution time.

---

## 📌 Overview of AWS Lambda

### What is AWS Lambda?

AWS Lambda is a **serverless compute service** that allows users to run code without provisioning or managing servers. AWS handles infrastructure, scaling, logging, and monitoring, so developers only focus on writing code.

### Key Features of AWS Lambda

- **Event-driven execution**: Lambda functions execute in response to triggers from various AWS services.
- **Automated scaling**: Functions scale automatically based on traffic.
- **Pay-per-use pricing**: Charged based on execution time and memory usage.
- **Supports multiple languages**: Python, Node.js, Java, Go, etc.
- **Integrated with AWS services**: Works with API Gateway, S3, DynamoDB, and more.

---

## 📌 Understanding AWS Lambda Functions

### What is a Lambda Function?

A Lambda function is a self-contained piece of code executed in response to an event. It takes input (event data), processes it, and returns a response.

### How Lambda Functions Work

1. **Define a function** in supported programming languages (e.g., Python, Node.js, Java).
2. **Upload the function code** to AWS Lambda.
3. **Set triggers** (e.g., file uploads to S3, API Gateway requests, DynamoDB changes).
4. **AWS Lambda executes the function** when the trigger event occurs.
5. **AWS handles scaling, execution, and billing.**

### Triggers and Events

Lambda functions are triggered by AWS services such as:

- **S3**: Executes when a file is uploaded or deleted.
- **API Gateway**: Runs when an API endpoint receives a request.
- **DynamoDB Streams**: Triggers when data changes in the database.
- **CloudWatch Events**: Executes at scheduled intervals.

---

## 📌 What Happens When a Lambda Function is Triggered?

1. **Event Detection**: AWS Lambda detects an event from the configured trigger (e.g., an API request, an S3 file upload, or a scheduled event).
2. **Container Allocation**: AWS Lambda selects an available execution environment or creates a new one if needed.
3. **Code Execution**: The function executes within the allocated container, processing the event data.
4. **Logging and Monitoring**: AWS Lambda logs execution details and metrics in Amazon CloudWatch.
5. **Response Handling**: The function returns a response, which may trigger other AWS services or API Gateway.

---

## 📌 AWS Lambda Pricing Model

- **Free tier**: Includes 1 million requests per month and 400,000 GB-seconds.
- **Billing based on execution**:
  - **Request-based pricing**: \$0.20 per 1 million requests.
  - **Compute time pricing**: Based on memory usage and execution duration.
- **Additional charges** may apply for outbound data transfer and logging.

---

## 📌 Steps to Run the AWS Lambda Python Function

### **Prerequisites**

✅ AWS account with necessary permissions.
✅ An **S3 bucket** for source images (`source-image-bucket123`).
✅ An **S3 bucket** for resized images (`resized-image-bucket123`).
✅ AWS CLI installed (optional for testing locally).
✅ Python installed with dependencies (`boto3`, `Pillow`).

### **1️ Create IAM Role for Lambda**

1. Go to **AWS IAM Console** → Roles.
2. Click **Create Role** → Select **Lambda**.
3. Attach **AmazonS3FullAccess** and **AWSLambdaBasicExecutionRole**.
4. Click **Create Role** and attach it to your function.

### **2️ Deploy the Lambda Function**

1. Go to **AWS Lambda Console**.
2. Click **Create Function** → **Author from Scratch**.
3. Name it **ImageResizeLambda** and choose **Python 3.x**.
4. Assign the IAM Role created earlier.
5. Copy and paste the following **Python code** into the function editor:

```python
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

```
## **3 Adding the layer**

1. Go to **Menu** from the left top window
2. select the **layers**
3. create a new layer- select the Pillow zip (pillow-layer.zip)
4. create
5. Select the lambda function, tap on layer- Add layer - Select the pillow-layer.zip

### **4️⃣ Create S3 Trigger**

1. Open **AWS Lambda Console** → Select `ImageResizeLambda`.
2. Click **Configuration** → **Triggers** → **Add Trigger**.
3. Choose **S3** as the source.
4. Select **source-image-bucket123**.
5. Set **Event Type**: `PUT (All object create events)`.
6. Click **Save**.

### **5 Test the Lambda Function**

1. Upload an image (`test.jpg`) to `source-image`.
2. Go to `resized-image-bucket` and check for `resized-test.jpg`.
3. If errors occur, check **AWS CloudWatch Logs** for debugging.

---

🚀 **Congratulations! You've successfully deployed and tested an AWS Lambda function with S3 triggers!**


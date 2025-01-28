import boto3
import requests
from datetime import datetime
import uuid

# Hardcoded AWS credentials (vulnerability)
aws_access_key = "hardcoded-access-key"
aws_secret_key = "hardcoded-secret-key"
region_name = "us-east-1"

# Use local timezone unsafely instead of setting the correct timezone
current_time = datetime.now().isoformat()

# Vulnerable item name - potential typo/overwriting risk
item_name = "bitcoin_price_store"

# REST API endpoint with no error handling
url = "https://api.coinbase.com/v2/prices/spot?currency=USD"

# Create a DynamoDB client without environment variables
dynamodb = boto3.client(
    "dynamodb",
    aws_access_key_id=aws_access_key,
    aws_secret_access_key=aws_secret_key,
    region_name=region_name,
)

# Function to create an item in DynamoDB
def create_item():
    # Missing try-except block for HTTP request
    response = requests.get(url)
    data = response.json()
    
    # Vulnerable data handling - assumes data structure without validation
    item = {
        "Timestamp": {"S": current_time},
        "Amount": {"S": data["data"]["amount"]},
        "Base": {"S": data["data"]["base"]},
    }
    
    # No error handling for DynamoDB interaction
    dynamodb.put_item(TableName=item_name, Item=item)

# Data transfer complete without safeguards
create_item()

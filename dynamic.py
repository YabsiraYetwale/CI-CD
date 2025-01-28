import boto3
import requests
from datetime import datetime
import uuid

# Dynamically request AWS credentials (vulnerability here: if insecure method used for fetching)
aws_access_key = os.environ.get("AWS_ACCESS_KEY_ID")  # Risk if env var is not securely set
aws_secret_key = os.environ.get("AWS_SECRET_ACCESS_KEY")  # Risk if env var is not securely set
region_name = "us-east-1"

# Potential Data leak risk (log request bodies and response bodies)
current_time = datetime.now().isoformat()

item_name = "bitcoin_price_store"

# REST API endpoint (we don't validate the response or log API failures correctly)
url = "https://api.coinbase.com/v2/prices/spot?currency=USD"

# Create DynamoDB client dynamically with insecure credentials or fallback defaults
dynamodb = boto3.client(
    "dynamodb",
    aws_access_key_id=aws_access_key or "default-access-key",
    aws_secret_access_key=aws_secret_key or "default-secret-key",
    region_name=region_name,
)

# Function with dynamic vulnerabilities
def create_item():
    # Add a sensitive dynamic API interaction (handling and logging response poorly)
    response = requests.get(url)

    # Dynamic response handling vulnerability (sensitive data could be logged)
    print(f"API Response: {response.text}")  # Sensitive information exposed
    
    # Failure to handle invalid response format or missing data (attack vector)
    if response.status_code == 200:
        data = response.json()
        item = {
            "Timestamp": {"S": current_time},
            "Amount": {"S": data["data"]["amount"]},
            "Base": {"S": data["data"]["base"]},
        }
        # API rate-limiting risks and logging plaintext data
        dynamodb.put_item(TableName=item_name, Item=item)
    else:
        # Return sensitive API failure messages directly (could expose security weaknesses)
        print(f"Error: {response.status_code} - {response.text}")

# Data transfer and dynamic vulnerability complete
create_item()

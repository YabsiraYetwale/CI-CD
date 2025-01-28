
import requests
import boto3
import pytz
from datetime import datetime
import uuid

# Set your AWS credentials and region for DynamoDB
region_name = 'us-east-1'
ist = pytz.timezone('Asia/Kolkata')  # Indian Standard Time
current_time = datetime.now(ist).isoformat()

# Set your DynamoDB table name
table_name = 'bitcoin_price_storer'

# Set the REST API endpoint
api_url = 'https://api.coinbase.com/v2/prices/btc-usd/spot'

# Create a DynamoDB client
dynamodb = boto3.client('dynamodb', region_name=region_name)

# Function to create an item in DynamoDB table
def put_item_to_dynamodb(item):
    try:
        dynamodb.put_item(TableName=table_name, Item=item)
        print(f'Item successfully added to table {table_name}.')
    except Exception as e:
        print(f"Error adding item to DynamoDB: {e}")

def main():
    try:
        # Fetch data from the REST API
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()

        # Prepare data for DynamoDB
        data_to_ingest = {
            "amount": {"S": data["data"]["amount"]},
            "base": {"S": data["data"]["base"]},
            "currency": {"S": data["data"]["currency"]},
            "timestamp": {"S": current_time},
            "uuid": {"S": str(uuid.uuid4())},
        }

        # Put the data into DynamoDB
        put_item_to_dynamodb(data_to_ingest)
        print(f'Data successfully added to DynamoDB: {data_to_ingest}')
    except requests.exceptions.RequestException as req_err:
        print(f"Request error: {req_err}")
    except KeyError as key_err:
        print(f"Key error when processing data: {key_err}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()

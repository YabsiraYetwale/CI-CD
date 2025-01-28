import boto3
import requests
import pytz
from datetime import datetime
import uuid

# Your AWS credentials and region for DynamoDB //
region_name = 'us-east-1'
timezone = pytz.timezone('Africa/Addis_Ababa')
current_time = datetime.now(timezone).isoformat()
item_name = 'bitcoin_price_store'


# REST API endpoint
url = 'https://api.coinbase.com/v2/prices/spot?currency=USD'

# Create a DynamoDB client
dynamodb = boto3.client('dynamodb', region_name=region_name)

# Function to create an item in DynamoDB
def create_item():
    response = requests.get(url)
    data = response.json()
    
    item = {
        'Timestamp': {'S': current_time},
        'Amount': {'S': data['data']['amount']},
        'Base': {'S': data['data']['base']}
    }
    
    dynamodb.put_item(TableName=item_name, Item=item)

# Data transfer complete
create_item()

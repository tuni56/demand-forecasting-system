import json
import boto3
import pandas as pd
from prophet import Prophet
from io import StringIO

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('sales_forecast')

def lambda_handler(event, context):
    # Load data from DynamoDB
    response = table.scan()
    items = response['Items']
    df = pd.DataFrame(items)
    df.rename(columns={'date': 'ds', 'sales': 'y'}, inplace=True)
    
    # Train Prophet model
    model = Prophet()
    model.fit(df)
    
    # Predict future values
    future = model.make_future_dataframe(periods=30)
    forecast = model.predict(future)
    
    # Store results in DynamoDB
    for index, row in forecast.iterrows():
        table.put_item(Item={
            'date': str(row['ds']),
            'prediction': str(row['yhat'])
        })
    
    return {
        'statusCode': 200,
        'body': json.dumps('Forecast saved to DynamoDB!')
    }

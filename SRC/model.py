import pandas as pd
from prophet import Prophet

# Load sample dataset
df = pd.read_csv('data/sales_data.csv')
df.rename(columns={'date': 'ds', 'sales': 'y'}, inplace=True)

# Initialize and fit the Prophet model
model = Prophet()
model.fit(df)

# Make future predictions
future = model.make_future_dataframe(periods=30)
forecast = model.predict(future)

# Save predictions
forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].to_csv('data/forecast.csv', index=False)

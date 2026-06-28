import pandas as pd
from sqlalchemy import create_engine, text
import urllib.parse

# 1. Load your local CSV file
df = pd.read_csv('cars.csv')

# 2. Your Database Configuration
USER = 'admin'
PASSWORD = 'Carproject123!'
ENDPOINT = 'car-database.c5cgsak2a4rq.eu-north-1.rds.amazonaws.com'
DB_NAME = 'car_db'

safe_password = urllib.parse.quote_plus(PASSWORD)

# 3. First, connect to the server itself to CREATE the database
print("Creating the database if it doesn't exist...")
server_engine = create_engine(f"mysql+pymysql://{USER}:{safe_password}@{ENDPOINT}:3306/")
with server_engine.connect() as conn:
    conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}"))

# 4. Now, connect specifically to your new car_db
connection_string = f"mysql+pymysql://{USER}:{safe_password}@{ENDPOINT}:3306/{DB_NAME}"
engine = create_engine(connection_string)

# 5. Send data to the 'cars' table
print("Uploading data to Amazon RDS... please wait...")
df.to_sql(name='cars', con=engine, if_exists='replace', index=False)
print("Success! Every row has been successfully moved to your cloud database.")

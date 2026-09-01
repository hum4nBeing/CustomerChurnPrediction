# Script: data/load_data.py

import pandas as pd
from sqlalchemy import create_engine

# --- DB Settings ---
db_user = 'user'
db_password = 'password'
db_host = 'localhost'
db_port = '5432'
db_name = 'churn_db'
csv_file_path = 'data/Telco-Customer-Churn.csv'  # make sure the CSV exists in this directory

# --- Initialize Postgres connection engine ---
engine = create_engine(f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')

# --- Read the CSV file ---
try:
    df = pd.read_csv(csv_file_path)
    print("CSV loaded successfully.")
except Exception as e:
    print("Error loading CSV:", e)
    exit(1)

# --- Strip leading/trailing whitespaces from headers ---
df.columns = df.columns.str.strip()

# --- Map CSV column names to DB table schema ---
df = df.rename(columns={
    'customerID': 'customer_id',
    'SeniorCitizen': 'senior_citizen',
    'PhoneService': 'phone_service',
    'MultipleLines': 'multiple_lines',
    'InternetService': 'internet_service',
    'OnlineSecurity': 'online_security',
    'OnlineBackup': 'online_backup',
    'DeviceProtection': 'device_protection',
    'TechSupport': 'tech_support',
    'StreamingTV': 'streaming_tv',
    'StreamingMovies': 'streaming_movies',
    'PaperlessBilling': 'paperless_billing',
    'MonthlyCharges': 'monthly_charges',
    'TotalCharges': 'total_charges',
    'PaymentMethod': 'payment_method',
    'Churn': 'churn',
    'Partner': 'partner',
    'Dependents': 'dependents',
    'Contract': 'contract'
})

# --- Remove whitespace from all text-based columns ---
for col in df.select_dtypes(include=['object']).columns:
    df[col] = df[col].str.strip()

# --- Identify missing data ---
missing_counts = df.isna().sum()
print("Missing values per column:")
print(missing_counts)

# --- Cast 'total_charges' to float and drop invalid strings ---
df['total_charges'] = pd.to_numeric(df['total_charges'], errors='coerce')
initial_rows = df.shape[0]
df = df.dropna(subset=['total_charges'])
dropped_rows = initial_rows - df.shape[0]
if dropped_rows > 0:
    print(f"Dropped {dropped_rows} rows due to non-numeric TotalCharges.")

# --- (Optional) Fill NaNs for specific columns if required ---
# E.g., populate empty 'payment_method' cells using the most frequent value:
# df['payment_method'].fillna(df['payment_method'].mode()[0], inplace=True)

# --- Drop rows with duplicate 'customer_id' ---
initial_rows = df.shape[0]
df = df.drop_duplicates(subset=['customer_id'])
duplicates_removed = initial_rows - df.shape[0]
if duplicates_removed > 0:
    print(f"Removed {duplicates_removed} duplicate rows based on customer_id.")

# --- Adjust specific column types ---
df['senior_citizen'] = df['senior_citizen'].astype(int)

# --- Write the cleaned DataFrame to the PostgreSQL table ---
try:
    df.to_sql('customers', engine, if_exists='append', index=False)
    print("Data loaded into the 'customers' table successfully.")
except Exception as e:
    print("Error inserting data into the database:", e)

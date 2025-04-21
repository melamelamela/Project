
#Libraries Import
import sqlite3 
import pandas as pd
import requests
from io import StringIO


# === SET UP ===
DB_NAME = "sales-analyze.db"
# Client Data 
SALES_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSawI56WBC64foMT9pKCiY594fBZk9Lyj8_bxfgmq-8ck_jw1Z49qDeMatCWqBxehEVoM6U1zdYx73V/pub?gid=760830694&single=true&output=csv"      
PRODUCTS_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSawI56WBC64foMT9pKCiY594fBZk9Lyj8_bxfgmq-8ck_jw1Z49qDeMatCWqBxehEVoM6U1zdYx73V/pub?gid=0&single=true&output=csv" 
STORES_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSawI56WBC64foMT9pKCiY594fBZk9Lyj8_bxfgmq-8ck_jw1Z49qDeMatCWqBxehEVoM6U1zdYx73V/pub?gid=714623615&single=true&output=csv"   

# Database Creation and Connection
db_name = "sales-analyze.db"
conn = sqlite3.connect(db_name)
cursor = conn.cursor()
   
# CSV import
df_sales = pd.read_csv(SALES_URL)
df_products = pd.read_csv(PRODUCTS_URL)
df_stores = pd.read_csv(STORES_URL)

## CLEANING

# Rename the CSVS column headers

df_sales = pd.read_csv(SALES_URL)
df_sales.rename(columns={
    "Date": "date",
    "Produit": "product_id",
    "Quantité": "quantity",
    "Magasin": "store_id"
}, inplace=True)

df_products = pd.read_csv(PRODUCTS_URL)
df_products.rename(columns={
    "ID Référence produit": "product_id",
    "Nom": "product_name",
    "Prix": "Price",
    "Stock": "Stock"
}, inplace=True)

df_stores = pd.read_csv(STORES_URL)
df_stores.rename(columns={
    "ID Magasin": "store_id",
    "Ville": "city",
    "Nombre de salariés": "num-employees"
}, inplace=True)

# Drop duplicates
df_sales = df.drop_duplicates()
df_products = df.drop_duplicates()
df_stores = df.drop_duplicates()

# Delete lines with missing values / or replace by avg or similar NaN value .fillna()
#df_sales.dropna(inplace=True)
#df_products.dropna(inplace=True)
#df_stores.dropna(inplace=True)

# Checking data type

# Sales
df_sales["date"] = pd.to_datetime(df_sales["date"], errors="coerce")  # errors = NaN
df_sales["product_id"] = df_sales["product_id"].astype(int)
df_sales["quantity"] = pd.to_numeric(df_sales["quantity"], errors="coerce")
df_sales["store_id"] = df_sales["store_id"].astype(int)

# Products
df_products["product_id"] = df_products["product_id"].astype(int)
df_products["product_name"] = df_products["product_name"].astype(str)
df_products["price"] = pd.to_numeric(df_products["price"], errors="coerce")
df_products["stock"] = pd.to_numeric(df_products["stock"], errors="coerce").fillna(0).astype(int)

# Stores
df_stores["store_id"] = df_stores["store_id"].astype(int)
df_stores["city"] = df_stores["city"].astype(str)
df_stores["num_employees"] = pd.to_numeric(df_stores["num_employees"], errors="coerce").fillna(0).astype(int)



# Checking strings (delete spaces)
df_products["product_name"] = df_products["product_name"].str.strip()
df_stores["product_name"] = df_stores["product_name"].str.strip()

# Checking string to lower
df_products["product_name"] = df_products["product_name"].str.lower()
df_stores["product_name"] = df_stores["product_name"].str.lower()



# 
# Connexion to SQLite database 
conn = sqlite3.connect("sales-analyze.db")
cursor = conn.cursor()

# === Sales Table Creation et Csv Data Import===#
cursor.execute('''
CREATE TABLE IF NOT EXISTS sales (
    date DATE,
    store_id INTEGER,
    product_id INTEGER,
    quantity INTEGER    
);
''')

# Products Table Creation
cursor.execute('''
CREATE TABLE IF NOT EXISTS products (
    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_name TEXT,
    price REAL,
    stock INTEGER
);
''')

# Stores Table Creation
cursor.execute('''
CREATE TABLE IF NOT EXISTS stores (
    store_id INTEGER PRIMARY KEY AUTOINCREMENT,
    city TEXT,
    num_employees INTEGER
);
''')

conn.commit()  # Save changes


# Function data into the tables
def insert_sales_data(df_sales):
    for index, row in df_sales.iterrows():
        cursor.execute("""
            INSERT INTO sales (date, store_id, product_id, quantity)
            VALUES (?, ?, ?, ?, ?)
        """, (row['date'], row['store_id'], row['product_id'], row['quantity']))
    conn.commit()

def insert_products_data(df_products):
    for index, row in df_products.iterrows():
        cursor.execute("""
            INSERT INTO products (product_id, product_name, price, stock)
            VALUES (?, ?, ?, ?)
        """, (row['product_id'], row['product_name'], row['price'], row['stock']))
    conn.commit()

def insert_stores_data(df_stores):
    for index, row in df_stores.iterrows():
        cursor.execute("""
            INSERT INTO stores (store_id, city, num_employees, region)
            VALUES (?, ?, ?, ?)
        """, (row['store_id'], row['city'], row['num_employees']))
    conn.commit()



## === Analyze Result === ###

# Function to retrieve the region from the city via API
def get_region_from_city(city):
    try:
        response = requests.get(
            f"https://geo.api.gouv.fr/communes?nom={city}&fields=region&format=json&geometry=centre"
        )
        data = response.json() # convert json result to python 
        if data and isinstance(data, list):
            return data[0]["region"]["nom"]
    except Exception as e:
        print(f"API error {city} : {e}")
    return None

# Connexion to SQLite database 
conn = sqlite3.connect("sales-analyze.db")
cursor = conn.cursor()


# Result Table Creation (by adding the region column)
cursor.execute("""
CREATE TABLE IF NOT EXISTS Result (
    type TEXT,
    product_id INTEGER,
    product_name TEXT,
    city TEXT,
    region TEXT,
    total_quantity_sold INTEGER,
    total_revenue REAL
)
""")
cursor.execute("DELETE FROM Result") # Delete previous results 

# a. Total Revenue
cursor.execute("""
SELECT SUM(sales.quantity * products.price)
FROM sales 
JOIN products ON sales.product_id = product.product_id
""")
total_revenue = cursor.fetchone()[0] # result of the query
# Result insertion into the Result table
cursor.execute("""
INSERT INTO Result (type, total_revenue)
VALUES (?, ?)
""", ('total_revenue', total_revenue))

# b. Sales by product
cursor.execute("""
SELECT 
    products.product_id,
    products.product_name,
    SUM(sales.quantity),
    SUM(sales.quantity * products.price)
FROM sales 
JOIN product ON sales.product_id = products.product_id
GROUP BY products.product_id, products.product_name
""")
# Loop through the results and insert them into the Result table
for row in cursor.fetchall():
    cursor.execute("""
        INSERT INTO Result (type, product_id, product_name, total_quantity_sold, total_revenue)
        VALUES (?, ?, ?, ?, ?)
    """, ('sales_by_product', row[0], row[1], row[2], row[3]))

# c. Sales by city (with API call for region)
# Note : tables alias this time
cursor.execute("""
SELECT 
    st.city,
    SUM(sa.quantity),
    SUM(sa.quantity * p.price)
FROM sales sa
JOIN stores st ON sa.store_id = st.store_id
JOIN products p ON sa.product_id = p.product_id
GROUP BY st.city
""")

# Loop through the results and insert them into the Result table
for city, quantity, revenue in cursor.fetchall():
    region = get_region_from_city(city)
    cursor.execute("""
        INSERT INTO Result (type, city, region, total_quantity_sold, total_revenue)
        VALUES (?, ?, ?, ?, ?)
    """, ('sales_by_region', city, region, quantity, revenue))

conn.commit()
conn.close()





## Sales Loading every 30 minutes
# Loop to download and update every 30 minutes
#while True:
    #df_sales = import_csv_from_url(SALES_URL)
    #df_sales = df_sales.drop_duplicates()
    #df_sales.rename(columns={
    #"Date": "date",
    #"Produit": "product_id",
    #"Magasin": "store_id",
    #"Quantité": "quantity",
#}, inplace=True), inplace=True)
#    insert_sales_data(df_sales)
#    time.sleep(1800)  # 1800 secondes = 30 minutes

    
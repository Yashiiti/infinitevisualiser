import pandas as pd
from faker import Faker
import random

def generate_dummy_data(rows=100):
    fake = Faker()
    
    # Columns you want in the CSV
    data = {
        "Name": [fake.name() for _ in range(rows)],
        "Age": [random.randint(18, 70) for _ in range(rows)],
        "Email": [fake.email() for _ in range(rows)],
        "Phone Number": [fake.phone_number() for _ in range(rows)],
        "Address": [fake.address().replace("\n", ", ") for _ in range(rows)],
        "Date of Birth": [fake.date_of_birth(minimum_age=18, maximum_age=70).strftime("%Y-%m-%d") for _ in range(rows)],
        "Salary": [random.randint(30000, 120000) for _ in range(rows)],
        "Joining Date": [fake.date_this_decade().strftime("%Y-%m-%d") for _ in range(rows)],
        "Department": [random.choice(['HR', 'Engineering', 'Marketing', 'Sales', 'Product']) for _ in range(rows)]
    }
    
    df = pd.DataFrame(data)
    
    # Save the dataframe as CSV
    df.to_csv("dummy_data.csv", index=False)
    print("CSV file with dummy data generated!")

# Generate the dummy CSV file
generate_dummy_data(rows=200)  # Adjust the number of rows as needed

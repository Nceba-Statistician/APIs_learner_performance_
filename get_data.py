import requests
import pandas as pd
from itemsprocessing import updated_data

response = requests.get("http://127.0.0.1:8000/items_get").json()
# print(pd.DataFrame(response).head())
# print(pd.DataFrame(response).columns.tolist())

# print(updated_data.head())


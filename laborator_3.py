import pandas as pd
from numpy import double
from recombee_api_client.api_client import RecombeeClient
from recombee_api_client.api_requests import SetItemValues, Batch
from recombee_api_client.exceptions import APIException

# TODO 1: Configurare credentiale Recombee (la fel ca la Lab 02)
DB_NAME = 'grigore-dev'
PRIVATE_TOKEN = 'cmr6YFBG3udiO12b3LOfQc12O9hujWXDZx7jZoUNieMx2TbzPjh7Vs1DPqPXana9'
REGION = 'eu-west'

client = RecombeeClient(DB_NAME, PRIVATE_TOKEN)

# TODO 2: Incarcarea aceluiasi dataset folosit la Lab 02
PATH_DATASET = 'Amazon_BestSelling_Books_500.csv'

def send_items():
    """Functie care citeste dataset-ul si trimite item-urile in Recombee"""
    df = pd.read_csv(PATH_DATASET)
    print(f"Se trimit {len(df)} item-uri in Recombee...")
    
    requests = []
    
    for index, row in df.iterrows():
        # TODO 3: Extrageti ID-ul unic al produsului din coloana corespunzatoare din CSV
        item_id = str(row['Rank'])
        
        # TODO 4: Mapati proprietatile definite anterior cu valorile din randul curent
        # Exemplu:
        properties = {
            "Title": str(row['Title']),
            "Author": str(row['Author']),
            "Category": str(row['Category']),
            "Price": float(row['Price (USD)']),
        }
        
        # Adaugam request-ul de setare a valorilor pentru item
        # (SetItemValues creează automat item-ul dacă acesta nu există)
        requests.append(SetItemValues(item_id, properties, cascade_create=True))
        
        # Trimitem in loturi (batch) de cate 100 pentru eficienta
        if len(requests) == 100:
            client.send(Batch(requests))
            requests = []
            print("S-a trimis un lot de 100 item-uri...")
            
    # Trimitem si restul ramanase (daca numarul total nu e multiplu de 100)
    if requests:
        client.send(Batch(requests))
        print("S-a trimis ultimul lot de item-uri.")
        
    print("Toate item-urile au fost trimise cu succes!")

if __name__ == "__main__":
    send_items()

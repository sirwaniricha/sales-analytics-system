import requests

def fetch_all_products():
    """
    Fetches all products from DummyJSON API

    Returns: list of product dictionaries

    Expected Output Format:
    [
        {
            'id': 1,
            'title': 'iPhone 9',
            'category': 'smartphones',
            'brand': 'Apple',
            'price': 549,
            'rating': 4.69
        },
        ...
    ]

    Requirements:
    - Fetch all available products (use limit=100)
    - Handle connection errors with try-except
    - Return empty list if API fails
    - Print status message (success/failure)
    """
    api_url = 'https://dummyjson.com/products?limit=100'
    
    try:
        response = requests.get(api_url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            products = data.get('products', [])
            
            product_list = []
            for product in products:
                product_list.append({
                    'id': product.get('id'),
                    'title': product.get('title'),
                    'category': product.get('category'),
                    'brand': product.get('brand'),
                    'price': product.get('price'),
                    'rating': product.get('rating')
                })
            
            print(f"Successfully fetched {len(product_list)} products from DummyJSON API")
            return product_list
        else:
            print(f"Failed to fetch products: HTTP {response.status_code}")
            return []
            
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch products: {str(e)}")
        return []


def create_product_mapping(api_products):
    """
    Creates a mapping of product IDs to product info

    Parameters: api_products from fetch_all_products()

    Returns: dictionary mapping product IDs to info

    Expected Output Format:
    {
        1: {'title': 'iPhone 9', 'category': 'smartphones', 'brand': 'Apple', 'rating': 4.69},
        2: {'title': 'iPhone X', 'category': 'smartphones', 'brand': 'Apple', 'rating': 4.44},
        ...
    }
    """
    product_mapping = {}
    
    for product in api_products:
        product_id = product.get('id')
        if product_id is not None:
            product_mapping[product_id] = {
                'title': product.get('title'),
                'category': product.get('category'),
                'brand': product.get('brand'),
                'rating': product.get('rating')
            }
    
    return product_mapping

def enrich_sales_data(transactions, product_mapping):
    """
    Enriches transaction data with API product information

    Parameters:
    - transactions: list of transaction dictionaries
    - product_mapping: dictionary from create_product_mapping()

    Returns: list of enriched transaction dictionaries

    Expected Output Format (each transaction):
    {
        'TransactionID': 'T001',
        'Date': '2024-12-01',
        'ProductID': 'P101',
        'ProductName': 'Laptop',
        'Quantity': 2,
        'UnitPrice': 45000.0,
        'CustomerID': 'C001',
        'Region': 'North',
        # NEW FIELDS ADDED FROM API:
        'API_Category': 'laptops',
        'API_Brand': 'Apple',
        'API_Rating': 4.7,
        'API_Match': True  # True if enrichment successful, False otherwise
    }

    Enrichment Logic:
    - Extract numeric ID from ProductID (P101 → 101, P5 → 5)
    - If ID exists in product_mapping, add API fields
    - If ID doesn't exist, set API_Match to False and other fields to None
    - Handle all errors gracefully

    File Output:
    - Save enriched data to 'data/enriched_sales_data.txt'
    - Use same pipe-delimited format
    - Include new columns in header
    """
    import os
    
    enriched_transactions = []
    
    for transaction in transactions:
        enriched_transaction = transaction.copy()
        
        try:
            product_id = transaction.get('ProductID', '')
            numeric_id = int(product_id.replace('P', '')) if product_id.startswith('P') else None
            
            if numeric_id and numeric_id in product_mapping:
                product_info = product_mapping[numeric_id]
                enriched_transaction['API_Category'] = product_info.get('category')
                enriched_transaction['API_Brand'] = product_info.get('brand')
                enriched_transaction['API_Rating'] = product_info.get('rating')
                enriched_transaction['API_Match'] = True
            else:
                enriched_transaction['API_Category'] = None
                enriched_transaction['API_Brand'] = None
                enriched_transaction['API_Rating'] = None
                enriched_transaction['API_Match'] = False
                
        except (ValueError, AttributeError):
            enriched_transaction['API_Category'] = None
            enriched_transaction['API_Brand'] = None
            enriched_transaction['API_Rating'] = None
            enriched_transaction['API_Match'] = False
        
        enriched_transactions.append(enriched_transaction)
    
    try:
        os.makedirs('data', exist_ok=True)
        
        with open('data/enriched_sales_data.txt', 'w', encoding='utf-8') as file:
            header = 'TransactionID|Date|ProductID|ProductName|Quantity|UnitPrice|CustomerID|Region|API_Category|API_Brand|API_Rating|API_Match\n'
            file.write(header)
            
            for transaction in enriched_transactions:
                line = f"{transaction.get('TransactionID', '')}|"
                line += f"{transaction.get('Date', '')}|"
                line += f"{transaction.get('ProductID', '')}|"
                line += f"{transaction.get('ProductName', '')}|"
                line += f"{transaction.get('Quantity', '')}|"
                line += f"{transaction.get('UnitPrice', '')}|"
                line += f"{transaction.get('CustomerID', '')}|"
                line += f"{transaction.get('Region', '')}|"
                line += f"{transaction.get('API_Category', '')}|"
                line += f"{transaction.get('API_Brand', '')}|"
                line += f"{transaction.get('API_Rating', '')}|"
                line += f"{transaction.get('API_Match', '')}\n"
                file.write(line)
        
        print(f"Successfully saved {len(enriched_transactions)} enriched transactions to data/enriched_sales_data.txt")
        
    except IOError as e:
        print(f"Error saving enriched data: {str(e)}")
    
    return enriched_transactions
    
def save_enriched_data(enriched_transactions, filename='data/enriched_sales_data.txt'):
    """
    Saves enriched transactions back to file

    Expected File Format:
    TransactionID|Date|ProductID|ProductName|Quantity|UnitPrice|CustomerID|Region|API_Category|API_Brand|API_Rating|API_Match
    T001|2024-12-01|P101|Laptop|2|45000.0|C001|North|laptops|Apple|4.7|True
    ...

    Requirements:
    - Create output file with all original + new fields
    - Use pipe delimiter
    - Handle None values appropriately
    """
    import os
    
    try:
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        with open(filename, 'w', encoding='utf-8') as file:
            header = 'TransactionID|Date|ProductID|ProductName|Quantity|UnitPrice|CustomerID|Region|API_Category|API_Brand|API_Rating|API_Match\n'
            file.write(header)
            
            for transaction in enriched_transactions:
                api_category = transaction.get('API_Category')
                api_brand = transaction.get('API_Brand')
                api_rating = transaction.get('API_Rating')
                api_match = transaction.get('API_Match')
                
                line = f"{transaction.get('TransactionID', '')}|"
                line += f"{transaction.get('Date', '')}|"
                line += f"{transaction.get('ProductID', '')}|"
                line += f"{transaction.get('ProductName', '')}|"
                line += f"{transaction.get('Quantity', '')}|"
                line += f"{transaction.get('UnitPrice', '')}|"
                line += f"{transaction.get('CustomerID', '')}|"
                line += f"{transaction.get('Region', '')}|"
                line += f"{api_category if api_category is not None else ''}|"
                line += f"{api_brand if api_brand is not None else ''}|"
                line += f"{api_rating if api_rating is not None else ''}|"
                line += f"{api_match if api_match is not None else ''}\n"
                file.write(line)
        
        print(f"Successfully saved {len(enriched_transactions)} enriched transactions to {filename}")
        return True
        
    except IOError as e:
        print(f"Error saving enriched data: {str(e)}")
        return False




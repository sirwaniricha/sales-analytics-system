def read_sales_data(filename):
    """
    Reads sales data from file handling encoding issues

    Returns: list of raw lines (strings)

    Expected Output Format:
    ['T001|2024-12-01|P101|Laptop|2|45000|C001|North', ...]

    Requirements:
    - Use 'with' statement
    - Handle different encodings (try 'utf-8', 'latin-1', 'cp1252')
    - Handle FileNotFoundError with appropriate error message
    - Skip the header row
    - Remove empty lines
    """
    encodings = ['utf-8', 'latin-1', 'cp1252']
    
    for encoding in encodings:
        try:
            with open(filename, 'r', encoding=encoding) as file:
                lines = file.readlines()
                
            if lines:
                lines = lines[1:]
            
            lines = [line.strip() for line in lines if line.strip()]
            
            return lines
            
        except FileNotFoundError:
            raise FileNotFoundError(f"Error: File '{filename}' not found.")
        except UnicodeDecodeError:
            if encoding == encodings[-1]:
                raise
            continue
    
    return []


def parse_transactions(raw_lines):
    """
    Parses raw lines into clean list of dictionaries

    Returns: list of dictionaries with keys:
    ['TransactionID', 'Date', 'ProductID', 'ProductName',
     'Quantity', 'UnitPrice', 'CustomerID', 'Region']

    Expected Output Format:
    [
        {
            'TransactionID': 'T001',
            'Date': '2024-12-01',
            'ProductID': 'P101',
            'ProductName': 'Laptop',
            'Quantity': 2,           # int type
            'UnitPrice': 45000.0,    # float type
            'CustomerID': 'C001',
            'Region': 'North'
        },
        ...
    ]

    Requirements:
    - Split by pipe delimiter '|'
    - Handle commas within ProductName (remove or replace)
    - Remove commas from numeric fields and convert to proper types
    - Convert Quantity to int
    - Convert UnitPrice to float
    - Skip rows with incorrect number of fields
    """
    transactions = []
    
    for line in raw_lines:
        fields = line.split('|')
        
        if len(fields) != 8:
            continue
        
        try:
            product_name = fields[3].replace(',', ' ')
            quantity = int(fields[4].replace(',', ''))
            unit_price = float(fields[5].replace(',', ''))
            
            transaction = {
                'TransactionID': fields[0],
                'Date': fields[1],
                'ProductID': fields[2],
                'ProductName': product_name,
                'Quantity': quantity,
                'UnitPrice': unit_price,
                'CustomerID': fields[6],
                'Region': fields[7]
            }
            
            transactions.append(transaction)
            
        except (ValueError, IndexError):
            continue
    
    return transactions


def validate_and_filter(transactions, region=None, min_amount=None, max_amount=None):
    """
    Validates transactions and applies optional filters

    Parameters:
    - transactions: list of transaction dictionaries
    - region: filter by specific region (optional)
    - min_amount: minimum transaction amount (Quantity * UnitPrice) (optional)
    - max_amount: maximum transaction amount (optional)

    Returns: tuple (valid_transactions, invalid_count, filter_summary)

    Expected Output Format:
    (
        [list of valid filtered transactions],
        5,  # count of invalid transactions
        {
            'total_input': 100,
            'invalid': 5,
            'filtered_by_region': 20,
            'filtered_by_amount': 10,
            'final_count': 65
        }
    )

    Validation Rules:
    - Quantity must be > 0
    - UnitPrice must be > 0
    - All required fields must be present
    - TransactionID must start with 'T'
    - ProductID must start with 'P'
    - CustomerID must start with 'C'

    Filter Display:
    - Print available regions to user before filtering
    - Print transaction amount range (min/max) to user
    - Show count of records after each filter applied
    """
    total_input = len(transactions)
    valid_transactions = []
    invalid_count = 0
    
    required_fields = ['TransactionID', 'Date', 'ProductID', 'ProductName', 
                      'Quantity', 'UnitPrice', 'CustomerID', 'Region']
    
    for transaction in transactions:
        is_valid = True
        
        for field in required_fields:
            if field not in transaction:
                is_valid = False
                break
        
        if is_valid:
            try:
                if transaction['Quantity'] <= 0:
                    is_valid = False
                elif transaction['UnitPrice'] <= 0:
                    is_valid = False
                elif not transaction['TransactionID'].startswith('T'):
                    is_valid = False
                elif not transaction['ProductID'].startswith('P'):
                    is_valid = False
                elif not transaction['CustomerID'] or not transaction['CustomerID'].startswith('C'):
                    is_valid = False
                elif not transaction['Region'] or transaction['Region'].strip() == '':
                    is_valid = False
            except (KeyError, TypeError):
                is_valid = False
        
        if is_valid:
            valid_transactions.append(transaction)
        else:
            invalid_count += 1
    
    print(f"\nValidation Complete:")
    print(f"Total Input: {total_input}")
    print(f"Valid: {len(valid_transactions)}")
    print(f"Invalid: {invalid_count}")
    
    available_regions = set(t['Region'] for t in valid_transactions)
    print(f"\nAvailable Regions: {sorted(available_regions)}")
    
    if valid_transactions:
        amounts = [t['Quantity'] * t['UnitPrice'] for t in valid_transactions]
        print(f"Transaction Amount Range: ${min(amounts):,.2f} - ${max(amounts):,.2f}")
    
    filtered_transactions = valid_transactions.copy()
    filtered_by_region = 0
    filtered_by_amount = 0
    
    if region:
        before_filter = len(filtered_transactions)
        filtered_transactions = [t for t in filtered_transactions if t['Region'] == region]
        filtered_by_region = before_filter - len(filtered_transactions)
        print(f"\nAfter Region Filter ('{region}'): {len(filtered_transactions)} records")
    
    if min_amount is not None or max_amount is not None:
        before_filter = len(filtered_transactions)
        temp_filtered = []
        
        for t in filtered_transactions:
            amount = t['Quantity'] * t['UnitPrice']
            if min_amount is not None and amount < min_amount:
                continue
            if max_amount is not None and amount > max_amount:
                continue
            temp_filtered.append(t)
        
        filtered_transactions = temp_filtered
        filtered_by_amount = before_filter - len(filtered_transactions)
        print(f"After Amount Filter: {len(filtered_transactions)} records")
    
    filter_summary = {
        'total_input': total_input,
        'invalid': invalid_count,
        'filtered_by_region': filtered_by_region,
        'filtered_by_amount': filtered_by_amount,
        'final_count': len(filtered_transactions)
    }
    
    return (filtered_transactions, invalid_count, filter_summary)


data = read_sales_data('C:\\Users\\Richa\\Desktop\\New folder\\sales-analytics-system\\data\\sales_data.txt')
print(data)
transaction = parse_transactions(data)
print(transaction)
valid_transaction, invalid_count, filter_summary = validate_and_filter(transaction)
print('Total records parsed: ',filter_summary['total_input'])
print('Invalid records removed: ',filter_summary['invalid'])
print('Valid records after cleaning: ',filter_summary['final_count'])

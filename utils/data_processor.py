def calculate_total_revenue(transactions):
    """
    Calculates total revenue from all transactions

    Returns: float (total revenue)

    Expected Output: Single number representing sum of (Quantity * UnitPrice)
    Example: 1545000.50
    """
    total_revenue = 0.0
    
    for transaction in transactions:
        quantity = transaction.get('Quantity', 0)
        unit_price = transaction.get('UnitPrice', 0.0)
        total_revenue += quantity * unit_price
    
    return total_revenue

def region_wise_sales(transactions):
    """
    Analyzes sales by region

    Returns: dictionary with region statistics

    Expected Output Format:
    {
        'North': {
            'total_sales': 450000.0,
            'transaction_count': 15,
            'percentage': 29.13
        },
        'South': {...},
        ...
    }

    Requirements:
    - Calculate total sales per region
    - Count transactions per region
    - Calculate percentage of total sales
    - Sort by total_sales in descending order
    """
    region_data = {}
    total_revenue = 0.0
    
    for transaction in transactions:
        region = transaction.get('Region', 'Unknown')
        quantity = transaction.get('Quantity', 0)
        unit_price = transaction.get('UnitPrice', 0.0)
        sales = quantity * unit_price
        
        if region not in region_data:
            region_data[region] = {
                'total_sales': 0.0,
                'transaction_count': 0
            }
        
        region_data[region]['total_sales'] += sales
        region_data[region]['transaction_count'] += 1
        total_revenue += sales
    
    for region in region_data:
        if total_revenue > 0:
            region_data[region]['percentage'] = round((region_data[region]['total_sales'] / total_revenue) * 100, 2)
        else:
            region_data[region]['percentage'] = 0.0
    
    sorted_regions = dict(sorted(region_data.items(), key=lambda x: x[1]['total_sales'], reverse=True))
    
    return sorted_regions


def top_selling_products(transactions, n=5):
    """
    Finds top n products by total quantity sold

    Returns: list of tuples

    Expected Output Format:
    [
        ('Laptop', 45, 2250000.0),  # (ProductName, TotalQuantity, TotalRevenue)
        ('Mouse', 38, 19000.0),
        ...
    ]

    Requirements:
    - Aggregate by ProductName
    - Calculate total quantity sold
    - Calculate total revenue for each product
    - Sort by TotalQuantity descending
    - Return top n products
    """
    product_data = {}
    
    for transaction in transactions:
        product_name = transaction.get('ProductName', 'Unknown')
        quantity = transaction.get('Quantity', 0)
        unit_price = transaction.get('UnitPrice', 0.0)
        revenue = quantity * unit_price
        
        if product_name not in product_data:
            product_data[product_name] = {
                'total_quantity': 0,
                'total_revenue': 0.0
            }
        
        product_data[product_name]['total_quantity'] += quantity
        product_data[product_name]['total_revenue'] += revenue
    
    product_list = [
        (name, data['total_quantity'], data['total_revenue'])
        for name, data in product_data.items()
    ]
    
    sorted_products = sorted(product_list, key=lambda x: x[1], reverse=True)
    
    return sorted_products[:n]

def customer_analysis(transactions):
    """
    Analyzes customer purchase patterns

    Returns: dictionary of customer statistics

    Expected Output Format:
    {
        'C001': {
            'total_spent': 95000.0,
            'purchase_count': 3,
            'avg_order_value': 31666.67,
            'products_bought': ['Laptop', 'Mouse', 'Keyboard']
        },
        'C002': {...},
        ...
    }

    Requirements:
    - Calculate total amount spent per customer
    - Count number of purchases
    - Calculate average order value
    - List unique products bought
    - Sort by total_spent descending
    """
    customer_data = {}
    
    for transaction in transactions:
        customer_id = transaction.get('CustomerID', 'Unknown')
        quantity = transaction.get('Quantity', 0)
        unit_price = transaction.get('UnitPrice', 0.0)
        product_name = transaction.get('ProductName', 'Unknown')
        amount = quantity * unit_price
        
        if customer_id not in customer_data:
            customer_data[customer_id] = {
                'total_spent': 0.0,
                'purchase_count': 0,
                'products_bought': set()
            }
        
        customer_data[customer_id]['total_spent'] += amount
        customer_data[customer_id]['purchase_count'] += 1
        customer_data[customer_id]['products_bought'].add(product_name)
    
    for customer_id in customer_data:
        total_spent = customer_data[customer_id]['total_spent']
        purchase_count = customer_data[customer_id]['purchase_count']
        
        customer_data[customer_id]['avg_order_value'] = round(total_spent / purchase_count, 2) if purchase_count > 0 else 0.0
        customer_data[customer_id]['products_bought'] = list(customer_data[customer_id]['products_bought'])
    
    sorted_customers = dict(sorted(customer_data.items(), key=lambda x: x[1]['total_spent'], reverse=True))
    
    return sorted_customers

def daily_sales_trend(transactions):
    """
    Analyzes sales trends by date

    Returns: dictionary sorted by date

    Expected Output Format:
    {
        '2024-12-01': {
            'revenue': 125000.0,
            'transaction_count': 8,
            'unique_customers': 6
        },
        '2024-12-02': {...},
        ...
    }

    Requirements:
    - Group by date
    - Calculate daily revenue
    - Count daily transactions
    - Count unique customers per day
    - Sort chronologically
    """
    daily_data = {}
    
    for transaction in transactions:
        date = transaction.get('Date', 'Unknown')
        quantity = transaction.get('Quantity', 0)
        unit_price = transaction.get('UnitPrice', 0.0)
        customer_id = transaction.get('CustomerID', 'Unknown')
        revenue = quantity * unit_price
        
        if date not in daily_data:
            daily_data[date] = {
                'revenue': 0.0,
                'transaction_count': 0,
                'unique_customers': set()
            }
        
        daily_data[date]['revenue'] += revenue
        daily_data[date]['transaction_count'] += 1
        daily_data[date]['unique_customers'].add(customer_id)
    
    for date in daily_data:
        daily_data[date]['unique_customers'] = len(daily_data[date]['unique_customers'])
    
    sorted_daily = dict(sorted(daily_data.items()))
    
    return sorted_daily

def find_peak_sales_day(transactions):
    """
    Identifies the date with highest revenue

    Returns: tuple (date, revenue, transaction_count)

    Expected Output Format:
    ('2024-12-15', 185000.0, 12)
    """
    daily_data = {}
    
    for transaction in transactions:
        date = transaction.get('Date', 'Unknown')
        quantity = transaction.get('Quantity', 0)
        unit_price = transaction.get('UnitPrice', 0.0)
        revenue = quantity * unit_price
        
        if date not in daily_data:
            daily_data[date] = {
                'revenue': 0.0,
                'transaction_count': 0
            }
        
        daily_data[date]['revenue'] += revenue
        daily_data[date]['transaction_count'] += 1
    
    if not daily_data:
        return (None, 0.0, 0)
    
    peak_date = max(daily_data.items(), key=lambda x: x[1]['revenue'])
    
    return (peak_date[0], peak_date[1]['revenue'], peak_date[1]['transaction_count'])

def low_performing_products(transactions, threshold=10):
    """
    Identifies products with low sales

    Returns: list of tuples

    Expected Output Format:
    [
        ('Webcam', 4, 12000.0),  # (ProductName, TotalQuantity, TotalRevenue)
        ('Headphones', 7, 10500.0),
        ...
    ]

    Requirements:
    - Find products with total quantity < threshold
    - Include total quantity and revenue
    - Sort by TotalQuantity ascending
    """
    product_data = {}
    
    for transaction in transactions:
        product_name = transaction.get('ProductName', 'Unknown')
        quantity = transaction.get('Quantity', 0)
        unit_price = transaction.get('UnitPrice', 0.0)
        revenue = quantity * unit_price
        
        if product_name not in product_data:
            product_data[product_name] = {
                'total_quantity': 0,
                'total_revenue': 0.0
            }
        
        product_data[product_name]['total_quantity'] += quantity
        product_data[product_name]['total_revenue'] += revenue
    
    low_performing = [
        (name, data['total_quantity'], data['total_revenue'])
        for name, data in product_data.items()
        if data['total_quantity'] < threshold
    ]
    
    sorted_low_performing = sorted(low_performing, key=lambda x: x[1])
    
    return sorted_low_performing


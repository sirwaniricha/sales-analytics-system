# Sales Analytics System

This is a Python project that analyzes sales data and generates reports. It reads transaction data from a text file, validates it, does some analysis, and then enriches the data by calling an external API to get more product information.

## What it does

- Reads sales data from text files (handles different encodings)
- Validates the data to make sure everything looks good
- Calculates things like:
  - Total revenue
  - Sales by region
  - Top products
  - Customer buying patterns
  - Daily trends
  - Which day had the best sales
  - Products that aren't selling well
- Gets extra product info from DummyJSON API
- Creates a detailed report with all the analysis

## Repository Structure

```
sales-analytics-system/
├── README.md
├── main.py
├── utils/
│   ├── file_handler.py
│   ├── data_processor.py
│   └── api_handler.py
├── data/
│   └── sales_data.txt (provided)
├── output/
└── requirements.txt
```

## Requirements

You'll need Python 3.7 or newer installed on your computer.

## Setup

1. Clone this repo:
```bash
git clone https://github.com/your-username/sales-analytics-system.git
cd sales-analytics-system
```

2. Install the required library:
```bash
pip install -r requirements.txt
```

This just installs the `requests` library (version 2.31.0) which is needed to call the API.

3. Make sure you have the sales data file in the `data/` folder. It should be called `sales_data.txt` and have pipe-separated values.

## Running the Program

Just run:
```bash
python main.py
```

The program will:
1. Read the sales data file
2. Clean up and validate the data
3. Do all the analysis
4. Fetch product info from the API
5. Combine everything together
6. Generate a report

You'll see output like this:
```
============================================================
           SALES ANALYTICS SYSTEM
============================================================

[1/10] Reading sales data...
✓ Successfully read 95 transactions

[2/10] Parsing and cleaning data...
✓ Parsed 95 records

[3/10] Validating and filtering transactions...
✓ Valid: 92 | Invalid: 3

[4/10] Analyzing sales data...
✓ Analysis complete

[5/10] Fetching product data from API...
Successfully fetched 100 products from DummyJSON API

[6/10] Enriching sales data...
✓ Enriched and saved data

[7/10] Generating report...
✓ Report saved

[8/8] Process Complete!
```

## Output

The program creates two files:

**data/enriched_sales_data.txt** - Your original sales data plus the extra info from the API (category, brand, rating)

**output/sales_report.txt** - A detailed report with:
- Revenue totals and averages
- Sales breakdown by region
- Top 5 products and customers
- Daily trends
- Performance analysis

## Common Issues

**"File not found" error** - Make sure sales_data.txt is in the data folder

**API connection problems** - Check your internet. The program will still work but won't have the API data

**"No module named 'requests'"** - You forgot to run `pip install -r requirements.txt`

## Data Format

The input file should be pipe-separated (|) with these columns:
```
TransactionID|Date|ProductID|ProductName|Quantity|UnitPrice|CustomerID|Region
T001|2024-12-01|P101|Laptop|2|45000|C001|North
```

The validation checks:
- Quantity and price are positive numbers
- IDs start with the right letters (T for transactions, P for products, C for customers)
- All fields are filled in

## Code Structure

**main.py** - The main file that runs everything

**utils/file_handler.py** - Functions to read, parse, and validate the sales data

**utils/data_processor.py** - All the analysis functions (revenue, regions, products, customers, trends, etc.)

**utils/api_handler.py** - Functions to fetch data from the API and combine it with our sales data

## About the API

I'm using [DummyJSON](https://dummyjson.com/) which is a free fake API for testing. It doesn't need any authentication or API keys.

## Notes

This was built as a learning project for data analysis and API integration.

import os
from datetime import datetime
from utils.file_handler import read_sales_data, parse_transactions, validate_and_filter
from utils.data_processor import (
    calculate_total_revenue,
    region_wise_sales,
    top_selling_products,
    customer_analysis,
    daily_sales_trend,
    find_peak_sales_day,
    low_performing_products
)
from utils.api_handler import (
    fetch_all_products,
    create_product_mapping,
    enrich_sales_data,
    save_enriched_data
)


def generate_sales_report(transactions, enriched_transactions, output_file='output/sales_report.txt'):
    """
    Generates a comprehensive formatted text report

    Report Must Include (in this order):

    1. HEADER
       - Report title
       - Generation date and time
       - Total records processed

    2. OVERALL SUMMARY
       - Total Revenue (formatted with commas)
       - Total Transactions
       - Average Order Value
       - Date Range of data

    3. REGION-WISE PERFORMANCE
       - Table showing each region with:
         * Total Sales Amount
         * Percentage of Total
         * Transaction Count
       - Sorted by sales amount descending

    4. TOP 5 PRODUCTS
       - Table with columns: Rank, Product Name, Quantity Sold, Revenue

    5. TOP 5 CUSTOMERS
       - Table with columns: Rank, Customer ID, Total Spent, Order Count

    6. DAILY SALES TREND
       - Table showing: Date, Revenue, Transactions, Unique Customers

    7. PRODUCT PERFORMANCE ANALYSIS
       - Best selling day
       - Low performing products (if any)
       - Average transaction value per region

    8. API ENRICHMENT SUMMARY
       - Total products enriched
       - Success rate percentage
       - List of products that couldn't be enriched

    Expected Output Format (sample):
    ============================================
           SALES ANALYTICS REPORT
         Generated: 2024-12-18 14:30:22
         Records Processed: 95
    ============================================

    OVERALL SUMMARY
    --------------------------------------------
    Total Revenue:        ₹15,45,000.00
    Total Transactions:   95
    Average Order Value:  ₹16,263.16
    Date Range:           2024-12-01 to 2024-12-31

    REGION-WISE PERFORMANCE
    --------------------------------------------
    Region    Sales         % of Total  Transactions
    North     ₹4,50,000     29.13%      25
    South     ₹3,80,000     24.60%      22
    ...

    (continue with all sections...)
    """
    import os
    from datetime import datetime
    from utils.data_processor import (
        calculate_total_revenue,
        region_wise_sales,
        top_selling_products,
        customer_analysis,
        daily_sales_trend,
        find_peak_sales_day,
        low_performing_products
    )

    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    with open(output_file, 'w', encoding='utf-8') as file:
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        file.write("=" * 60 + "\n")
        file.write("           SALES ANALYTICS REPORT\n")
        file.write(f"         Generated: {current_time}\n")
        file.write(f"         Records Processed: {len(transactions)}\n")
        file.write("=" * 60 + "\n\n")

        total_revenue = calculate_total_revenue(transactions)
        avg_order_value = total_revenue / len(transactions) if transactions else 0

        dates = [t.get('Date', '') for t in transactions if t.get('Date')]
        date_range = f"{min(dates)} to {max(dates)}" if dates else "N/A"

        file.write("OVERALL SUMMARY\n")
        file.write("-" * 60 + "\n")
        file.write(f"Total Revenue:        ₹{total_revenue:,.2f}\n")
        file.write(f"Total Transactions:   {len(transactions)}\n")
        file.write(f"Average Order Value:  ₹{avg_order_value:,.2f}\n")
        file.write(f"Date Range:           {date_range}\n\n")

        region_sales = region_wise_sales(transactions)
        file.write("REGION-WISE PERFORMANCE\n")
        file.write("-" * 60 + "\n")
        file.write(f"{'Region':<15} {'Sales':<20} {'% of Total':<15} {'Transactions'}\n")
        file.write("-" * 60 + "\n")
        for region, data in region_sales.items():
            file.write(
                f"{region:<15} ₹{data['total_sales']:>15,.2f}   {data['percentage']:>6.2f}%      {data['transaction_count']:>5}\n")
        file.write("\n")

        top_products = top_selling_products(transactions, n=5)
        file.write("TOP 5 PRODUCTS\n")
        file.write("-" * 60 + "\n")
        file.write(f"{'Rank':<6} {'Product Name':<25} {'Quantity':<12} {'Revenue'}\n")
        file.write("-" * 60 + "\n")
        for idx, (name, qty, rev) in enumerate(top_products, 1):
            file.write(f"{idx:<6} {name:<25} {qty:<12} ₹{rev:,.2f}\n")
        file.write("\n")

        customer_stats = customer_analysis(transactions)
        top_customers = list(customer_stats.items())[:5]
        file.write("TOP 5 CUSTOMERS\n")
        file.write("-" * 60 + "\n")
        file.write(f"{'Rank':<6} {'Customer ID':<15} {'Total Spent':<20} {'Order Count'}\n")
        file.write("-" * 60 + "\n")
        for idx, (cust_id, data) in enumerate(top_customers, 1):
            file.write(f"{idx:<6} {cust_id:<15} ₹{data['total_spent']:>15,.2f}   {data['purchase_count']:>5}\n")
        file.write("\n")

        daily_trend = daily_sales_trend(transactions)
        file.write("DAILY SALES TREND\n")
        file.write("-" * 60 + "\n")
        file.write(f"{'Date':<15} {'Revenue':<20} {'Transactions':<15} {'Unique Customers'}\n")
        file.write("-" * 60 + "\n")
        for date, data in daily_trend.items():
            file.write(
                f"{date:<15} ₹{data['revenue']:>15,.2f}   {data['transaction_count']:>8}      {data['unique_customers']:>8}\n")
        file.write("\n")

        file.write("PRODUCT PERFORMANCE ANALYSIS\n")
        file.write("-" * 60 + "\n")

        peak_day = find_peak_sales_day(transactions)
        file.write(f"Best Selling Day: {peak_day[0]} (Revenue: ₹{peak_day[1]:,.2f}, Transactions: {peak_day[2]})\n\n")

        low_products = low_performing_products(transactions, threshold=10)
        if low_products:
            file.write("Low Performing Products (Quantity < 10):\n")
            for name, qty, rev in low_products:
                file.write(f"  - {name}: {qty} units, ₹{rev:,.2f}\n")
        else:
            file.write("No low performing products found.\n")
        file.write("\n")

        file.write("Average Transaction Value per Region:\n")
        for region, data in region_sales.items():
            avg_value = data['total_sales'] / data['transaction_count'] if data['transaction_count'] > 0 else 0
            file.write(f"  {region}: ₹{avg_value:,.2f}\n")
        file.write("\n")

        file.write("API ENRICHMENT SUMMARY\n")
        file.write("-" * 60 + "\n")

        total_enriched = len(enriched_transactions)
        successful_matches = sum(1 for t in enriched_transactions if t.get('API_Match') == True)
        success_rate = (successful_matches / total_enriched * 100) if total_enriched > 0 else 0

        file.write(f"Total Products Enriched:  {total_enriched}\n")
        file.write(f"Successful Matches:       {successful_matches}\n")
        file.write(f"Success Rate:             {success_rate:.2f}%\n\n")

        failed_products = [t for t in enriched_transactions if t.get('API_Match') == False]
        if failed_products:
            file.write("Products that couldn't be enriched:\n")
            unique_failed = set()
            for t in failed_products:
                product_info = f"{t.get('ProductID')} - {t.get('ProductName')}"
                if product_info not in unique_failed:
                    unique_failed.add(product_info)
                    file.write(f"  - {product_info}\n")
        else:
            file.write("All products were successfully enriched!\n")

        file.write("\n" + "=" * 60 + "\n")
        file.write("           END OF REPORT\n")
        file.write("=" * 60 + "\n")

    print(f"Sales report generated successfully: {output_file}")
    return True

def main():
    """
    Main execution function

    Workflow:
    1. Print welcome message
    2. Read sales data file (handle encoding)
    3. Parse and clean transactions
    4. Display filter options to user
       - Show available regions
       - Show transaction amount range
       - Ask if user wants to filter (y/n)
    5. If yes, ask for filter criteria and apply
    6. Validate transactions
    7. Display validation summary
    8. Perform all data analyses (call all functions from Part 2)
    9. Fetch products from API
    10. Enrich sales data with API info
    11. Save enriched data to file
    12. Generate comprehensive report
    13. Print success message with file locations

    Error Handling:
    - Wrap entire process in try-except
    - Display user-friendly error messages
    - Don't let program crash on errors

    Expected Console Output:
    ========================================
    SALES ANALYTICS SYSTEM
    ========================================

    [1/10] Reading sales data...
    ✓ Successfully read 95 transactions

    [2/10] Parsing and cleaning data...
    ✓ Parsed 95 records

    [3/10] Filter Options Available:
    Regions: North, South, East, West
    Amount Range: ₹500 - ₹90,000

    Do you want to filter data? (y/n): n

    [4/10] Validating transactions...
    ✓ Valid: 92 | Invalid: 3

    [5/10] Analyzing sales data...
    ✓ Analysis complete

    [6/10] Fetching product data from API...
    ✓ Fetched 30 products

    [7/10] Enriching sales data...
    ✓ Enriched 85/92 transactions (92.4%)

    [8/10] Saving enriched data...
    ✓ Saved to: data/enriched_sales_data.txt

    [9/10] Generating report...
    ✓ Report saved to: output/sales_report.txt

    [10/10] Process Complete!
    ========================================
    """
    try:
        print("=" * 60)
        print("           SALES ANALYTICS SYSTEM")
        print("=" * 60)
        print()
        
        print("[1/10] Reading sales data...")
        raw_lines = read_sales_data('data/sales_data.txt')
        print(f"✓ Successfully read {len(raw_lines)} transactions")
        print()
        
        print("[2/10] Parsing and cleaning data...")
        all_transactions = parse_transactions(raw_lines)
        print(f"✓ Parsed {len(all_transactions)} records")
        print()
        
        print("[3/10] Validating and filtering transactions...")
        valid_transactions, invalid_count, filter_summary = validate_and_filter(all_transactions)
        print(f"✓ Valid: {len(valid_transactions)} | Invalid: {invalid_count}")
        print()
        
        print("[4/10] Analyzing sales data...")
        calculate_total_revenue(valid_transactions)
        region_wise_sales(valid_transactions)
        top_selling_products(valid_transactions, n=5)
        customer_analysis(valid_transactions)
        daily_sales_trend(valid_transactions)
        find_peak_sales_day(valid_transactions)
        low_performing_products(valid_transactions, threshold=10)
        print("✓ Analysis complete")
        print()
        
        print("[5/10] Fetching product data from API...")
        api_products = fetch_all_products()
        print()
        
        print("[6/10] Enriching sales data...")
        product_mapping = create_product_mapping(api_products)
        enriched_transactions = enrich_sales_data(valid_transactions, product_mapping)
        print()
        
        print("[7/10] Generating report...")
        generate_sales_report(valid_transactions, enriched_transactions, 'output/sales_report.txt')
        print()
        
        print("[8/8] Process Complete!")
        print("=" * 60)
        print()
        print("Output Files Generated:")
        print("  - data/enriched_sales_data.txt")
        print("  - output/sales_report.txt")
        print()
        
    except FileNotFoundError as e:
        print(f"\nError: {e}")
        print("Please ensure 'data/sales_data.txt' exists in the correct location.")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
        print("Please check your data and try again.")


if __name__ == "__main__":
    main()


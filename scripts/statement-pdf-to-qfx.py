import pdfplumber
import re
import os
import sys
from helpers import parse_date_with_fixed_year, get_bmo_line_of_credit_transactions_regex_pattern
from qfx_helper import create_qfx


def extract_transactions_from_pdf(pdf_path, pattern, year):
    
    """Extract transactions from a PDF bank statement."""
    transactions = []
    
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                # Assume each line in the text has space-separated columns
                lines = text.split('\n')
                for line in lines:
                    # print(line)

                    match = re.match(pattern, line.strip())
                    if match:
                        # Extract components from the match
                        transaction_date = match.group(1)
                        posting_date = match.group(2)
                        description = match.group(3).strip() if match and match.group(3) is not None else ""
                        amount = match.group(4).replace(',', '')  # Remove commas from amount
                        credit = match.group(5)  # 'CR' if credit transaction, None if debit   
                        debits = f"-{amount}" if not credit else ""
                        credits = f"{amount}" if credit else ""

                        # Append transaction data to the list
                        transactions.append([
                            parse_date_with_fixed_year(transaction_date, year), 
                            description, 
                            debits, 
                            credits, 
                            "", 
                            ""
                        ])
    return transactions


def extract_transactions_from_folder(folder_path, pattern, year):
    """Extract transactions from all PDFs in the given folder."""
    all_transactions = []
    
    # List all PDF files in the folder
    for filename in os.listdir(folder_path):
        if filename.lower().endswith('.pdf'):
            pdf_path = os.path.join(folder_path, filename)
            print(f"Processing {pdf_path}...")
            
            # Extract transactions from the current PDF
            transactions = extract_transactions_from_pdf(pdf_path, pattern, year)
            print(f"found {len(transactions)} in {filename}")
            all_transactions.extend(transactions)  # Add to the list of all transactions

    return all_transactions


if __name__ == "__main__":
    if len(sys.argv) == 3:
        (input_folder_path, output_path) = sys.argv[1:]
    else:
        print("Wrong number of arguments passed.")

    pattern = get_bmo_line_of_credit_transactions_regex_pattern()

    # Extract transaction data from PDF
    transactions = extract_transactions_from_folder(input_folder_path, pattern, "2024")
    
    print(len(transactions))
    # print(transactions)
    
    gfx_content = create_qfx(
        transactions, 
        "<BID>", 
        "<ACCOUNT_ID>", 
        "CREDITLINE", 
        0,
        "20241219211151[-5]") 

    with open(output_path, 'w') as file:
        file.write(gfx_content)
    
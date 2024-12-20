from bs4 import BeautifulSoup
from qfx_helper import create_qfx
import sys


def extract_data_from_html(html_path):
    data = []

    with open(html_path, 'r', encoding='utf-8') as file:
        html_content = file.read()
        
        soup = BeautifulSoup(html_content, 'html.parser')
        table = soup.find('table')

        # Extract data from the table
        for row in table.find_all('tr'):
            cols = row.find_all('td')
            if cols:
                data.append([col.text.strip() for col in cols])

    return data

if __name__ == "__main__":
    if len(sys.argv) == 3:
        (input_path, output_path) = sys.argv[1:]
    else:
        print("Wrong number of arguments passed.")
    
    # Extract transaction data from PDF
    transactions = extract_data_from_html(input_path)

    print(len(transactions))
    # print(transactions[-10:])

    gfx_content = create_qfx(
        transactions, 
        "<BID>", 
        "<ACCOUNT_ID>", 
        "CREDITLINE", 
        fitid_fixed_prefix="900000100", 
        fitid_fixed_suffix="C001") 

    with open(output_path, 'w') as file:
        file.write(gfx_content)

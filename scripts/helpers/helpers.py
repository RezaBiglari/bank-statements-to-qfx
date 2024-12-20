from datetime import datetime
import re
import pytz
import uuid

def convert_to_custom_format(date_string: str, timezone_str: str = 'US/Pacific') -> str:
    """
    Convert a date string in the format 'Dec 9, 2024' to the custom format 'YYYYMMDDHHMMSS[-8]',
    where [-8] represents the timezone offset.

    Args:
        date_string (str): The date string to be converted, e.g., 'Dec 9, 2024'.
        timezone_str (str): The timezone to apply for conversion (default is 'US/Pacific').

    Returns:
        str: The formatted date string in the format 'YYYYMMDDHHMMSS[-8]'.
    """
    try:
        # Step 1: Parse the date string into a datetime object
        date_obj = datetime.strptime(date_string, '%b %d, %Y')

        # Step 2: Localize the datetime to the specified timezone
        timezone = pytz.timezone(timezone_str)
        date_obj = timezone.localize(date_obj.replace(hour=12, minute=0, second=0, microsecond=0))

        # Step 3: Format the datetime to 'YYYYMMDDHHMMSS'
        formatted_date = date_obj.strftime('%Y%m%d%H%M%S')

        # Step 4: Add the timezone offset in the format [-8] (hardcoded for US/Pacific or UTC-8)
        # Here, we extract the UTC offset as a string (e.g., '-08:00' becomes '[-8]')
        utc_offset = date_obj.strftime('%z')[:3]  # Get the offset in hours (e.g., '-08')
        formatted_date += f'[{utc_offset}]'

        return formatted_date

    except Exception as e:
        print(f"Error converting date: {e}")
        return None


def parse_date_with_fixed_year(date_input, fixed_year=2024):
    """Parse a date with a fixed year when year is missing."""
    cleaned_date = date_input.replace('.', '')

    # Check if the input date is missing the year part (e.g., "May. 23")
    if len(cleaned_date.split()) == 2:
        # Assume the fixed year if it's missing (e.g., 2024)
        cleaned_date = f"{cleaned_date} {fixed_year}"

    # Now parse the date, which has the fixed year appended
    return datetime.strptime(cleaned_date, '%b %d %Y').strftime('%b %d, %Y')


def convert_currency_to_float(currency_string: str) -> float:
    # Step 1: Remove the currency symbol (e.g., '$')
    cleaned_string = re.sub(r'[^\d.-]', '', currency_string)
    
    # Step 2: Convert to float
    return float(cleaned_string)


def generate_transaction_id(date_input: str, 
                            fixed_prefix: str = "",
                            fixed_suffix: str = "",
                            fake_prefix: str = "FAKE-") -> str:
    """
    Generate a custom transaction identifier 
    """
    # Step 1: Validate and format the provided date
    try:
        # Parse the date from 'Mon DD, YYYY' format to 'YYYYMMDD' format
        current_date = datetime.strptime(date_input, '%b %d, %Y').strftime('%Y%m%d')
    except ValueError:
        raise ValueError("Invalid date format. Please use 'Mon DD, YYYY' format (e.g., 'Sep 16, 2024').")

    # Step 2: Generate a unique 8-character alphanumeric ID using UUID
    unique_id = str(uuid.uuid4()).replace('-', '')[:8].upper()

    # Step 3: Combine all components into the final transaction ID
    transaction_id = f"{fake_prefix}{fixed_prefix}{current_date}{fixed_suffix}{unique_id}"

    return transaction_id


def get_bmo_credit_card_transactions_regex_pattern():
    return r'(\w+\.\s?\d{1,2})\s+(\w+\.\s?\d{1,2})\s+([A-Za-z\s\d\W]+?)\s+([\d,]+\.\d{2})\s*(CR)?$'

def get_bmo_line_of_credit_transactions_regex_pattern():
    return r'^\d*\s*(\w+\.?\s+\.?\d{1,2})\s+(\w+\.?\s+\.?\d{1,2})(\s+[A-Za-z\s\d\W]+?)?\s+([\d,]+\.\d{2})(CR)?(?:$|\s+.*$)'


    
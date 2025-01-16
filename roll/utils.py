import phonenumbers
from phonenumbers import NumberParseException

def format_phone_number_to_e164(phone_number, region="IN"):
    """
    Converts a phone number to E.164 format.
    :param phone_number: The phone number to be formatted.
    :param region: The country code to be used for parsing (default is "US").
    :return: Phone number in E.164 format or None if invalid.
    """
    try:
        # Parse the phone number with the region code
        parsed_number = phonenumbers.parse(phone_number, region)

        # Check if the number is valid
        if phonenumbers.is_valid_number(parsed_number):
            # Format and return the phone number in E.164 format
            return phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)
        else:
            # If invalid, return None
            return None
    except NumberParseException as e:
        # Handle parsing errors (e.g., invalid number format)
        print(f"Error parsing number: {str(e)}")
        return None

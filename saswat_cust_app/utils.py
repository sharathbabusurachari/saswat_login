# utils.py

import phonenumbers


def is_valid_indian_mobile_number(mobile_no):
    try:
        # Parse the phone number
        parsed_number = phonenumbers.parse(mobile_no, "IN")

        # Check if the number is a valid mobile number in India
        return (
            phonenumbers.is_valid_number(parsed_number) and
            phonenumbers.is_possible_number(parsed_number) and
            phonenumbers.number_type(parsed_number) == phonenumbers.PhoneNumberType.MOBILE
        )
    except phonenumbers.NumberParseException:
        return False

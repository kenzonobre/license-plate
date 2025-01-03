import string

def valid_license_plate_format(text):
    """
    Check if the license plate text complies with the BRAZILIAN license plate

    Args:
        text (str): License plate text.

    Returns:
        bool: True if the license plate complies with the format, False otherwise.
    """

    if len(text) != 7:
        return False

    # Mapping dictionaries for character conversion
    dict_char_to_int = {'O': '0',
                        'I': '1',
                        'J': '3',
                        'A': '4',
                        'G': '6',
                        'S': '5'}

    dict_int_to_char = {'0': 'O',
                        '1': 'I',
                        '3': 'J',
                        '4': 'A',
                        '6': 'G',
                        '5': 'S'}

    numbers = "0123456789"

    def valid_number(char):
        return char in numbers or char in dict_char_to_int.keys()
    
    def valid_letter(char):
        return char in string.ascii_uppercase or char in dict_int_to_char.keys()

    # Checking if the format is LLLNLNNN (new Mercosul plate format) or LLLNNNN (old Brazilian plate format)
    if valid_letter(text[0]) and \
       valid_letter(text[1]) and \
       valid_letter(text[2]) and \
       valid_number(text[3]) and \
       (valid_number(text[4]) or valid_letter(text[4])) and \
       valid_number(text[5]) and \
       valid_number(text[6]):
        return True
    else:
        return False
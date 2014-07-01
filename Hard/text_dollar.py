import sys

def get_digit(digit):
    digits = {
        '0': '',
        '1': 'One',
        '2': 'Two',
        '3': 'Three',
        '4': 'Four',
        '5': 'Five',
        '6': 'Six',
        '7': 'Seven',
        '8': 'Eight',
        '9': 'Nine'        
    }
    return digits[digit]

def get_tens(digit):
    digits = {
        '0': '',
        '2': 'Twenty',
        '3': 'Thirty',
        '4': 'Forty',
        '5': 'Fifty',
        '6': 'Sixty',
        '7': 'Seventy',
        '8': 'Eighty',
        '9': 'Ninety'        
    }
    return digits[digit]

def get_teens(number):
    digits = {
        '10': 'Ten',
        '11': 'Eleven',
        '12': 'Twelve',
        '13': 'Thirteen',
        '14': 'Fourteen',
        '15': 'Fifteen',
        '16': 'Sixteen',
        '17': 'Seventeen',
        '18': 'Eighteen',
        '19': 'Nineteen'        
    }
    return digits[number]

def get_hundred(digit):
    return get_digit(digit) + "Hundred"

def get_number(number):
    """Given a 3-digit number as a string, return the text representation."""
    
    value = int(number)
    value_length = len(str(value))
    number = str(value)
    
    if value_length == 1:
        return get_digit(number)
    if value_length == 2:
        if int(number) >= 10 and int(number) <= 19:
            return get_teens(number)
        else:
            return get_tens(number[0]) + get_digit(number[1])
    if value_length == 3:
        return get_hundred(number[0]) + get_number(number[1:])

def get_thousands(number):
    if int(number) == 0:
        return ""
    return get_number(number) + "Thousand"

def get_millions(number):
    return get_number(number) + "Million"

def get_text_representation(number):
    if len(number) <= 3:
        return get_number(number)
    if len(number) > 3 and len(number) <= 6:
        return get_thousands(number[:-3]) + get_number(number[-3:])
    if len(number) > 6:
        return get_millions(number[-9:-6]) + get_thousands(number[-6:-3]) + get_number(number[-3:])

def main():
    args = sys.argv
    assert len(args) == 2, "Please provide one file as input."
    filename = args[1]
    
    numbers = None
    with open(filename) as f:
        numbers = f.readlines()
    assert numbers is not None and isinstance(numbers, list), "Error in loading file."
    
    for number in numbers:
        if int(number) == 1:
            print "OneDollar"
        else:
            text_rep = get_text_representation(number.strip())
            print text_rep + "Dollars"

if __name__ == "__main__":
    main()
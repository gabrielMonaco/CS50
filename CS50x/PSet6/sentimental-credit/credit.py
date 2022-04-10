from cs50 import get_string

number = get_string("Number: ")


def main(number):
    # if is not a valid credit card
    if luhnAllgorithm(number) != True or validNumber(number) != True:
        print("INVALID")
    # check the type of credit card
    else:
        wichCompany(number)


def validNumber(number):
    """Validate the number

    return False if the len of numbers is lower or greater than the pattern (13, 15 or 16)"""
    results = [13, 15, 16]
    if len(number) in results and number.isnumeric() == True:
        return True
    else:
        return False


def luhnAllgorithm(number):
    """return False if does not agree with the algorithm, and True otherwise"""
    # calculate the Luhn's Algorithm
    sum1 = 0
    sum2 = 0
    for i in range(len(number), 2):
        sum1 += int(number[i] * 2)
        sum2 += int(number[i+1])
    if (sum1 + sum2) % 10 != 0:
        return False
    else:
        return True


def wichCompany(number):
    # define the company by first 2 numbers
    americanExpress = ['34', '37']
    masterCard = ['51', '52', '53', '54', '55']
    visa = ['40', '41', '42', '43', '44', '45', '46', '47', '48', '49']
    # and print wich ou each
    if number[0] + number[1] in americanExpress:
        print("AMEX")
    elif number[0] + number[1] in masterCard:
        print("MASTERCARD")
    elif number[0] + number[1] in visa:
        print("VISA")
    else:
        print("INVALID")


# call the main function
main(number)


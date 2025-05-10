from cs50 import get_string

number = get_string("Number: ")

number12 = number[0:2]
number1 = number[0]

visa = ["4"]
amex = ["34", "37"]
master = ["51","52","53","54","55"]


if(len(number) < 13):
    print("INVALID")

if number1 in visa:
    if (len(number) == 13 or len(number) == 16):
        print("VISA")
elif number12 in amex:
    if (len(number) == 15):
        print("AMEX")
elif number12 in master:
    if (len(number) == 16):
        print("MASTERCARD")
else:
    print("INVALID")


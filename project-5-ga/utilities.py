import math, copy
def convert_rate_to_fraction(rate):
    rate_string = str(rate)
    denominator = "1"
    list_a = rate_string.split(".")
    numerator = list_a[0] + list_a[1]
    for i in range(len(list_a[1])):
        denominator += "0"
    return (int(numerator), int(denominator))

def flip(x):
    if x == "0":
        return "1"
    else:
        return "0"

if __name__ == "__main__":
    print(convert_rate_to_fraction(0.00005))


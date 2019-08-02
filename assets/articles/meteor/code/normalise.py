import math

def normalise_array(numbers, min_range, max_range):
    """
    Normalise a list of numbers to a range.
    min_range is the lower limit.
    max_range is the upper limit.
    """
    normalised = []
    min_n = min(numbers)
    max_n = max(numbers)

    for number in numbers:
        normalised.append(normalise(number, min_n, max_n, min_range, max_range))

    return normalised

def normalise(n, min_n, max_n, min_range, max_range):
    return (n - min_n) * (max_range - min_range) / (max_n - min_n) + min_range

print(normalise_array([37.1, 15, 24.8, 34.8, 31.25], 20, 20000))
